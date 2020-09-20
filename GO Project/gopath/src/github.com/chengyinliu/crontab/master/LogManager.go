package master

import (
	"context"
	"github.com/chengyinliu/crontab/common"
	"github.com/mongodb/mongo-go-driver/mongo"
	"github.com/mongodb/mongo-go-driver/mongo/clientopt"
	"github.com/mongodb/mongo-go-driver/mongo/findopt"
	"time"
)

type LogManager struct{
	client *mongo.Client
	logCollection *mongo.Collection
}

var (
	G_logManager *LogManager
)

func InitLogManager() (err error) {
	var (
		client *mongo.Client
	)
	config := common.GetConfig()
	uri := "mongodb+srv://"+ config.Username + ":"+ config.Password +"@cluster0.gke6f.mongodb.net/GO?retryWrites=true&w=majority"
	client, err = mongo.Connect(context.TODO(), uri, clientopt.ConnectTimeout(time.Duration(G_config.MongodbConnectTimeout) * time.Millisecond))
	if err != nil{
		return
	}

	G_logManager = &LogManager{
		client: client,
		logCollection: client.Database("cron").Collection("log"),
	}

	return
}

func (logManager *LogManager) ListLog(name string, skip int, limit int)(logArr []*common.JobLog, err error){
	logArr = make([]*common.JobLog, 0)

	filter := &common.JobLogFilter{
		name,
	}
	logSort := &common.SortLogByStartTime{-1}
	cursor, err := logManager.logCollection.Find(context.TODO(), filter, findopt.Sort(logSort), findopt.Skip(int64(skip)), findopt.Limit(int64(limit)))
	if err != nil{
		return
	}
	defer cursor.Close(context.TODO())
	for cursor.Next(context.TODO()){
		jobLog := &common.JobLog{}
		err = cursor.Decode(jobLog)
		if err != nil{
			continue
		}
		logArr = append(logArr, jobLog)
	}
	return
}