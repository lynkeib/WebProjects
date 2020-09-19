package worker

import (
	"context"
	"github.com/chengyinliu/crontab/common"
	"github.com/coreos/etcd/clientv3"
	"github.com/coreos/etcd/mvcc/mvccpb"
	"time"
)

// job manager
type JobManager struct{
	client *clientv3.Client
	kv clientv3.KV
	lease clientv3.Lease
	watcher clientv3.Watcher
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
	watcher := clientv3.NewWatcher(client)

	// assign singleton
	G_jobManager = &JobManager{
		client: client,
		kv: kv,
		lease: lease,
		watcher:watcher,
	}

	// start listening
	G_jobManager.watchJobs()

	return
}

// listen job changes
func (jobManager *JobManager) watchJobs() (err error){
	// 1. get jobs from "cron/jobs", and the revision of current cluster
	getResp, err := jobManager.kv.Get(context.TODO(), common.JOB_SAVE_DIR, clientv3.WithPrefix())
	if err != nil{
		return err
	}

	for _, kv := range getResp.Kvs{
		// deserialize job to get json
		job, err := common.UnpackJob(kv.Value)
		if err != nil{
			continue
		}
		jobEvent := common.BuildJobEvent(common.JOB_EVENT_SAVE, job)
		jobEvent = jobEvent
		//TODO: send this job to Scheduler

	}

	// 2. listen events from this revision
	go func(){
		watchStartRevision := getResp.Header.Revision + 1
		watchChan := jobManager.watcher.Watch(context.TODO(), common.JOB_SAVE_DIR, clientv3.WithRev(watchStartRevision))
		for watchResp := range watchChan{
			for _, watchEvent := range watchResp.Events{
				switch watchEvent.Type{
				case mvccpb.PUT:
					job, err := common.UnpackJob(watchEvent.Kv.Value)
					if err != nil{
						continue
					}
					jobEvent := common.BuildJobEvent(common.JOB_EVENT_SAVE, job)
					jobEvent = jobEvent
					// TODO: push to scheduler
					break
				case mvccpb.DELETE:
					jobName := common.ExtractJobName(string(watchEvent.Kv.Key))
					jobEvent := common.BuildJobEvent(common.JOB_EVENT_SAVE, &common.Job{Name:jobName})
					jobEvent = jobEvent
					// TODO: push to scheduler
					break
				}
			}

		}
	}()

	return
}