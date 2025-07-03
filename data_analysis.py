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


# Concatenate all Knesset DataFrames into a single DataFrame
all_knesset_list = list(all_knesset_df.values())
elections_raw_df = pd.concat(
    all_knesset_list,
    ignore_index=True)



mask = [elections_raw_df['בזב']> 12000]
election_years = sorted(elections_raw_df.knesset.unique().tolist())





with st.sidebar:
    st.write("Use the filters below to analyze the data by year, party, and other criteria.")
    year_range = st.slider(
        label="Select Election Year Range:",
        min_value=min(election_years),
        max_value=max(election_years),
        value=(min(election_years), max(election_years)),
        )
    st.write("Election Year Range: ", year_range)



#
#     st.write("Select your preferred genre(s) and year to view the movies released that year and on that genre")
#
#     #create a multiselect option that holds genre
#     new_genre_list = st.multiselect('Choose Genre:', genre_list, default = ['Animation', 'Horror', 'Fantasy', 'Romance'])
#
#     #create a selectbox option that holds all unique years
#     year = st.selectbox('Choose a Year', year_list, 0)
#
# #Configure the slider widget for interactivity
# score_info = (movies_data['score'].between(*new_score_rating))
#
#
#
#
# #Configure the selectbox and multiselect widget for interactivity
# new_genre_year = (movies_data['genre'].isin(new_genre_list)) & (movies_data['year'] == year)
#
# #VISUALIZATION SECTION
# #group the columns needed for visualizations
# # col1, col2 = st.columns([2,3],border=True)
#
# col1 = st.columns(1, gap="large")[0]
# with col1:
#     st.write("""#### Lists of movies filtered by year and Genre """)
#     dataframe_genre_year = movies_data[new_genre_year].groupby(['name', 'genre'])['year'].sum()
#     dataframe_genre_year = dataframe_genre_year.reset_index()
#     st.dataframe(dataframe_genre_year, width = 700)
#
# # with col2:
# #     st.write("""#### User score of movies and their genre """)
# #     rating_count_year = movies_data[score_info].groupby('genre')['score'].count()
# #     rating_count_year = rating_count_year.reset_index()
# #     figpx = px.line(rating_count_year, x = 'genre', y = 'score')
# #     st.plotly_chart(figpx)
#
#
#
#
#  # creating a bar graph with matplotlib
# st.write("""
# Average Movie Budget, Grouped by Genre
#     """)
# avg_budget = movies_data.groupby('genre')['budget'].mean().round()
# avg_budget = avg_budget.reset_index()
# genre = avg_budget['genre']
# avg_bud = avg_budget['budget']
#
# fig = plt.figure(figsize = (19, 10))
#
# plt.bar(genre, avg_bud, color = 'maroon')
# plt.xlabel('genre')
# plt.ylabel('budget')
# plt.title('Matplotlib Bar Chart Showing The Average Budget of Movies in Each Genre')
# st.pyplot(fig)
#
#
