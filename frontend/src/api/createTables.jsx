import axios from "axios";
import { tables } from "../seed/data";
import { useMutation } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { baseURL } from "./api";


const CreateTable = () => {
    const { slug } = useParams()
    const postItem = async (data) => {
        return axios.post(`${baseURL}/restaurants/${slug}/create_table`, data).then(
            (res) => res.data
        )
    }

    const createItemMutation = useMutation({
        mutationFn: postItem,
        onError: (error, variables, context) => {
          console.log(error.response.data.msg)
        },
        onSuccess: (data, variables, context) => {
          console.log(data, variables)
        }
    })

    const handleSubmit = () => {
        // e.preventDefault()
        tables.map(table => createItemMutation.mutate(table))
      }

    return (
        <div className="text-center">
            <h3 className="text-reg font-bold m-4">Add Tables</h3>
            <button className="rounded-md bg-slate-400 px-8 py-4" onClick={() => handleSubmit()}>Post tables</button>
        </div>
    )
}

export default CreateTable