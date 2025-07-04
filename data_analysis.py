import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit.components.v1 as components


# Set the page configuration for the Streamlit app
st.set_page_config(
    page_title="Elections Results Dashboard",
    layout='wide',
    page_icon=":bar_chart:"
)
# # Load the data from CSV files for each Knesset election
knesset_25_df = pd.read_csv('data/25.csv',encoding="utf-8-sig", usecols=lambda col: not (col.startswith('Unnamed') or col == 'סמל ועדה'))
knesset_25_df.insert(0,'knesset',25)
knesset_24_df = pd.read_csv('data/24.csv',encoding="iso-8859-8", usecols=lambda col: not (col.startswith('Unnamed') or col == 'סמל ועדה'))
knesset_24_df.insert(0,'knesset',24)
knesset_23_df = pd.read_csv('data/23.csv',encoding="iso-8859-8", usecols=lambda col: not (col.startswith('Unnamed') or col == 'סמל ועדה'))
knesset_23_df.insert(0,'knesset',23)
knesset_22_df = pd.read_csv('data/22.csv',encoding="iso-8859-8", usecols=lambda col: not (col.startswith('Unnamed') or col == 'סמל ועדה'))
knesset_22_df.insert(0,'knesset',22)
knesset_21_df = pd.read_csv('data/21.csv',encoding="iso-8859-8", usecols=lambda col: not (col.startswith('Unnamed') or col == 'סמל ועדה'))
knesset_21_df.insert(0,'knesset',21)

# Combine all Knesset DataFrames into a dictionary for easier access
all_knesset_df = {
    'knesset_25': knesset_25_df,
    'knesset_24': knesset_24_df,
    'knesset_23': knesset_23_df,
    'knesset_22': knesset_22_df,
    'knesset_21': knesset_21_df
}
all_knesset_list = list(all_knesset_df.values())
elections_raw_df = pd.concat(all_knesset_list, ignore_index=True)

######################################################################





Knesset_number = sorted(elections_raw_df.knesset.unique().tolist())
all_parties = elections_raw_df.columns[7:].tolist()
votes_by_party_and_knesset = elections_raw_df.groupby('knesset')[elections_raw_df.columns[7:]].sum()
top_10_parties_per_row = votes_by_party_and_knesset.apply(lambda row: row.nlargest(10).index.tolist(), axis=1)


party_list = sorted(top_10_parties_per_row.explode().unique().tolist())




col1, col2 = st.columns([1, 3], gap="large",border=True)
with col1:
    st.markdown("### Filter the Data")

    st.write(
        "Use the filters below to explore the election data by Knesset number and party. "
        "You can narrow the data using the slider and compare specific parties of interest."
    )

    # Knesset range slider
    Knesset_range = st.slider(
        label="Knesset number range:",
        min_value=min(Knesset_number),
        max_value=max(Knesset_number),
        value=(min(Knesset_number), max(Knesset_number)),
        key="Knesset_range_slider"
    )
    st.write("Selected Knesset range:", Knesset_range)

    st.markdown("---")

    st.markdown("### Compare Parties")

    st.write(
        "Select up to **3 party letters** (ballot symbols) to compare. "
        "The list below includes only parties that appeared in the **Top 10** in at least one of the last 5 elections."
    )

    party_choice = st.multiselect(
        label="Select up to 3 parties:",
        options=party_list,
        key="party_choice_multiselect",
        max_selections=3,
        accept_new_options=True,
        help="You can type a party letter (in Hebrew) or select from the list."
    )

    # Validation
    valid_choices = [p for p in party_choice if p in all_parties]
    invalid_choices = [p for p in party_choice if p not in all_parties]

    if invalid_choices:
        st.warning(f"Invalid entries removed: {invalid_choices}")
        st.info("Please select valid party letters only.")
    else:
        if valid_choices:
            st.success(f"Selected parties: {', '.join(valid_choices)}")

    # Additional info
    st.markdown("""
        If you can't find a party in the dropdown, try typing its ballot letter manually.

        All parties are listed by their official **ballot letters** (e.g. `מחל` for Likud).
    """)

    st.markdown("For reference, here is the full list of known party letters:")

    with st.expander("Show / Hide full party letter list"):
        st.markdown(
            " ".join(
                f"<span style='background-color:#eee; padding:6px 10px; margin:5px; "
                f"border-radius:8px; display:inline-block; font-size:18px; font-family:sans-serif'>{party}</span>"
                for party in all_parties
            ),
            unsafe_allow_html=True
        )

with col2:
    pass