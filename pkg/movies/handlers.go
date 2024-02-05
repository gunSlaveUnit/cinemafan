package movies

import (
    "net/http"
    "encoding/json"


	"github.com/gunslaveunit/cinemafan/pkg/common"
)

var movies = []Movie {
    {
        Entity: common.Entity {
            ID: 1,
        },
        Title: "Iron man",
    },
    {
        Entity: common.Entity {
            ID: 2,
        },
        Title: "Cyberpunk: Edgerunners",
    },
    {
        Entity: common.Entity {
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
