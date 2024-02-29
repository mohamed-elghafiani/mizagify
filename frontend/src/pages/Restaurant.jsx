import RestaurantHeader from '../components/restaurant/RestaurantHeader'
import RestaurantNavBar from '../components/restaurant/RestaurantNavBar'
import RestaurantTitle from '../components/restaurant/RestaurantTitle'
import RestaurantRating from '../components/restaurant/RestaurantRating'
import RestaurantDescription from '../components/restaurant/RestaurantDescription'
import RestaurantImages from '../components/restaurant/RestaurantImages'
import RestaurantReview from '../components/restaurant/RestaurantReview'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { fetchRestaurantBySlug } from '../api/api'
import RestaurantPageSkeleton from '../loading/RestaurantPageSkeleton'

const Restaurant = () => {
  const {slug} = useParams()

  const {data: restaurant, isError, isLoading} = useQuery({
    queryKey: ["restaurant"],
    queryFn: () => fetchRestaurantBySlug(slug)
  })

  if (isError) {
    throw Error("Can't fetch restaurant!")
  }
  return (
    <>{isLoading ? <RestaurantPageSkeleton /> : (
      <div className="relative">
        <RestaurantHeader slug={restaurant.slug} open_time={restaurant.open_time} close_time={restaurant.close_time} imgs={restaurant.images} />
        <div className="flex m-auto max-w-[800px] justify-between items-start -mt-11">
            <div className="bg-white w-full rounded p-3 shadow">
                <RestaurantNavBar slug={restaurant.slug} />
                <RestaurantTitle name={restaurant.name} />
                <RestaurantRating reviews={restaurant.reviews} />
                <RestaurantDescription description={restaurant.description} />
                <RestaurantImages images={restaurant.images} />
                <RestaurantReview reviews={restaurant.reviews} />
            </div>
        </div>
      </div>
    )}
    </>
  )
}

export default Restaurant