import './App.css'
import {useEffect, useState} from "react";
import {API_URL_COLLECTOR} from "./components/constants/constants";

    import card1 from './images/cards_final-01.png';
    import card2 from './images/cards_final-02.png';
    import card3 from './images/cards_final-03.png';
    import card4 from './images/cards_final-04.png';
    import card5 from './images/cards_final-05.png';
    import card6 from './images/cards_final-06.png';

import SingleCard from "./components/SingleCard";
import axios, * as others from 'axios';
axios.defaults.withCredentials = true;


    export const cardImage = [
        card1,
        card2,
        card3,
        card4,
        card5,
        card6
    ];

function App() {

    const [cards, setCards] = useState([])
    const [credits, setCredits] = useState(200)
    const [choiceOne, setChoiceOne] = useState(null)
    const [choiceTwo, setChoiceTwo] = useState(null)
    const [disabled, setDisabled] = useState(false)
    const [gameEnd, setGameEnd] = useState(false)

    // shuffle cards
    const shuffleCards = () => {
        const shuffledCards = [...cardImage, ...cardImage]
            .sort(() => Math.random() - 0.5)
            .map((card) => ({card, matched: false, id: Math.random() }))

        setChoiceOne(null)
        setChoiceTwo(null)
        setCards(shuffledCards)
        setCredits(200)
        getAndUpdateUserInfo()

    }




    const handleChoice = (card) => {
        choiceOne ? setChoiceTwo(card) : setChoiceOne(card)
    }

    useEffect(() => {
        if (choiceOne && choiceTwo){
            setDisabled(true)
            if (choiceOne.card === choiceTwo.card) {
                setCards(prevCards => {
                    return prevCards.map(card => {
                        if (card === choiceOne) {
                            choiceTwo.matched = true
                            choiceOne.matched = true
                            if (isGameEnd()){
                                setGameEnd(true)
                                console.log("Game Over")
                                //getAndUpdateUserInfo()
                            }
                            return card
                        } else {
                            return card
                        }
                    })
                })
                resetTurn()
            } else{
                setTimeout(() => resetTurn(), 1000)
            }
        }
        }
    , [choiceOne, choiceTwo])


    const resetTurn = () => {
        setChoiceOne(null)
        setChoiceTwo(null)
        if (credits > 0) {
            setCredits(prevTurns => prevTurns - 10)
        }

        setDisabled(false)
    }

    useEffect(() => {
        shuffleCards()
    }, [])

    function isGameEnd ()   {
        for( let card of cards) {
            if (!card.matched){
                return false;
            }
        }
         return true;
    }


    async function getAndUpdateUserInfo() {
        const query_string = window.location.search
        const url_param = new URLSearchParams(query_string)
        const user_id = url_param.get('id')
        const response = await axios.get(API_URL_COLLECTOR + '/game/' + user_id);
        console.log(response.data.credits)
        let user = response.data
        user.credits = user.credits + credits
        console.log(user)
        console.log(API_URL_COLLECTOR + '/' + user.user)


        const put = await axios.put(API_URL_COLLECTOR + '/' + user.user, {
            'user': user.user,
            'full_name': user.full_name,
            'nickname': user.nickname,
            'power': user.power,
            'credits': user.credits
        });

         window.location.replace('http://127.0.0.1:8000/SneakerCards/buy_booster');
    }



// {"user":4,"full_name":"Nuno Monteiro","nickname":"Nuno","power":0,"credits":0}



  return (
      <div className="body">
                <div className="App">
      <h1>Sneaker Cards</h1>
      <button onClick={shuffleCards}>Win Credits</button>

        <div className={"card-grid"}>
            {cards.map(card => (
            <SingleCard
                key={card.id}
                card={card}
                handleChoice={handleChoice}
                flipped={card === choiceOne  || card === choiceTwo|| card.matched}
                disabled={disabled}
            />
            ))}
        </div>
          <h3>Credits: {credits}</h3>

    </div>


      </div>

  );
}

export default App