import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError #library for control flow of change
# streamlit.stop to make the change made here doesn't influence the control flow in snowflakes
streamlit.stop()
streamlit.title('My Parents New Healthy Diner')

streamlit.header('🥣 Breakfast Menu')
streamlit.text(' 🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🐔 Kale, Spinach, and Rocket Smoothies')
streamlit.text(' 🥑🍞 Hard-Boiled Free-range Eggs')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list= my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected= streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# create function
def get_fruityvice_data(this_fruit_choice):
    # streamlit.text(fruityvice_response.json())
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    # normalize the data into flat and categorize 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# import requests
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
    streamlit.write('The user entered ', fruit_choice)
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    # make the data into dataframe
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()


# import snowflake.connector
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)

# for fruit data
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("the fruit list contain")
streamlit.dataframe(my_data_row)

# Add other data input
# add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
# streamlit.write('Thanks for adding ', add_my_fruit )

# my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
import streamlit as st

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
        return 'Thanks for adding ' + new_fruit
    

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', add_my_fruit )

streamlit.header("The fruit load list contains:")
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function= insert_row_snowflake(add_my_fruit)
    streamlit.dataframe(back_from_function)
    my_cnx.close()

           
