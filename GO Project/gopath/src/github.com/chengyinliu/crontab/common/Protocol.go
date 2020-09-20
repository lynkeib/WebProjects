package common

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/gorhill/cronexpr"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

// jobs
type Job struct{
	Name string `json:"name"`
	Command string `json:"command"`
	CronExpr string `json:"cronExpr"`
}

// response
type Response struct{
	Error int `json:"err"`
	Message string `json:"message"`
	Data interface{} `json:"data"`
}

// event (save, delete)
type JobEvent struct{
	EventType int //SAVE DELETE
	Job *Job
}

// job scheduler plan
type JobSchedulePlan struct{
	Job *Job
	Expr *cronexpr.Expression
	NextTime time.Time
}

// job execution status
type JobExecutionStatus struct{
	Job *Job
	PlanTime time.Time
	RealTime time.Time
	CancelCtx context.Context
	CancelFunc context.CancelFunc
}

// job execution result
type JobExecutionResult struct{
	ExecutionStatus *JobExecutionStatus
	Output []byte
	Err error
	StartTime time.Time
	EndTime time.Time
}

type ConfigMongo struct{
	Username string
	Password string
}

// search log filters
type JobLogFilter struct{
	JobName string `bson:"jobName"`
}

// log order
type SortLogByStartTime struct{
	SortOrder int `bson:"startTime"` // order by startTime:-1
}

// job log
type JobLog struct{
	JobName string `bson:"jobName"`
	Command string `bson:"command"`
	Err string `bson:"error"`
	Output string `bson:"output"`
	PlanTime int64 `bson:"planTime"`
	ScheduleTime int64 `bson:"scheduleTime"`
	StartTime int64 `bson:"startTime"`
	EndTime int64 `bson:"endTime"`
}

// log batch
type LogBatch struct {
	Logs []interface{}
}

// build response
func BuildResponse(error int, message string, data interface{}) (res []byte, err error){
	// define a response
	resp := Response{
		error,
		message,
		data,
	}

	// serialize
	res, err = json.Marshal(resp)
	return res, err
}

// deserialize job
func UnpackJob(value []byte) (res *Job, err error){

	job := &Job{}
	err = json.Unmarshal(value, job)
	if err != nil{
		return
	}
	res = job
	return
}

// get job name from etcd keys
func ExtractJobName(jobKey string)(string){
	return strings.TrimPrefix(jobKey, JOB_SAVE_DIR)
}

// get job name from etcd keys
func ExtractKillerName(killerKey string)(string){
	return strings.TrimPrefix(killerKey, JOB_KILL_DIR)
}

func BuildJobEvent(eventType int, job *Job) (event *JobEvent){
	return &JobEvent{
		EventType: eventType,
		Job:job,
	}
}

// build job schedule plan
func BuildJobSchedulePlan(job *Job)(jobSchedulePlan *JobSchedulePlan, err error){

	// parse
	expr, err := cronexpr.Parse(job.CronExpr)
	if err != nil{
		return
	}

	jobSchedulePlan = &JobSchedulePlan{
		job,
		expr,
		expr.Next(time.Now()),
	}
	return
}

// build job execution status
func BuildJobExecutionStatus(jobSchedulePlan *JobSchedulePlan) (jobExecutionStatus *JobExecutionStatus){
	jobExecutionStatus = &JobExecutionStatus{
		Job:jobSchedulePlan.Job,
		PlanTime: jobSchedulePlan.NextTime,
		RealTime: time.Now(),
	}
	jobExecutionStatus.CancelCtx, jobExecutionStatus.CancelFunc = context.WithCancel(context.TODO())
	return
}

// build job result
func BuildJobExecutionResult(info *JobExecutionStatus, output []byte, err error, startTime time.Time, endTime time.Time)(jobExecutionResult *JobExecutionResult){
	jobExecutionResult = &JobExecutionResult{
		info,
		output,
		err,
		startTime,
		endTime,
	}
	return
}


func GetConfig() ConfigMongo{
	var config ConfigMongo
	file, err := os.Open("config.json")
	if err != nil{
		fmt.Println(err)
		return config
	}
	defer file.Close()
	byteValue, _ := ioutil.ReadAll(file)
	err = json.Unmarshal(byteValue, &config)
	if err != nil{
		fmt.Println(err)
		return config
	}
	return config
}