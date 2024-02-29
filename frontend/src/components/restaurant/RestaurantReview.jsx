import ReviewCard from "./ReviewCard"

const RestaurantReview = ({reviews}) => {
    return (
        <div>
            <h1 className="font-bold text-3xl mt-10 mb-7 border-b p-5">
                What's people are saying
            </h1>
            {reviews && reviews.length > 0 ? ( 
                reviews.map(review => <ReviewCard key={review.id} review={review} /> )
                ) : (
                    <div>No reviews yet!</div>   
                )
        }
        </div>
    )
}

export default RestaurantReview