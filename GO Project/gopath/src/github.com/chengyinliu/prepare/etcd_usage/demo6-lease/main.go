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
		lease clientv3.Lease
		leaseGrantResoinse *clientv3.LeaseGrantResponse
		putRep *clientv3.PutResponse
		getRep *clientv3.GetResponse
		//leaseChan *clientv3.LeaseKeepAliveResponse
		//keepRepChan <-chan *clientv3.LeaseKeepAliveResponse
	)

	config = clientv3.Config{
		Endpoints: []string{"127.0.0.1:2379"},
		DialTimeout: 5 * time.Second,
	}

	// create a client
	client, err = clientv3.New(config)

	// get kv object
	kv = clientv3.NewKV(client)

	if err != nil{return}

	// lease
	lease = clientv3.NewLease(client)

	// 10s lease
	leaseGrantResoinse, _ = lease.Grant(context.TODO(), 10)
	//keepRepChan, err = lease.KeepAlive(context.TODO(), leaseGrantResoinse.ID)

	// put kv under the lease
	putRep, _ = kv.Put(context.TODO(),"test", "", clientv3.WithLease(leaseGrantResoinse.ID))
	getRep, err = kv.Get(context.TODO(),"test")

	fmt.Println(putRep)
	fmt.Println(getRep.Count)

	time.Sleep(11 * time.Second)

	getRep, err = kv.Get(context.TODO(),"test")

	fmt.Println(getRep.Count)

}
