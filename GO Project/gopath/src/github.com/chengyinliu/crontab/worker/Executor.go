package worker

import (
	"github.com/chengyinliu/crontab/common"
	"math/rand"
	"os/exec"
	"time"
)

type Executor struct{

}

var (
	G_executor *Executor
)

func (executor *Executor) ExecuteJob(info *common.JobExecutionStatus){

	var (
		startTIme time.Time
		output []byte
		err error
		endTime time.Time
	)

	go func(){
		// get lock first
		jobLock := G_jobManager.CreateJobLock(info.Job.Name)

		startTIme = time.Now()

		// random sleep for distributing jobs evenly
		time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)
		err = jobLock.TryLock()
		defer jobLock.Unlock()

		if err != nil{
			endTime = time.Now()
		}else{
			cmd := exec.CommandContext(info.CancelCtx, "/bin/bash", "-c", info.Job.Command)
			startTIme = time.Now()
			output, err = cmd.CombinedOutput()
			endTime = time.Now()
		}
		jobResult:= common.BuildJobExecutionResult(info, output, err, startTIme, endTime)
		G_scheduler.PushJobResult(jobResult)
	}()
}

// init
func InitExecutor()(err error){
	G_executor = &Executor{}
	return
}