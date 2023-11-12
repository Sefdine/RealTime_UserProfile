from dash import Dash, html, dcc
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["user_profiles"]
mongo_collection = mongo_db["users"]

# Load data from MongoDB into a Pandas DataFrame
data_from_mongo = list(mongo_collection.find())
df = pd.DataFrame(data_from_mongo)

# Convert dob_date and registration_date to datetime format
df['dob_date'] = pd.to_datetime(df['dob_date'])
df['registration_date'] = pd.to_datetime(df['registration_date'])

# Create a Dash web application
app = Dash(__name__)

# Define layout
app.layout = html.Div(children=[
    html.H1(children='User Profiles Analysis'),

    dcc.Graph(
        id='age-distribution',
        figure={
            'data': [
                {'x': df['gender'], 'y': df['age'], 'type': 'bar', 'name': 'Age Distribution'},
            ],
            'layout': {
                'title': 'Age Distribution by Gender'
            }
        }
    ),

    dcc.Graph(
        id='registration-date-distribution',
        figure={
            'data': [
                {'x': df['registration_date'], 'y': df['age'], 'mode': 'markers', 'name': 'Registration Date Distribution'}
            ],
            'layout': {
                'title': 'Registration Date Distribution',
                'xaxis': {'title': 'Registration Date'},
                'yaxis': {'title': 'Age'}
            }
        }
    ),

    dcc.Graph(
        id='nationality-count',
        figure={
            'data': [
                {'x': df['nat'].value_counts().index, 'y': df['nat'].value_counts().values, 'type': 'bar', 'name': 'Nationality Count'},
            ],
            'layout': {
                'title': 'User Count by Nationality',
                'xaxis': {'title': 'Nationality'},
                'yaxis': {'title': 'User Count'}
            }
        }
    )
])

# Run the Dash web application
if __name__ == '__main__':
    app.run_server(debug=True)
