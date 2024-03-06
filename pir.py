import random

def spin_wheel():
    # Spin the wheel and return a value between 0.05 and 1.00 in 0.05 increments.
    return random.choice([x * 0.05 for x in range(1, 21)])

def contestant_spin(current_winning_value):
    # Simulate spins for a contestant and return their final score and if they won the bonus.
    first_spin = spin_wheel()
    if first_spin >= current_winning_value:
        return first_spin, first_spin == 1.00
    second_spin = spin_wheel()
    total = first_spin + second_spin
    if total <= 1.00:
        return total, total == 1.00
    return 0, False  # Bust if over 1.00

def simulate_game(initial_winning_value, second_spin_choice):
    # Simulate a single game, allowing for a second spin for Contestant 1 if chosen.
    bonuses = [False, False, False]  # Initialize bonuses for each contestant
    
    # Handle Contestant 1's second spin choice
    if second_spin_choice and initial_winning_value < 1.00:
        second_spin = spin_wheel()
        total = initial_winning_value + second_spin
        if total > 1.00:
            # Contestant 1 busts if the total exceeds 1.00
            initial_winning_value = 0
        else:
            # Update initial value if the second spin doesn't cause a bust
            initial_winning_value = total
            if total == 1.00:
                bonuses[0] = True  # Set bonus if total is exactly 1.00

    contestant_scores = [initial_winning_value]  # Start with Contestant 1's updated score

    # Contestants 2 and 3 take their turns
    for i in range(2):
        score, bonus = contestant_spin(0)  # Contestants 2 and 3 start fresh
        contestant_scores.append(score)
        bonuses[i+1] = bonus

    max_score = max(contestant_scores)
    if max_score == 0:  # All contestants disqualified
        winner = None
    else:
        winner = contestant_scores.index(max_score)

    return winner, bonuses, contestant_scores

def simulate_games(num_games, initial_winning_value, second_spin_choice):
    wins = [0, 0, 0]
    bonus_wins = [0, 0, 0]
    winning_values = [[], [], []]

    for _ in range(num_games):
        winner, bonuses, scores = simulate_game(initial_winning_value, second_spin_choice)
        if winner is not None:
            wins[winner] += 1
            winning_values[winner].append(scores[winner])
        for i, bonus in enumerate(bonuses):
            if bonus:
                bonus_wins[i] += 1

    return wins, bonus_wins, winning_values

def calculate_mean(values):
    # Calculate the mean of a list of values.
    return sum(values) / len(values) if values else 0

def main():
    winning_value = float(input("Enter the winning value for contestant one (0.05 to 1.00): "))
    second_spin_choice = input("Would Contestant 1 like to take a second spin? (yes/no): ").lower() == "yes"
    num_games = int(input("Enter the number of times the game will be played: "))
    
    wins, bonuses, winning_values = simulate_games(num_games, winning_value, second_spin_choice)
    for i, (win_count, bonus_count, values) in enumerate(zip(wins, bonuses, winning_values), start=1):
        mean_winning_value = calculate_mean(values)
        print(f"Contestant {i} won {win_count} times, received the $1000 bonus {bonus_count} times, and had a mean winning value of {mean_winning_value:.2f}.")

if __name__ == "__main__":
    main()

