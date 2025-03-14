import csv
from datetime import datetime, timedelta
import streamlit as st
import os

# Function to generate round-robin schedule
def automate_match_scheduling(teams, start_date):
    n = len(teams)
    matches = []
    match_days = {}
    match_day = start_date
    num_days = n - 1
    
    for day in range(num_days):
        while match_day in match_days.values():  
            match_day += timedelta(days=1)
        match_days[day] = match_day
        for j in range(n // 2):
            match = (teams[j], teams[n - 1 - j])
            matches.append((match_day, match))
            match_day += timedelta(days=1)
        teams.insert(1, teams.pop())  
        
    return matches, match_days

# Function to generate single elimination playoff schedule
def single_elimination_schedule(teams, start_date):
    matches = []
    match_days = {}
    match_day = start_date
    num_teams = len(teams)
    num_rounds = num_teams - 1
    
    for i in range(num_rounds):
        while match_day in match_days.values():  
            match_day += timedelta(days=1)
        match_days[i] = match_day
        for i in range(num_teams // 2):
            match = (teams[i], teams[num_teams - 1 - i])
            matches.append((match_day, match))
            match_day += timedelta(days=1)
        teams = teams[:num_teams // 2]  
        num_teams //= 2
        
    return matches, match_days

# Function to generate tournament brackets
def generate_tournament_brackets(match_day, matches):
    tour_table = [["Date", "Team 1", "", "Team 2"]]
    for match_day, match in matches:
        tour_table.append([match_day.strftime("%Y-%m-%d"), match[0], "vs", match[1]])
    st.table(tour_table)    

def save_schedule_to_csv(round_robin_schedule, playoff_schedule, final_match_schedule, filename):
    # Write new data to CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the title for round-robin schedule
        writer.writerow(["Round Robin"])
        writer.writerow(["Date", "Team 1", "Team 2"])
        for match_day, match in round_robin_schedule:
            writer.writerow([match_day.strftime("%Y-%m-%d"), match[0], match[1]])

        # Write the title for playoff schedule
        writer.writerow([])
        writer.writerow(["Playoff"])
        writer.writerow(["Date", "Team 1", "Team 2"])
        for match_day, match in playoff_schedule:
            writer.writerow([match_day.strftime("%Y-%m-%d"), match[0], match[1]])

        # Write the title for final match schedule
        writer.writerow([])
        writer.writerow(["Final"])
        writer.writerow(["Date", "Team 1", "Team 2"])
        writer.writerow([final_match_schedule[0].strftime("%Y-%m-%d"), final_match_schedule[1], final_match_schedule[2]])

# Streamlit app
def main():
    st.set_page_config(page_title="Sports tournament scheduler")
    st.image("image")
    st.markdown("<h1>Sports tournament scheduler</h1>", unsafe_allow_html=True)

    # User input
    selected_sport = st.selectbox("Select the sport:", ['Cricket', 'Football', 'Hockey'])
    num_teams = st.number_input("Enter the Number of teams (minimum five):", min_value=5, max_value=16)

    # Input team names
    st.markdown("<h3>Enter Team Names</h3>", unsafe_allow_html=True)
    with st.form("teamForm"):
        team_names = []
        for i in range(1, num_teams + 1):
            st.write(f"Enter Team {i} Name:")
            team_name = st.text_input(f"Team {i}", key=f"{i}")
            team_names.append(team_name.strip())
        start_date_str = st.text_input("Enter the starting date (YYYY-MM-DD):", "2021-12-12")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

        if st.form_submit_button("Generate Schedule"):
            # Round-robin scheduling
            matches, match_days = automate_match_scheduling(list(team_names), start_date)

            st.write("\nRound Robin Schedule:")
            generate_tournament_brackets(match_days, matches)
            # enter top 4 teams
            st.write("\nEnter the top 4 teams:")
            top_teams = []
            for i in range(4):

                team_name = st.text_input(f"Team {i}", key=f"{i+9}") 
                if team_name in team_names:
                    top_teams.append(team_name)

            playoff_matches_rank1_2, _ = single_elimination_schedule(top_teams[:2], start_date + timedelta(days=len(match_days) + 1))
            playoff_matches_rank3_4, _ = single_elimination_schedule(top_teams[2:], start_date + timedelta(days=len(match_days) + 2))

            if len(playoff_matches_rank1_2) != 0 and len(playoff_matches_rank3_4) != 0:
                st.write("\nPlayoff Schedule (Rank 1 vs Rank 2) & (Rank 3 vs Rank 4):")
                generate_tournament_brackets(match_days, playoff_matches_rank1_2 + playoff_matches_rank3_4)

                # Final match
                st.write("\nEnter the top 2 teams after playoffs:")
                final_teams = []
                for j in range(2):
                    team_name = st.text_input("Teams {}: ".format(j + 1))
                    if team_name in top_teams:
                        final_teams.append(team_name)

                if len(final_teams) == 2:
                    final_match_day = max(match_days.values()) + timedelta(days=1)
                    final_match_schedule = [final_match_day, final_teams[0], final_teams[1]]
                    st.write("\nFinal Match:")
                    final_match_table = [["Date", "Team 1", "", "Team 2"]]
                    final_match_table.append([final_match_day.strftime("%Y-%m-%d"), final_teams[0], "vs", final_teams[1]])
                    st.table(final_match_table)

                    # Save the schedule to a CSV file
                    save_schedule_to_csv(matches, playoff_matches_rank1_2 + playoff_matches_rank3_4, final_match_schedule, "tournament_schedule.csv")

if __name__ == "__main__":
    main()