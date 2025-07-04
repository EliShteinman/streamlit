import streamlit as st
from core.ui import apply_rtl
# Set the Streamlit page configuration for a wide layout and a relevant browser tab icon.
st.set_page_config(
    page_title="תוצאות בחירות בישראל",
    layout='wide',
    page_icon="🇮🇱"
)
apply_rtl()

st.title("📊 דאשבורד תוצאות הבחירות בישראל")
st.write("חקור את תוצאות הבחירות מהכנסת ה־16 ועד הכנסת ה־25...")

st.markdown("""
---
👈 בחר דף מהתפריט בצד שמאל כדי להתחיל לחקור את הנתונים.

🔍 בדף **`party_votes_over_time`** תוכל להשוות בין מפלגות ולראות כיצד השתנה כוחן (לפי מספר הקולות) לאורך הכנסות 16–25.

📊 בהמשך יוצגו דפים נוספים עם פילוחים והשוואות מתקדמות.
""")