""" This script will play a variably defined number of games of Showcase Showdown with no user prompts.
    It assumes all possible Contestant 1 behavior.
    Results are put into a csv file named pir_fullsim_results.csv' """


import random
import csv

def spin_wheel():
    # Returns a random value from the wheel.
    return random.choice([x * 0.05 for x in range(1, 21)])

def simulate_spin(initial_spin):
    # Simulates a single spin for a contestant.
    second_spin = spin_wheel()
    total = initial_spin + second_spin
    if total > 1.00:
        return 0  # Bust
    return total

def simulate_competitors(contestant1_final_score):
    # Simulate the actions of Contestants 2 and 3, making strategic decisions based on the current score to beat.
    scores = []
    score_to_beat = contestant1_final_score

    for _ in range(2):  # Simulate for both Contestants 2 and 3
        first_spin = spin_wheel()
        final_score = first_spin
        if first_spin < score_to_beat:  # Decide whether a second spin is needed
            final_score = simulate_spin(first_spin)

        scores.append(final_score)

        # Update the score to beat for the next contestant
        score_to_beat = max(score_to_beat, final_score)

    return scores

def simulate_game(initial_winning_value, second_spin_choice):
    # Simulate a single game, including all contestant's decisions.
    # Contestant 1's decision to take a second spin
    contestant1_score = initial_winning_value if not second_spin_choice else simulate_spin(initial_winning_value)
    
    # Simulate Contestants 2 and 3's turns
    competitor_scores = simulate_competitors(contestant1_score)

    all_scores = [contestant1_score] + competitor_scores
    max_score = max(all_scores)

    # Handling ties by selecting a random winner among tied contestants
    winners = [i for i, score in enumerate(all_scores) if score == max_score]
    winner = random.choice(winners) if len(winners) > 1 else winners[0]

    return winner, all_scores

def run_full_simulation():
    # Run the simulation for all initial values and choices to take a second spin, calculating win percentages.
    num_simulations = 1000000
    results = []
    for initial_value in [x * 0.05 for x in range(1, 21)]:
        for second_spin_choice in [True, False]:
            wins = [0, 0, 0]  # Reset wins for each scenario
            for _ in range(num_simulations):  # Simulate 1000 games for each scenario
                winner, _ = simulate_game(initial_value, second_spin_choice)
                wins[winner] += 1
            win_percentages = [win / num_simulations * 100 for win in wins]
            results.append([initial_value, second_spin_choice, *win_percentages])

    return results

def write_results_to_csv(results):
    # Write the simulation results, including win percentages, to a CSV file.
    with open('pir_fullsim_results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Initial Value', 'Second Spin Choice', 'Contestant 1 Win %', 'Contestant 2 Win %', 'Contestant 3 Win %'])
        for result in results:
            writer.writerow([result[0], 'Yes' if result[1] else 'No', *result[2:]])

def main():
    results = run_full_simulation()
    write_results_to_csv(results)
    print("Simulation complete. Results have been saved to 'pir_fullsim_results.csv'.")

if __name__ == "__main__":
    main()
