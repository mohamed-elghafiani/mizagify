import {useState} from "react"
import axios from "axios"
import { baseURL } from "./useAuth"


export default function useAvailability() {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [data, setData] = useState(null)

    const fetchAvailabilities = async ({slug, party_size, date, time}) => {
        setLoading(true)
        try {
            const res = await axios.get(`${baseURL}/avail/${slug}`, {
                params: {
                    date,
                    time,
                    party_size
                }
            })

            setLoading(false)
            setData(res.data)
        } catch(error) {
            setLoading(false)
            setError(error.response.data.msg)
        }
    }

    return {loading, error, data, fetchAvailabilities}
}