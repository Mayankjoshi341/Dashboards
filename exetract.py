import json
import os
import pandas as pd
matches = []
file_path = "C:\\Users\\mayan\\gitrepos\\Dashboards\\IPL Analysis & Dashboard\\IPL_Json_files"
def extract_match_info(file_path):
    for file in os.listdir(file_path):
        if file.endswith(".json"):
            with open(os.path.join(file_path, file), "r") as f:
                data = json.load(f)
                match_info = {
                    "match_id": data["info"].get("match_id"),
                    "season": data["info"].get("season"),
                    "date": data["info"].get("dates")[0],
                    "city": data["info"].get("city"),
                    "venue": data["info"].get("venue"),
                    "teams_1": data["info"].get("teams")[0],
                    "teams_2": data["info"].get("teams")[1],
                    "team_batting_first": data["info"].get("toss").get("winner"),
                    "team_batting_second": data["info"].get("toss").get("loser"),
                    "toss_winner": data["info"].get("toss").get("winner"),
                    "toss_decision": data["info"].get("toss").get("decision"),
                    "result_type": data["info"]["outcome"].get("result_type"),
                    "result_margin": data["info"]["outcome"].get("result_margin"),
                    "winner": data["info"]["outcome"].get("winner"),
                    "win_by_runs": data["info"]["outcome"].get("win_by_runs"),
                    "win_by_wickets": data["info"]["outcome"].get("win_by_wickets"),
                    "player_of_match": data["info"].get("player_of_match")[0] if data["info"].get("player_of_match") else None,
                    "match_type": data["info"].get("match_type"),
                    "overs": data["info"].get("overs"),
                    "balls_per_over": data["info"].get("balls_per_over")
                }
                matches.append(match_info)
                matches_df = pd.DataFrame(matches)
                matches_df.to_csv("matches.csv", index=False)
    print("Match information extracted and saved to matches.csv")

# extract_match_info(file_path)


deliveries = []
def extract_deliveries_info(json_folder):
    for file_name in os.listdir(json_folder):

        if not file_name.endswith(".json"):
            continue

        match_id = file_name.replace(".json", "")

        with open(
            os.path.join(json_folder, file_name),
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        innings = data["innings"]

        for inning_no, inning in enumerate(innings, start=1):

            batting_team = inning["team"]

            for over_data in inning["overs"]:

                over = over_data["over"]

                # Create phase column
                if over <= 5:
                    phase = "Powerplay"
                elif over <= 14:
                    phase = "Middle"
                else:
                    phase = "Death"

                for ball_no, delivery in enumerate(
                    over_data["deliveries"],
                    start=1
                ):

                    batter = delivery.get("batter")
                    bowler = delivery.get("bowler")
                    non_striker = delivery.get("non_striker")

                    runs = delivery.get("runs", {})

                    batter_runs = runs.get("batter", 0)
                    extras = runs.get("extras", 0)
                    total_runs = runs.get("total", 0)

                    # Boundaries
                    is_boundary_4 = 1 if batter_runs == 4 else 0
                    is_boundary_6 = 1 if batter_runs == 6 else 0

                    # Wickets
                    is_wicket = 0
                    dismissal_type = None
                    player_out = None

                    if "wickets" in delivery:

                        wicket = delivery["wickets"][0]

                        is_wicket = 1
                        dismissal_type = wicket.get("kind")
                        player_out = wicket.get("player_out")

                    deliveries.append({
                        "match_id": match_id,
                        "inning": inning_no,
                        "batting_team": batting_team,
                        "phase": phase,

                        "over": over,
                        "ball": ball_no,

                        "batter": batter,
                        "bowler": bowler,
                        "non_striker": non_striker,

                        "batter_runs": batter_runs,
                        "extras": extras,
                        "total_runs": total_runs,

                        "is_wicket": is_wicket,
                        "dismissal_type": dismissal_type,
                        "player_out": player_out,
                        "is_dot_ball": 1 if total_runs == 0 else 0,

                        "is_single": 1 if batter_runs == 1 else 0,
                        "is_boundary_4": is_boundary_4,
                        "is_boundary_6": is_boundary_6
                    })

    df_deliveries = pd.DataFrame(deliveries)

    print(df_deliveries.head())

    df_deliveries.to_csv(
        "deliveries.csv",
        index=False
    )

    print("deliveries.csv created successfully!")

extract_deliveries_info(file_path)

    
