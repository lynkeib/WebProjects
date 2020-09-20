package worker

import (
	"context"
	"github.com/chengyinliu/crontab/common"
	"github.com/coreos/etcd/clientv3"
	"net"
	"time"
)

// register node to etcd for helping master find healthy nodes
type Register struct{
	client *clientv3.Client
	kv clientv3.KV
	lease clientv3.Lease

	localIP string
}

var (
	G_register *Register
)

func getLocalIp()(ipv4 string, err error){

	addrs, err := net.InterfaceAddrs()
	if err != nil{
		return
	}
	// get first non-localhost
	for _, addr := range addrs{
		ipNet, isIpNet := addr.(*net.IPNet)
		if isIpNet && !ipNet.IP.IsLoopback(){
			if ipNet.IP.To4() != nil{
				ipv4 = ipNet.IP.String()
				return
			}
		}

	}
	err = common.ERR_NO_LOCAL_IP_FOUND
	return
}

func InitRegister()(err error){
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

	// get local ip
	localip, err := getLocalIp()
	if err != nil{
		return
	}
	G_register = &Register{
		client,
		kv,
		lease,
		localip,
	}
	go G_register.keepOnline()
	return
}

// register to /cron/workers/IP and auto-lease
func (register *Register) keepOnline(){

	var(
		regKey string
		leaseResp *clientv3.LeaseGrantResponse
		err error
		keepAliveChan <- chan *clientv3.LeaseKeepAliveResponse
		//putResp *clientv3.PutResponse
		keepAliveResp *clientv3.LeaseKeepAliveResponse
		cancelCtx context.Context
		cancelFunc context.CancelFunc
	)

	regKey = common.JOB_WORKER_DIR + register.localIP
	for{

		cancelFunc = nil

		leaseResp, err = register.lease.Grant(context.TODO(), 10)
		if err != nil{
			goto RETRY
		}

		// auto-lease
		keepAliveChan, err = register.lease.KeepAlive(context.TODO(), leaseResp.ID)
		if err != nil{
			goto RETRY
		}

		cancelCtx, cancelFunc = context.WithCancel(context.TODO())

		// register to etcd
		_ ,err = register.kv.Put(cancelCtx, regKey, "", clientv3.WithLease(leaseResp.ID))
		if err !=nil{
			goto RETRY
		}

		for{
			select{
			case keepAliveResp = <- keepAliveChan:
				if keepAliveResp == nil{
					goto RETRY
				}
			}
		}

		RETRY:
			time.Sleep(1 * time.Second)
			if cancelFunc != nil{
				cancelFunc()
			}
	}
}
