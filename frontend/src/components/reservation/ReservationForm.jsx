import { useEffect, useState } from "react"
import useReservation from "../../hooks/useReservation"
import { CircularProgress } from "@mui/material"

const ReservationForm = ({slug, date, time, party_size}) => {
    const [inputs, setInputs] = useState({
        booker_first_name: "",
        booker_last_name: "",
        booker_phone: "",
        booker_email: "",
        booker_occasion: "",
        booker_request: ""
    })
    const {error, loading, createReservation} = useReservation()
    const [disabled, setDisabled] = useState(true)

    const [didBook, setDidBook] = useState(false)

    useEffect(()=> {
        if(inputs.booker_first_name && inputs.booker_last_name && inputs.booker_email && inputs.booker_phone) {
            setDisabled(false)
        } else {
            setDisabled(true)
        }
    }, [inputs])

    const handleChangeInput = (e) => {
        setInputs({
            ...inputs,
            [e.target.name]: e.target.value,
        })
    }

    const handleClick = async () => {
        const booking = await createReservation({
            slug,
            time,
            date,
            party_size,
            booker_first_name: inputs.booker_first_name,
            booker_last_name: inputs.booker_last_name,
            booker_email: inputs.booker_email,
            booker_phone: inputs.booker_phone,
            booker_occasion: inputs.booker_occasion,
            booker_request: inputs.booker_request,
            setDidBook
        })
    }

    return (
        <div className="mt-10 flex flex-wrap justify-between w-[660px]">
            {didBook ? (<div>
                <h1>You are all booked up</h1>
                <p>Enjoy your reservation</p>
            </div>) : (
                <>
                <input type="text" className="border rounded p-3 w-80 mb-4" placeholder="First Name" name="booker_first_name" value={inputs.booker_first_name} onChange={handleChangeInput} />
                <input type="text" className="border rounded p-3 w-80 mb-4" placeholder="Last Name" name="booker_last_name" value={inputs.booker_last_name} onChange={handleChangeInput} />
                <input type="text" className="border rounded p-3 w-80 mb-4" placeholder="Phone Number" name="booker_phone" value={inputs.booker_phone} onChange={handleChangeInput} />
                <input type="text" className="border rounded p-3 w-80 mb-4" placeholder="Email" name="booker_email" value={inputs.booker_email} onChange={handleChangeInput} />
                <input type="text" className="border rounded p-3 w-80 mb-4" placeholder="Occasion (optional)" name="booker_occasion" value={inputs.booker_occasion} onChange={handleChangeInput} />
                <input type="text" className="border rounded p-3 w-80 mb-4" placeholder="Request (optional)" name="booker_request" value={inputs.booker_request} onChange={handleChangeInput} />
                <button onClick={handleClick} disabled={disabled || loading} className="bg-red-600 w-full p-3 text-white font-bold rounded disabled:bg-gray-300">
                    {loading ? <CircularProgress color="inherit" /> : "Complete Reservation"}
                </button>
                <p className="text-sm mt-4">
                    By clicking "Complete Reservation" you agree to the Chahiya Terms of Use and Privacy Policy. Standard
                    Text message rates may apply. You may opt out of receiving text messages at any time.
                </p>
                </>)
            }
        </div>
    )
}

export default ReservationForm