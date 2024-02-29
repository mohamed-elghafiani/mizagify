import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import { Link, useLocation } from "react-router-dom"
import {baseURL} from "../../api/api"


const SearchSideBar = () => {

    const location = useLocation();

    const handleLinkClick = (paramKey, paramValue) => {
        const queryParams = new URLSearchParams(location.search || '');
        queryParams.set(paramKey, paramValue);
        const searchString = queryParams.toString();
        return {
          pathname: location.pathname,
          search: searchString ? `?${searchString}` : '',
        };
    };

    const fetchData = async (type) => {
        return axios.get(`${baseURL}/restaurants/${type}`).then(
            res => res.data
        )
    }

    // Locations data
    const {data: locations, isLoading: isLoading_loc, isError: isError_loc, error: error_loc} = useQuery({
        queryKey: ["locations"],
        queryFn: () => fetchData("locations")
    })
    console.log("Locations: ", locations)
    
    // Cuisines data
    const {data: cuisines, isLoading, isError, error} = useQuery({
        queryKey: ["cuisines"],
        queryFn: () => fetchData("cuisines")
    })
    console.log("Cuisines: ", cuisines)
    
    return (
        <div className="w-1/5">
            <div className="border-b pb-4">
                <h1 className="mb-2">Region</h1>
                {locations && locations.map(location => (
                    <Link to={handleLinkClick("city", location.name)} key={location.id} className="font-light text-reg capitalize block">{location.name}</Link>
                ))}
            </div>
            <div className="border-b pb-4 mt-3">
                <h1 className="mb-2">Cuisine</h1>
                {cuisines && cuisines.map(cuisine => (
                    <Link to={handleLinkClick("cuisine", cuisine.name)} key={cuisine.id} className="font-light text-reg capitalize block">{cuisine.name}</Link>
                ))}
            </div>
            <div className="mt-3 pb-4">
                <h1 className="mb-2">Price</h1>
                <div className="flex">
                    <Link to={handleLinkClick("price", "CHEAP")} className="border w-full text-reg font-light rounded-l p-2">$</Link>
                    <Link to={handleLinkClick("price", "REGULAR")} className="border-r border-t border-b w-full text-reg font-light p-2">$$</Link>
                    <Link to={handleLinkClick("price", "EXPENSIVE")} className="border-r border-t border-b w-full text-reg font-light rounded-r p-2">$$$</Link>
                </div>
            </div>
        </div>
    )
}

export default SearchSideBar