import React from 'react'
import { Link } from 'react-router-dom'

export const NotFound = () => {
  return (
    <div className="flex flex-col gap-2">
        Oops! Page Not Found
        <Link to="/">Home form link</Link>
        <a href="/">Home from a</a>
    </div>
  )
}
