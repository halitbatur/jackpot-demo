probability_no_jackpot = (3199999 / 3200000) ** 100
probability_at_least_one_jackpot = 1 - probability_no_jackpot
print(f"Probability of hitting at least one jackpot in 100 spins: {probability_at_least_one_jackpot:.10f}")