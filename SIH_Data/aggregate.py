import numpy as np
import pandas as pd
import os


def get_region(file):
    return file[2:4]


def calc_age(row):
    if row["COD_IDADE"] == 4:
        return row["IDADE"]
    if row["COD_IDADE"] == 2:
        return 0
    if row["COD_IDADE"] == 3:
        return 0
    return np.nan


# Shannon Entropy
def calc_entropy(counts):
    counts = np.array(counts, dtype=float)
    total = counts.sum()
    if total == 0:
        return 0.0
    p = counts / total
    p = p[p > 0]  # remove zeros
    return -np.sum(p * np.log(p))


# Data reading
files = os.listdir("./Filtered_Data/")
dfs = []
for f in files:
    df = pd.read_csv("./Filtered_Data/" + f, index_col=0).reset_index(drop=True)
    df["region"] = get_region(f)
    dfs.append(df)
main_df = pd.concat(dfs)  # Joining all data in a single Data Frame

# New atribute for age in years (read "calc_age" for formula)
main_df["age_years"] = main_df.apply(calc_age, axis=1)


# Filtering of data by month/year
def get_df_month_year(month, year):
    floor = year * 10000 + month * 100
    celling = floor + 31
    return main_df.loc[(main_df.DT_INTER >= floor) & (main_df.DT_INTER <= celling)]


# List of lists of processed values for a data point
# Each list corresponds to a hospital for a given month/year
# Values (columns), in order
# [year, month, CNES (Hospital), region, quarter, time_index, sin_month, cos_month,
# J_count, J_morte_share, J_dias_perm_mean, J_dias_perm_p90, J_uti_share, J_uti_days_mean,
# J_val_tot_mean, J_val_tot_p90, J_val_uti_share, J_sex_f_share, J_sex_m_share, J_age_60p_share,
# J_missing_raca_share, J00_06_share, J09_18_share, J20_22_share, J40_47_share, J_bucket_entropy,
# catchment_munic_unique, catchment_top1_share, catchment_entropy, catchment_outside_local_share,
# J_missing_diag_sec_share, J_missing_proc_share]
data_month_hosp = []


month = 1
year = 2022

