import { Link } from 'react-router-dom'

const RestaurantNavBar = ({slug}) => {
    return (
        <nav className="flex text-reg border-b pb-2">
            <Link to={`/restaurant/${slug}`} className="mr-7">Overview</Link>
            <Link to={`/restaurant/${slug}/menu`} className="mr-7">Menu</Link>
        </nav>
    )
}

export default RestaurantNavBar