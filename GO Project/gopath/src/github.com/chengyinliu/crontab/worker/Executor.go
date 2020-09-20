package worker

import (
	"context"
	"github.com/chengyinliu/crontab/common"
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
		cmd := exec.CommandContext(context.TODO(), "/bin/bash", "-c", info.Job.Command)

		// get lock first
		jobLock := G_jobManager.CreateJobLock(info.Job.Name)

		startTIme = time.Now()
		err = jobLock.TryLock()
		defer jobLock.Unlock()

		if err != nil{
			endTime = time.Now()
		}else{
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