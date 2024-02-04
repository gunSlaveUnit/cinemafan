package handlers

import (
    "net/http"
    "encoding/json"
)

type Entity struct {
    ID int `json:"id"`
}

type Movie struct {
    Entity
    
    Title string `json:"title"`
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

func Items(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    
    body := map[string]interface{} {
        "data": movies,
    }

    response, _ := json.Marshal(body)
    
    w.Write(response)
}
