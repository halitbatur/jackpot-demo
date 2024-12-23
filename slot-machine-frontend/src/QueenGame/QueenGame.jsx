import { useState } from 'react'
import './QueenGame.css'

function QueenGame() {
  const [board, setBoard] = useState(Array(8).fill(null).map(() => Array(8).fill(false)))
  const [queensPlaced, setQueensPlaced] = useState(0)

  const isValidPosition = (row, col) => {
    // Check row and column
    for (let i = 0; i < 8; i++) {
      if (board[row][i] || board[i][col]) return false
    }
    
    // Check diagonals
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 8; j++) {
        if (board[i][j] && 
            (Math.abs(row - i) === Math.abs(col - j))) {
          return false
        }
      }
    }
    return true
  }

  const handleCellClick = (row, col) => {
    if (board[row][col]) {
      const newBoard = [...board]
      newBoard[row][col] = false
      setBoard(newBoard)
      setQueensPlaced(queensPlaced - 1)
      return
    }

    if (queensPlaced >= 8) return
    
    if (isValidPosition(row, col)) {
      const newBoard = [...board]
      newBoard[row][col] = true
      setBoard(newBoard)
      setQueensPlaced(queensPlaced + 1)
    }
  }

  return (
    <div className="game-container">
      <h1>Eight Queens Puzzle</h1>
      <div className="board">
        {board.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {row.map((cell, colIndex) => (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={`cell ${(rowIndex + colIndex) % 2 === 0 ? 'white' : 'black'} ${cell ? 'queen' : ''}`}
                onClick={() => handleCellClick(rowIndex, colIndex)}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="status">
        Queens placed: {queensPlaced}/8
      </div>
    </div>
  )
}

export default QueenGame