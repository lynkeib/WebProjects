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
		putResponse *clientv3.PutResponse
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

	putResponse, err = kv.Put(context.TODO(), "/cron/jons/jobs", "bye", clientv3.WithPrevKV())
	if err != nil{return}
	fmt.Println(putResponse.Header.Revision)
	if putResponse.PrevKv != nil{
		fmt.Println(string(putResponse.PrevKv.Value ))
	}

}
