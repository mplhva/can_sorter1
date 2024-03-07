# Pad van Anaconda
# cd OneDrive\Bureaublad\Data_Science\Visual_Analytics\Presentaties\Presentatie_2

# Streamlit:
# streamlit run app_page_1.py

import plotly.express as px
import matplotlib.cm as cm
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import os
import shutil
from zipfile import ZipFile
from datetime import datetime
import matplotlib.cm as cm

# Dictionary mapping color names to colormaps
color_map = {
    'red': 'Reds',
    'blue': 'Blues',
    'green': 'Greens',
    'yellow': 'YlOrBr',
    'orange': 'Oranges',
    'purple': 'Purples',
    'pink': 'pink'
}

def page1():
    # loading data in
    df1 = pd.read_csv('leafly_strain_data.csv')

    # cleaning data
    df1t = df1.dropna(subset=df1.columns.difference(['img_url']))
    df1tt = df1t.sort_values(by=['thc_level'])

    df1tt['thc_level'] = pd.to_numeric(df1tt['thc_level'].str.replace('%', ''), errors='coerce')
    df1tt = df1tt.sort_values(by=['thc_level'])
    df1tt['thc_level'] = df1tt['thc_level'].astype(str) + '%'

    st.title("Kinds of cannabis and their thc-level")
    # Create a Plotly Express scatter plot with a slider
    fig = px.scatter(df1tt, x='thc_level', y='name',
                     labels={'name': '', 'thc_level': 'thc level'},
                     range_x=[df1tt['thc_level'].min(), df1tt['thc_level'].max()],
                     range_y=[df1tt['name'].min(), df1tt['name'].max()])

    # Update layout to include a slider
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="category"))

    # Display the plot
    st.plotly_chart(fig)

    st.title('Cannabis sorter')
    st.markdown('Here you can look for a specific strain of cannabis to learn more about it')
    st.markdown('You can also look by the most common terpene found in a strain and what kind of cannabis it is')
    
    # dropdown menus
    sort_by_name = st.selectbox('Sort by name:', ['All'] + df1tt['name'].unique().tolist())
    sort_by_terpene = st.selectbox('Sort by terpene:', ['All'] + df1tt['most_common_terpene'].unique().tolist())
    sort_by_type = st.selectbox('Sort by type:', ['All'] + df1tt['type'].unique().tolist())

    # filtering
    if sort_by_name == 'All':
        sorted_df1tt = df1tt
    else:
        sorted_df1tt = df1tt[df1tt['name'] == sort_by_name]

    if sort_by_terpene != 'All':
        sorted_df1tt = sorted_df1tt[sorted_df1tt['most_common_terpene'] == sort_by_terpene]

    if sort_by_type != 'All':
        sorted_df1tt = sorted_df1tt[sorted_df1tt['type'] == sort_by_type]

    # displaying
    st.write(sorted_df1tt)


