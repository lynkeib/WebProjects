package master

import (
	"encoding/json"
	"github.com/chengyinliu/crontab/common"
	"net"
	"net/http"
	"strconv"
	"time"
)

// singleton
var(
	G_apiServer *ApiServer
)

// job's http interface
type ApiServer struct{
	httpServer *http.Server
}

// save job interface
// POST jon = {"name":"job", "command":"echo hello", "cronExp":"* * * * *"}
func handleJobSave(resp http.ResponseWriter, req *http.Request){
	// jobs need to be saved to etcd
	var(
		postJob string
		job *common.Job
		oldJob *common.Job
		bytes []byte
	)
	// 1. parse post
	err := req.ParseForm()
	if err != nil{
		goto ERR
	}

	// 2. take job info
	postJob = req.PostForm.Get("job")

	// 3. deserialize job
	err = json.Unmarshal([]byte(postJob), &job)
	if err != nil{
		goto ERR
	}

	// 4. save to etcd
	oldJob, err = G_jobManager.SaveJob(job)
	if err != nil{
		goto ERR
	}

	// return normal response
	// {err:0, message:"",data:{...}}
	bytes, err = common.BuildResponse(0, "success", oldJob)
	if err == nil{
		resp.Write(bytes)
	}
	return

	ERR:
		// return err response
		bytes, err = common.BuildResponse(-1, err.Error(), nil)
		if err == nil{
			resp.Write(bytes)
		}
}

// delete job interface
// POST name=job1
func handleJobDelete(resp http.ResponseWriter, req *http.Request){
	// jobs need to be deleted from etcd
	var(
		err error
		name string
		oldJob *common.Job
		bytes []byte
	)

	// 1. parse form
	err = req.ParseForm()
	if err != nil{
		goto ERR
	}

	// 2. take job info
	name = req.PostForm.Get("name")

	// 3. delete job
	oldJob, err = G_jobManager.DeleteJob(name)
	if err != nil{
		goto ERR
	}

	// return normal response
	// {err:0, message:"",data:{...}}
	bytes, err = common.BuildResponse(0, "success", oldJob)
	if err == nil{
		resp.Write(bytes)
	}

	return

	ERR:
		bytes, err = common.BuildResponse(-1, err.Error(), nil)
		if err == nil{
			resp.Write(bytes)
		}
}

// list job interface
// GET
func handleJobList(resp http.ResponseWriter, req *http.Request){
	var(
		err error
		bytes []byte
	)
	jobs, err := G_jobManager.ListJobs()
	if err != nil{
		goto ERR
	}

	// return normal response
	// {err:0, message:"",data:{...}}
	bytes, err = common.BuildResponse(0, "success", jobs)
	if err == nil{
		resp.Write(bytes)
	}

	return

	ERR:
		bytes, err = common.BuildResponse(-1, err.Error(), nil)
		if err == nil{
			resp.Write(bytes)
		}
}

// initialize service
func InitApiServer()(err error){
	// config url
	mux := http.NewServeMux()
	mux.HandleFunc("/job/save", handleJobSave)
	mux.HandleFunc("/job/delete", handleJobDelete)
	mux.HandleFunc("/job/list", handleJobList)

	// start TCP listen
	listener, err := net.Listen("tcp", ":" + strconv.Itoa(G_config.ApiPort))
	if err != nil{
		return err
	}

	// create a http service
	httpServer := &http.Server{
		ReadTimeout: time.Duration(G_config.ApiReadTimeout) * time.Millisecond,
		WriteTimeout:time.Duration(G_config.ApiWriteTimeout) * time.Millisecond,
		Handler: mux,
	}

	// assign singleton
	G_apiServer = &ApiServer{
		httpServer: httpServer,
	}

	// start server
	go httpServer.Serve(listener)
	return
}

func main() {


}
