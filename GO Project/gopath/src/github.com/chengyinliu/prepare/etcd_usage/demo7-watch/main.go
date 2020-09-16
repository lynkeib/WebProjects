package main

import (
	"context"
	"fmt"
	"github.com/coreos/etcd/clientv3"
	"github.com/coreos/etcd/mvcc/mvccpb"
	"time"
)

func main() {
	var(
		config clientv3.Config
		client *clientv3.Client
		//err error
		kv clientv3.KV
		getRep *clientv3.GetResponse
	)

	config = clientv3.Config{
		Endpoints: []string{"127.0.0.1:2379"},
		DialTimeout: 5 * time.Second,
	}

	// create a client
	client, _ = clientv3.New(config)

	// get kv object
	kv = clientv3.NewKV(client)

	go func(){
		for{
			kv.Put(context.TODO(), "test", "jon")
			kv.Delete(context.TODO(), "test")
			time.Sleep(1 * time.Second)
		}
	}()

	getRep, _ = kv.Get(context.TODO(), "test")

	fmt.Println(getRep.Kvs[0].Value)

	watchStart := getRep.Header.Revision + 1

	// create watcher
	watcher := clientv3.NewWatcher(client)

	// start watch
	watchChan := watcher.Watch(context.TODO(), "test", clientv3.WithRev(watchStart))

	for watchRep := range watchChan{
		for _, event := range watchRep.Events{
			switch event.Type {
			case mvccpb.PUT:
				fmt.Println("PUT", string(event.Kv.Value), event.Kv.CreateRevision, event.Kv.ModRevision)
			case mvccpb.DELETE:
				fmt.Println("DELETE", string(event.Kv.Value), event.Kv.ModRevision)
			}
		}
		fmt.Println()
	}

}
