package master

import (
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

func handleJobSave(w http.ResponseWriter, r *http.Request){
	// jobs need to be saved to etcd

}

// initialize service
func InitApiServer()(err error){
	// config url
	mux := http.NewServeMux()
	mux.HandleFunc("/job/save", handleJobSave)

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