def page3():
    # Load the dataset
    csv_file = '2012-2014_Substate_SAE_Table_2.csv'
    df = pd.read_csv(csv_file)

    # Remove percentage signs and convert to numeric values (easier to work with)
    df['Small \nArea Estimate'] = pd.to_numeric(df['Small \nArea Estimate'].str.replace('%', ''), errors='coerce')
    df['95% CI (Lower)'] = pd.to_numeric(df['95% CI (Lower)'].str.replace('%', ''), errors='coerce')
    df['95% CI (Upper)'] = pd.to_numeric(df['95% CI (Upper)'].str.replace('%', ''), errors='coerce')

    # Title for the app
    st.title('Scatterplots with Sliders')

    # Describe the plot
    st.text('''
            The scatterplots below give an analytical visualisation of the estimated users 
            per state:
            
            Figure 1. Allows you to examine the 'Small Area Estimate' values 
            for different states, with a slider enabling you to focus on 
            specific ranges of 'Small Area Estimate' values.
            ''')

    # Create a Plotly Express scatter plot with a slider for 'Small \nArea Estimate'
    fig1 = px.scatter(df, x='State', y='Small \nArea Estimate', title='Figure 1. The Small \nArea Estimate per State',
                      labels={'Small \nArea Estimate': 'Small \nArea Estimate (%)', 'State': 'State'},
                      width=700, height=500,
                      range_x=[df['State'].min(), df['State'].max()],
                      range_y=[0, 30])

    # Update layout to include a slider
    fig1.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="category"))
    st.plotly_chart(fig1)

    # Describe the plot
    st.text('''
            Figure 2. Allows you to examine the '95% CI (Lower)' values
            for different states, with a slider enabling you to focus on 
            specific ranges of '95% CI (Lower)' values.
            ''')

    # Create a Plotly Express scatter plot with a slider for '95% CI (Lower)'
    fig2 = px.scatter(df, x='State', y='95% CI (Lower)', title='Figure 2. 95% CI (Lower) per State',
                      labels={'95% CI (Lower)': '95% CI (Lower) (%)', 'State': 'State'},
                      width=700, height=500,
                      range_x=[df['State'].min(), df['State'].max()],
                      range_y=[0, 25])

    # Update layout to include a slider
    fig2.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="category"))
    st.plotly_chart(fig2)

    # Describe the plot
    st.text('''
            Figure 3. Allows you to examine the '95% CI (Upper)' values 
            for different states, with a slider enabling you to focus on 
            specific ranges of '95% CI (Upper)' values.
            ''')

    # Create a Plotly Express scatter plot with a slider for '95% CI (Upper)'
    fig3 = px.scatter(df, x='State', y='95% CI (Upper)', title='Figure 3. 95% CI (Upper) per State',
                      labels={'95% CI (Upper)': '95% CI (Upper) (%)', 'State': 'State'},
                      width=700, height=500,
                      range_x=[df['State'].min(), df['State'].max()],
                      range_y=[0, 35])

    # Update layout to include a slider
    fig3.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="category"))
    st.plotly_chart(fig3)

    #%%

    # Title for the app
    st.title('Checkboxes')

    # Descibe the plots
    st.text('''
            The checkboxes below provide an interactive interface for you to filter data 
            based on the values in the 'Map Group' column and display the original 
            and filtered DataFrames.''')

    # Display the dataframe
    st.write("Original DataFrame:")
    st.write(df)

    # Describe the checkboxes
    st.text('''
            Checkboxes to filter based on Map Group
            ''')

    # Seperate the Map Group in subcolumns
    df_mg = pd.get_dummies(df, columns=['Map Group'], prefix='Group')

    # Checkbox to filter by individuals with a degree
    g1 = st.checkbox('Filter by Map Group 1')
    g2 = st.checkbox('Filter by Map Group 2', value=not g1)
    g3 = st.checkbox('Filter by Map Group 3', value=not g2)
    g4 = st.checkbox('Filter by Map Group 4', value=not g3)
    g5 = st.checkbox('Filter by Map Group 5', value=not g4)

    # Filter data based on checkbox state
    filtered_g1 = df[df_mg['Group_1'] == g1]
    filtered_g2 = df[df_mg['Group_2'] == g2]
    filtered_g3 = df[df_mg['Group_3'] == g3]
    filtered_g4 = df[df_mg['Group_4'] == g4]
    filtered_g5 = df[df_mg['Group_5'] == g5]

    # Display filtered data
    st.write('Filtered Data:')
    st.write(filtered_g1)
    st.write(filtered_g2)
    st.write(filtered_g3)
    st.write(filtered_g4)
    st.write(filtered_g5)
    
        # Title for the app
    st.title('Dropdown Menus')
    
    # Dropdown menus
    sorted_state = st.selectbox('Sort by State:', ['All States'] + df['State'].unique().tolist())
    sorted_substate = st.selectbox('Sort by Substate Region:', ['All States'] + df['Substate Region'].unique().tolist())
    
    # Filtering the menus
    if sorted_state == 'All States':
        sort = df
    else:
        sort = df[df['State'] == sorted_state]
    
    if sorted_substate != 'All States':
        sort = sort[sort['Substate Region'] == sorted_substate]
        
    # Display selected dropdown values
    st.text('Search information by state and substate region')
    st.write(sort)

