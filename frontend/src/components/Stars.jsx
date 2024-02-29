import fullStar from "../assets/icons/full-star.png"
import halfStar from "../assets/icons/half-star.png"
import emptyStar from "../assets/icons/empty-star.png"
import { calculateReviewRatingArg } from "../../utils/calculateReviewRatingAvg"

const Stars = ({reviews, reviewRating}) => {
    const rating = reviewRating || calculateReviewRatingArg(reviews)

    const stars = [];
    for(let i = 0; i < 5; i++) {
        const diff = parseFloat((rating - i).toFixed(1));
        if(diff >= 1) stars.push(fullStar);
        else if(diff < 1 && diff > 0) {
            if(diff <= 0.2) stars.push(emptyStar);
            else if(diff > 0.2 && diff <= 0.6) stars.push(halfStar)
            else stars.push(fullStar)
        }
        else stars.push(emptyStar)
    }

    return (
        <div className="flex items-center">
            {stars.map(star => {
                return (
                    <img src={star} alt="star icon" className="w-4 h-4 mr-1" key={new Int8Array(Math.random() * 10000)} />
                )}
            )}
        </div>
    )
}

export default Stars