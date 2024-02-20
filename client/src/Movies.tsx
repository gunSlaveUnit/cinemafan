import React from "react"

import IMovie from "./IMovie"
import MovieCard from "./MovieCard"

const Movies = () => {
  const [movies, setMovies] = React.useState<IMovie[]>([]);

  React.useEffect(() => {
    const fetchMovies = async () => {
      const response = await fetch('http://localhost:8000/api/v1/movies')
      const json = await response.json()
      const data = json['data']
      setMovies(data)
    }

    fetchMovies()
  }, [])

  return (
    <div>
      {movies
          .map(m => <MovieCard key={m.id} id={m.id} originalTitle={m.originalTitle} translatedTitle={m.translatedTitle} />)}
    </div>
  )
}

export default Movies
