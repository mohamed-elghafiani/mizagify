import axios from "axios"
import { useContext } from "react";
import { AuthenticationContext } from "../contexts/authContext";
import Cookies from 'js-cookie';


export const baseURL = 'http://127.0.0.1:5000/api';

export const api = axios.create({
    withCredentials: true
})

const useAuth = () => {
    const {data, error, loading, setAuthState} = useContext(AuthenticationContext)
    const signin = async ({email, password}, handleClose) => {
        setAuthState({
            data: null,
            loading: true,
            error: false
        })
        try {
            const res = await api.post(`${baseURL}/auth/login`, {email, password})
            setAuthState({
                data: res.data,
                loading: false,
                error: false
            })
            handleClose()
        } catch (error) {
            setAuthState({
                data: null,
                loading: false,
                error: error.response.data.message
            })
        }
    }

    // Sign Up Hook 
    const signup = async ({first_name, last_name, email, password, city, phone}) => {
        setAuthState({
            data: null,
            loading: true,
            error: false
        })
        try {
            const res = await axios.post(`${baseURL}/auth/signup`, {first_name, last_name, email, password, city, phone})
            setAuthState({
                data: res.data,
                loading: false,
                error: false
            })
            handleClose()
        } catch (error) {
            setAuthState({
                data: null,
                loading: false,
                error: error.response.data.message
            })
        }
    }

    const logout = () => {
        try {
            Cookies.remove("access_token")
            setAuthState({
                data: null,
                error: null,
                loading: false
            })
        } catch (error) {
            setAuthState({
              data: data,
              error: error.response.data.message,
              loading: false
            })
        }
      }

    return {
        signin,
        signup,
        logout
    }
}

export default useAuth;