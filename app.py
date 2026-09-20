import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sqlalchemy import create_engine

# ---------------------------------------------------------
# Page Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title='Stroke Risk Analytics',
    page_icon='🏥',
    layout='wide'
)

st.title('🏥 Healthcare Stroke Risk Analytics')
st.markdown('An interactive dashboard analyzing stroke risk factors across patient demographics and health indicators.')


# ---------------------------------------------------------
# Data Loading (SQL Server with CSV Fallback)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    """Attempts SQL Server connection; falls back to CSV for cloud deployment."""
    try:
        connection_string = (
            "mssql+pyodbc://localhost/Healthcare_Analytics"
            "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        )
        engine = create_engine(connection_string)
        qyery = 'select * from stroke_data'
        df = pd.read_sql(query,con=engine)
        return df,'SQL Server'
    except Exception:
        # Fallback for Streamlit Cloud deployment
        csv_path = 'data/cleaned_stroke_data.csv'
        df = pd.read_csv(csv_path)
        return df, 'Cleaned CSV File'
df, data_source = load_data()
st.sidebar.caption(f'📁 Data Source: **{data_source}**')

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------

# Gender filter
genders = ['All'] + list(df['gender'].unique())
selected_gender = st.sidebar.selectbox('Gender',genders)

# Work Type filter
work_types = ['All']+list(df['work_type'].unique())
selected_work = st.sidebar.selectbox('Work Type',work_types)

# Age Range Slider
min_age , max_age = int(df['age'].min()),int(df['age'].max())
selected_age = st.sidebar.slider('Age Range',min_age,max_age,(min_age,max_age))

# Health Conditions Filter
hypertension_filter = st.sidebar.multiselect(
    'Hypertension',
    options = df['hypertension_label'].unique(),
    default = df['hypertension_label'].unique()
)

# Apply Filters
filtered_df = df[
    (df['age']>=selected_age[0])&
    (df['age']<=selected_age[1])&
    (df['hypertension_label'].isin(hypertension_filter))
]

if selected_gender !='All':
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

if selected_work !='All':
    filtered_df = filtered_df[filtered_df['work_type']==selected_work]


# ---------------------------------------------------------
# Key Performance Indicators (KPIs)
# ---------------------------------------------------------
total_patients = len(filtered_df)
stroke_cases = filtered_df['stroke'].sum()
stroke_rate = (stroke_cases/total_patients * 100) if total_patients > 0 else 0
avg_bmi = filtered_df['bmi'].mean() if total_patients > 0 else 0
avg_glucose = filtered_df['avg_glucose_level'].mean() if total_patients > 0 else 0


col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Patients',f'{total_patients:,}')
col2.metric('Stroke Cases',f'{stroke_cases:,}')
col3.metric('Stroke Rate',f'{stroke_rate:.1f}%')
col4.metric('Avg Glucose Level',f'{avg_glucose:.1f} mg/dL')

st.markdown('---')


# ---------------------------------------------------------
# Visualizations
# ---------------------------------------------------------
col_left, col_right = st.columns(2)

#Stroke Rate by Age Group
with col_left:
    st.subheader('Stroke Prevalence by Age Group')
    fig1, ax1 = plt.subplots(figsize=(8,4.5))
    age_stroke = filtered_df.groupby('age_group',observed=False)['stroke'].mean().reset_index()
    age_stroke['stroke_pct'] = age_stroke['stroke'] * 100

    sns.barplot(data = age_stroke, x='age_group',y='stroke_pct',palette ='Reds_d',ax=ax1)
    ax1.set_ylabel('Stroke Rate (%)')
    ax1.set_xlabel('Age Group')
    if not age_stroke.empty:
        ax1.set_ylim(0, max(age_stroke['stroke_pct'].max()*1.2, 10))


    for p in ax1.patches:
        ax1.annotate(
            f'{p.get_height():.1f}%',
            (p.get_x() + p.get_width()/2., p.get_height()),
            ha='center',va='center',xytext=(0,5),textcoords='offset points'
        )

    sns.despine()
    st.pyplot(fig1)

#Glucose vs BMI Scatter Distribution
with col_right:
    st.subheader('Avg Glucose vs. BMI by Stroke Status')
    fig2, ax2 = plt.subplots(figsize=(8, 4.5))
    sns.scatterplot(
        data = filtered_df,
        x='bmi',
        y='avg_glucose_level',
        hue = 'stroke_label',
        palette = {'Stroke':'#d9534f','No Stroke': '#5bc0de'},
        alpha=0.7,
        ax=ax2
    )

    ax2.set_xlabel('Body Mass Index (BMI)')
    ax2.set_ylabel('Average Glucose Level (mg/dL)')
    ax2.legend(title='Status')
    sns.despine()
    st.pyplot(fig2)

# ---------------------------------------------------------
# SQL Dataset Inspector
# ---------------------------------------------------------
with st.expander('🔍 Inspect Cleaned Data'):
    st.dataframe(filtered_df.head(100),use_container_width=True)