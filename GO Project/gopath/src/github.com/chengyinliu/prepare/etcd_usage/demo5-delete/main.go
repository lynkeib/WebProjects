package main

import (
	"context"
	"fmt"
	"github.com/coreos/etcd/clientv3"
	"time"
)

func main() {
	var(
		config clientv3.Config
		client *clientv3.Client
		err error
		kv clientv3.KV
		deleteResponse *clientv3.DeleteResponse
	)

	config = clientv3.Config{
		Endpoints: []string{"127.0.0.1:2379"},
		DialTimeout: 5 * time.Second,
	}

	// create a client
	client, err = clientv3.New(config)

	if err != nil{return}

	// for read and write etcd key-value pair
	kv = clientv3.NewKV(client)

	// delete
	deleteResponse, err = kv.Delete(context.TODO(), "/cron/jobs/job2")

	if err != nil{
		return
	}

	fmt.Print(deleteResponse)
}
