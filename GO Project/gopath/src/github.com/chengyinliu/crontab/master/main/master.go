package main

import (
	"flag"
	"fmt"
	"github.com/chengyinliu/crontab/master"
	"runtime"
	"time"
)

var (
	confFile string // config file path
)

// parse command line args
func initArgs() {
	// master -config ./master.json
	flag.StringVar(&confFile, "config", "./master.json", "assign master config")
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
	err = master.InitConfig(confFile)
	if err != nil{
		goto ERR
	}

	// init worker manager
	err = master.InitWorkManager()
	if err != nil{
		goto ERR
	}

	// init log manager
	err = master.InitLogManager()
	if err != nil{
		goto ERR
	}

	// init job manager
	err = master.InitJobManager()
	if err != nil{
		goto ERR
	}

	// initialize Api Http service
	err = master.InitApiServer()
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