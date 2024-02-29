import SearchHeader from '../components/search/SearchHeader'
import SearchSideBar from '../components/search/SearchSideBar'
import SearchRestaurantCard from '../components/search/SearchRestaurantCard'
import { useLocation } from 'react-router-dom'
import axios from 'axios'
import { useQuery } from '@tanstack/react-query'
import { useEffect } from 'react'
import { baseURL } from '../hooks/useAuth'

const SearchPage = () => {
  const location = useLocation()
  const queryParams = location.search
  console.log("locationl: ", queryParams)

  const fetchRestaurantsByLocation = async () => {
    const res = await axios.get(`${baseURL}/restaurants/filter${queryParams}`)
    
    if(!res.status == 200) {
      throw Error("Cannot fetch restaurants")
    }
    console.log(res)
    return res.data
  }

  const {data: restaurants, isError, isLoading, error, refetch} = useQuery({
    queryKey: ["restaurants", "location"],
    queryFn: () => fetchRestaurantsByLocation(),
    
  })

  useEffect(() => {
    // Refetch the restaurants whenever the city changes
    console.log("useEffect Called!")
    refetch();
  }, [queryParams]);

  if (isLoading) {
    return <div>Loading ...</div>
  } else if (isError) {
    return <div>Oops Something wron happened!</div>
  }
  return (
    <>
      <div className="bg-gradient-to-r to-[#FAEAB3] from-[#843030] p-2">
        <SearchHeader />
      </div>
      <div className="flex py-4 m-auto w-2/3 justify-between items-start">
          <SearchSideBar />
          <div className="w-5/6">
            {restaurants.length === 0 ? (
                <p>No match found!</p>
              ) : (
                <>
                  {
                    restaurants.map(restaurant => (
                        <SearchRestaurantCard key={restaurant.id} restaurant={restaurant} />
                      )
                    )
                  }
                </>
              )
            }
          </div>
      </div>
    </>
  )
}

export default SearchPage