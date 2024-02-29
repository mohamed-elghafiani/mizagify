import { Link } from "react-router-dom"
import Price from "../restaurant/Price"
import { calculateReviewRatingArg } from "../../../utils/calculateReviewRatingAvg"
import Stars from "../Stars"

const SearchRestaurantCard = ({ restaurant }) => {
    const renderRatingText = () => {
        const rating = calculateReviewRatingArg(restaurant.reviews)

        if(rating > 4) return "Awesome";
        else if(rating <= 4 && rating > 3) return "Good";
        else if(rating <= 3 && rating > 0) return "Average";
        else return ""
    }
    return (
        <div className="border-b flex pb-5 ml-4">
            <img className="w-44 h-36 rounded"  src={restaurant.images.split("||")[0].slice(6)} alt="restaurant main image" />
            <div className="pl-5">
                <h2 className="text-3xl">{restaurant.name}</h2>
                <div className="flex items-start">
                    <Stars reviews={restaurant.reviews} />
                    <p className="ml-2 text-sm">{renderRatingText()}</p>
                </div>
                <div className="mb-9">
                    <div className="font-light flex text-reg">
                        <Price price={restaurant.price} />
                        <p className="mr-4 capitalize">{restaurant.cuisine}</p>
                        <p className="mr-4 capitalize">{restaurant.location}</p>
                    </div>
                </div>
                <div className="text-red-600">
                    <Link to={`/restaurant/${restaurant.slug}`}>View More Informations</Link>
                </div>
            </div>
        </div>
    )
}

export default SearchRestaurantCard