import { createContext, useEffect, useState } from "react"
import useAuth, { api, baseURL } from "../hooks/useAuth"
import Cookies from "js-cookie"

export const AuthenticationContext = createContext({
    data: null,
    loading: false,
    error: false,
    setAuthState: () => {}
})

export default function AuthContext({children}) {
    const [authState, setAuthState] = useState({
        data: null,
        loading: true,
        error: null,
    })

    const fetchUser = async () => {
        setAuthState({
            data: null,
            loading: true,
            error: null
        })
        try {
            const jwt = Cookies.get('access_token', { domain: '127.0.0.1', path:"/" });
            if (!jwt) {
                console.log("JWT doesn't exist!");
                return setAuthState({
                    user: null,
                    loading: false,
                    error: null
                })
            }
            const res = await api.get(`${baseURL}/auth/me`, { headers: { Authorization: `Bearer ${jwt}` } });
            api.defaults.headers.common["Authorization"] = `Bearer ${jwt}`;
            
            setAuthState({
                data: res.data,
                loading: false,
                error: null
            })
        } catch (err) {
            console.log(err)
            setAuthState({
                data: null,
                loading: false,
                error: err.response.data.message
            })
        }
    }

    useEffect(() => {
        fetchUser()
    }, [])

    return <AuthenticationContext.Provider value={{...authState, setAuthState}}>{children}</AuthenticationContext.Provider>
}