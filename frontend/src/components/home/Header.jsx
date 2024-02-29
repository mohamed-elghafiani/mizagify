import { useState } from "react";
import { Form, useNavigate } from "react-router-dom";
import SearchHeader from "../search/SearchHeader";

const Header = () => {
    const navigate = useNavigate();
    const [location, setLocation] = useState("");
    return (
        <div className="h-64 bg-gradient-to-r to-[#FAEAB3] from-[#843030] p-2">
            <div className="text-center mt-10">
                <h1 className="text-white text-4xl font-bold mb-2">Satisfy your <span className="bg-gradient-to-r from-red-500 to-primary text-transparent bg-clip-text">Chahiya</span> with just a few clicks!</h1>
                <SearchHeader />
            </div>
        </div>
    )
}

export default Header