package movies

import (
    "net/http"
    "encoding/json"


	"github.com/gunslaveunit/cinemafan/pkg/shared"
)

var movies = []Movie {
    {
        Entity: shared.Entity {
            ID: 1,
        },
        Title: "Iron man",
    },
    {
        Entity: shared.Entity {
            ID: 2,
        },
        Title: "Cyberpunk: Edgerunners",
    },
    {
        Entity: shared.Entity {
            ID: 3,
        },
        Title: "The Raid: Redemption",
    },
}

func Items(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Access-Control-Allow-Origin", "http://localhost:3000")
    
    body := map[string]interface{} {
        "data": movies,
    }

    response, _ := json.Marshal(body)
    
    w.Write(response)
}
