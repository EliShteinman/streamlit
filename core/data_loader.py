import streamlit as st
import pandas as pd



# --- Data Loading and Preparation ---
def load_and_prepare_data():
    # Defines a function to filter out unnecessary columns during the data loading process.
    def pormat(col):
        """
        Determines if a column should be kept. Returns False for columns to be dropped.
        """
        return not (col.startswith('Unnamed') or col in ['סמל ועדה', 'סמל ישוב', 'מספר קלפי', 'סמל קלפי', 'ת. עדכון', 'כתובת'])


    # Load election data for Knessets 17 through 25 from various file formats (CSV and Excel).
    try:
        # Read data for the 25th Knesset and add a 'knesset' identifier column.
        knesset_25_df = pd.read_csv('data/25.csv', encoding="utf-8-sig", usecols=pormat)
        knesset_25_df.insert(0, 'knesset', 25)

        # Read data for the 24th Knesset and add a 'knesset' identifier column.
        knesset_24_df = pd.read_csv('data/24.csv', encoding="iso-8859-8", usecols=pormat)
        knesset_24_df.insert(0, 'knesset', 24)

        # Read data for the 23rd Knesset and add a 'knesset' identifier column.
        knesset_23_df = pd.read_csv('data/23.csv', encoding="iso-8859-8", usecols=pormat)
        knesset_23_df.insert(0, 'knesset', 23)

        # Read data for the 22nd Knesset and add a 'knesset' identifier column.
        knesset_22_df = pd.read_csv('data/22.csv', encoding="iso-8859-8", usecols=pormat)
        knesset_22_df.insert(0, 'knesset', 22)

        # Read data for the 21st Knesset and add a 'knesset' identifier column.
        knesset_21_df = pd.read_csv('data/21.csv', encoding="iso-8859-8", usecols=pormat)
        knesset_21_df.insert(0, 'knesset', 21)

        # Read data for the 20th Knesset and add a 'knesset' identifier column.
        knesset_20_df = pd.read_csv('data/20.csv', encoding="utf-8-sig", usecols=pormat)
        knesset_20_df.insert(0, 'knesset', 20)

        # Read data for the 19th Knesset and add a 'knesset' identifier column.
        knesset_19_df = pd.read_csv('data/19.csv', encoding="utf-8-sig", usecols=pormat)
        knesset_19_df.insert(0, 'knesset', 19)

        # Read data for the 18th Knesset and add a 'knesset' identifier column.
        knesset_18_df = pd.read_csv('data/18.csv', encoding="iso-8859-8", usecols=pormat)
        knesset_18_df.insert(0, 'knesset', 18)

        # Read data for the 17th Knesset and add a 'knesset' identifier column.
        knesset_17_df = pd.read_excel('data/17.xls', usecols=pormat)
        knesset_17_df.insert(0, 'knesset', 17)

        # Read data for the 16th Knesset and add a 'knesset' identifier column.
        knesset_16_df = pd.read_excel('data/16.xls', usecols=pormat)
        knesset_16_df.insert(0, 'knesset', 16)

        # Store all individual Knesset DataFrames in a dictionary for structured access.
        all_knesset_df = {
            'knesset_25': knesset_25_df, 'knesset_24': knesset_24_df, 'knesset_23': knesset_23_df,
            'knesset_22': knesset_22_df, 'knesset_21': knesset_21_df, 'knesset_20': knesset_20_df,
            'knesset_19': knesset_19_df, 'knesset_18': knesset_18_df, 'knesset_17': knesset_17_df,
            'knesset_16': knesset_16_df
        }

        # Create a list of DataFrames from the dictionary values for easier processing.
        all_knesset_list = list(all_knesset_df.values())

        # Iterate through each DataFrame to clean up column names before merging.
        for df in all_knesset_list:
            # Remove extra whitespace and quotation marks from column headers.
            df.columns = df.columns.str.strip().str.replace("''", "", regex=False).str.replace('"', '', regex=False).str.replace('בוחרים','בזב')

        # Combine all individual Knesset DataFrames into a single, comprehensive DataFrame.
        elections_raw_df = pd.concat(all_knesset_list, ignore_index=True)

        # --- Prepare data for UI filters ---

        # Get a sorted, unique list of Knesset numbers for use in sliders and filters.
        Knesset_number = sorted(elections_raw_df.knesset.unique().tolist())
        # Extract the list of all party names from the column headers.
        all_parties = elections_raw_df.columns[6:].tolist()

        # Group data by Knesset and sum the total votes for each party.
        votes_by_party_and_knesset = elections_raw_df.groupby('knesset')[all_parties].sum()

        last_6_knessets = votes_by_party_and_knesset.index.sort_values(ascending=False)[:6]
        votes_last_6_elections = votes_by_party_and_knesset.loc[last_6_knessets]

        # For each Knesset, identify the top 10 parties by vote count.
        top_10_parties_per_row = votes_last_6_elections.apply(lambda row: row.nlargest(10).index.tolist(), axis=1)
        # Create a unified, sorted list of all parties that were in the top 10 in at least one election.
        party_list = sorted(top_10_parties_per_row.explode().unique().tolist())

        return(elections_raw_df, Knesset_number, all_parties, party_list, votes_by_party_and_knesset)

    # Handle cases where the data files are not found in the 'data' directory.
    except FileNotFoundError:
        st.error("שגיאה: אחד או יותר מקבצי הנתונים לא נמצאו. אנא ודא שהקבצים נמצאים בתיקיית 'data'.")
        st.stop() # Stop the app execution if data is missing.

