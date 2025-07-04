# Import necessary libraries for the application
import streamlit as st  # For creating the web app interface
import pandas as pd  # For data manipulation and analysis
import plotly.express as px  # For creating interactive plots

# Set the page configuration for the Streamlit app
# This function sets the title that appears in the browser tab, the layout width, and the icon.
st.set_page_config(
    page_title="Elections Results Dashboard",
    layout='wide',  # 'wide' layout uses the full screen width
    page_icon=":bar_chart:"  # An emoji used as the page icon
)


pormat = lambda col: not (col.startswith('Unnamed')
                          or col == 'סמל ועדה'
                          or col == 'סמל ישוב'
                          or col == 'מספר קלפי'
                          or col == 'סמל קלפי'
                          or col == 'ת. עדכון'
                          or col == 'כתובת')


# # Load the data from CSV files for each Knesset election
# The following section reads election data for Knessets 21 through 25 from separate CSV files.

# Load data for the 25th Knesset
# 'encoding="utf-8-sig"' is used to handle Hebrew characters correctly.
knesset_25_df = pd.read_csv('data/25.csv', encoding="utf-8-sig", usecols=pormat)
# Add a 'knesset' column to identify which election this data belongs to.
knesset_25_df.insert(0, 'knesset', 25)

# Load data for the 24th Knesset
# 'encoding="iso-8859-8"' is used to handle Hebrew characters correctly.
knesset_24_df = pd.read_csv('data/24.csv', encoding="iso-8859-8", usecols=pormat)
knesset_24_df.insert(0, 'knesset', 24)

# Load data for the 23rd Knesset
knesset_23_df = pd.read_csv('data/23.csv', encoding="iso-8859-8", usecols=pormat)
knesset_23_df.insert(0, 'knesset', 23)

# Load data for the 22nd Knesset
knesset_22_df = pd.read_csv('data/22.csv', encoding="iso-8859-8", usecols=pormat)
knesset_22_df.insert(0, 'knesset', 22)

# Load data for the 21st Knesset
knesset_21_df = pd.read_csv('data/21.csv', encoding="iso-8859-8", usecols=pormat)
knesset_21_df.insert(0, 'knesset', 21)


knesset_20_df = pd.read_csv('data/20.csv',encoding="utf-8-sig", usecols=pormat)
knesset_20_df.insert(0,'knesset',20)
knesset_19_df = pd.read_csv('data/19.csv',encoding="utf-8-sig", usecols=pormat)
knesset_19_df.insert(0,'knesset',19)
knesset_18_df = pd.read_csv('data/18.csv',encoding="iso-8859-8", usecols=pormat)
knesset_18_df.insert(0,'knesset',18)
knesset_17_df = pd.read_excel('data/17.xls',usecols=pormat)
knesset_17_df.insert(0,'knesset',17)


# Combine all Knesset DataFrames into a dictionary for easier access
all_knesset_df = {
    'knesset_25': knesset_25_df,
    'knesset_24': knesset_24_df,
    'knesset_23': knesset_23_df,
    'knesset_22': knesset_22_df,
    'knesset_21': knesset_21_df,
    'knesset_20': knesset_20_df,
    'knesset_19': knesset_19_df,
    'knesset_18': knesset_18_df,
    'knesset_17': knesset_17_df
}

# Create a list of all the dataframes
all_knesset_list = list(all_knesset_df.values())
for knesset in all_knesset_list:
    knesset.columns = knesset.columns.str.strip().str.replace("''", "", regex=False)

# Concatenate all dataframes into a single, comprehensive dataframe
# 'ignore_index=True' resets the index of the combined dataframe.
elections_raw_df = pd.concat(all_knesset_list, ignore_index=True)

######################################################################
# Data Preparation for UI Elements and Visualization

# Get a sorted list of unique Knesset numbers from the raw data.
Knesset_number = sorted(elections_raw_df.knesset.unique().tolist())

# Get a list of all party names (column headers starting from the 8th column).
all_parties = elections_raw_df.columns[6:].tolist()

# Group the data by 'knesset' and calculate the sum of votes for each party in each Knesset.
# This creates a summary table of total votes per party for each election.
votes_by_party_and_knesset = elections_raw_df.groupby('knesset')[elections_raw_df.columns[6:]].sum()

# For each Knesset (each row), find the names of the top 10 parties by vote count.
top_10_parties_per_row = votes_by_party_and_knesset.apply(lambda row: row.nlargest(10).index.tolist(), axis=1)

# Create a single, sorted list of unique party names that appeared in the top 10 of at least one election.
# This list will be used to populate the party selection dropdown to keep it relevant.
party_list = sorted(top_10_parties_per_row.explode().unique().tolist())

######################################################################
# User Interface (UI) Layout and Widgets

