import { useLocation, useParams, useSearchParams } from 'react-router-dom'
import ReservationForm from '../components/reservation/ReservationForm'
import ReservationHeader from '../components/reservation/ReservationHeader'

const ReservationPage = () => {
    const {slug} = useParams()
    const location = useLocation()
    const params = new URLSearchParams(location.search)
    const time = params.get("time")
    const date = params.get("date")
    const party_size = params.get("party_size")
    const main_img = params.get("main_img")

    return (
        <div className="border-t h-screen">
            <div className="py-9 w-3/5 m-auto">
                <ReservationHeader slug={slug} time={time} date={date} party_size={party_size} main_img={main_img} />
                <ReservationForm slug={slug} time={time} date={date} party_size={party_size} />
            </div>
        </div>
    )
}

export default ReservationPage