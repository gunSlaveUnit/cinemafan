import IMovie from "./IMovie"

const MovieCard = (data: IMovie) => {
  return (
    <div>
      <h1>{data.translatedTitle}</h1>
      {data.originalTitle}
    </div>
  )
}

export default MovieCard;
