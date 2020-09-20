package worker

import (
	"encoding/json"
	"io/ioutil"
)

// program config
type Config struct{
	EtcdEndpoints []string `json:"ETCD_ENDPOINTS"`
	EtcdDialTimeout int `json:"ECTD_DIALTIMEOUT"`
	MongodbConnectTimeout int `json:"MONGODB_CONNECT_TIMEOUT"`
	LogBatchSize int `json:"JOB_LOG_BATCH_SIZE"`
	AutoLogCommitTime int `json:"AUTO_LOG_COMMIT_TIME"`
}

// singleton
var (
	G_config *Config
)

func InitConfig(filename string)(err error){
	// read config file
	content, err := ioutil.ReadFile(filename)
	if err != nil{
		return err
	}

	// de-serialize file
	var config Config
	err = json.Unmarshal(content, &config)
	if err != nil{
		return err
	}

	// assign singleton
	G_config = &config
	return
}