# Loop from 01/2022 to 11/2025
while year < 2025 or month < 12:
    # Print for checking progress
    print(year, "/", month)

    df = get_df_month_year(month, year)

    # Hospital Values
    cnes = df["CNES"].unique()
    for hos in cnes:
        h_df = df[df.CNES == hos]
        sizeh = h_df.shape[0]

        # Auxiliary calculations
        uti_mean = 0
        if not h_df["UTI_MES_TO"].isnull().values.any():
            uti_mean = h_df["UTI_MES_TO"].mean()

        bucket_1 = (
            h_df["DIAG_PRINC"][
                h_df.DIAG_PRINC.str.contains(r"J0[0-6]", na=False)
            ].shape[0]
            / sizeh
        )
        bucket_2 = (
            h_df["DIAG_PRINC"][
                h_df.DIAG_PRINC.str.contains(r"J09|J1[0-8]", na=False)
            ].shape[0]
            / sizeh
        )
        bucket_3 = (
            h_df["DIAG_PRINC"][
                h_df.DIAG_PRINC.str.contains(r"J2[0-2]", na=False)
            ].shape[0]
            / sizeh
        )
        bucket_4 = (
            h_df["DIAG_PRINC"][
                h_df.DIAG_PRINC.str.contains(r"J4[0-7]", na=False)
            ].shape[0]
            / sizeh
        )

        munic_uni = h_df["MUNIC_RES"].unique()

        data_month_hosp.append(
            [
                year,  # year
                month,  # month
                hos,  # CNES
                h_df["region"].values[0],  # region
                int((month - 1) / 3 + 1),  # quarter
                year * 12 + month,  # time_index
                np.sin(2 * np.pi * month / 12),  # sin_month
                np.cos(2 * np.pi * month / 12),  # cos_month
                h_df.shape[0],  # J_count
                h_df["MORTE"][h_df.MORTE == 1].shape[0] / sizeh,  # J_death_share
                h_df["DIAS_PERM"].mean(),  # J_days_in_mean
                np.percentile(h_df["DIAS_PERM"], 90),  # J_days_in_p90
                h_df["UTI_MES_TO"][h_df.UTI_MES_TO > 0].shape[0] / sizeh,  # J_uti_share
                uti_mean,  # J_uti_days_mean
                h_df["VAL_TOT"].mean(),  # J_val_tot_mean
                np.percentile(h_df["VAL_TOT"], 90),  # J_val_tot_p90
                h_df["VAL_UTI"][h_df.VAL_UTI > 0].shape[0] / sizeh,  # J_val_uti_share
                h_df["SEXO"][(h_df.SEXO == "F") | (h_df.SEXO == 3)].shape[0]
                / sizeh,  # J_sex_f_share
                h_df["SEXO"][(h_df.SEXO == "M") | (h_df.SEXO == 1)].shape[0]
                / sizeh,  # J_sex_m_share
                h_df["age_years"][h_df.age_years >= 60].shape[0]
                / sizeh,  # J_age_60p_share
                h_df["age_years"][(h_df.age_years < 60) & (h_df.age_years >= 15)].shape[
                    0
                ]
                / sizeh,  # J_age_15_59_share
                h_df["age_years"][h_df.age_years < 15].shape[0]
                / sizeh,  # J_age_0_14_share
                h_df["RACA_COR"][
                    (h_df.RACA_COR.isnull())
                    | (h_df.RACA_COR == 0)
                    | (h_df.RACA_COR >= 6)
                ].shape[0]
                / sizeh,  # J_missing_race_share
                h_df["RACA_COR"][h_df.RACA_COR == 1].shape[0]
                / sizeh,  # J_race_white_share
                h_df["RACA_COR"][h_df.RACA_COR == 2].shape[0]
                / sizeh,  # J_race_black_share
                h_df["RACA_COR"][(h_df.RACA_COR >= 3) & (h_df.RACA_COR <= 5)].shape[0]
                / sizeh,  # J_race_others_share
                bucket_1,  # J00_06_share
                bucket_2,  # J09_18_share
                bucket_3,  # J20_22_share
                bucket_4,  # J40_47_share
                calc_entropy(
                    [bucket_1, bucket_2, bucket_3, bucket_4]
                ),  # J_bucket_entropy
                len(munic_uni),  # catchment_munic_unique
                max(
                    [
                        h_df["MUNIC_RES"][h_df.MUNIC_RES == m].shape[0] / sizeh
                        for m in munic_uni
                    ]
                ),  # catchment_top1_share
                calc_entropy(
                    [h_df["MUNIC_RES"][h_df.MUNIC_RES == m].shape[0] for m in munic_uni]
                ),  # catchment_entropy
                h_df[["MUNIC_RES", "MUNIC_MOV"]][
                    h_df.MUNIC_RES != h_df.MUNIC_MOV
                ].shape[0]
                / sizeh,  # catchment_outside_local_share
                h_df["DIAG_SECUN"][
                    (h_df.DIAG_SECUN.isnull()) | (h_df.DIAG_SECUN == "")
                ].shape[0]
                / sizeh,  # J_missing_diag_sec_share
                h_df["PROC_REA"][
                    (h_df.PROC_REA.isnull()) | (h_df.PROC_REA == "")
                ].shape[0]
                / sizeh,  # J_missing_proc_share
            ]
        )

    month += 1
    if month > 12:
        month -= 12
        year += 1

df_final = pd.DataFrame(
    data_month_hosp,
    columns=[
        "year",
        "month",
        "CNES",
        "region",
        "quarter",
        "time_index",
        "sin_month",
        "cos_month",
        "J_count",
        "J_death_share",
        "J_days_in_mean",
        "J_days_in_p90",
        "J_uti_share",
        "J_uti_days_mean",
        "J_val_tot_mean",
        "J_val_tot_p90",
        "J_val_uti_share",
        "J_sex_f_share",
        "J_sex_m_share",
        "J_age_60p_share",
        "J_age_15_59_share",
        "J_age_0_14_share",
        "J_missing_race_share",
        "J_race_white_share",
        "J_race_black_share",
        "J_race_others_share",
        "J00_06_share",
        "J09_18_share",
        "J20_22_share",
        "J40_47_share",
        "J_bucket_entropy",
        "catchment_munic_unique",
        "catchment_top1_share",
        "catchment_entropy",
        "catchment_outside_local_share",
        "J_missing_diag_sec_share",
        "J_missing_proc_share",
    ],
)
df_final.to_csv("./Aggregated_table.csv", index=False)
