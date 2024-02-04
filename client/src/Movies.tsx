import React from "react"

import IMovie from "./IMovie"
import MovieCard from "./MovieCard"

const Movies = () => {
  const [movies, setmovies] = React.useState<IMovie[]>([
    {
      id: 1,
      title: "Boo",
    },
    {
      id: 2,
      title: "Foo",
    },
    {
      id: 3,
      title: "Bar",
    },
  ]);

  return (
    <div>
      {movies.map(m => <MovieCard id={m.id} title={m.title} />)}
    </div>
  )
}

export default Movies
