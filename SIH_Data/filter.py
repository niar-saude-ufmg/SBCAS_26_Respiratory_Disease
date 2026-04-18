import pandas as pd
import os


i = 0
files = os.listdir("./Data_csv/")
for file in files:
    i += 1
    df = pd.read_csv("./Data_csv/" + file)
    df = df[
        [
            "CNES",
            "DT_INTER",
            "ANO_CMPT",
            "MES_CMPT",
            "DIAG_PRINC",
            "N_AIH",
            "MORTE",
            "DIAS_PERM",
            "UTI_MES_TO",
            "VAL_TOT",
            "VAL_UTI",
            "SEXO",
            "COD_IDADE",
            "IDADE",
            "RACA_COR",
            "MUNIC_RES",
            "MUNIC_MOV",
            "DIAG_SECUN",
            "PROC_REA",
        ]
    ]

    # Only diagnostics for respiratory diseases will be used.
    # Diagnostics that starts with "J" (also the only with "J")
    df = df.loc[df["DIAG_PRINC"].str.contains("J")]
    df.to_csv("./Filtered_Data/" + file)

    # Print for checking progress
    print(i, "/", len(files))
