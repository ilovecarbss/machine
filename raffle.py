import pandas as pd
import random
import concurrent.futures

def simulate_raffle(tickets, num_winners, my_tickets):
    my_wins = 0
    for _ in range(num_winners):
        if not tickets:
            break
        winner = random.choice(tickets)
        tickets.remove(winner)

        if winner in my_tickets:
            my_wins += 1

    return my_wins

def run_simulation(simulation_id, tickets, num_winners, my_tickets, num_my_accounts):
    shuffled_tickets = tickets.copy()
    random.shuffle(shuffled_tickets)
    my_wins = simulate_raffle(shuffled_tickets, num_winners, my_tickets)
    win_percentage = (my_wins / num_my_accounts) * 100
    print(f"Simulation {simulation_id} completed. Win percentage: {win_percentage}%")
    return my_wins, win_percentage

def add_my_entries(participants, num_accounts, tickets_per_account):
    for i in range(num_accounts):
        address = f'my_account_{i}'  # Identifier for your accounts
        participants[address] = tickets_per_account
    return participants

# Load the CSV file
df = pd.read_csv('code\Part B\data.csv')  # Replace with your CSV file path

# Prepare the data from CSV
participants = {}
for index, row in df.iterrows():
    participants[row['address']] = row['tickets_bought']

# Add your entries
num_my_accounts = 143  # Number of your accounts
tickets_per_account = 10  # Tickets per account
participants = add_my_entries(participants, num_my_accounts, tickets_per_account)

# Create a list of tickets
tickets = []
my_tickets = set()
for participant, num_tickets in participants.items():
    for _ in range(num_tickets):
        ticket = f"{participant}_{random.randint(0, 9999):04d}"  # Unique ticket ID
        tickets.append(ticket)
        if 'my_account' in participant:
            my_tickets.add(ticket)

# Number of winners, simulations, and threads
num_winners = 2150
num_simulations = 200
num_threads = 20  # Set the number of threads for parallel execution

# Using ThreadPoolExecutor to run simulations in parallel
results = []
win_percentages = []
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = {executor.submit(run_simulation, i+1, tickets, num_winners, my_tickets, num_my_accounts): i for i in range(num_simulations)}
    print("sum of tickets:", len(tickets))
    for future in concurrent.futures.as_completed(futures):
        my_wins, win_percentage = future.result()
        results.append(my_wins)
        win_percentages.append(win_percentage)

# Compute the average number of wins and win percentage
average_wins = sum(results) / len(results)
average_win_percentage = sum(win_percentages) / len(win_percentages)
ethcost= 0.05*2100
s1 = 630-ethcost
s2 = 1050-ethcost
s3 = 2100-ethcost
cost = num_my_accounts*20
print("sum of tickets:", len(tickets))
print("Average number of wins for your accounts:", average_wins)
print("Average win percentage:", average_win_percentage, "%")
print(f"Total cost of tickets: {cost} USD")
print(f"Total winnings: {average_wins*s1} USD or {average_wins*s2} or USD or {average_wins*s3} USD")
print(f"Scenario 1 285mil fdv: {average_wins*s1-cost} USD")
print(f"Scenario 2 475mil fdv: {average_wins*s2-cost} USD")
print(f"Scenario 3 950mil fdv: {average_wins*s3-cost} USD")
