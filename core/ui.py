import streamlit as st
def apply_rtl():
    st.markdown("""
        <style>
        /* יישום RTL רק על אזור התוכן הראשי */
        section.main {
            direction: rtl;
            text-align: right;
        }

        section.main h1, section.main h2, section.main h3, section.main h4, section.main h5, section.main h6 {
            text-align: right !important;
        }

        section.main input, section.main textarea {
            direction: rtl !important;
            text-align: right !important;
        }

        section.main .stMarkdown, section.main .stText, section.main .stWrite {
            direction: rtl;
            text-align: right;
        }

        section.main .stAlert {
            direction: rtl;
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)