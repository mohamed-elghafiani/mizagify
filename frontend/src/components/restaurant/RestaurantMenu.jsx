import MenuCard from "../menu/MenuCard"

const Menu = ({ menu }) => {
    return (
        <main className="bg-white mt-5">
            <div>
                <div className="mt-4 mb-1 pb-1">
                    <h1 className="font-bold text-4xl">Menu</h1>
                </div>
                { menu.length > 0 ? (
                    <div className="flex flex-wrap justify-between">
                    {
                        menu.map(item => (
                            <MenuCard key={item.id} item={item} />
                        ))
                    }
                    </div>
                ) : (
                    <div className="flex flex-wrap justify-between">
                        <p>This restaurant does not have a menu!</p>
                    </div>
                )}
            </div>
        </main>
    )
}

export default Menu