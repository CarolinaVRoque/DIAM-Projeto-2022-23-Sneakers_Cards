import './SingleCard.css'
export default function SingleCard({card, handleChoice, flipped, disabled}) {
    const handleClick = () => {
        if (!disabled) {
            handleChoice(card)
        }
    }


    return (
         <div className="card">
                    <div className={flipped ? "flipped" : ""}>
                        <img className="front" src={card.card} alt={"card front"} />
                        <img className="back"
                             onClick={handleClick}
                             src={require('../images/pb.png')}
                             alt={"card back"}
                        />
                    </div>
                </div>
    )
}