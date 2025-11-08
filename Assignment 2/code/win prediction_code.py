# ============================================
# FIFA 2026 - Match Winner Prediction (48 Teams)


import numpy as np
import random

# Load saved Random Forest model
rf = joblib.load('random_forest_model.pkl')

# Select 48 teams from dataset (randomly or manually adjust)
available_teams = sorted(list(team_stats.index))
if len(available_teams) >= 48:
    selected_teams = random.sample(available_teams, 48)
else:
    selected_teams = available_teams  # if dataset has <48 teams

# Display the 48 teams with numbers
print("========== 48 Qualified Teams ==========\n")
for i, team in enumerate(selected_teams, start=1):
    print(f"{i}. {team}")

# Get team numbers from user
print("\nEnter two team numbers to predict the match outcome:")
try:
    home_no = int(input("Enter number for Home Team: "))
    away_no = int(input("Enter number for Away Team: "))

    if home_no == away_no:
        print("Error: Please choose two different teams.")
    elif 1 <= home_no <= len(selected_teams) and 1 <= away_no <= len(selected_teams):
        home_team = selected_teams[home_no - 1]
        away_team = selected_teams[away_no - 1]

        # Retrieve their stats
        ht = team_stats.loc[home_team]
        at = team_stats.loc[away_team]

        # Prepare features for prediction
        X_new = np.array([[ 
            ht['avg_scored'], at['avg_scored'],
            ht['avg_conceded'], at['avg_conceded'],
            ht['win_rate'], at['win_rate']
        ]])

        # Predict result using Random Forest
        pred = rf.predict(X_new)[0]

        # Display result
        print("\n-------------------------------------------")
        print(f"Match: {home_team} (Home)  vs  {away_team} (Away)")
        if pred == 2:
            print(f"Predicted Winner: {home_team}")
        elif pred == 0:
            print(f"Predicted Winner: {away_team}")
        else:
            print("Predicted Result: Draw")
        print("-------------------------------------------")

    else:
        print("Error: Invalid team numbers entered.")

except ValueError:
    print("Invalid input. Please enter valid team numbers only.")
