package master

import (
	"context"
	"encoding/json"
	"github.com/chengyinliu/crontab/common"
	"github.com/coreos/etcd/clientv3"
	"time"
)

// job manager
type JobManager struct{
	client *clientv3.Client
	kv clientv3.KV
	lease clientv3.Lease
}

var(
	G_jobManager *JobManager
)

// init Job Manager
func InitJobManager()(err error){

	// init config
	config := clientv3.Config{
		Endpoints: G_config.EtcdEndpoints, // cluster address
		DialTimeout: time.Duration(G_config.EtcdDialTimeout) * time.Millisecond,
	}

	// build connection
	client, err := clientv3.New(config)
	if err != nil{
		return err
	}

	// get KV and lease API subset
	kv := clientv3.NewKV(client)
	lease := clientv3.NewLease(client)

	// assign singleton
	G_jobManager = &JobManager{
		client: client,
		kv: kv,
		lease: lease,
	}

	return
}

// save job
func (jobManager *JobManager) SaveJob(job *common.Job)(oldJob *common.Job, err error){
	// save job to "/cron/jobs/<jobName>" : json
	jobKey := common.JOB_SAVE_DIR + job.Name
	jobValue, err := json.Marshal(job)
	if err != nil{
		return nil, err
	}
	// save to etcd
	putResp, err := jobManager.kv.Put(context.TODO(), jobKey,string(jobValue), clientv3.WithPrevKV())
	if err != nil{
		return nil, err
	}

	// if we are updating then return old value
	if putResp.PrevKv != nil{
		var oldJobObj *common.Job
		err = json.Unmarshal(putResp.PrevKv.Value, &oldJobObj)
		if err != nil{
			return nil, err
		}
		oldJob = oldJobObj
		return oldJob, nil
	}
	return nil, nil
}


// delete job
func (jobManager *JobManager) DeleteJob(name string)(oldJob *common.Job, err error){
	// delete job from "/cron/jobs/<jobName>" : json
	jobKey := common.JOB_SAVE_DIR+ name

	// delete from etcd
	delResp, err := jobManager.kv.Delete(context.TODO(), jobKey, clientv3.WithPrevKV())
	if err != nil{
		return nil, err
	}

	// return deleted job info
	if len(delResp.PrevKvs) != 0{
		var oldJobObj *common.Job
		err = json.Unmarshal(delResp.PrevKvs[0].Value, &oldJobObj)
		if err != nil{
			return nil, err
		}
		oldJob = oldJobObj
		return oldJob, nil
	}
	return nil, err

}