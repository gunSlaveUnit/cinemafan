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
    apiMux := http.NewServeMux()

    moviesMux := http.NewServeMux()
    moviesMux.HandleFunc("/movies", handlers.Items)

    apiMux.HandleFunc("/", apiInfo)
    apiMux.Handle("/api/v1/movies", http.StripPrefix("/api/v1", moviesMux))

    server := &http.Server {
        Addr: ":8000",
        Handler: apiMux,
    }

    server.ListenAndServe()
}