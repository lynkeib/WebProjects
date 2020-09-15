package main

import (
	"fmt"
	"github.com/gorhill/cronexpr"
	"time"
)

func main() {
	var (
		expr *cronexpr.Expression
		err error
		now time.Time
		nextTime time.Time
	)
	expr, err = cronexpr.Parse("*/5 * * * *")
	if err != nil{
		fmt.Println(err)
	}
	// curr time
	now = time.Now()
	// next job time
	nextTime = expr.Next(now)
	// waiting timer
	time.AfterFunc(nextTime.Sub(now), func(){
		fmt.Print("asd")
	})
	// this package supports seconds and years
}
