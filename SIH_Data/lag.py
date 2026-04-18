import pandas as pd
import numpy as np


def calc_lag(year, month, lag):
    r_month = month - lag
    r_year = year
    if r_month < 1:
        r_month += 12
        r_year -= 1
    return (r_year, r_month)


def get_df_month_year(year, month, df):
    return df[(df.year == year) & (df.month == month)]


def get_feat_group1(lag_df):
    return [
        lag_df.J_count.values[0],  # J_count_lagN
        lag_df.J00_06_share.values[0],  # J00_06_share_lagN
        lag_df.J09_18_share.values[0],  # J09_18_share_lagN
        lag_df.J20_22_share.values[0],  # J20_22_share_lagN
        lag_df.J40_47_share.values[0],  # J40_47_share_lagN
        lag_df.J_bucket_entropy.values[0],  # J_bucket_entropy_lagN
    ]


def get_feat_group2(lag_df):
    return [
        lag_df.J_death_share.values[0],  # J_death_share_lagN
        lag_df.J_days_in_mean.values[0],  # J_days_in_mean_lagN
        lag_df.J_days_in_p90.values[0],  # J_days_in_p90_lagN
        lag_df.J_uti_share.values[0],  # J_uti_share_lagN
        lag_df.J_uti_days_mean.values[0],  # J_uti_days_mean_lagN
        lag_df.J_val_tot_mean.values[0],  # J_val_tot_mean_lagN
        lag_df.J_val_tot_p90.values[0],  # J_val_tot_p90_lagN
        lag_df.J_val_uti_share.values[0],  # J_val_uti_share_lagN
        lag_df.J_sex_m_share.values[0],  # J_sex_m_share_lagN
        lag_df.J_sex_f_share.values[0],  # J_sex_f_share_lagN
        lag_df.J_age_60p_share.values[0],  # J_age_60p_share_lagN
        lag_df.J_age_15_59_share.values[0],  # J_age_15_59_share_lagN
        lag_df.J_age_0_14_share.values[0],  # J_age_0_14_share_lagN
        lag_df.J_race_white_share.values[0],  # J_race_white_share_lagN
        lag_df.J_race_black_share.values[0],  # J_race_black_share_lagN
        lag_df.J_race_others_share.values[0],  # J_race_others_share_lagN
        lag_df.J_missing_race_share.values[0],  # J_missing_race_share_lagN
        lag_df.catchment_munic_unique.values[0],  # catchment_munic_unique_lagN
        lag_df.catchment_top1_share.values[0],  # catchment_top1_share_lagN
        lag_df.catchment_entropy.values[0],  # catchment_entropy_lagN
        lag_df.catchment_outside_local_share.values[
            0
        ],  # catchment_outside_local_share_lagN
        lag_df.J_missing_diag_sec_share.values[0],  # J_missing_diag_sec_share_lagN
        lag_df.J_missing_proc_share.values[0],  # J_missing_proc_share_lagN
    ]


def get_J_count_window(df, year, month, size):
    year_floor, month_floor = calc_lag(year, month, size)
    return df[
        ((df.year > year_floor) | ((df.year == year_floor) & (df.month >= month_floor)))
        & ((df.year < year) | ((df.year == year) & (df.month < month)))
    ]["J_count"]


main_df = pd.read_csv("./Aggregated_table.csv")
data_final = []

# Filtering low hospitalization count hospitals
filt_hos = []
hos_group = []
for hos in main_df["CNES"].unique():
    total = main_df[["CNES", "J_count"]][main_df.CNES == hos]["J_count"].sum()

    # Month average lower than 5
    if total / 35 <= 5:
        filt_hos.append(hos)
    else:
        hos_group.append([hos, total])


# Feature: size
# Based on quantile
main_df = main_df[main_df.CNES.isin(filt_hos) == False]
hos_df = pd.DataFrame(hos_group, columns=["CNES", "Total"])
[q1, q2, q3] = hos_df["Total"].quantile([0.25, 0.5, 0.75])
main_df = pd.merge(main_df, hos_df, on="CNES", how="left")


