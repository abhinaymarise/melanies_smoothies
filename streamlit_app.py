# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie.
  """
)

name_on_order=st.text_input("Name on smoothie")
st.write("The Name on your Smoothie will be:",name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredient_lists=st.multiselect('Choose upto 5 ingredients',my_dataframe,max_selections=6)

if ingredient_lists:

    ingredients_string=''

    for each_fruit in ingredient_lists:
        ingredients_string+=each_fruit+' '
        st.subheader(each_fruit + '&nbsp;Nutrient Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    
    submit_button=st.button("Submit Order")
    
    if submit_button:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is Ordered,&nbsp;'+name_on_order)






