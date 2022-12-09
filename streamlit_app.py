import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# create repeatable code block / new function
def get_fruityvice_data(this_fruit_choice):
	fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
	fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
	return fruityvice_normalized

#New section to display fruity vice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
	if not fruit_choice:
		streamlit.error("Please enter a fruit to get information.")
	else:
		back_from_function = get_fruityvice_data(fruit_choice)
		streamlit.dataframe(back_from_function)
except URLError as e:
	streamlit.error()

streamlit.header("The Fruit Load List Contains: ")
#Snowflake related functions
def get_fruit_load_list():
	with my_cnx.cursor() as my_cur:
	     my_cur.execute("select * from fruit_load_list")
	     return my_cur.fetchall()
#add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_rows = get_fruit_load_list()
	streamlit.dataframe(my_data_rows)

#Allow end user to add fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'Enter Fruit Name')
streamlit.write('Thanks for adding: ', add_my_fruit)

#Don't run anything past here while troubleshooting
streamlit.stop()

#This will not work as written but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
