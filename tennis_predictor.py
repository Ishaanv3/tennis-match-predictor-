import pandas as pd
# URL Link
url = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2026.csv"
df = pd.read_csv(url)
# Factors determining player Statistics
df["w_bp_rate"] = (df["w_bpSaved"] / df["w_bpFaced"]).fillna(0)
df["l_bp_rate"] = (df["l_bpSaved"] / df["l_bpFaced"]).fillna(0)
df["w_bp_conversion"] = ((df["l_bpFaced"] - df["l_bpSaved"]) / df["l_bpFaced"]).fillna(0)
df["l_bp_conversion"] = ((df["w_bpFaced"] - df["w_bpSaved"]) / df["w_bpFaced"]).fillna(0)
df["w_first_serve_pct"] = df["w_1stIn"] / df["w_svpt"]
df["l_first_serve_pct"] = df["l_1stIn"] / df["l_svpt"]

# Use previous statistics and categorize into winner and loser
winner_stats = df.groupby("winner_name")[["w_ace", "w_df", "w_bp_conversion", "winner_rank", "w_first_serve_pct"]].mean()
loser_stats = df.groupby("loser_name")[["l_ace", "l_df", "l_bp_conversion", "loser_rank", "l_first_serve_pct"]].mean()
# Rename loser_stats to match winner_stats so it can be merged
loser_stats.columns = ["w_ace", "w_df", "w_bp_conversion", "winner_rank", "w_first_serve_pct"]
player_stats = pd.concat([winner_stats, loser_stats]).groupby(level=0).mean()

# If player average rank missing, change to 300
player_stats["winner_rank"] = player_stats["winner_rank"].fillna(300)
player_stats = player_stats.fillna(0)



def predict_match(p1, p2):
    if p1 not in player_stats.index or p2 not in player_stats.index:
        print("❌ Player not found or invalid spelling.")
        return

    p1_stats = player_stats.loc[p1]
    p2_stats = player_stats.loc[p2]

    p1_score = ((500 / p1_stats["winner_rank"])+ (p1_stats["w_ace"] * 2)- p1_stats["w_df"]+ (p1_stats["w_bp_conversion"] * 15)+ (p1_stats["w_first_serve_pct"] * 10))
    p2_score = ((500 / p2_stats["winner_rank"])+ (p2_stats["w_ace"] * 2)- p2_stats["w_df"]+ (p2_stats["w_bp_conversion"] * 15)+ (p2_stats["w_first_serve_pct"] * 10))

    total = p1_score + p2_score

    p1_prob = (p1_score / total) * 100
    p2_prob = (p2_score / total) * 100

    print("\n ===============PREDICTION ================")
    if p1_prob > p2_prob:
        print(f"\n{p1} is expected to win the match. ({p1_prob:.2f}% Confidence.)\n {p1} Score: {p1_score:.2f} \n{p2} Score: {p2_score:.2f} ")
    else:
        print(f"{p2} is expected to win the match. ({p2_prob:.2f}% Confidence.)\n{p1} Score: {p1_score:.2f} \n{p2} Score: {p2_score:.2f} ")

player_a = input("Enter player 1 (e.g., Carlos Alcaraz): ")
player_b = input("Enter player 2 (e.g., Jannik Sinner): ")
predict_match(player_a, player_b)
