# Import necessary libraries for data manipulation, web app creation, and plotting.
import streamlit as st
import pandas as pd
import plotly.express as px

# Set the Streamlit page configuration for a wide layout and a relevant browser tab icon.
st.set_page_config(
    page_title="תוצאות בחירות בישראל",
    layout='wide',
    page_icon="🇮🇱"
)

# --- Data Loading and Preparation ---

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

# Handle cases where the data files are not found in the 'data' directory.
except FileNotFoundError:
    st.error("שגיאה: אחד או יותר מקבצי הנתונים לא נמצאו. אנא ודא שהקבצים נמצאים בתיקיית 'data'.")
    st.stop() # Stop the app execution if data is missing.

# --- User Interface (UI) Layout ---

# Display the main title and a descriptive subtitle for the dashboard.
st.header("📊 דאשבורד תוצאות הבחירות בישראל")
st.write("חקור את תוצאות הבחירות לכנסת, מהכנסת ה-17 ועד הכנסת ה-25. ניתן לסנן את הנתונים לפי מספר כנסת ולהשוות את נתוני ההצבעה למפלגות השונות לאורך זמן.")

# Create a two-column layout for the UI elements. The right column is 3x wider than the left.
col1, col2 = st.columns([1, 3], gap="large", border=True)

# The 'with' block places the following elements inside the first column.
with col1:
    st.markdown("### סנן את הנתונים")

    # Define the min and max values for the Knesset range slider.
    min_knesset, max_knesset = int(min(Knesset_number)), int(max(Knesset_number))
    # Create a slider widget to allow users to select a range of Knessets.
    Knesset_range = st.slider(
        label="בחר טווח כנסות:",
        min_value=min_knesset,
        max_value=max_knesset,
        value=(min_knesset, max_knesset), # Default range is all Knessets.
    )
    # Display an informational message showing the selected range.
    st.info(f"הצגת נתונים מהכנסת ה-{Knesset_range[0]} עד הכנסת ה-{Knesset_range[1]}")

    st.markdown("---") # Add a visual separator.

    st.markdown("### השווה בין מפלגות")

    st.caption("הרשימה מציגה מפלגות מובילות מהבחירות האחרונות לנוחיותך.")

    # Check if a selection already exists in the session state to handle potential invalid entries.
    if "party_choice_multiselect" in st.session_state:
        selected_parties = st.session_state.party_choice_multiselect
        # Find any selected parties that are no longer valid (e.g., due to data changes).
        invalid_parties = [p for p in selected_parties if p not in all_parties]

        # If invalid parties are found, warn the user and remove them from the selection.
        if invalid_parties:
            st.warning(f"הבחירות הבאות אינן חוקיות והוסרו: {', '.join(invalid_parties)}")
            # Update the session state to only contain valid party selections.
            st.session_state.party_choice_multiselect = [p for p in selected_parties if p in all_parties]

    # Create a multi-select dropdown for choosing up to 3 parties to compare.
    party_choice = st.multiselect(
        label="בחר עד 3 מפלגות להשוואה:",
        options=party_list,
        key="party_choice_multiselect",  # Link the widget's state to the session state.
        default=['ג', 'שס'], # Pre-select default parties.
        max_selections=3,
        accept_new_options=True, # Allow users to type in party symbols.
        help="ניתן לבחור מהרשימה או להקליד אות של **כל מפלגה** מהעבר (גם אם אינה ברשימה) וללחוץ Enter."
    )

    # Create an expandable section to show all available party symbols.
    with st.expander("הצג/הסתר את רשימת כל אותיות המפלגות"):
        # Display all party symbols with custom styling using HTML.
        st.markdown(
            " ".join(
                f"<span style='background-color:#eee; padding:6px 10px; margin:5px; border-radius:8px; display:inline-block; font-size:18px; font-family:sans-serif'>{party}</span>"
                for party in all_parties
            ),
            unsafe_allow_html=True
        )
    # Get the currently valid party choices from the session state.
    valid_choices = st.session_state.get("party_choice_multiselect", [])


# Filter the aggregated data based on the selected Knesset range and parties.
party_votes_over_time = votes_by_party_and_knesset.loc[Knesset_range[0]:Knesset_range[1], valid_choices]

# The 'with' block places the following elements inside the second column.
with col2:
    # If no valid parties are selected, display an informational message.
    if not valid_choices:
        st.info("יש לבחור לפחות מפלגה אחת חוקית כדי להציג גרף.")
    # Otherwise, create and display the line chart.
    else:
        # Generate a line chart using Plotly Express.
        figpx = px.line(
            party_votes_over_time,
            x=party_votes_over_time.index.astype(str), # Use Knesset number as the x-axis.
            y=valid_choices, # Plot lines for each selected party.
            title="הצבעות למפלגות לאורך זמן",
            labels={"value": "מספר קולות", "knesset": "כנסת", "variable": "מפלגה"},
            markers=True # Add markers to each data point on the lines.
        )
        # Ensure the x-axis is treated as a categorical axis.
        figpx.update_xaxes(type="category")
        # Set the title for the chart's legend.
        figpx.update_layout(legend_title_text='מפלגות')
        # Display the Plotly chart in the Streamlit app, making it fit the container's width.
        st.plotly_chart(figpx, use_container_width=True)