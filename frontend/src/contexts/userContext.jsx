import axios from 'axios';
import Cookies from 'js-cookie';
import React, { createContext, useState, useContext, useEffect } from 'react';

export const UserContext = createContext({
    user: null,
    loading: false,
    error: false,
    setUser: () => {}
});

const baseURL = 'http://localhost:5000/api';

const api = axios.create({
    withCredentials: true
})

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const jwt = Cookies.get('access_token');
                if (!jwt) {
                    console.log("JWT doesn't exist!");
                    return setUser({
                        user: null,
                        loading: null,
                        error: "Error while retrieving JWT token"
                    })
                }
                const res = await api.get(`${baseURL}/auth/me`, { headers: { Authorization: `Bearer ${jwt}` } });
                // Set jwt common for all subsequent requests
                api.defaults.headers.common["Authorization"] = `Bearer ${jwt}`;

                setUser(res.data);
                console.log("user data:", res.data);
            } catch (err) {
                console.error("failed fetching user data:", err);
            }
        };
    
        fetchUserData();
    }, []);

    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
};