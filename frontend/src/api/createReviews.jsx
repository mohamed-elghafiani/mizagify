import axios from "axios";
import { reviews } from "../seed/data";
import { useMutation } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { baseURL } from "./api";


const CreateReviews = () => {
    const { slug } = useParams()
    const postItem = async (item) => {
        return axios.post(`${baseURL}/reviews/create-review`, item).then(
            (res) => res.data
        )
    }

    const createItemMutation = useMutation({
        mutationFn: postItem,
        onError: (error, variables, context) => {
          console.log(error)
        },
        onSuccess: (data, variables, context) => {
          console.log(data, variables)
        }
    })
    // const getSlug = (item) => {
    //     return data.filter(restaurant => restaurant["name"] === item["restaurant_name"])[0]["slug"]
    // }
    const handleSubmit = () => {
        // e.preventDefault()
        reviews.map(item => createItemMutation.mutate(item))
      }

    // console.log("heelo", postRestaurant(data[0]))
    // const data_ = data;
    // data.map(rest => {
    //     console.log(rest)
    // })

    return (
        <div className="text-center">
            <h3 className="text-reg font-bold m-4">Add Reviews</h3>
            <button className="rounded-md bg-slate-400 px-8 py-4" onClick={() => handleSubmit()}>Post reviews</button>
        </div>
    )
}

export default CreateReviews