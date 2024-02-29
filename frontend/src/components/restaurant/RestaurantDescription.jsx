import React from 'react'

const RestaurantDescription = ({description}) => {
    return (
        <div className="mt-4">
            <p className="text-lg font-light">
            {description}
            </p>
        </div>
    )
}

export default RestaurantDescription