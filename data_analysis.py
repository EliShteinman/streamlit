# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration for a wide layout and a relevant icon
st.set_page_config(
    page_title="תוצאות בחירות בישראל",
    layout='wide',
    page_icon="🇮🇱"
)

# --- Data Loading and Preparation ---

# A function to filter out unnecessary columns during file reading
def pormat(col):
    return not (col.startswith('Unnamed') or col in ['סמל ועדה', 'סמל ישוב', 'מספר קלפי', 'סמל קלפי', 'ת. עדכון', 'כתובת'])


# Load data for Knessets 17-25 from various file formats
try:
    knesset_25_df = pd.read_csv('data/25.csv', encoding="utf-8-sig", usecols=pormat)
    knesset_25_df.insert(0, 'knesset', 25)

    knesset_24_df = pd.read_csv('data/24.csv', encoding="iso-8859-8", usecols=pormat)
    knesset_24_df.insert(0, 'knesset', 24)

    knesset_23_df = pd.read_csv('data/23.csv', encoding="iso-8859-8", usecols=pormat)
    knesset_23_df.insert(0, 'knesset', 23)

    knesset_22_df = pd.read_csv('data/22.csv', encoding="iso-8859-8", usecols=pormat)
    knesset_22_df.insert(0, 'knesset', 22)

    knesset_21_df = pd.read_csv('data/21.csv', encoding="iso-8859-8", usecols=pormat)
    knesset_21_df.insert(0, 'knesset', 21)

    knesset_20_df = pd.read_csv('data/20.csv', encoding="utf-8-sig", usecols=pormat)
    knesset_20_df.insert(0, 'knesset', 20)

    knesset_19_df = pd.read_csv('data/19.csv', encoding="utf-8-sig", usecols=pormat)
    knesset_19_df.insert(0, 'knesset', 19)

    knesset_18_df = pd.read_csv('data/18.csv', encoding="iso-8859-8", usecols=pormat)
    knesset_18_df.insert(0, 'knesset', 18)

    knesset_17_df = pd.read_excel('data/17.xls', usecols=pormat)
    knesset_17_df.insert(0, 'knesset', 17)

    # Combine all Knesset DataFrames into a dictionary as originally requested
    all_knesset_df = {
        'knesset_25': knesset_25_df, 'knesset_24': knesset_24_df, 'knesset_23': knesset_23_df,
        'knesset_22': knesset_22_df, 'knesset_21': knesset_21_df, 'knesset_20': knesset_20_df,
        'knesset_19': knesset_19_df, 'knesset_18': knesset_18_df, 'knesset_17': knesset_17_df
    }

    # Create a list from the dictionary's values
    all_knesset_list = list(all_knesset_df.values())

    # Clean column names for all DataFrames before concatenation
    for df in all_knesset_list:
        # Chain replacements to handle both '' and "
        df.columns = df.columns.str.strip().str.replace("''", "", regex=False).str.replace('"', '', regex=False)

    # Combine all data into a single DataFrame
    elections_raw_df = pd.concat(all_knesset_list, ignore_index=True)

    # --- Prepare data for UI filters ---

    Knesset_number = sorted(elections_raw_df.knesset.unique().tolist())
    all_parties = elections_raw_df.columns[6:].tolist()

    votes_by_party_and_knesset = elections_raw_df.groupby('knesset')[all_parties].sum()
    top_10_parties_per_row = votes_by_party_and_knesset.apply(lambda row: row.nlargest(10).index.tolist(), axis=1)
    party_list = sorted(top_10_parties_per_row.explode().unique().tolist())

except FileNotFoundError:
    st.error("שגיאה: אחד או יותר מקבצי הנתונים לא נמצאו. אנא ודא שהקבצים נמצאים בתיקיית 'data'.")
    st.stop()

# --- User Interface (UI) Layout ---
# (The UI code remains the same as the previous good version)
st.header("📊 דאשבורד תוצאות הבחירות בישראל")
st.write("חקור את תוצאות הבחירות לכנסת, מהכנסת ה-17 ועד הכנסת ה-25. ניתן לסנן את הנתונים לפי מספר כנסת ולהשוות את נתוני ההצבעה למפלגות השונות לאורך זמן.")

col1, col2 = st.columns([1, 3], gap="large", border=True)

with col1:
    st.markdown("### סנן את הנתונים")

    min_knesset, max_knesset = int(min(Knesset_number)), int(max(Knesset_number))
    Knesset_range = st.slider(
        label="בחר טווח כנסות:",
        min_value=min_knesset,
        max_value=max_knesset,
        value=(min_knesset, max_knesset),
    )
    st.info(f"הצגת נתונים מהכנסת ה-{Knesset_range[0]} עד הכנסת ה-{Knesset_range[1]}")

    # Add a horizontal line for visual separation.
    st.markdown("---")

    st.markdown("### השווה בין מפלגות")
    if "party_choice_multiselect" in st.session_state:
        selected_parties = st.session_state.party_choice_multiselect
        invalid_parties = [p for p in selected_parties if p not in all_parties]

        if invalid_parties:
            st.warning(f"הבחירות הבאות אינן חוקיות והוסרו: {', '.join(invalid_parties)}")
            # עדכון ה-session_state לרשימה הנקייה בלבד
            st.session_state.party_choice_multiselect = [p for p in selected_parties if p in all_parties]

    party_choice = st.multiselect(
        label="בחר עד 3 מפלגות להשוואה:",
        options=party_list,
        key="party_choice_multiselect",  # הקישור ל-session_state
        default=['ג', 'שס'],
        max_selections=3,
        accept_new_options=True,
        help="ניתן להקליד את אות המפלגה או לבחור מהרשימה."
    )


    with st.expander("הצג/הסתר את רשימת כל אותיות המפלגות"):
        st.markdown(
            " ".join(
                f"<span style='background-color:#eee; padding:6px 10px; margin:5px; border-radius:8px; display:inline-block; font-size:18px; font-family:sans-serif'>{party}</span>"
                for party in all_parties
            ),
            unsafe_allow_html=True
        )
    valid_choices = st.session_state.get("party_choice_multiselect", [])



party_votes_over_time = votes_by_party_and_knesset.loc[Knesset_range[0]:Knesset_range[1], valid_choices]

with col2:
    if not valid_choices:
        st.info("יש לבחור לפחות מפלגה אחת חוקית כדי להציג גרף.")
    else:
        figpx = px.line(
            party_votes_over_time,
            x=party_votes_over_time.index.astype(str),
            y=valid_choices,
            title="הצבעות למפלגות לאורך זמן",
            labels={"value": "מספר קולות", "knesset": "כנסת", "variable": "מפלגה"},
            markers=True
        )
        figpx.update_xaxes(type="category")
        figpx.update_layout(legend_title_text='מפלגות')
        st.plotly_chart(figpx, use_container_width=True)