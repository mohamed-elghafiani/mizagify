import { Outlet } from 'react-router-dom'
import Navbar from '../components/main/Navbar'
import AuthenticationContext from '../contexts/authContext'

const MainLayout = () => {
    return (
        <main className="bg-gray-100 min-h-screen">
            <AuthenticationContext>
                <main className="max-w-screen-2xl m-auto bg-white">
                    <Navbar />
                    <Outlet />
                </main>
            </AuthenticationContext>
        </main>
    )
}

export default MainLayout