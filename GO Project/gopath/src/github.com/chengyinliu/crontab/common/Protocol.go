package common

import (
	"encoding/json"
	"strings"
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

func BuildJobEvent(eventType int, job *Job) (event *JobEvent){
	return &JobEvent{
		EventType: eventType,
		Job:job,
	}
}