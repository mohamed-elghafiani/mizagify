import validator from "validator"
import axios from 'axios';
import Cookies from 'js-cookie';

// axios.defaults.withCredentials = true

const baseURL = 'http://localhost:5000/api';

export const validateSignUpInputs = (inputs) => {
    const {first_name, last_name, email, phone, city, password} = inputs
    const errors = []

    const validatorSchema = [
        {
            valid: validator.isLength(first_name, {min: 4, max: 50}),
            errorMessage: "First name should be more than 4 characters and less than 50 characters"
        },
        {
            valid: validator.isLength(last_name, {min: 4, max: 50}),
            errorMessage: "Last name should be more than 4 characters and less than 50 characters"
        },
        {
            valid: validator.isEmail(email),
            errorMessage: "Email is invalid"
        },
        {
            valid: validator.isMobilePhone(phone),
            errorMessage: "Phone number is invalid"
        },
        {
            valid: validator.isLength(city, {min: 1}),
            errorMessage: "Please enter a city"
        },
        {
            valid: validator.isStrongPassword(password),
            errorMessage: "Password is not strong enough"
        },
    ]

    validatorSchema.forEach((check) => {
        if(!check.valid) {
            errors.push(check["errorMessage"])
        }
    })

    if(errors.length) {
        return errors[0]
    }
}


export const postCreateUserData = async (inputs) => {
    const res = await axios.post(`${baseURL}/auth/signup`, inputs)
    if (res.status === 200 || res.status === 201) {
        return JSON.stringify(res.data)
    } else {
        return JSON.stringify({"msg": "An error occured!"})
    }
}

export const validateLogInInputs = (inputs) => {
    const {email, password} = inputs
    const errors = []

    const validatorSchema = [
        {
            valid: validator.isEmail(email),
            errorMessage: "Email is invalid"
        },
        {
            valid: validator.isLength(password, {min: 1}),
            errorMessage: "Password shouldn't be empty"
        },
    ]

    validatorSchema.forEach((check) => {
        if(!check.valid) {
            errors.push(check["errorMessage"])
        }
    })

    if(errors.length) {
        return JSON.stringify({"msg": errors[0]})
    }
}

const api = axios.create({
    withCredentials: true
  })
  
export const postLogInUserData = async (inputs) => {
    const res = await api.post(`${baseURL}/auth/login`, inputs)
    return res.data;
}