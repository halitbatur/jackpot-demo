import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import PayoutTable from '../components/PayoutTable';
import SymbolLegend from '../components/SymbolLegend';
import './SlotMachine.css';
import axios from 'axios';

const SYMBOLS = {
  "Vestra Coin": { weight: 2, image: "🪙" },
  "Brolyz": { weight: 3, image: "🎭" },
  "CMLE head": { weight: 4, image: "👑" },
  "Vestran Helmet": { weight: 6, image: "⛑️" },
  "Vesty": { weight: 8, image: "🎪" }
};

const SYMBOL_NAMES = Object.keys(SYMBOLS);

const SlotMachine = () => {
  const [reels, setReels] = useState(Array(5).fill(SYMBOL_NAMES[0]));
  const [spinning, setSpinning] = useState(false);
  const [stoppingReels, setStoppingReels] = useState(Array(5).fill(false));
  const [payout, setPayout] = useState(0);

  const getVisibleSymbols = (currentSymbol) => {
    const currentIndex = SYMBOL_NAMES.indexOf(currentSymbol);
    const prevIndex = currentIndex === 0 ? SYMBOL_NAMES.length - 1 : currentIndex - 1;
    const nextIndex = currentIndex === SYMBOL_NAMES.length - 1 ? 0 : currentIndex + 1;
    return {
      prev: SYMBOL_NAMES[prevIndex],
      current: currentSymbol,
      next: SYMBOL_NAMES[nextIndex]
    };
  };

  const spin = async () => {
    if (spinning) return;
    
    setSpinning(true);
    setStoppingReels(Array(5).fill(false));
    setPayout(0);

    try {
      const response = await axios.get('http://localhost:8000/spin/user123');
      const { reels: resultReels, payout: resultPayout, points_remaining } = response.data;
      
      for (let i = 0; i < 5; i++) {
        setTimeout(() => {
          setStoppingReels(prev => {
            const newState = [...prev];
            newState[i] = true;
            return newState;
          });

          setReels(prev => {
            const newReels = [...prev];
            newReels[i] = resultReels[i];
            return newReels;
          });

          if (i === 4) {
            setTimeout(() => {
              setSpinning(false);
              setPayout(resultPayout);
            }, 300);
          }
        }, 1500 + (i * 500));
      }
    } catch (error) {
      console.error('Error spinning:', error);
      setSpinning(false);
    }
  };

  const renderSymbol = (symbolName) => (
    <div className="symbol-content">
      <div className="symbol-image">{SYMBOLS[symbolName].image}</div>
    </div>
  );

  const initialSymbolsView = (symbol) => (
    <div className="final-symbols-container">
      <div className="symbol prev">
        {renderSymbol(getVisibleSymbols(symbol).prev)}
      </div>
      <div className="symbol current">
        {renderSymbol(symbol)}
      </div>
      <div className="symbol next">
        {renderSymbol(getVisibleSymbols(symbol).next)}
      </div>
    </div>
  );

  return (
    <div className="slot-machine-wrapper">
      <motion.div className="slot-machine">
        <div className="slot-machine-top">
          You won {payout}
          {[0, 1, 2].map((light) => (
            <motion.div
              key={light}
              className="slot-light"
              animate={{
                opacity: [0.4, 1],
                scale: [1, 1.1, 1],
              }}
              transition={{
                repeat: Infinity,
                duration: 1,
                delay: light * 0.3,
              }}
            />
          ))}
        </div>
        
        <div className="slot-machine-body">
          <div className="reels-container">
            {reels.map((symbol, index) => (
              <div key={index} className="reel-container">
                <div className="reel-mask">
                  {spinning && !stoppingReels[index] ? (
                    <motion.div
                      className="reel-strip"
                      initial={{ y: 0 }}
                      animate={{
                        y: [-1000, 0],
                        transition: {
                          duration: 0.5,
                          repeat: Infinity,
                          ease: "linear",
                          repeatType: "loop"
                        }
                      }}
                    >
                      {Array(20).fill(SYMBOL_NAMES).flat().map((sym, symIndex) => (
                        <div key={symIndex} className="symbol">
                          {renderSymbol(sym)}
                        </div>
                      ))}
                    </motion.div>
                  ) : (
                    initialSymbolsView(symbol)
                  )}
                </div>
                <div className="reel-highlight-top" />
                <div className="reel-highlight-bottom" />
              </div>
            ))}
          </div>
        </div>

        <div className="slot-machine-bottom">
          <motion.button 
            className={`spin-button ${spinning ? 'disabled' : ''}`}
            onClick={spin}
            disabled={spinning}
            whileHover={!spinning ? { scale: 1.05 } : {}}
            whileTap={!spinning ? { scale: 0.95 } : {}}
          >
            SPIN
          </motion.button>
        </div>
      </motion.div>
      <SymbolLegend />
      <PayoutTable />
    </div>
  );
};

export default SlotMachine;