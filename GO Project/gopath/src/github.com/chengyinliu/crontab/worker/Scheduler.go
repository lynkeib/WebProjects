package worker

import (
	"fmt"
	"github.com/chengyinliu/crontab/common"
	"time"
)

type Scheduler struct{
	jobEventChan chan *common.JobEvent
	jobPlanTable map[string]*common.JobSchedulePlan
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
	}
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
			// TODO: try execute job
			fmt.Println(jobPlan.Job.Name)
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
	}

	// start schedule routine
	go G_scheduler.scheduleLoop()
	return
}