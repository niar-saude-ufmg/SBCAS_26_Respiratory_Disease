import pyreaddbc
import os

files = os.listdir("./Data/")

for f in files:
    dfs = pyreaddbc.dbc2dbf(
        "./Data/" + f, "./Data_dbf/" + f.removesuffix(".dbc") + ".dbf"
    )
