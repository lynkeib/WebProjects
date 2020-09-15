package main

import (
	"context"
	"fmt"
	"os/exec"
	"time"
)

type result struct{
	err error
	output []byte
}

func main() {

	var (
		ctx context.Context
		cancelFunc context.CancelFunc
		cmd *exec.Cmd
		output []byte
		err error
		resultChan chan *result
		res *result
	)

	// create result queue
	resultChan = make(chan *result, 1000)

	ctx, cancelFunc = context.WithCancel(context.TODO())
	// return types
	// context: chan byte
	// cancelFunc: close(chan byte)


	// create goroutine
	go func(){
		cmd = exec.CommandContext(ctx, "/bin/bash", "-c", "sleep 2; echo hello;")

		// execute cmd and capture output
		output, err = cmd.CombinedOutput()

		// pass output to main routine
		resultChan <- &result{
			err: err,
			output: output,
		}
	}()

	// sleep 1
	time.Sleep(1 * time.Second)

	// Kill
	cancelFunc()

	// output result
	res = <- resultChan

	// print cmd result
	fmt.Println(res.err, string(res.output))
}
