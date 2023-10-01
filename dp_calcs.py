import pandas as pd
from pybaseball import batting_stats
from pybaseball import pitching_stats

def calculate_percentiles(df):
    percentile_50 = df.quantile(0.5)
    percentile_62 = df.quantile(0.62)
    percentile_80 = df.quantile(0.8)
    percentile_87 = df.quantile(0.87)
    percentile_93 = df.quantile(0.93)
    percentile_99 = df.quantile(0.99)
    print("50th percentile:", percentile_50)
    print("62nd percentile:", percentile_62)
    print("80th percentile:", percentile_80)
    print("87th percentile:", percentile_87)
    print("93rd percentile:", percentile_93)
    print("99th percentile:", percentile_99)   

def calculate__reverse_percentiles(df):
    percentile_50 = df.quantile(0.5)
    percentile_38 = df.quantile(0.38)
    percentile_20 = df.quantile(0.2)
    percentile_13 = df.quantile(0.13)
    percentile_7 = df.quantile(0.07)
    percentile_1 = df.quantile(0.01)
    print("50th percentile:", percentile_50)
    print("62nd percentile:", percentile_38)
    print("80th percentile:", percentile_20)
    print("87th percentile:", percentile_13)
    print("93rd percentile:", percentile_7)
    print("99th percentile:", percentile_1)

def sp_or_rp(row):
    ip = row['IP']
    g = row['G']
    ip_per_g = ip/g
    if ip_per_g >= 3:
        return "Starter"
    else:
        return "Reliever"

year = input("What year are you calculating for?: ")

hitter_data = batting_stats(year, qual=150)

print("\n", year, "BATTING DATA:\n")
print(hitter_data)

dp_hitter_stat_columns = ['R','HR','RBI','SB','AVG','OPS']
dp_hitters = hitter_data[dp_hitter_stat_columns].loc[hitter_data['AB'] >= 150].copy()

print("\nTotal hitters:", len(hitter_data))
print("\nTotal DP hitters:", len(dp_hitters))

for stat in dp_hitter_stat_columns:
    print("calculating ranges for", stat)
    calculate_percentiles(dp_hitters[stat])

pitching_data = pitching_stats(year, qual=50)
pitching_data['sp_or_rp'] = pitching_data.apply (lambda row: sp_or_rp(row), axis=1)
print(pitching_data.sample(10))
dp_sp = pitching_data.loc[pitching_data['sp_or_rp'] == 'Starter'].copy()
dp_rp = pitching_data.loc[pitching_data['sp_or_rp'] == 'Reliever'].copy()

dp_sp_pitching_stat_columns = ['SO','W','ERA','WHIP']
dp_rp_pitching_stat_columns = ['SO','SV','HLD','ERA','WHIP']

for stat in dp_sp_pitching_stat_columns:
    print("calculating ranges for SP", stat)
    if stat in ['SO', 'W']:
        calculate_percentiles(dp_sp[stat])
    else:
        calculate__reverse_percentiles(dp_sp[stat])

for stat in dp_rp_pitching_stat_columns:
    print("calculating ranges for RP", stat)
    if stat in ['SO', 'SV', 'HLD']:
        calculate_percentiles(dp_rp[stat])
    else:
        calculate__reverse_percentiles(dp_rp[stat])