def get_hosp_porte(linha):
    if linha["Total"] < q1:
        return 0
    if linha["Total"] < q2:
        return 1
    if linha["Total"] < q3:
        return 2
    return 3


main_df["hospital_size"] = main_df.apply(get_hosp_porte, axis=1)


# Main loop
year = 2022
month = 1

while year < 2025 or month < 12:
    # Print for checking progress
    print(year, "/", month)

    df_temp = get_df_month_year(year, month, main_df)
    hos_all = df_temp.CNES.unique()

    for hos in hos_all:
        hos_df = main_df[main_df.CNES == hos]

        val = [
            year,  # year
            month,  # month
            hos,  # CNES
            hos_df.region.values[0],  # region
            int((month - 1) / 3 + 1),  # quarter
            year * 12 + month,  # time_index
            np.sin(2 * np.pi * month / 12),  # sin_month
            np.cos(2 * np.pi * month / 12),  # cos_month
            hos_df.hospital_size.values[0],  # hospital_size
        ]

        # Lagged Features
        for lag in [1, 2, 3, 6, 12]:
            (l_ano, l_mes) = calc_lag(year, month, lag)
            lag_df = get_df_month_year(l_ano, l_mes, hos_df)

            # In case there is no info on previous month
            if lag_df.empty:
                if lag == 2 or lag == 6:
                    val.extend([np.nan for _ in range(0, 6)])
                else:
                    val.extend([np.nan for _ in range(0, 29)])
            else:
                val.extend(get_feat_group1(lag_df))
                if lag == 1 or lag == 3 or lag == 12:
                    val.extend(get_feat_group2(lag_df))

        # Calculo do moving average
        df_aux = main_df[["year", "month", "CNES", "J_count"]][main_df.CNES == hos]
        ma3 = get_J_count_window(df_aux, year, month, 3)
        ma6 = get_J_count_window(df_aux, year, month, 6)
        ma12 = get_J_count_window(df_aux, year, month, 12)

        val_ma3 = np.nan
        if ma3.shape[0] == 3:
            val_ma3 = ma3.mean()

        val_ma6 = np.nan
        if ma6.shape[0] == 6:
            val_ma6 = ma6.mean()

        val_ma12 = np.nan
        if ma12.shape[0] == 12:
            val_ma12 = ma12.mean()

        val.extend(
            [
                val_ma3,  # J_count_ma3_lag1
                val_ma6,  # J_count_ma6_lag1
                val_ma12,  # J_count_ma12_lag1
                val[9] - val[38],  # J_growth_1m_lag1
            ]
        )

        current_df = get_df_month_year(year, month, hos_df)
        val.extend(get_feat_group1(current_df))
        val.extend(get_feat_group2(current_df))

        data_final.append(val)

    month += 1
    if month > 12:
        month -= 12
        year += 1


