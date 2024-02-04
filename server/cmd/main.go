package main

import (
    "net/http"
    "encoding/json"

    "github.com/gunslaveunit/cinemafan/pkg/handlers"
)

func apiInfo(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    
    body := map[string]interface{} {
        "title": "Cinemafan API",
        "purpose": "",
        "api": []map[string]string {
            {
                "version": "1",
                "status": "development",
                "description": "",
            },
        },
    }

    response, _ := json.Marshal(body)
    
    w.Write(response)
}


func main() {
    router := http.NewServeMux()

    router.HandleFunc("/", apiInfo)
    router.HandleFunc("/api/v1/movies", handlers.Items)

    server := &http.Server {
        Addr: ":8000",
        Handler: router,
    }

    server.ListenAndServe()
}