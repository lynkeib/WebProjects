package common

import "encoding/json"

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