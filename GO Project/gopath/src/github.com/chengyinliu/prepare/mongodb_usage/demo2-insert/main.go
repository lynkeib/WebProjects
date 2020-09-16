package main

import (
	"context"
	"encoding/json"
	"fmt"
	"github.com/mongodb/mongo-go-driver/bson/objectid"
	"io/ioutil"
	"github.com/mongodb/mongo-go-driver/mongo"
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

func main() {
	config := getConfig()
	client, err := mongo.Connect(context.TODO(), "mongodb+srv://"+ config.Username + ":"+ config.Password +"@cluster0.gke6f.mongodb.net/GO?retryWrites=true&w=majority")
	if err != nil{
		fmt.Println(err)
		return
	}
	db := client.Database("GO")
	collection := db.Collection("log")

	// create a log
	record := &LogRecord{
		"job10",
		"echo hello",
		"",
		"hello",
		TimePoint{time.Now().Unix(), time.Now().Unix() + 10},

	}

	res, err := collection.InsertOne(context.TODO(), record)
	if err != nil{
		fmt.Println(err)
		return
	}

	// _id if user doesn't assign _id, global unique id, 12 byte
	docId := res.InsertedID.(objectid.ObjectID)
	fmt.Println(docId.Hex())
}
