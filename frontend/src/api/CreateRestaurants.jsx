import axios from "axios";
import { data } from "../seed/data";
import { useMutation } from "@tanstack/react-query";


const CreateRestaurants = () => {

    const postRestaurant = async (restaurant) => {
        return axios.post(`${baseURL}/restaurants/`, restaurant).then(
            (res) => res.data
        )
    }

    const createRestaurantMutation = useMutation({
        mutationFn: postRestaurant,
        onError: (error, variables, context) => {
          console.log(error)
        },
        onSuccess: (data, variables, context) => {
          console.log(data, variables)
        }
    })

    const handleSubmit = (e) => {
        // e.preventDefault()
        data.slice(1).map(restaurant => createRestaurantMutation.mutate(restaurant))
      }

    // console.log("heelo", postRestaurant(data[0]))
    // const data_ = data;
    // data.map(rest => {
    //     console.log(rest)
    // })

    return (
        <div className="text-center">
            <h3 className="text-reg font-bold m-4">Create a restaurant</h3>
            <button className="rounded-md bg-slate-400 px-8 py-4" onClick={() => handleSubmit()}>Post restaurant</button>
        </div>
    )
}

export default CreateRestaurants