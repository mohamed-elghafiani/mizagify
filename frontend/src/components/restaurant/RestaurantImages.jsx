import React from 'react'

const RestaurantImages = ({images}) => {
    const imgs_url = []
    imgs_url.push(images.split("||")[0].slice(6))
    images.split("||")[1].slice(7).split(";").forEach(url => {
        imgs_url.push(url)        
    });
    return (
        <div>
            <h1 className="font-bold text-3xl mt-10 mb-7 border-b pb-5">
                {imgs_url.length} photo{imgs_url.length > 1 ? "s" : ""}
            </h1>
            <div className="flex flex-wrap">
                {
                    imgs_url.map(url => (
                        url && <img key={Math.random() * 10000} className="w-56 h-44 mr-1 mb-1" src={url} alt="" />
                    ))
                }
            </div>
        </div>
    )
}

export default RestaurantImages