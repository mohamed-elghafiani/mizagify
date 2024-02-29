import { convertToDisplayTime } from "../../../utils/convertToDisplayTime"
import {format} from "date-fns"

const ReservationHeader = ({slug, date, time, party_size, main_img}) => {
    const renderTitle = (slug) => {
        const nameTitle = slug.split("-").map(str => {
            return str.charAt(0).toUpperCase() + str.slice(1)
        })
        nameTitle[nameTitle.length - 1] = `(${nameTitle[nameTitle.length - 1]})`
        return nameTitle.join(" ")
    }

    console.log("Time: ", time)
    console.log("Date: ", date)

    return (
        <div>
            <h3 className="font-bold">You're almost done!</h3>
            <div className="mt-5 flex">
                <img className="w-32 h-18 rounded" src={main_img} alt="" />
                <div className="ml-4">
                    <h1 className="text-3xl font-bold">
                        {renderTitle(slug)}
                    </h1>
                    <div className="flex mt-3">
                        <p className="mr-6">{format(new Date(date), "ccc, LLL d")}</p>
                        <p className="mr-6">{convertToDisplayTime(time + ".000Z")}</p>
                        <p className="mr-6">{party_size} {parseInt(party_size) === 1 ? "person" : "people"}</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ReservationHeader