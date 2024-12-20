from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from random import random
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# Define symbols with their weights (higher number = more frequent)
REEL_SYMBOLS = {
    "Vestra Coin": 2, 
    "Brolyz": 3,   
    "CMLE head": 4,
    "Vestran Helmet": 6, 
    "Vesty": 8           
}

# Adjusted payout table with more significant payouts
PAYOUT_TABLE = {
    # 5 of a kind - Jackpot
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "Vestra Coin", "Vestra Coin"): 10000,
    ("Brolyz", "Brolyz", "Brolyz", "Brolyz", "Brolyz"): 5000,
    ("CMLE head", "CMLE head", "CMLE head", "CMLE head", "CMLE head"): 2500,
    ("Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Vestran Helmet"): 1000,
    ("Vesty", "Vesty", "Vesty", "Vesty", "Vesty"): 500,

    # 4 of a kind
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "Vestra Coin", "Any"): 750,
    ("Brolyz", "Brolyz", "Brolyz", "Brolyz", "Any"): 500,
    ("CMLE head", "CMLE head", "CMLE head", "CMLE head", "Any"): 375,
    ("Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Any"): 250,
    ("Vesty", "Vesty", "Vesty", "Vesty", "Any"): 175,

    # 3 of a kind
    ("Vestra Coin", "Vestra Coin", "Vestra Coin", "Any", "Any"): 150,
    ("Brolyz", "Brolyz", "Brolyz", "Any", "Any"): 125,
    ("CMLE head", "CMLE head", "CMLE head", "Any", "Any"): 100,
    ("Vestran Helmet", "Vestran Helmet", "Vestran Helmet", "Any", "Any"): 75,
    ("Vesty", "Vesty", "Vesty", "Any", "Any"): 50,
}

# Define request/response models
class SpinResponse(BaseModel):
    reels: list[str]
    payout: int
    points_remaining: int
    streak_bonus: int | None

# Global variables
USER_DATA = {}
SPIN_COST = 50
BONUS_THRESHOLD = 5

def weighted_choice():
    """
    Returns a random symbol based on weight distribution
    """
    total = sum(REEL_SYMBOLS.values())
    r = random() * total
    running_sum = 0
    for symbol, weight in REEL_SYMBOLS.items():
        running_sum += weight
        if r <= running_sum:
            return symbol
    return list(REEL_SYMBOLS.keys())[0]

@app.get("/spin/{user_id}", response_model=SpinResponse)
def spin_jackpot(user_id: str):
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"points": 5000, "streak_counter": 0}

    user_points = USER_DATA[user_id]["points"]
    streak_counter = USER_DATA[user_id]["streak_counter"]

    if user_points < SPIN_COST:
        return SpinResponse(reels=[], payout=0, points_remaining=user_points, streak_bonus=None)

    USER_DATA[user_id]["points"] -= SPIN_COST

    # Use weighted choice for more realistic probability
    reels = [weighted_choice() for _ in range(5)]

    def calculate_payout(reels):
        symbol_counts = {}
        for symbol in reels:
            symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
        
        max_payout = 0
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
                max_payout = max(max_payout, payout)
        
        return max_payout

    payout = calculate_payout(reels)
    USER_DATA[user_id]["points"] += payout

    streak_bonus = None
    if streak_counter >= BONUS_THRESHOLD:
        streak_bonus = 100  # Increased bonus
        USER_DATA[user_id]["points"] += streak_bonus
        USER_DATA[user_id]["streak_counter"] = 0

    return SpinResponse(reels=reels, payout=payout, points_remaining=USER_DATA[user_id]["points"], streak_bonus=streak_bonus)

@app.get("/points/{user_id}", response_model=dict)
def get_points(user_id: str):
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"points": 5000, "streak_counter": 0}
    return {"points": USER_DATA[user_id]["points"], "streak_counter": USER_DATA[user_id]["streak_counter"]}

@app.get("/streak/{user_id}", response_model=dict)
def increment_streak(user_id: str):
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {"points": 0, "streak_counter": 0}
    USER_DATA[user_id]["streak_counter"] += 1
    if USER_DATA[user_id]["streak_counter"] >= BONUS_THRESHOLD:
        return {"message": "Streak bonus unlocked! Spin to claim bonus points."}
    return {"streak": USER_DATA[user_id]["streak_counter"], "message": "Streak incremented."}

# Example to run the server (only for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
