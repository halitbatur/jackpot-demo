const BASE_URL = "http://localhost:8000";
const userId = "user_1"; // Change this to test with different users

const symbols = {
    "Vestra Coin": "🪙",
    "Vestran Helmet": "⛑️",
    "Brolyz": "💎",
    "CMLE head": "👤",
    "Vesty": "🎩"
};

const PAYOUT_TABLE = {
    // Full matches (5 of a kind)
    "5x Vestra Coin": 10000,
    "5x Vestran Helmet": 5000,
    "5x Brolyz": 2500,
    "5x CMLE head": 1000,
    "5x Vesty": 500,

    // 4 of a kind
    "4x Vestra Coin": 500,
    "4x Vestran Helmet": 300,
    "4x Brolyz": 200,
    "4x CMLE head": 100,
    "4x Vesty": 50,

    // 3 of a kind
    "3x Vestra Coin": 150,
    "3x Vestran Helmet": 100,
    "3x Brolyz": 75,
    "3x CMLE head": 50,
    "3x Vesty": 25
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function createSymbolsString(count) {
    const symbolsArray = Object.values(symbols);
    let result = '';
    for (let i = 0; i < count; i++) {
        const randomSymbol = symbolsArray[Math.floor(Math.random() * symbolsArray.length)];
        result += `<div class="symbol">${randomSymbol}</div>`;
    }
    return result;
}

function createReel(finalSymbol) {
    return `
        <div class="reel">
            <div class="symbols-container">
                ${createSymbolsString(10)}
                <div class="symbol">${finalSymbol}</div>
                ${createSymbolsString(3)}
            </div>
        </div>
    `;
}

async function spinReel(reel, finalSymbol, index) {
    return new Promise(async (resolve) => {
        const symbolsContainer = reel.querySelector('.symbols-container');
        const startDelay = index * 400;
        
        await sleep(startDelay);
        
        // Start spin
        reel.classList.add('spinning');
        
        // Calculate final position
        const symbolHeight = 100; // height of one symbol
        const finalPosition = -symbolHeight * 10; // position where final symbol will be visible
        
        await sleep(1000 + (index * 500));
        
        // Stop spin
        reel.classList.remove('spinning');
        symbolsContainer.style.top = `${finalPosition}px`;
        
        await sleep(200); // Wait for transition to complete
        resolve();
    });
}

function createPayoutTable() {
    const table = document.createElement('table');
    table.className = 'payout-table';
    
    // Create header
    const header = table.createTHead();
    const headerRow = header.insertRow();
    const headers = ['Combination', 'Symbol', 'Payout'];
    headers.forEach(text => {
        const th = document.createElement('th');
        th.textContent = text;
        headerRow.appendChild(th);
    });

    // Create table body
    const tbody = table.createTBody();
    for (const [combination, payout] of Object.entries(PAYOUT_TABLE)) {
        const row = tbody.insertRow();
        
        // Combination name
        const nameCell = row.insertCell();
        nameCell.textContent = combination;
        
        // Symbol
        const symbolCell = row.insertCell();
        const symbolName = combination.split('x ')[1];
        symbolCell.textContent = symbols[symbolName] || '';
        
        // Payout
        const payoutCell = row.insertCell();
        payoutCell.textContent = payout;
    }

    return table;
}

document.getElementById("handle").addEventListener("click", async () => {
    const handle = document.getElementById("handle");
    const reelsContainer = document.getElementById("reels");
    
    // Disable handle during spin
    handle.style.pointerEvents = "none";
    handle.classList.add("pulled");

    try {
        const response = await fetch(`${BASE_URL}/spin/${userId}`);
        const data = await response.json();

        // Create reels with symbols
        const reelSymbols = data.reels.map(symbol => symbols[symbol] || "❓");
        reelsContainer.innerHTML = reelSymbols.map(symbol => createReel(symbol)).join("");

        const reelElements = reelsContainer.querySelectorAll(".reel");
        
        // Spin each reel
        const spinPromises = Array.from(reelElements).map((reel, index) => 
            spinReel(reel, reelSymbols[index], index)
        );

        // Wait for all reels to stop
        await Promise.all(spinPromises);

        // Update results
        document.getElementById("result").textContent = `Payout: ${data.payout}`;
        document.getElementById("points").textContent = `Points Remaining: ${data.points_remaining}`;

        // Reset handle
        handle.classList.remove("pulled");
        handle.style.pointerEvents = "auto";

    } catch (error) {
        console.error("Error spinning:", error);
        document.getElementById("result").textContent = "Error spinning. Please try again.";
        handle.classList.remove("pulled");
        handle.style.pointerEvents = "auto";
    }
});

// Add payout table to the container when page loads
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.payout-container').appendChild(createPayoutTable());
});