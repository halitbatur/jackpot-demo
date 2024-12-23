import './App.css'
import SlotMachine from './SlotMachine/SlotMachine'
import PayoutTable from './components/PayoutTable'
import QueenGame from './QueenGame/QueenGame'
function App() {
  return (
    <div className="app">
      <h1>Vestran Slot Machine</h1>
      <SlotMachine />
      {/* <QueenGame /> */}
    </div>
  )
}

export default App
