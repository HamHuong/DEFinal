from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os
from datetime import timedelta
from sklearn.model_selection  import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from airflow.providers.postgres.operators.postgres import PostgresOperator
import psycopg2

def load_data():
    train = pd.read_csv("/opt/airflow/dags/training_sample.csv",low_memory=True)

    predictors = train.drop(['ordered','UserID','device_mobile'], axis=1)
    targets = train.ordered
    X_train, X_test, y_train, y_test  =  train_test_split(predictors, targets, test_size=.3)

    classifier=GaussianNB()
    classifier=classifier.fit(X_train,y_train)
    predictions=classifier.predict(X_test)

    yesterday_prospects = pd.read_csv("/opt/airflow/dags/testing_sample.csv",low_memory=True)
    userids = yesterday_prospects.UserID
    yesterday_prospects = yesterday_prospects.drop(['ordered','UserID','device_mobile'], axis=1)
    yesterday_prospects['propensity'] = classifier.predict_proba(yesterday_prospects)[:,1]
    pd.DataFrame(userids)
    results = pd.concat([userids, yesterday_prospects], axis=1)
    results.to_csv("/opt/airflow/dags/processed_data.csv",index=False)


def insert_data():
    df = pd.read_csv("/opt/airflow/dags/processed_data.csv", low_memory=True)

    conn = psycopg2.connect(
        dbname='test',
        user='airflow',
        password='airflow',
        host='host.docker.internal',
        port='5432'
    )
    cur = conn.cursor()
    try:
        for index, row in df.iterrows():
            cur.execute("INSERT INTO propensity_list (UserID, basket_icon_click, basket_add_list, basket_add_detail, "
            "sort_by, image_picker, account_page_click, promo_banner_click, detail_wishlist_add, "
            "list_size_dropdown, closed_minibasket_click, checked_delivery_detail, "
            "checked_returns_detail, sign_in, saw_checkout, saw_sizecharts, saw_delivery, "
            "saw_account_upgrade, saw_homepage, device_computer, device_tablet, returning_user, "
            "loc_uk, propensity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
            "%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (str(row['UserID']), row['basket_icon_click'], row['basket_add_list'],
             row['basket_add_detail'], row['sort_by'], row['image_picker'], row['account_page_click'],
             row['promo_banner_click'], row['detail_wishlist_add'], row['list_size_dropdown'],
             row['closed_minibasket_click'], row['checked_delivery_detail'], row['checked_returns_detail'],
             row['sign_in'], row['saw_checkout'], row['saw_sizecharts'], row['saw_delivery'],
             row['saw_account_upgrade'], row['saw_homepage'], row['device_computer'], row['device_tablet'],
             row['returning_user'], row['loc_uk'], row['propensity']))


        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error occurred during data insertion:", e)
    finally:
        cur.close()
        conn.close()



# initializing the default arguments that we'll pass to our DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(5)
}

ingestion_dag = DAG(
    'data_ingestion',
    default_args=default_args,
    description='Aggregates records for data analysis',
    schedule_interval=timedelta(days=1),
    catchup=False
)

create_table = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_localhost',
    sql='''CREATE TABLE IF NOT EXISTS propensity_list (
            UserID VARCHAR(255) NOT NULL,
            basket_icon_click VARCHAR(255),
            basket_add_list VARCHAR(255),
            basket_add_detail VARCHAR(255),
            sort_by VARCHAR(255),
            image_picker VARCHAR(255),
            account_page_click VARCHAR(255),
            promo_banner_click VARCHAR(255),
            detail_wishlist_add VARCHAR(255),
            list_size_dropdown VARCHAR(255),
            closed_minibasket_click VARCHAR(255),
            checked_delivery_detail VARCHAR(255),
            checked_returns_detail VARCHAR(255),
            sign_in VARCHAR(255),
            saw_checkout VARCHAR(255),
            saw_sizecharts VARCHAR(255),
            saw_delivery VARCHAR(255),
            saw_account_upgrade VARCHAR(255),
            saw_homepage VARCHAR(255),
            device_computer VARCHAR(255),
            device_tablet VARCHAR(255),
            returning_user VARCHAR(255),
            loc_uk VARCHAR(255),
            propensity VARCHAR(255)
        );''',
    dag=ingestion_dag,
)

task_1 = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=ingestion_dag,
)


task_2 = PythonOperator(
    task_id='insert_data',
    python_callable=insert_data,
    dag=ingestion_dag,
)

create_table >> task_1 >> task_2