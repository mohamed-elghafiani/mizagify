import { calculateReviewRatingArg } from "../../../utils/calculateReviewRatingAvg"
import Stars from "../Stars"

const RestaurantRating = ({reviews}) => {
    return (
        <div className="flex items-end">
            <div className="ratings mt-2 flex items-center">
                <Stars reviews={reviews} />
                <p className="text-reg ml-3">{calculateReviewRatingArg(reviews).toFixed(1)}</p>
            </div>
            <div className="text-reg ml-4">
                {reviews.length} Review{reviews.length === 1 ? "" : "s"}
            </div>
        </div>
    )
}

export default RestaurantRating