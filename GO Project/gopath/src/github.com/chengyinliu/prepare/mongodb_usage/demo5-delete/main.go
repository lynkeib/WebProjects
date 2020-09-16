package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/mongodb/mongo-go-driver/mongo"
	"io/ioutil"
	"os"
	"time"
)

type Config struct{
	Username string
	Password string
}

func getConfig() Config{
	var config Config
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

type TimePoint struct{
	StartTime int64 `bson:"start_time"`
	EndTime int64 `bson:"end_time"`
}

type LogRecord struct{
	JobName string `bson:"job_name"`
	Command string `bson:"command"`
	Err string `bson:"err"`
	Content string `bson:"content"`
	TimePoint TimePoint `bson:"time_point"`
}

type TimeBeforeCond struct{
	Before int64 `bson:"$lt"`
}

type DeleteCond struct{
	TimeBefore TimeBeforeCond`bson:"time_point.start_time"`
}

func main() {
	config := getConfig()
	client, err := mongo.Connect(context.TODO(), "mongodb+srv://"+ config.Username + ":"+ config.Password +"@cluster0.gke6f.mongodb.net/GO?retryWrites=true&w=majority")
	if err != nil{
		fmt.Println(err)
		return
	}
	db := client.Database("GO")
	collection := db.Collection("log")

	delCond := &DeleteCond{TimeBeforeCond{time.Now().Unix()}}

	delRes, err := collection.DeleteMany(context.TODO(),delCond)
	if err != nil{
		fmt.Println(err)
		return
	}
	fmt.Println(delRes.DeletedCount)
}
