package main

import (
	"fmt"
	"net/http"
)

type Entity struct {
	ID int
}

type Movie struct {
	Entity
	Title string
}

var movies = []Movie {
	{
		Entity: Entity {
			ID: 1,
		},
		Title: "Iron man",
	},
	{
		Entity: Entity {
			ID: 2,
		},
		Title: "Cyberpunk: Edgerunners",
	},
	{
		Entity: Entity {
			ID: 3,
		},
		Title: "The Raid: Redemption",
	},
}

func main() {
	fmt.Println(movies)

	server := &http.Server {
		Addr: ":8000",
	}

	server.ListenAndServe()
}