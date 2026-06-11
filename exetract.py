import json
import os
import pandas as pd

file_path = r"C:\Users\mayan\gitrepos\Dashboards\IPL Analysis & Dashboard\IPL_Json_files"


def extract_match_info(json_folder):

    matches = []

    for file in os.listdir(json_folder):

        if not file.endswith(".json"):
            continue

        with open(
            os.path.join(json_folder, file),
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        info = data["info"]

        match_id = file.replace(".json", "")

        outcome = info.get("outcome", {})

        winner = outcome.get("winner")

        result_type = None
        result_margin = None
        win_by_runs = 0
        win_by_wickets = 0

        if "by" in outcome:

            if "runs" in outcome["by"]:

                result_type = "Runs"
                result_margin = outcome["by"]["runs"]
                win_by_runs = result_margin

            elif "wickets" in outcome["by"]:

                result_type = "Wickets"
                result_margin = outcome["by"]["wickets"]
                win_by_wickets = result_margin

        else:
            result_type = outcome.get("result", "Unknown")

        teams = info.get("teams", [])

        toss_winner = info.get("toss", {}).get("winner")
        toss_decision = info.get("toss", {}).get("decision")

        if toss_decision == "bat":
            team_batting_first = toss_winner

        else:
            team_batting_first = (
                teams[0]
                if teams[1] == toss_winner
                else teams[1]
            )

        team_batting_second = (
            teams[0]
            if teams[0] != team_batting_first
            else teams[1]
        )

        matches.append({

            "match_id": match_id,
            "season": info.get("season"),
            "match_number": info.get("match_number"),
            "date": info.get("dates")[0] if info.get("dates") else None,

            "city": info.get("city"),
            "venue": info.get("venue"),

            "team1": teams[0] if len(teams) > 0 else None,
            "team2": teams[1] if len(teams) > 1 else None,

            "team_batting_first": team_batting_first,
            "team_batting_second": team_batting_second,

            "toss_winner": toss_winner,
            "toss_decision": toss_decision,

            "winner": winner,

            "result_type": result_type,
            "result_margin": result_margin,

            "win_by_runs": win_by_runs,
            "win_by_wickets": win_by_wickets,

            "player_of_match":
                info.get("player_of_match")[0]
                if info.get("player_of_match")
                else None,

            "match_type": info.get("match_type"),

            "overs": info.get("overs"),
            "balls_per_over": info.get("balls_per_over")
        })

    matches_df = pd.DataFrame(matches)

    matches_df.to_csv(
        "matches.csv",
        index=False
    )

    print("\nMATCHES SUMMARY")
    print(matches_df.shape)
    print(matches_df.head())

    print("\nmatches.csv created successfully!")


def extract_deliveries_info(json_folder):

    deliveries = []

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

        for inning_no, inning in enumerate(
            innings,
            start=1
        ):

            batting_team = inning["team"]

            for over_data in inning["overs"]:

                over = over_data["over"]

                if over <= 5:
                    phase = "Powerplay"
                    phase_id = 1

                elif over <= 14:
                    phase = "Middle"
                    phase_id = 2

                else:
                    phase = "Death"
                    phase_id = 3

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

                    extra_info = delivery.get("extras", {})

                    wide_runs = extra_info.get("wides", 0)
                    noball_runs = extra_info.get("noballs", 0)
                    bye_runs = extra_info.get("byes", 0)
                    legbye_runs = extra_info.get("legbyes", 0)

                    is_legal_delivery = (
                        0
                        if wide_runs > 0 or noball_runs > 0
                        else 1
                    )

                    is_boundary_4 = (
                        1 if batter_runs == 4 else 0
                    )

                    is_boundary_6 = (
                        1 if batter_runs == 6 else 0
                    )

                    is_dot_ball = (
                        1 if total_runs == 0 else 0
                    )

                    is_single = (
                        1 if batter_runs == 1 else 0
                    )

                    is_wicket = 0
                    dismissal_type = None
                    player_out = None
                    fielder = None

                    if "wickets" in delivery:

                        wicket = delivery["wickets"][0]

                        is_wicket = 1
                        dismissal_type = wicket.get("kind")
                        player_out = wicket.get("player_out")

                        if (
                            "fielders" in wicket
                            and wicket["fielders"]
                        ):
                            fielder = wicket["fielders"][0].get("name")

                    deliveries.append({

                        "match_id": match_id,

                        "inning": inning_no,
                        "batting_team": batting_team,

                        "phase": phase,
                        "phase_id": phase_id,

                        "over": over,
                        "ball": ball_no,

                        "batter": batter,
                        "bowler": bowler,
                        "non_striker": non_striker,

                        "batter_runs": batter_runs,
                        "extras": extras,
                        "total_runs": total_runs,

                        "wide_runs": wide_runs,
                        "noball_runs": noball_runs,
                        "bye_runs": bye_runs,
                        "legbye_runs": legbye_runs,

                        "is_legal_delivery": is_legal_delivery,

                        "is_dot_ball": is_dot_ball,
                        "is_single": is_single,

                        "is_boundary_4": is_boundary_4,
                        "is_boundary_6": is_boundary_6,

                        "is_wicket": is_wicket,
                        "dismissal_type": dismissal_type,
                        "player_out": player_out,
                        "fielder": fielder
                    })

    deliveries_df = pd.DataFrame(deliveries)

    deliveries_df.to_csv(
        "deliveries.csv",
        index=False
    )

    print("\nDELIVERIES SUMMARY")
    print(deliveries_df.shape)

    print(
        f"Unique Matches: "
        f"{deliveries_df['match_id'].nunique():,}"
    )

    print(
        f"Unique Batters: "
        f"{deliveries_df['batter'].nunique():,}"
    )

    print(
        f"Unique Bowlers: "
        f"{deliveries_df['bowler'].nunique():,}"
    )

    print("\ndeliveries.csv created successfully!")


extract_match_info(file_path)
extract_deliveries_info(file_path)