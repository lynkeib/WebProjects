package worker

import (
	"context"
	"github.com/chengyinliu/crontab/common"
	"github.com/coreos/etcd/clientv3"
)

// distributed lock (TXN transaction)
type JobLock struct{
	kv clientv3.KV
	lease clientv3.Lease
	jobName string

	cancelFunc context.CancelFunc
	leaseId clientv3.LeaseID
	isLocked bool
}

func InitJobLock(jobName string, kv clientv3.KV, lease clientv3.Lease)(jobLock *JobLock){
	jobLock = &JobLock{
		kv:kv,
		lease:lease,
		jobName:jobName,
	}
	return
}

func (jobLock *JobLock) TryLock()(err error){

	var (
		lockKey string
		txn clientv3.Txn
		txnResp *clientv3.TxnResponse
	)

	// 1. create lease
	leaseResp, err := jobLock.lease.Grant(context.TODO(), 5)
	if err != nil{
		return
	}

	// 2. auto extent lease
	cancelCtx, cancelFunc := context.WithCancel(context.TODO())
	leaseID := leaseResp.ID

	keepRespChan, err := jobLock.lease.KeepAlive(cancelCtx, leaseID)
	if err != nil{
		goto FAIL
	}

	go func(){
		for{
			select {
			case keepResp := <- keepRespChan:
				if keepResp == nil{
					goto END
				}
			}
		}
		END:
	}()

	// 3. create TXN
	txn = jobLock.kv.Txn(context.TODO())

	lockKey = common.JOB_LOCK_DIR + jobLock.jobName

	// 4. try get lock
	txn.If(clientv3.Compare(clientv3.CreateRevision(lockKey), "=", 0)).
		Then(clientv3.OpPut(lockKey, "", clientv3.WithLease(leaseID))).
		Else(clientv3.OpGet(lockKey))

	txnResp, err = txn.Commit()
	if err != nil{
		goto FAIL
	}

	// 5. if success return, else release lease
	if !txnResp.Succeeded{
		err = common.ERR_LOCK_ALREADY_REQUIRED
		goto FAIL
	}

	jobLock.leaseId = leaseID
	jobLock.cancelFunc = cancelFunc
	jobLock.isLocked = true

	return

	FAIL:
		cancelFunc()
		jobLock.lease.Revoke(context.TODO(), leaseID)
		return
}

// release lock
func (jobLock *JobLock) Unlock(){
	if jobLock.isLocked{
		jobLock.cancelFunc()
		jobLock.lease.Revoke(context.TODO(), jobLock.leaseId)
	}

}