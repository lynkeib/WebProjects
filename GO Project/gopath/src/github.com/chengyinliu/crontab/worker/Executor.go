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
	go func(){
		cmd := exec.CommandContext(context.TODO(), "/bin/bash", "-c", info.Job.Command)

		startTIme := time.Now()
		output, err := cmd.CombinedOutput()
		endTime := time.Now()
		jobResult:= common.BuildJobExecutionResult(info, output, err, startTIme, endTime)
		G_scheduler.PushJobResult(jobResult)
	}()
}

// init
func InitExecutor()(err error){
	G_executor = &Executor{}
	return
}