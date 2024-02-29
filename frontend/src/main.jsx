import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import "react-datepicker/dist/react-datepicker.css"
import Restaurant from './pages/Restaurant.jsx'
import Menu from './pages/Menu.jsx'
import SearchPage from './pages/SearchPage.jsx'
import ReservationPage from './pages/ReservationPage.jsx'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import MainLayout from './pages/MainLayout.jsx'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import CreateRestaurants from './api/CreateRestaurants.jsx'
import CreateItems from './api/createItems.jsx'
import CreateReviews from './api/createReviews.jsx'
import CreateUsers from './api/createUsers.jsx'
import Error from './pages/error-pages/Error.jsx'
import CreateTable from './api/createTables.jsx'
import Home from './pages/Home.jsx'


const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    errorElement: <Error />,
    children: [
      {
        path: "/",
        element: <Home />
      },
      {
        path: "/reserve/:slug",
        element: <ReservationPage />
      },
      {
        path: "/search",
        element: <SearchPage />
      },
      {
        path: "/restaurant/:slug",
        element: <Restaurant />,
      },
      {
        path: "/restaurant/:slug/menu",
        element: <Menu />
      }
    ]
  },
  {
    path: "/api/create-restaurants",
    element: <CreateRestaurants />,
    errorElement: <div>Error!</div>
  },
  {
    path: "/api/restaurant/:slug/add-items",
    element: <CreateItems />,
    errorElement: <div>Error!</div>
  },
  {
    path: "/api/restaurant/:slug/create-table",
    element: <CreateTable />,
    errorElement: <div>Error!</div>
  },
  {
    path: "/api/add-reviews",
    element: <CreateReviews />,
    errorElement: <div>Error!</div>
  },
  {
    path: "/api/add-users",
    element: <CreateUsers />,
    errorElement: <div>Error!</div>
  }
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={new QueryClient()}>
      <RouterProvider router={router} />
      <ReactQueryDevtools />
    </QueryClientProvider>
  </React.StrictMode>
)
