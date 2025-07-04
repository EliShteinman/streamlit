# Import the necessary libraries for data manipulation, web app creation, and plotting.
import streamlit as st
import plotly.express as px
from core.data_loader import load_and_prepare_data
from core.ui import apply_rtl
st.set_page_config(
    page_title="השוואת קולות למפלגות",
    page_icon="📈",
    layout="wide"
)
apply_rtl()


elections_raw_df, Knesset_number, all_parties, party_list, votes_by_party_and_knesset = load_and_prepare_data()

# --- User Interface (UI) Layout ---

# Display the main title and a descriptive subtitle for the dashboard.

st.title("📈 השוואת מספר הקולות למפלגות לפי כנסת")
st.write("בדף זה ניתן להשוות בין מפלגות לפי מספר הקולות שקיבלו בכל אחת מהכנסות שנבחרו.")
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


st.markdown('___')