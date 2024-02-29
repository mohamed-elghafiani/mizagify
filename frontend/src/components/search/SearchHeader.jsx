import { useState } from "react";
import { Form, useNavigate } from "react-router-dom";

const SearchHeader = () => {
  const navigate = useNavigate()
  const [location, setLocation] = useState("")

  return (
    <>
        <div className="text-left py-3 m-auto flex justify-center" role="search" id="search-from">
            <input onChange={(e) => setLocation(e.target.value)} value={location} className="rounded text-lg mr-3 p-2 w-[450px]" type="text" placeholder="State, City or town" name="search" />
            <button className="bg-red-600 rounded px-9 py-2 text-white"
            onClick={() => {
            if(location === "") return;
                navigate({pathname: "/search", search: `?city=${location}`})
                setLocation("")
            }}>
            Let's go
            </button>
        </div>
    </>
  )
}

export default SearchHeader