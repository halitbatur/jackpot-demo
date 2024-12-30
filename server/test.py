import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Test Parameters
TEST_PARAMS = {
    "BASE_URL": "http://localhost:8000",
    "TOTAL_USERS": 10,
    "TOTAL_SPINS": 200,
    "STARTING_POINTS": 5000,
    "SPIN_COST": 50,
    "MAX_WORKERS": 10
}

def spin_for_user(user_id, total_spins, base_url):
    # Initialize user points
    requests.get(f"{base_url}/points/{user_id}")

    max_points = 0
    total_payout = 0
    jackpot_wins = 0
    biggest_jackpot = 0

    for i in range(total_spins):
        # Spin the reels for each user
        response = requests.get(f"{base_url}/spin/{user_id}").json()
        points_remaining = response["points_remaining"]
        payout = response["payout"]
        total_payout += payout

        # Track jackpot wins
        if response["jackpot_won"]:
            jackpot_wins += 1
            biggest_jackpot = max(biggest_jackpot, payout)
            print(f"\n🎰 JACKPOT WIN! 🎰")
            print(f"User {user_id} won the grand jackpot of {payout} VP!")
            print(f"Winning combination: {response['reels']}\n")

        # Update max points if current points are higher
        if points_remaining > max_points:
            max_points = points_remaining

        # Print each spin result
        print(f"User: {user_id}, Spin {i+1}, Payout: {payout}, Points: {points_remaining}, Current Jackpot: {response['grand_jackpot']}")

        time.sleep(0.1)

    avg_payout = total_payout / total_spins
    final_points = requests.get(f"{base_url}/points/{user_id}").json()["points"]

    return final_points, max_points, avg_payout, total_payout, jackpot_wins, biggest_jackpot

def test_multiple_users_parallel():
    user_ids = [f"user_{i}" for i in range(TEST_PARAMS["TOTAL_USERS"])]
    user_final_points = []
    user_max_points = []
    user_avg_payouts = []
    user_total_payouts = []
    winners = []
    losers = []

    with ThreadPoolExecutor(max_workers=TEST_PARAMS["MAX_WORKERS"]) as executor:
        futures = {executor.submit(spin_for_user, user_id, TEST_PARAMS["TOTAL_SPINS"], TEST_PARAMS["BASE_URL"]): user_id for user_id in user_ids}
        for future in as_completed(futures):
            user_id = futures[future]
            try:
                final_points, max_points, avg_payout, total_payout, jackpot_wins, biggest_jackpot = future.result()
                user_final_points.append(final_points)
                user_max_points.append(max_points)
                user_avg_payouts.append(avg_payout)
                user_total_payouts.append(total_payout)
                
                # Track winners and losers
                if avg_payout >= TEST_PARAMS["SPIN_COST"]:
                    winners.append((user_id, avg_payout))
                else:
                    losers.append((user_id, avg_payout))
                    
            except Exception as exc:
                print(f"User {user_id} generated an exception: {exc}")

    # Calculate overall averages
    average_points = sum(user_final_points) / len(user_final_points)
    average_payout_all_users = sum(user_avg_payouts) / len(user_avg_payouts)
    total_payout_all_users = sum(user_total_payouts)

    print("\n=== Test Parameters ===")
    print(f"Total Users: {TEST_PARAMS['TOTAL_USERS']}")
    print(f"Spins per User: {TEST_PARAMS['TOTAL_SPINS']}")
    print(f"Starting Points: {TEST_PARAMS['STARTING_POINTS']}")
    print(f"Spin Cost: {TEST_PARAMS['SPIN_COST']}")
    print(f"Total Spins Executed: {TEST_PARAMS['TOTAL_USERS'] * TEST_PARAMS['TOTAL_SPINS']}")
    
    print("\n=== Overall Statistics ===")
    print(f"Average points after {TEST_PARAMS['TOTAL_SPINS']} spins: {average_points:.2f}")
    print(f"Average payout per spin across all users: {average_payout_all_users:.2f}")
    print(f"Total payout across all users: {total_payout_all_users}")
    
    print("\n=== Winners and Losers Analysis ===")
    print(f"Total Winners: {len(winners)} ({(len(winners)/len(user_ids)*100):.1f}%)")
    print(f"Total Losers: {len(losers)} ({(len(losers)/len(user_ids)*100):.1f}%)")
    
    if winners:
        avg_winner_payout = sum(w[1] for w in winners) / len(winners)
        print(f"Average winner payout: {avg_winner_payout:.2f}")
        top_winner = max(winners, key=lambda x: x[1])
        print(f"Top winner: {top_winner[0]} (avg payout: {top_winner[1]:.2f})")
    
    if losers:
        avg_loser_payout = sum(l[1] for l in losers) / len(losers)
        print(f"Average loser payout: {avg_loser_payout:.2f}")
        worst_loser = min(losers, key=lambda x: x[1])
        print(f"Biggest loser: {worst_loser[0]} (avg payout: {worst_loser[1]:.2f})")

    total_spins = TEST_PARAMS['TOTAL_USERS'] * TEST_PARAMS['TOTAL_SPINS']
    total_spent = total_spins * TEST_PARAMS['SPIN_COST']
    rtp = (total_payout_all_users / total_spent) * 100

    print(f"\n=== RTP Analysis ===")
    print(f"Total money spent: {total_spent}")
    print(f"Total money returned: {total_payout_all_users}")
    print(f"RTP: {rtp:.2f}%")

    # Add jackpot statistics
    total_jackpot_wins = sum(future.result()[4] for future in as_completed(futures))
    biggest_jackpot_win = max(future.result()[5] for future in as_completed(futures))
    
    print("\n=== Jackpot Statistics ===")
    print(f"Total Jackpot Wins: {total_jackpot_wins}")
    if total_jackpot_wins > 0:
        print(f"Biggest Jackpot Won: {biggest_jackpot_win} VP")
        jackpot_win_rate = (total_jackpot_wins / (TEST_PARAMS['TOTAL_USERS'] * TEST_PARAMS['TOTAL_SPINS'])) * 100
        print(f"Jackpot Win Rate: {jackpot_win_rate:.4f}%")

if __name__ == "__main__":
    test_multiple_users_parallel()