df_final = pd.DataFrame(
    data_final,
    columns=[
        "year",
        "month",
        "CNES",
        "region",
        "quarter",
        "time_index",
        "sin_month",
        "cos_month",
        "hospital_size",
        "J_count_lag1",
        "J00_06_share_lag1",
        "J09_18_share_lag1",
        "J20_22_share_lag1",
        "J40_47_share_lag1",
        "J_bucket_entropy_lag1",
        "J_death_share_lag1",
        "J_days_in_mean_lag1",
        "J_days_in_p90_lag1",
        "J_uti_share_lag1",
        "J_uti_days_mean_lag1",
        "J_val_tot_mean_lag1",
        "J_val_tot_p90_lag1",
        "J_val_uti_share_lag1",
        "J_sex_m_share_lag1",
        "J_sex_f_share_lag1",
        "J_age_60p_share_lag1",
        "J_age_15_59_share_lag1",
        "J_age_0_14_share_lag1",
        "J_race_white_share_lag1",
        "J_race_black_share_lag1",
        "J_race_others_share_lag1",
        "J_missing_race_share_lag1",
        "catchment_munic_unique_lag1",
        "catchment_top1_share_lag1",
        "catchment_entropy_lag1",
        "catchment_outside_local_share_lag1",
        "J_missing_diag_sec_share_lag1",
        "J_missing_proc_share_lag1",
        "J_count_lag2",
        "J00_06_share_lag2",
        "J09_18_share_lag2",
        "J20_22_share_lag2",
        "J40_47_share_lag2",
        "J_bucket_entropy_lag2",
        "J_count_lag3",
        "J00_06_share_lag3",
        "J09_18_share_lag3",
        "J20_22_share_lag3",
        "J40_47_share_lag3",
        "J_bucket_entropy_lag3",
        "J_death_share_lag3",
        "J_days_in_mean_lag3",
        "J_days_in_p90_lag3",
        "J_uti_share_lag3",
        "J_uti_days_mean_lag3",
        "J_val_tot_mean_lag3",
        "J_val_tot_p90_lag3",
        "J_val_uti_share_lag3",
        "J_sex_m_share_lag3",
        "J_sex_f_share_lag3",
        "J_age_60p_share_lag3",
        "J_age_15_59_share_lag3",
        "J_age_0_14_share_lag3",
        "J_race_white_share_lag3",
        "J_race_black_share_lag3",
        "J_race_others_share_lag3",
        "J_missing_race_share_lag3",
        "catchment_munic_unique_lag3",
        "catchment_top1_share_lag3",
        "catchment_entropy_lag3",
        "catchment_outside_local_share_lag3",
        "J_missing_diag_sec_share_lag3",
        "J_missing_proc_share_lag3",
        "J_count_lag6",
        "J00_06_share_lag6",
        "J09_18_share_lag6",
        "J20_22_share_lag6",
        "J40_47_share_lag6",
        "J_bucket_entropy_lag6",
        "J_count_lag12",
        "J00_06_share_lag12",
        "J09_18_share_lag12",
        "J20_22_share_lag12",
        "J40_47_share_lag12",
        "J_bucket_entropy_lag12",
        "J_death_share_lag12",
        "J_days_in_mean_lag12",
        "J_days_in_p90_lag12",
        "J_uti_share_lag12",
        "J_uti_days_mean_lag12",
        "J_val_tot_mean_lag12",
        "J_val_tot_p90_lag12",
        "J_val_uti_share_lag12",
        "J_sex_m_share_lag12",
        "J_sex_f_share_lag12",
        "J_age_60p_share_lag12",
        "J_age_15_59_share_lag12",
        "J_age_0_14_share_lag12",
        "J_race_white_share_lag12",
        "J_race_black_share_lag12",
        "J_race_others_share_lag12",
        "J_missing_race_share_lag12",
        "catchment_munic_unique_lag12",
        "catchment_top1_share_lag12",
        "catchment_entropy_lag12",
        "catchment_outside_local_share_lag12",
        "J_missing_diag_sec_share_lag12",
        "J_missing_proc_share_lag12",
        "J_count_ma3_lag1",
        "J_count_ma6_lag1",
        "J_count_ma12_lag1",
        "J_growth_1m",
        "J_count",
        "J00_06_share_lag0",
        "J09_18_share_lag0",
        "J20_22_share_lag0",
        "J40_47_share_lag0",
        "J_bucket_entropy_lag0",
        "J_death_share_lag0",
        "J_days_in_mean_lag0",
        "J_days_in_p90_lag0",
        "J_uti_share_lag0",
        "J_uti_days_mean_lag0",
        "J_val_tot_mean_lag0",
        "J_val_tot_p90_lag0",
        "J_val_uti_share_lag0",
        "J_sex_m_share_lag0",
        "J_sex_f_share_lag0",
        "J_age_60p_share_lag0",
        "J_age_15_59_share_lag0",
        "J_age_0_14_share_lag0",
        "J_race_white_share_lag0",
        "J_race_black_share_lag0",
        "J_race_others_share_lag0",
        "J_missing_race_share_lag0",
        "catchment_munic_unique_lag0",
        "catchment_top1_share_lag0",
        "catchment_entropy_lag0",
        "catchment_outside_local_share_lag0",
        "J_missing_diag_sec_share_lag0",
        "J_missing_proc_share_lag0",
    ],
)

df_final.to_csv("./Final_Table.csv", index=False)
