package worker

import (
	"context"
	"fmt"
	"github.com/chengyinliu/crontab/common"
	"github.com/mongodb/mongo-go-driver/mongo"
	"github.com/mongodb/mongo-go-driver/mongo/clientopt"
	"time"
)

type LogSink struct {
	client *mongo.Client
	logCollection *mongo.Collection
	logChan chan *common.JobLog
	autoCommitChan chan *common.LogBatch
}

var (
	G_logSink *LogSink
)

func (logSink *LogSink) saveLogs(batch *common.LogBatch) {
	logSink.logCollection.InsertMany(context.TODO(), batch.Logs)
}

func (logSink *LogSink) writeLoop() {
	var (
		log *common.JobLog
		logBatch *common.LogBatch
		commitTimer *time.Timer
		timeoutBatch *common.LogBatch
	)

	for {
		select {
		case log = <- logSink.logChan:
			if logBatch == nil {
				logBatch = &common.LogBatch{}
				commitTimer = time.AfterFunc(
					time.Duration(G_config.AutoLogCommitTime) * time.Millisecond,
					func(batch *common.LogBatch) func() {
						return func() {
							logSink.autoCommitChan <- batch
						}
					}(logBatch),
				)
			}

			logBatch.Logs = append(logBatch.Logs, log)

			if len(logBatch.Logs) >= G_config.LogBatchSize {
				// send log
				logSink.saveLogs(logBatch)
				// clear logBatch
				logBatch = nil
				// cancel timer
				commitTimer.Stop()
			}
		case timeoutBatch = <- logSink.autoCommitChan: // expired batch
			// check if this batch is the current batch
			if timeoutBatch != logBatch {
				continue // if it is, means already committed
			}
			logSink.saveLogs(timeoutBatch)
			logBatch = nil
		}
	}
}

func InitLogSink() (err error) {
	var (
		client *mongo.Client
	)
	config := common.GetConfig()
	uri := "mongodb+srv://"+ config.Username + ":"+ config.Password +"@cluster0.gke6f.mongodb.net/GO?retryWrites=true&w=majority"
	client, err = mongo.Connect(context.TODO(), uri, clientopt.ConnectTimeout(time.Duration(G_config.MongodbConnectTimeout) * time.Millisecond))
	if err != nil{
		return
	}

	G_logSink = &LogSink{
		client: client,
		logCollection: client.Database("cron").Collection("log"),
		logChan: make(chan *common.JobLog, 1000),
		autoCommitChan: make(chan *common.LogBatch, 1000),
	}

	go G_logSink.writeLoop()
	return
}

// send log (api for out usage)
func (logSink *LogSink) Append(jobLog *common.JobLog) {
	select {
	case logSink.logChan <- jobLog:
		fmt.Println("Sending log", jobLog)
	default:
		// if the chan is full, then just discard
	}
}

