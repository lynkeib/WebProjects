package master

import (
	"context"
	"github.com/chengyinliu/crontab/common"
	"github.com/coreos/etcd/clientv3"
	"time"
)

type WorkManager struct{
	client *clientv3.Client
	kv clientv3.KV
	lease clientv3.Lease
}

var (
	G_workManager *WorkManager
)

func InitWorkManager()(err error){
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

	G_workManager = &WorkManager{
		client,
		kv,
		lease,
	}

	return
}

func (workManager *WorkManager) ListWorkers()(workArr []string, err error) {
	workArr = make([]string, 0)
	getResp, err := workManager.kv.Get(context.TODO(), common.JOB_WORKER_DIR, clientv3.WithPrefix())
	if err != nil{
		return
	}

	for _, kv := range getResp.Kvs{
		IP := common.ExtractWorkerIP(string(kv.Key))
		workArr = append(workArr, IP)
	}

	return
}