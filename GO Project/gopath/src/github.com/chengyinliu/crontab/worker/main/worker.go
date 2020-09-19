package main

import (
	"flag"
	"fmt"
	"github.com/chengyinliu/crontab/worker"
	"runtime"
	"time"
)

var (
	confFile string // config file path
)

// parse command line args
func initArgs() {
	// worker -config ./worker.json
	flag.StringVar(&confFile, "config", "./worker.json", "assign worker config")
	flag.Parse()
}

// init number of threads
func initEnv(){
	// make sure number of threads is equal to number of CPUs
	// to make use of GO
	runtime.GOMAXPROCS(runtime.NumCPU())
}

func main() {
	var(
		err error
	)

	// init command line arguments
	initArgs()

	// initialize thread
	initEnv()

	// load config
	err = worker.InitConfig(confFile)
	if err != nil{
		goto ERR
	}

	// init job scheduler
	err = worker.InitScheduler()
	if err != nil{
		goto ERR
	}

	// init job manager
	err = worker.InitJobManager()
	if err != nil{
		goto ERR
	}


	for{
		time.Sleep(1 * time.Second)
	}

	// regular exit
	return

ERR:
	fmt.Println(err)
}