export const calculateReviewRatingArg = (reviews) => {
    if(!reviews.length) return 0;

    return reviews.reduce((sum, review) => {
        return sum + review.rating
    }, 0) / reviews.length
}