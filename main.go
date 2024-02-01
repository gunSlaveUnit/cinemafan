package main

import "fmt"

type Entity struct {
	ID int
}

type Movie struct {
	Entity
	Title string
}

func main() {
	movie := Movie {
		Entity: Entity {
			ID: 1,
		},
		Title: "Iron man",
	}

	fmt.Println(movie)
}