st.header("Israeli Elections Results Dashboard")  # Main title of the app
st.subheader("Explore Election Results by Knesset and Party")  # Subtitle for context
st.write(
    "This dashboard allows you to explore the results of Israeli elections from Knesset 17 to Knesset 25. "
    "You can filter the data by Knesset number and compare votes for different parties over time."
)


# Create a layout with two columns: a smaller one for filters and a larger one for the chart.
# The ratio is 1:3, and a gap is added for visual separation.
col1, col2 = st.columns([1, 3], gap="large", border=True)

# ---- Sidebar Column (col1) for Filters and Controls ----
with col1:
    # Add a title for the filter section.
    st.markdown("### Filter the Data")

    # Add descriptive text for the user.
    st.write(
        "Use the filters below to explore the election data by Knesset number and party. "
        "You can narrow the data using the slider and compare specific parties of interest."
    )

    # Create a range slider for selecting the Knesset numbers to display.
    Knesset_range = st.slider(
        label="Knesset number range:",
        min_value=min(Knesset_number),  # Set the minimum possible value
        max_value=max(Knesset_number),  # Set the maximum possible value
        value=(min(Knesset_number), max(Knesset_number)),  # Default selected range
        key="Knesset_range_slider"  # Unique key for this widget
    )
    # Display the selected range to the user.
    st.write("Selected Knesset range:", Knesset_range)

    # Add a horizontal line for visual separation.
    st.markdown("---")

    # Add a sub-header for the party comparison section.
    st.markdown("### Compare Parties")

    # Add descriptive text explaining how to use the party selector.
    st.write(
        "Select up to **3 party letters** (ballot symbols) to compare. "
        "The list below includes only parties that appeared in the **Top 10** in at least one of the last 5 elections."
    )

    # Create a multi-select dropdown for choosing parties.
    party_choice = st.multiselect(
        label="Select up to 3 parties:",
        options=party_list,  # Populate with the list of top parties
        key="party_choice_multiselect",  # Unique key for this widget
        default=['ג', 'שס'],  # Default selected parties
        max_selections=3,  # Limit the user to a maximum of 3 selections
        accept_new_options=True,  # Allow user to type in party letters not in the list
        help="You can type a party letter (in Hebrew) or select from the list."  # Help tooltip
    )

    # --- Input Validation for Party Selection ---
    # Check which of the selected choices are valid (exist in the data columns).
    valid_choices = [p for p in party_choice if p in all_parties]
    # Check for any invalid entries.
    invalid_choices = [p for p in party_choice if p not in all_parties]

    # If there are invalid entries, show a warning.
    if invalid_choices:
        st.warning(f"Invalid entries removed: {invalid_choices}")
        st.info("Please select valid party letters only.")
    else:
        # If all choices are valid, show a success message.
        if valid_choices:
            st.success(f"Selected parties: {', '.join(valid_choices)}")

    # Add additional informational text in markdown.
    st.markdown("""
        If you can't find a party in the dropdown, try typing its ballot letter manually.

        All parties are listed by their official **ballot letters** (e.g. `מחל` for Likud).
    """)

    # --- Expander for Full Party List ---
    # Add a section that can be expanded to show all available party letters.
    st.markdown("For reference, here is the full list of known party letters:")
    with st.expander("Show / Hide full party letter list"):
        # Display all party letters with some styling for better readability.
        st.markdown(
            " ".join(
                f"<span style='background-color:#eee; padding:6px 10px; margin:5px; "
                f"border-radius:8px; display:inline-block; font-size:18px; font-family:sans-serif'>{party}</span>"
                for party in all_parties
            ),
            unsafe_allow_html=True  # Required to render the custom HTML styling
        )

# Filter the aggregated data based on the user's selections from the widgets.
# It selects the rows based on the Knesset range and the columns based on the chosen parties.
party_votes_over_time = votes_by_party_and_knesset.loc[Knesset_range[0]:Knesset_range[1], party_choice]

# ---- Main Content Column (col2) for the Chart ----
with col2:
    # Create an interactive line chart using Plotly Express.
    figpx = px.line(
        party_votes_over_time,  # The data to plot
        x=party_votes_over_time.index.astype(str),  # Knesset numbers on the x-axis (as string/category)
        y=party_choice,  # The selected parties to plot on the y-axis
        title="Party Votes Over Time",  # Title of the chart
        labels={"value": "Votes", "knesset": "Knesset Number"},  # Custom labels for axes
        markers=True  # Add markers to each data point on the lines
    )
    # Ensure the x-axis is treated as a categorical axis, not a continuous number.
    # This prevents Plotly from creating gaps for non-integer values.
    figpx.update_xaxes(type="category")

    # Display the Plotly chart in the Streamlit app.
    st.plotly_chart(figpx)