import ReservationModal from "../reservation/ReservationModal"

const RestaurantHeader = ({slug, open_time, close_time, imgs}) => {
    const renderTitle = (slug) => {
        const nameTitle = slug.split("-")
        nameTitle[nameTitle.length - 1] = `(${nameTitle[nameTitle.length - 1]})`
        return nameTitle.join(" ")
    }

    return (
        <div className="h-96 overflow-hidden"
            style={{ 
                backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(${imgs.split("||")[0].slice(6)})`,
                backgroundPosition: 'center',
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat'
            }}
            >
            <div className="bg-center h-full flex flex-col justify-center items-center">
                <h2 className="text-[4rem] text-white capitalize text-shadow text-center">
                {renderTitle(slug)}
                </h2>
                <ReservationModal slug={slug} open_time={open_time} close_time={close_time} imgs={imgs} />
            </div>
        </div>
    )
}

export default RestaurantHeader