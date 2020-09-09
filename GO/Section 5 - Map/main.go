package main

import "fmt"

func main() {
	colors := map[string]string{
		"red": "#ff0000",
	}
	colors["green"] = "#??????"
	// delete(colors, "red")
	printMap(colors)
}
func printMap(c map[string]string) {
	for color, hex := range c {
		fmt.Println("Color", color, "is", hex)
	}
}
