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
    "Vestra Coin": 1,    # (1/36 chance) - Most premium
    "Brolyz": 4,         # (4/36 chance)
    "CMLE head": 8,      # (8/36 chance)
    "Vestran Helmet": 10, # (10/36 chance)
    "Vesty": 13          # (13/36 chance) - Most common
}

# Updated payout table with slightly increased values
PAYOUT_TABLE = {
    # Five of a kind (any position)
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "Vestra Coin", "Vestra Coin"): 5000,
    ("Brolyz", "Brolyz", "Brolyz", "Brolyz", "Brolyz"): 2000,
    ("CMLE head", "CMLE head", "CMLE head", "CMLE head", "CMLE head"): 1000,
    ("Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Vestran Helmet"): 500,
    ("Vesty", "Vesty", "Vesty", "Vesty", "Vesty"): 250,

    # Four of a kind (increased)
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "Vestra Coin", "Any"): 500,
    ("Brolyz", "Brolyz", "Brolyz", "Brolyz", "Any"): 250,
    ("CMLE head", "CMLE head", "CMLE head", "CMLE head", "Any"): 175,
    ("Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Any"): 125,
    ("Vesty", "Vesty", "Vesty", "Vesty", "Any"): 85,

    # Full House combinations (increased)
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "Brolyz", "Brolyz"): 350,
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "CMLE head", "CMLE head"): 300,
    ("Brolyz", "Brolyz", "Brolyz", "Vestra Coin", "Vestra Coin"): 250,
    ("Brolyz", "Brolyz", "Brolyz", "CMLE head", "CMLE head"): 200,
    ("CMLE head", "CMLE head", "CMLE head", "Vestran Helmet", "Vestran Helmet"): 150,
    ("Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Vesty", "Vesty"): 100,

    # Three of a kind (increased)
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "Any", "Any"): 125,
    ("Brolyz", "Brolyz", "Brolyz", "Any", "Any"): 100,
    ("CMLE head", "CMLE head", "CMLE head", "Any", "Any"): 75,
    ("Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Any", "Any"): 60,
    ("Vesty", "Vesty", "Vesty", "Any", "Any"): 45,

    # Two pair combinations (increased)
    ("Vestra Coin", "Vestra Coin", "Brolyz", "Brolyz", "Any"): 75,
    ("Vestra Coin", "Vestra Coin", "CMLE head", "CMLE head", "Any"): 65,
    ("Brolyz", "Brolyz", "CMLE head", "CMLE head", "Any"): 55,
    ("CMLE head", "CMLE head", "Vestran Helmet", "Vestran Helmet", "Any"): 45,
    ("Vestran Helmet", "Vestran Helmet", "Vesty", "Vesty", "Any"): 35,

    # Two of a kind (increased)
    ("Vestra Coin", "Vestra Coin", "Any", "Any", "Any"): 35,
    ("Brolyz", "Brolyz", "Any", "Any", "Any"): 30,
    ("CMLE head", "CMLE head", "Any", "Any", "Any"): 25,
    ("Vestran Helmet", "Vestran Helmet", "Any", "Any", "Any"): 20,
    ("Vesty", "Vesty", "Any", "Any", "Any"): 15,
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
JACKPOT_INCREMENT = 10  # Each spin adds 15 to jackpot

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
    
    # Count occurrences of each symbol
    symbol_counts = {}
    for symbol in reels:
        symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
    
    # Check for grand jackpot (one of each symbol)
    if len(symbol_counts) == len(REEL_SYMBOLS):
        jackpot_amount = GRAND_JACKPOT
        GRAND_JACKPOT = 0  # Reset jackpot
        return jackpot_amount, True

    # Sort symbols by count (descending) and then by value (premium first)
    sorted_symbols = sorted(
        symbol_counts.items(),
        key=lambda x: (-x[1], -list(REEL_SYMBOLS.keys()).index(x[0]))
    )

    # Check for five of a kind
    if sorted_symbols[0][1] == 5:
        symbol = sorted_symbols[0][0]
        return PAYOUT_TABLE.get((symbol,) * 5, 0), False

    # Check for four of a kind
    if sorted_symbols[0][1] == 4:
        symbol = sorted_symbols[0][0]
        return PAYOUT_TABLE.get((symbol,) * 4 + ("Any",), 0), False

    # Check for full house (3 + 2)
    if len(sorted_symbols) >= 2 and sorted_symbols[0][1] == 3 and sorted_symbols[1][1] == 2:
        symbol1 = sorted_symbols[0][0]  # 3 of a kind
        symbol2 = sorted_symbols[1][0]  # pair
        full_house_key = (symbol1,) * 3 + (symbol2,) * 2
        if full_house_key in PAYOUT_TABLE:
            return PAYOUT_TABLE[full_house_key], False

    # Check for three of a kind
    if sorted_symbols[0][1] == 3:
        symbol = sorted_symbols[0][0]
        return PAYOUT_TABLE.get((symbol,) * 3 + ("Any", "Any"), 0), False

    # Check for two pair
    if len(sorted_symbols) >= 2 and sorted_symbols[0][1] == 2 and sorted_symbols[1][1] == 2:
        symbol1 = sorted_symbols[0][0]  # first pair
        symbol2 = sorted_symbols[1][0]  # second pair
        two_pair_key = (symbol1,) * 2 + (symbol2,) * 2 + ("Any",)
        if two_pair_key in PAYOUT_TABLE:
            return PAYOUT_TABLE[two_pair_key], False

    # Check for pair (two of a kind)
    if sorted_symbols[0][1] == 2:
        symbol = sorted_symbols[0][0]
        return PAYOUT_TABLE.get((symbol,) * 2 + ("Any", "Any", "Any"), 0), False

    # No winning combination
    return 0, False

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

