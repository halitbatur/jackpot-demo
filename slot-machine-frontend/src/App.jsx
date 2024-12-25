import './App.css'
import SlotMachine from './SlotMachine/SlotMachine'
import PayoutTable from './components/PayoutTable'
import QueenGame from './QueenGame/QueenGame'
import MemoryGame from './MemoryGame/MemoryGame'
function App() {
  return (
    <div className="app">
      {/* <SlotMachine /> */}
      <MemoryGame />
    </div>
  )
}

export default App
