import IMovie from "./IMovie"

const MovieCard = (data: IMovie) => {
  return (
    <div>
      <h1>{data.title}</h1>
    </div>
  )
}

export default MovieCard;
