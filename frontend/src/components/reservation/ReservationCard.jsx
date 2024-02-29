import { useState } from "react"
import { partSize, times } from "../../../data"
import DatePicker from "react-datepicker"
import useAvailability from "../../hooks/useAvailability"
import { CircularProgress } from "@mui/material"
import { Link } from "react-router-dom"
import { convertToDisplayTime } from "../../../utils/convertToDisplayTime"


const ReservationCard = ({slug, open_time, close_time, imgs}) => {
    const {loading, error, data, fetchAvailabilities} = useAvailability()
    const [partySize, setPartySize] = useState("2")
    const [time, setTime] = useState(open_time)
    const [date, setDate] = useState(new Date().toISOString().split("T")[0])
    const [selectedDate, setSelectedDate] = useState(new Date())    

    const main_img = imgs.split("||")[0].slice(6)

    const handleChangeDate = (date) => {
        if(date) {
            setDate(date.toISOString().split("T")[0])
            return setSelectedDate(date)
        }
        return setSelectedDate(null)
    }

    const handleClick = () => {
        fetchAvailabilities({
            slug,
            date,
            time,
            party_size: partySize
        })
    }

    const filterTime = () => {
        const timesWithinWindow = [];
        let isWithinWindow = false;
        times.forEach(time => {
            if(!isWithinWindow && time.time.slice(0, 8) === open_time) {
                isWithinWindow = true;
            }
            if(isWithinWindow) {
                timesWithinWindow.push(time)
            }
            if(time.time.slice(0, 8) === close_time) {
                isWithinWindow = false;
            }
        })
        return timesWithinWindow;
    }

    return (
        <div className="w-full h-[500px] bg-white rounded p-3">
            <div className="text-center pb-2 font-bold">
                <h4 className="mr-7 text-lg text-primary">Make a Reservarion</h4>
            </div>
            <div className="mt-4 my-5 flex flex-col">
                <label htmlFor="text-bold">Party size</label>
                <select name="party_size" className="pl-2 py-3 border-b font-light bg-gray-100" id="" value={partySize} onChange={(e) => setPartySize(e.target.value)} >
                    {partSize.map(size => (
                        <option key={Math.random() * 1000} value={size.value}>{size.label}</option>
                    ))}
                </select>
            </div>
            <div className="mt-5 flex justify-between">
                <div className="flex flex-col w-[48%]">
                    <label htmlFor="" className="text-bold">Date</label>
                    <DatePicker selected={selectedDate} onChange={handleChangeDate} className="bg-gray-100 pl-2 py-3 border-b font-light text-reg w-28" dateFormat="MMMM d" wrapperClassName="w-[48%]" />
                </div>
                <div className="flex flex-col w-[48%]">
                    <label htmlFor="" className="text-bold">Time</label>
                    <select name="time" id="" value={time} className="pl-2 py-3 border-b font-light bg-gray-100" onChange={(e) => setTime(e.target.value)} >
                        {filterTime().map(time => (
                            <option key={Math.random() * 1000} value={time.time}>{time.display_time}</option>
                        ))}
                    </select>
                </div>
            </div>
            <button onClick={handleClick} className="mt-4 bg-red-600 w-full text-white p-3 rounded text-lg mb-5" disabled={loading}>
                {loading ? <CircularProgress color="inherit" /> : "Find a time"}
            </button>
            {data && data.length ? (
                <div className='mt-4'>
                    <p className="text-reg">Select a time</p>
                    <div className="flex flex-wrap mt-2">
                        {data.map(t => {
                        return t.available ? <Link to={`/reserve/${slug}?date=${date}&time=${time}&party_size=${partySize}&main_img=${main_img}`} className="bg-red-600 cursor-pointer p-2 w-24 text-center text-white mb-3 rounded mr-3">
                            <p className="text-sm font-bold">{convertToDisplayTime(t.time)}</p>
                        </Link> : <p className="bg-gray-300 p-2 w-24 mb-3 rounded mr-3"></p>
                        })}
                    </div>
                </div>
            ) : null}
        </div>
    )
}

export default ReservationCard