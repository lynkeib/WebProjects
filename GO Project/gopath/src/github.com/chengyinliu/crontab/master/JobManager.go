package master

import (
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