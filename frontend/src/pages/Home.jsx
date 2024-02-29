import axios from 'axios';
import Header from '../components/home/Header';
import RestaurantCard from '../components/home/RestaurantCard';
import { useQuery } from '@tanstack/react-query';
import { useRef } from 'react';
import MainCardSkeleton from '../loading/MainCardSkeleton';
import { baseURL } from '../hooks/useAuth';


function Home() {
  const nameRef = useRef()

  const getResataurants = async () => {
		const res = await axios.get(`${baseURL}/restaurants/`);
		return res;
	};

  const handleSubmit = (e) => {
    e.preventDefault()
    createRestaurantMutation.mutate({
      name: nameRef.current.value
    })
  }
  
  const {data, isLoading} = useQuery({
    queryKey: ["restaurants"],
    queryFn: () => getResataurants()
  });

    return (
      <main>
        <Header />
        {isLoading ? (
            <MainCardSkeleton />
          ) : (
          <div className="py-3 px-36 mt-10 flex flex-wrap">
            {data.data?.map(item => {
              return (
                <RestaurantCard key={item.id} data={item} />
              )
            })}
          </div>
          )
        }
      </main>
  )
}

export default Home
