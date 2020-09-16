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
	)

	config = clientv3.Config{
		Endpoints: []string{"127.0.0.1:2379"},
		DialTimeout: 5 * time.Second,
	}

	// create a client
	client, _ = clientv3.New(config)

	// get kv object
	kv := clientv3.NewKV(client)

	// lease achieves lock auto-expiration
	// op
	// txn: if else then

	// 1. get lock (create lease, auto-lease, use lease to occupy a key)
	lease := clientv3.NewLease(client)
	ctx, cancelFunc := context.WithCancel(context.TODO())
	leaseGrantResp, _ := lease.Grant(context.TODO(), 5)
	leaseId := leaseGrantResp.ID

	defer cancelFunc() // will be executed at the end of the func
	defer lease.Revoke(context.TODO(), leaseId)

	keepRespChan, _ := lease.KeepAlive(ctx, leaseId)
	go func(){
		for{
			keepResp := <- keepRespChan
			if keepResp == nil{
				break
			}
			fmt.Println("Extend the lease")
		}
	}()

	// create transaction
	txn := kv.Txn(context.TODO())

	createRevision := clientv3.CreateRevision("test")
	txn.If(clientv3.Compare(createRevision, "=", 0)).
		Then(clientv3.OpPut("test", "", clientv3.WithLease(leaseId))).
		Else()

	TxnResp, _ := txn.Commit()
	// whether we have the lock
	if !TxnResp.Succeeded{
		fmt.Println("I didn't get the lock and I am going to return")
		return
	}

	// 2. execute
	fmt.Println("I get the lock and I am going to do sth")
	time.Sleep(5 * time.Second)

	// 3. release lock (cancel auto-lease, release lease)
	// defers above will release
}
