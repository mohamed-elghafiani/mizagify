import { Link } from 'react-router-dom'
import AuthModal from '../../auth/AuthModal'
import { useContext } from 'react'
import { AuthenticationContext } from '../../contexts/authContext'
import {AiOutlineLogout} from "react-icons/ai"
import useAuth from '../../hooks/useAuth'

const Navbar = () => {
  const {data, error, loading} = useContext(AuthenticationContext)
  const {logout} = useAuth()

  return (
    <nav className="bg-white p-2 flex justify-between ">
        <Link to="/" className="font-bold text-primary text-2xl">
        Chahiya
        </Link>
        <div>
            {loading ? null : (
              <div className='flex'>
              {data ? (
                <div className="flex justify-between items-center gap-5">
                  <button className="flex justify-between items-center gap-2" onClick={() => logout()}>
                    <AiOutlineLogout /> <span>Logout</span>
                  </button>
                  <span className="px-4 py-1 text-bold text-2xl rounded-full bg-primary text-white">
                    {data.first_name[0].toUpperCase()}
                  </span>
                </div>): (
                <>
                  <AuthModal isSignIn={true} />
                  <AuthModal isSignIn={false} />
                </>
              )}
            </div>
            )}
        </div>
    </nav>
  )
}

export default Navbar