package movies

import "github.com/gunslaveunit/cinemafan/pkg/shared"

type Movie struct {
    shared.Entity
    
    Title string `json:"title"`
}
