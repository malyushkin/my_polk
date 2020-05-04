from sqlalchemy import create_engine
from tqdm import tqdm 
import pandas as pd
import psycopg2
import config

engine = create_engine(config.Db.engine)
psycopg2_connect = psycopg2.connect(config.Db.engine)

INSTAGRAM_TABLE = config.Db.instagram_table


def update_db_row(query, data):
    try:
        db.execute(query, data)
        psycopg2_connect.commit()
        return True
    except Exception as e:
        print(e)
        return False

dat = pd.read_csv('../data/instagram_post_04-05-2020__with-tags.csv')
dat.dropna(subset=['tags'], inplace=True)
update_query = '''UPDATE {} SET tags = (%s) WHERE id = (%s);'''.format(INSTAGRAM_TABLE)
db = psycopg2_connect.cursor()
for idx, tags in tqdm(dat.iterrows(), total=dat.shape[0]):
	update_db_row(update_query, (tags.tags.strip('[]').replace('\'', '').split(', '), tags.id))
db.close()
