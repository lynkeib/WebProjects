package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	resp, err := http.Get("http://google.com")
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	// context := make([]byte, 99999)
	// resp.Body.Read(context)
	// fmt.Println(string(context))
	io.Copy(os.Stdout, resp.Body)
}
