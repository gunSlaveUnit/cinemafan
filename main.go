package main

import (
    "fmt"
    "net/http"
    "encoding/json"
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

func home(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "CINEMAFAN")
}

func items(w http.ResponseWriter, r *http.Request) {
    body := make(map[string]interface{})
    
    body["data"] = movies

    response, _ := json.Marshal(body)
    
    w.Write(response)
}

func main() {
    fmt.Println(movies)

    router := http.NewServeMux()

    router.HandleFunc("/", home)
    router.HandleFunc("/movies", items)

    server := &http.Server {
        Addr: ":8000",
        Handler: router,
    }

    server.ListenAndServe()
}