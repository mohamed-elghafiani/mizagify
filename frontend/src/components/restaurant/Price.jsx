import React from 'react'

const Price = ({price}) => {
    const renderPrice = () => {
        if(price === "Price.CHEAP") {
            return <>
                <span>$$</span> <span className="text-gray-400">$$</span>
            </>
        } else if(price === "Price.REGULAR") {
            return <>
                <span>$$$</span> <span className="text-gray-400">$</span>
            </>
        } else {
            return <>
                <span>$$$$</span>
            </>
        }
    }
    return (
        <p className="flex mr-3">{renderPrice()}</p>
    )
}

export default Price