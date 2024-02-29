import {useState} from "react"
import axios from "axios"
import { baseURL } from "./useAuth"


export default function useReservation() {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const createReservation = async ({slug, time, date, party_size, booker_first_name, booker_last_name, booker_phone, booker_email, booker_occasion, booker_request, setDidBook}) => {
        setLoading(true)
        try {
            const res = await axios.post(`${baseURL}/restaurant/${slug}/reserve`, 
            {
                booker_first_name,
                booker_last_name,
                booker_phone,
                booker_email,
                booker_occasion,
                booker_request
            },
            {
                params: {
                    date,
                    time, 
                    party_size,
                }
            }
            )

            setLoading(false)
            setDidBook(true)
            return res.data
        } catch(error) {
            setLoading(false)
            setError(error.response.data.msg)
        }
    }

    return {loading, error, createReservation}
}