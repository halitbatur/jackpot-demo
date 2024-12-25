import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import './MemoryGame.css';

const SYMBOLS = ["🎭", "🐼", "🐘", "🐒", "🦁", "🐰"];
const GRID_SIZE = { rows: 3, cols: 4 };

const MemoryGame = () => {
  const [cards, setCards] = useState([]);
  const [flippedIndices, setFlippedIndices] = useState([]);
  const [matchedPairs, setMatchedPairs] = useState([]);
  const [isChecking, setIsChecking] = useState(false);

  useEffect(() => {
    initializeGame();
  }, []);

  const initializeGame = () => {
    // Create pairs of symbols
    const symbolPairs = [...SYMBOLS, ...SYMBOLS].slice(0, (GRID_SIZE.rows * GRID_SIZE.cols) / 2);
    const pairedCards = [...symbolPairs, ...symbolPairs]
      .sort(() => Math.random() - 0.5)
      .map((symbol, index) => ({
        id: index,
        symbol,
        isFlipped: false,
        isMatched: false
      }));
    setCards(pairedCards);
  };

  console.log(cards)

  const handleCardClick = async (index) => {
    // Prevent clicking if already checking or card is already flipped/matched
    if (
      isChecking ||
      flippedIndices.includes(index) ||
      matchedPairs.includes(cards[index].symbol)
    ) {
      return;
    }

    // Here you could make an API call to validate the move
    // const response = await axios.post('http://localhost:8000/flip', { position: index });
    
    const newFlipped = [...flippedIndices, index];
    setFlippedIndices(newFlipped);

    // Check for matches when two cards are flipped
    if (newFlipped.length === 2) {
      setIsChecking(true);
      
      const [firstIndex, secondIndex] = newFlipped;
      if (cards[firstIndex].symbol === cards[secondIndex].symbol) {
        // Match found
        setMatchedPairs([...matchedPairs, cards[firstIndex].symbol]);
      }
      
      // Reset flipped cards after delay
      setTimeout(() => {
        setFlippedIndices([]);
        setIsChecking(false);
      }, 1000);
    }
  };

  return (
    <div className="memory-game">
      <h1>• Memory Game Cards •</h1>
      <div className="game-grid">
        {cards.map((card, index) => (
          <motion.div
            key={card.id}
            className="card-container"
            onClick={() => handleCardClick(index)}
          >
            <motion.div
              className="card"
              initial={false}
              animate={{
                rotateY: flippedIndices.includes(index) || matchedPairs.includes(card.symbol) ? 180 : 0
              }}
              transition={{ duration: 0.4, ease: "easeOut" }}
            >
              <div className="card-face card-back">❓</div>
              <div className="card-face card-front">{card.symbol}</div>
            </motion.div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default MemoryGame;