def page2():
    # Load data
    df2 = pd.read_csv('rqtv-uenj.csv')
    
    # Title of page 2
    st.title("Sales")
    st.write("Page 2")
    
    # Columns are:
    # SoldDate
    # AverageRetailPriceperOz
    # AverageRetailPriceperGm
    
    df_filtered = df2.dropna()
    
    # Convert 'SoldDate' to datetime
    df_filtered['SoldDate'] = pd.to_datetime(df_filtered['SoldDate'])
    
    # Sort the DataFrame by 'SoldDate' in ascending order
    df_filtered = df_filtered.sort_values(by='SoldDate', ascending=True)
     
    mean_value = df_filtered['AverageRetailPriceperOz'].mean()
    
    # Define a function to replace outliers with the mean
    def replace_outliers(value, mean_value):
        if value > mean_value * 3:  # Adjust the multiplier based on your definition of outliers
            return mean_value
        else:
            return value
    
    # Apply the function to the column to replace outliers with the mean
    df_filtered['AverageRetailPriceperOz'] = df_filtered['AverageRetailPriceperOz'].apply(replace_outliers, args=(mean_value,))
    
    # Select x-axis and y-axis columns using checkboxes
    x_column = st.sidebar.selectbox('Select X-axis:', ['SoldDate', 'AverageRetailPriceperOz', 'AverageRetailPriceperGm'], key='x_column_selectbox')
    y_column = st.sidebar.selectbox('Select Y-axis:', ['SoldDate', 'AverageRetailPriceperOz', 'AverageRetailPriceperGm'], key='y_column_selectbox')
    
    # Select plot type using a selectbox
    plot_type = st.sidebar.selectbox('Select plot type:', ['scatter', 'line', 'hist', 'box', 'bar'])
    
    # Select hue using a selectbox
    hue_options = ['None', 'SoldDate', 'AverageRetailPriceperOz', 'AverageRetailPriceperGm']
    hue_column = st.sidebar.selectbox('Select hue:', hue_options, key='hue_column_selectbox')
    
    # Select palette using a selectbox
    palette_options = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink']
    palette = st.sidebar.selectbox('Select palette:', palette_options, key='palette_selectbox')
    
    # Convert selected columns to appropriate scaling
    if x_column == 'SoldDate':
        x_min = df_filtered[x_column].min().timestamp()
        x_max = df_filtered[x_column].max().timestamp()
        x_range = st.sidebar.slider(f'Select range of {x_column}', x_min, x_max, (x_min, x_max), format="%.0f", key=f'x_range_{x_column}')
        x_range = (pd.Timestamp(x_range[0], unit='s'), pd.Timestamp(x_range[1], unit='s'))
    else:
        x_min = df_filtered[x_column].min()
        x_max = df_filtered[x_column].max()
        x_range = st.sidebar.slider(f'Select range of {x_column}', x_min, x_max, (x_min, x_max), key=f'x_range_{x_column}')

    if y_column == 'SoldDate':
        y_min = df_filtered[y_column].min().timestamp()
        y_max = df_filtered[y_column].max().timestamp()
        y_range = st.sidebar.slider(f'Select range of {y_column}', y_min, y_max, (y_min, y_max), format="%.0f", key=f'y_range_{y_column}')
        y_range = (pd.Timestamp(y_range[0], unit='s'), pd.Timestamp(y_range[1], unit='s'))
    else:
        y_min = df_filtered[y_column].min()
        y_max = df_filtered[y_column].max()
        y_range = st.sidebar.slider(f'Select range of {y_column}', y_min, y_max, (y_min, y_max), key=f'y_range_{y_column}')

    # Create the matplotlib diagram after applying the outlier replacement
    fig, ax = plt.subplots()
    
    if plot_type == 'scatter':
        if hue_column == 'None':
            scatter = ax.scatter(data=df_filtered, x=x_column, y=y_column, color=palette)
        else:
            cmap = cm.get_cmap(color_map[palette])
            scatter = ax.scatter(data=df_filtered, x=x_column, y=y_column, c=df_filtered[hue_column], cmap=cmap)
    elif plot_type == 'line':
        line = ax.plot(df_filtered[x_column], df_filtered[y_column])
    elif plot_type == 'hist':
        hist = ax.hist(df_filtered[x_column])
    elif plot_type == 'box':
        if x_column != 'SoldDate':  # Exclude 'SoldDate' column from boxplot
            box = ax.boxplot(df_filtered[x_column])
    elif plot_type == 'bar':
        bar = ax.bar(df_filtered[x_column], df_filtered[y_column])
    
    plt.title(f'Matplotlib {plot_type.capitalize()} Plot')
    plt.xlabel(x_column)
    plt.ylabel(y_column)

    # Function to update plot based on slider values
    def update_plot(x_range, y_range):
        ax.set_xlim(x_range[0], x_range[1])  # Update x-axis limits
        ax.set_ylim(y_range[0], y_range[1])  # Update y-axis limits
        fig.canvas.draw_idle()
    
    # Call the update_plot function with the selected ranges
    update_plot(x_range, y_range)

    # Display the plot in Streamlit
    st.pyplot(fig)

