package main

import (
	"fmt"
	"github.com/gorhill/cronexpr"
	"time"
)

type CronJob struct{
	expr *cronexpr.Expression
	nextTime time.Time
}

func main() {
	// need to have a routine to check expired cron jobs

	var (
		cronJob *CronJob
		expr *cronexpr.Expression
		now time.Time
		scheduleTable map[string]*CronJob // key: job name
	)
	scheduleTable = make(map[string]*CronJob)
	now = time.Now()

	// define two jobs
	expr = cronexpr.MustParse("*/5 * * * * * *")
	cronJob = &CronJob{
		expr,
		expr.Next(now),
	}

	// register job to table
	scheduleTable["job1"] = cronJob

	// define two jobs
	expr = cronexpr.MustParse("*/5 * * * * * *")
	cronJob = &CronJob{
		expr,
		expr.Next(now),
	}

	// register job to table
	scheduleTable["job2"] = cronJob

	// start routine
	go func(){
		var (
			jobName string
			cronJob *CronJob
			now time.Time
		)
		// check table
		for{
			now = time.Now()

			for jobName, cronJob = range scheduleTable{
				// check if expire
				if cronJob.nextTime.Before(now) || cronJob.nextTime.Equal(now){
					// exec jon
					go func(jobName string){
						fmt.Println(jobName)
					}(jobName)

					// calculate next time
					cronJob.nextTime = cronJob.expr.Next(now)
				}
			}
			select{
			case <- time.NewTimer(100 * time.Millisecond).C:
			}
		}
	}()
	time.Sleep(100 * time.Second)
}
