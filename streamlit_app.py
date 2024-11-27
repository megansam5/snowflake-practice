# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Chhose the fruits you want in your custom smoothie!
    """
)
name = st.text_input("Name:", "Your name")
st.write("Your order name is: ", name)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
ingredient_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe, 
                                max_selections=5)

if ingredient_list:

    ingredient_string = ''
    for ingredient in ingredient_list:
        ingredient_string += ingredient + " "
    st.write(ingredient_string)

     
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredient_string + """','""" + name + """')"""
    submit_button = st.button("Submit order!")
    if submit_button:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
