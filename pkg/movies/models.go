package movies

import "github.com/gunslaveunit/cinemafan/pkg/common"

type Movie struct {
    common.Entity
    
    Title string `json:"title"`
}