def create_zip():
    # Lijst met bestanden in de huidige map, exclusief .ipynb_checkpoints
    files = [file for file in os.listdir('.') if not file.startswith('.')]
    
    # Maak een tijdelijke map om bestanden te kopiëren
    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Kopieer alle bestanden naar de tijdelijke map
        for file in files:
            shutil.copy(file, temp_dir)
        
        # Maak een zip-bestand van de tijdelijke map
        with ZipFile('bestanden.zip', 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), file)
    finally:
        # Verwijder de tijdelijke map
        shutil.rmtree(temp_dir)

def main():
    # Page Configuration
    st.set_page_config(page_title="Cannabis Informary", page_icon='weed_cartoon.jpg', layout='wide')
    
    st.title("Cannabis Informary")
    
    # Statische tekst onder de titel
    st.markdown("**Description:**")
    st.markdown("This is the information page about cannabis.")
    st.markdown("Page 1 is about strains of cannabis and what they are.")
    st.markdown("Page 2 is about sales.")
    st.markdown("Page 3 is about the percentage of users in the United States.")
     
    st.sidebar.title('Navigation')

    option = st.sidebar.selectbox("Go to", ["Home", "Page 1", "Page 2", "Page 3"])

    if option == "Page 1":
        page1()
    elif option == "Page 2":
        page2()
    elif option == "Page 3":
        page3()
    elif option == "Home":
        show_sources()

    # Knop om bestanden te downloaden
    if st.button("Download alle bestanden als ZIP"):
        create_zip()
        # Geef de locatie van het ZIP-bestand terug
        zip_file_path = 'bestanden.zip'
        # Geef een downloadlink weer voor het ZIP-bestand
        st.markdown(f"[Download ZIP-bestand](./{zip_file_path})")


def show_sources():
    st.title("Sources")
    st.markdown("**Sources**")
    st.markdown("- [Massachusetts Cannabis Control Commission](https://masscannabiscontrol.com/open-data/data-catalog/)")
    st.markdown("- [Leafly Cannabis Strains Metadata](https://www.kaggle.com/datasets/gthrosa/leafly-cannabis-strains-metadata)")
    st.markdown("- [SAMHSA Marijuana Use in Past Year](https://data.world/samhsa/marijuana-use-in-past-year)")

if __name__ == "__main__":
    main()





