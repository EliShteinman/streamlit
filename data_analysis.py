import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Elections Results Dashboard",
    layout='wide',
    page_icon=":bar_chart:"
)



# Set the page configuration

@st.cache_data
def load_data():
    # Load the data from the CSV file
    df = pd.read_csv("israeli_elections_results_1996_to_2015.csv", encoding="iso-8859-8")
    return df
elections_raw_df = load_data()
print("Data loaded successfully!")




#
# st.header("Movie Analysis Dashboard :material/line_axis:",divider=True)
# st.subheader("A dashboard to analyze movies based on their genre, year and user score", anchor=False,divider="gray")
# st.subheader("****************************", anchor=False)
#
# #read in the file
# movies_data = pd.read_csv("movies.csv")
#
#
# # Creating sidebar widget filters from movies dataset
# year_list = movies_data['year'].unique().tolist()
# score_rating = movies_data['score'].unique().tolist()
# genre_list = movies_data['genre'].unique().tolist()
#
#
# # Add the filters. Every widget goes in here
# sl = st.sidebar
# sl.write("Welcome to the Movie Analysis Dashboard! :movie_camera:")
# with st.sidebar:
#     st.write("Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range ")
#     #create a slider to hold user scores
#     new_score_rating = st.slider(label = "Choose a value:",
#                                   min_value = 1.0,
#                                   max_value = 10.0,
#                                  value = (2.0,3.5))
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
