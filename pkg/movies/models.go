package movies

import "github.com/gunslaveunit/cinemafan/common"

type Movie struct {
    Entity
    
    Title string `json:"title"`
}
