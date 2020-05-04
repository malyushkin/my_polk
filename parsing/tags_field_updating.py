from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import config

engine = create_engine(config.Db.SQLALCHEMY_DATABASE_URI)
psycopg2_connect = psycopg2.connect(config.Db.SQLALCHEMY_DATABASE_URI)

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
update_query = '''UPDATE {} SET tags = (%s) WHERE id = (%s);'''.format(INSTAGRAM_TABLE)
db = psycopg2_connect.cursor()
for idx, tags in dat.tags:
    update_db_row(update_query, (tags.id, tags.tags))
db.close()
