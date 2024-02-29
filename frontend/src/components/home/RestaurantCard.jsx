import { Link } from 'react-router-dom'
import Price from '../restaurant/Price'
import Stars from '../Stars'

const RestaurantCard = ({data}) => {
    return (
        <Link to={`/restaurant/${data.slug}`}>
            <div className="w-64 h-72 m-3 rounded overflow-hidden border-primary border cursor-pointer">
            <img src={data.images.split("||")[0].slice(6)} alt="Image" className="w-full h-36" />
            <div className="p-1">
                <h3 className="font-bold text-2xl mb-2">{data.name}</h3>
                <div className="flex items-start">
                <Stars reviews={data.reviews} />
                <p className="ml-2">{data.reviews.length} review{data.reviews.length === 1 ? "" : "s"}</p>
                </div>
                <div className="text-reg font-light flex capitalize">
                <p className="mr-3">Mexican</p>
                <Price price={data.price} />
                <p>{data.location}</p>
                </div>
                <p className="text-sm mt-1 font-bold">Booked 3 times today</p>
            </div>
            </div>
        </Link>
    )
}

export default RestaurantCard