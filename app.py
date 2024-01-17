from flask import Flask, render_template, request, make_response, jsonify
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import nltk 
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')

from preprocess_data import preprocess_text, perform_sentiment_analysis

app_path = "/home/ubuntu/app"

source_complaint_data = r'./updated_feedback_data.csv'
source_products_data = r'./data.csv'

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'ubuntu',
    'host': 'localhost',
    'database': 'sample_ecom',
    'port': 3306  # Change if your MySQL server is running on a different port
}


@app.route('/insert_review', methods =["POST"])
def insert_review_data():
    df = pd.read_csv(source_complaint_data)
    df = df.drop('Intent', axis=1)
    df['date_of_complain'] = pd.to_datetime(df['date_of_complain'], format='%Y-%m-%d', errors='coerce')
    df['time_of_complain'] = pd.to_datetime(df['time_of_complain'], format='%I:%M %p').dt.time
    engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    df.to_sql('customer_feedback', con=engine, if_exists='append', index=False)

    return "Successfully inserted"


@app.route('/insert_products', methods =["POST"])
def insert_product_data():
    df = pd.read_csv(source_products_data)
    df = df.dropna()
    df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)', expand=False).astype(float)
    df['Price'] = df['Price'].astype(int)
    engine = create_engine(f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
    df.to_sql('products', con=engine, if_exists='append', index=False)

    return "Successfully inserted products"


@app.route('/review', methods =["POST"])
def get_response():
    review = request.form['review']
    preprocessed_tokens = preprocess_text(review)
    sentimental_analysis = perform_sentiment_analysis(preprocessed_tokens)

    return "Successfully inserted products"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
