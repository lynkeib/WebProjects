package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"github.com/mongodb/mongo-go-driver/mongo"
	"os"
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

func main() {
	config := getConfig()
	client, err := mongo.Connect(context.TODO(), "mongodb+srv://"+ config.Username + ":"+ config.Password +"@cluster0.gke6f.mongodb.net/GO?retryWrites=true&w=majority")
	if err != nil{
		fmt.Println(err)
		return
	}
	db := client.Database("GO")
	collection := db.Collection("jobSchedular")
	collection = collection
}
