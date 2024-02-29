import RestaurantHeader from '../components/restaurant/RestaurantHeader'
import RestaurantNavBar from '../components/restaurant/RestaurantNavBar'
import RestaurantMenu from '../components/restaurant/RestaurantMenu'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { useQuery } from '@tanstack/react-query'
import { baseURL } from '../hooks/useAuth'


const fetchMenu = async (slug) => {
  return axios.get(`${baseURL}/restaurants/${slug}/items`).then(
    res => res.data
  )
}

const Menu = () => {
  const {slug} = useParams()

  const {data: menuItems, isError, isLoading, error} = useQuery({
    queryKey: ["restaurant", slug,  "items"],
    queryFn: () => fetchMenu(slug)
  })

  if (isLoading) {
    return <div>Loading ...</div>
  } else if (isError) {
    return <div>Error {`${error}`}</div>
  }

  return (
    <>
        {/* <RestaurantHeader slug={slug} /> */}
        <div className="flex m-auto w-2/3 justify-between items-start -mt-11">
        <div className="flex m-auto w-2/3 justify-between items-start -mt-11">
            <div className="bg-white w-[100%] rounded p-3 shadow">
                <RestaurantNavBar slug={slug} />
                <RestaurantMenu menu={menuItems} />
            </div>
        </div>
        </div>
    </>
  )
}

export default Menu