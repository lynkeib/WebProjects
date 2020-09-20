package worker

import (
	"fmt"
	"github.com/chengyinliu/crontab/common"
	"time"
)

type Scheduler struct{
	jobEventChan chan *common.JobEvent
	jobPlanTable map[string]*common.JobSchedulePlan
	jobExecutionTable map[string]*common.JobExecutionStatus
	jobResultChan chan*common.JobExecutionResult
}

// singleton
var(
	G_scheduler *Scheduler
)

// handle event
func (scheduler *Scheduler) handleJobEvent(JobEvent *common.JobEvent){
	switch JobEvent.EventType{
	case common.JOB_EVENT_SAVE:
		jobSchedulePlan, err:= common.BuildJobSchedulePlan(JobEvent.Job)
		if err != nil{
			return
		}
		scheduler.jobPlanTable[JobEvent.Job.Name] = jobSchedulePlan

	case common.JOB_EVENT_DELETE:
		// check if job exists
		_, jobExists := scheduler.jobPlanTable[JobEvent.Job.Name]
		if jobExists{
			delete(scheduler.jobPlanTable, JobEvent.Job.Name)
		}
	case common.JOB_EVENT_KILL:
		jobExecuteStatus, isExecuting := scheduler.jobExecutionTable[JobEvent.Job.Name]
		if isExecuting {
			jobExecuteStatus.CancelFunc()
		}
	}
}

// handle job result
func (scheduler *Scheduler) handleJobResult(jobResult *common.JobExecutionResult){
	// delete execution table
	delete(scheduler.jobExecutionTable, jobResult.ExecutionStatus.Job.Name)

	fmt.Println("Job Done: " + jobResult.ExecutionStatus.Job.Name, string(jobResult.Output), jobResult.Err)

	// generate job log
	if jobResult.Err != common.ERR_LOCK_ALREADY_REQUIRED{
		jobLog := &common.JobLog{
			JobName:jobResult.ExecutionStatus.Job.Name,
			Command: jobResult.ExecutionStatus.Job.Command,
			Output: string(jobResult.Output),
			PlanTime: jobResult.ExecutionStatus.PlanTime.UnixNano() / 1000 / 1000,
			ScheduleTime: jobResult.ExecutionStatus.RealTime.UnixNano() / 1000 / 1000,
			StartTime: jobResult.StartTime.UnixNano()  / 1000 / 1000,
			EndTime: jobResult.EndTime.UnixNano()  / 1000 / 1000,
		}
		if jobResult.Err != nil{
			jobLog.Err = jobResult.Err.Error()
		}else{
			jobLog.Err = ""
		}
		// save to mongoDB
		G_logSink.Append(jobLog)
	}


}

// try start job
func (scheduler *Scheduler) TryStartJob(jobPlan *common.JobSchedulePlan){
	// check if this job iss executing
	jobExecutionStatus, jobExecuting := scheduler.jobExecutionTable[jobPlan.Job.Name]
	if jobExecuting{
		fmt.Println(jobPlan.Job.Name + " is running")
		return
	}

	// build job execution status
	jobExecutionStatus = common.BuildJobExecutionStatus(jobPlan)

	// save
	scheduler.jobExecutionTable[jobPlan.Job.Name] = jobExecutionStatus
	fmt.Println("JOb Execution table ", scheduler.jobExecutionTable)
	// execution
	fmt.Println("Executing Job " + jobPlan.Job.Name)
	G_executor.ExecuteJob(jobExecutionStatus)

}

// recalculate job schedule status
func (scheduler *Scheduler) TrySchedule()(scheduleAfter time.Duration){

	if len(scheduler.jobPlanTable) == 0{
		scheduleAfter = 1 * time.Second
		return
	}

	// current time
	curr := time.Now()

	// near time
	var nearTime *time.Time

	// 1. loop through all jobs
	for _, jobPlan := range scheduler.jobPlanTable{
		if jobPlan.NextTime.Before(curr) || jobPlan.NextTime.Equal(curr){
			// try execute job
			scheduler.TryStartJob(jobPlan)
			jobPlan.NextTime = jobPlan.Expr.Next(curr)
		}
		if nearTime == nil || jobPlan.NextTime.Before(*nearTime){
			nearTime = &jobPlan.NextTime
		}
	}

	// 3. calculate the next earliest executable job
	scheduleAfter = (*nearTime).Sub(curr)
	return
}

// Scheduler routine
func (scheduler *Scheduler) scheduleLoop(){
	scheduleAfter := scheduler.TrySchedule()

	// schedule timer
	scheduleTimer := time.NewTimer(scheduleAfter)

	for{
		select{
			case jobEvent := <- scheduler.jobEventChan: //listen job changes
				// maintain jobs in memory
				scheduler.handleJobEvent(jobEvent)
			case <- scheduleTimer.C: //
			case jobResult := <- scheduler.jobResultChan:
				scheduler.handleJobResult(jobResult)

		}
		scheduleAfter = scheduler.TrySchedule()
		scheduleTimer.Reset(scheduleAfter)
	}
}

// push job changes event
func  (scheduler *Scheduler) PushJobEvent(jobEvent *common.JobEvent){
	scheduler.jobEventChan <- jobEvent
}


// initialize Scheduler
func InitScheduler()(err error){
	G_scheduler = &Scheduler{
		make(chan *common.JobEvent, 1000),
		make(map[string]*common.JobSchedulePlan),
		make(map[string]*common.JobExecutionStatus),
		make(chan *common.JobExecutionResult, 1000),
	}

	// start schedule routine
	go G_scheduler.scheduleLoop()
	return
}

// return job result
func (scheduler *Scheduler) PushJobResult(jobResult *common.JobExecutionResult){
	scheduler.jobResultChan <- jobResult
}