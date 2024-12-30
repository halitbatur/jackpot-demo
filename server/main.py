from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from random import random
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define symbols with their weights (keeping the same distribution)
REEL_SYMBOLS = {
    "Vestra Coin": 1,    # (1/36 chance)
    "Brolyz": 4,         # (4/36 chance)
    "CMLE head": 8,      # (8/36 chance)
    "Vestran Helmet": 10, # (10/36 chance)
    "Vesty": 13          # (13/36 chance)
}

# Updated payout table with slightly reduced values
PAYOUT_TABLE = {
    # Five of a kind (keeping these high for excitement)
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "Vestra Coin", "Vestra Coin"): 5000,
    ("Brolyz", "Brolyz", "Brolyz", "Brolyz", "Brolyz"): 2500,
    ("CMLE head", "CMLE head", "CMLE head", "CMLE head", "CMLE head"): 1000,
    ("Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Vestran Helmet"): 750,
    ("Vesty", "Vesty", "Vesty", "Vesty", "Vesty"): 500,

    # Four of a kind (slightly reduced)
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "Vestra Coin", "Any"): 400,
    ("Brolyz", "Brolyz", "Brolyz", "Brolyz", "Any"): 200,
    ("CMLE head", "CMLE head", "CMLE head", "CMLE head", "Any"): 150,
    ("Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Any"): 100,
    ("Vesty", "Vesty", "Vesty", "Vesty", "Any"): 65,

    # Three of a kind (slightly reduced)
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "Any", "Any"): 85,
    ("Brolyz", "Brolyz", "Brolyz", "Any", "Any"): 65,
    ("CMLE head", "CMLE head", "CMLE head", "Any", "Any"): 50,
    ("Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Any", "Any"): 40,
    ("Vesty", "Vesty", "Vesty", "Any", "Any"): 30,

    # Two of a kind (keeping 5 VP increments)
    ("Vestra Coin", "Vestra Coin", "Any", "Any", "Any"): 25,
    ("Brolyz", "Brolyz", "Any", "Any", "Any"): 20,
    ("CMLE head", "CMLE head", "Any", "Any", "Any"): 15,
    ("Vestran Helmet", "Vestran Helmet", "Any", "Any", "Any"): 10,
    ("Vesty", "Vesty", "Any", "Any", "Any"): 5,
}

# Updated response model to include jackpot info
class SpinResponse(BaseModel):
    reels: list[str]
    payout: int
    points_remaining: int
    grand_jackpot: int
    jackpot_won: bool = False

# Global variables
USER_DATA = {}
SPIN_COST = 50
STARTING_POINTS = 5000
GRAND_JACKPOT = 0
JACKPOT_INCREMENT = 15  # Each spin adds 15 to jackpot

def weighted_choice():
    total = sum(REEL_SYMBOLS.values())
    r = random() * total
    running_sum = 0
    for symbol, weight in REEL_SYMBOLS.items():
        running_sum += weight
        if r <= running_sum:
            return symbol
    return list(REEL_SYMBOLS.keys())[0]

def calculate_payout(reels: list[str]) -> tuple[int, bool]:
    global GRAND_JACKPOT
    
    # Check for grand jackpot (one of each symbol)
    unique_symbols = set(reels)
    jackpot_won = False
    total_payout = 0
    
    if len(unique_symbols) == len(REEL_SYMBOLS):
        # Won the grand jackpot!
        total_payout = GRAND_JACKPOT
        jackpot_won = True
        GRAND_JACKPOT = 0  # Reset jackpot
    
    # Calculate regular wins
    symbol_counts = {}
    for symbol in reels:
        symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1

    max_regular_payout = 0
    for pattern, payout in PAYOUT_TABLE.items():
        pattern_counts = {}
        for symbol in pattern:
            if symbol != "Any":
                pattern_counts[symbol] = pattern_counts.get(symbol, 0) + 1

        matches = True
        for symbol, count in pattern_counts.items():
            if symbol_counts.get(symbol, 0) < count:
                matches = False
                break

        if matches:
            max_regular_payout = max(max_regular_payout, payout)

    return (total_payout + max_regular_payout, jackpot_won)

@app.get("/spin/{user_id}", response_model=SpinResponse)
async def spin_jackpot(user_id: str):
    global GRAND_JACKPOT
    
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"points": STARTING_POINTS}
    
    if USER_DATA[user_id]["points"] < SPIN_COST:
        return SpinResponse(
            reels=[],
            payout=0,
            points_remaining=USER_DATA[user_id]["points"],
            grand_jackpot=GRAND_JACKPOT,
            jackpot_won=False
        )

    # Increment jackpot and deduct spin cost
    GRAND_JACKPOT += JACKPOT_INCREMENT
    USER_DATA[user_id]["points"] -= SPIN_COST
    
    # Generate reels and calculate payout
    reels = [weighted_choice() for _ in range(5)]
    payout, jackpot_won = calculate_payout(reels)
    USER_DATA[user_id]["points"] += payout

    return SpinResponse(
        reels=reels,
        payout=payout,
        points_remaining=USER_DATA[user_id]["points"],
        grand_jackpot=GRAND_JACKPOT,
        jackpot_won=jackpot_won
    )

@app.get("/points/{user_id}")
async def get_points(user_id: str):
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"points": STARTING_POINTS}
    return {
        "points": USER_DATA[user_id]["points"],
        "grand_jackpot": GRAND_JACKPOT
    }

