package movies

import "github.com/gunslaveunit/cinemafan/pkg/shared"

type Movie struct {
    shared.Entity
    
    OriginalTitle string `json:"originalTitle"`
    TranslatedTitle string `json:"translatedTitle"`
}
