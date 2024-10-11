from sqlalchemy import create_engine
import pandas as pd

conn_string = 'postgresql://phuc:1234@localhost/actionCustomerList'
db = create_engine(conn_string)
conn = db.connect()

df = pd.read_csv('D:\\DEFinal\\Backend\\processed_data.csv')
df.to_sql('actionCustomerList',con=conn,if_exists='replace',index=False)
