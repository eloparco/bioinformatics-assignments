import sys
import numpy as np
import pandas as pd
import requests
from scipy import stats


def ensg_to_common_name(ensg):
    if "ENSGR" in ensg:
        # Replace 'R with '0'
        ensg = ensg[:4] + "0" + ensg[5:]

    server = "https://rest.ensembl.org"
    ext = "/overlap/id/" + ensg.split(".")[0] + "?feature=gene"

    r = requests.get(
        server + ext, headers={"Content-Type": "application/json"}
    )

    # No match found
    if not r.ok:
        return ensg

    decoded = r.json()
    return decoded[0]["external_name"]


def main():
    # One row for each patient, one column for each gene
    df = pd.read_csv("dataset.csv")
    print(f"shape before: {df.shape}")

    # Level of significance
    alpha = 0.05

    lum_A = df[df["l"].str.strip() == "Luminal A"]
    lum_B = df[df["l"].str.strip() == "Luminal B"]

    for col in df.columns[1:]:  # Skip first column
        # T-test statistics
        t_value, p_value = stats.ttest_ind(
            np.array(lum_A[col]), np.array(lum_B[col]), equal_var=False
        )

        # Bonferroni adjustment
        if p_value > alpha / len(df):
            df = df.drop(col, 1)
        else:
            common_name = ensg_to_common_name(col)
            df = df.rename(columns={col: common_name})

    print(f"shape after: {df.shape}")
    df.to_csv("reduced_dataset.csv", index=False)


if __name__ == "__main__":
    main()
