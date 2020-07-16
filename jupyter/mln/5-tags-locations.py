#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import random
import re 
import time 

# DB
import psycopg2

# SSH
# from sshtunnel import SSHTunnelForwarder

# NER
from natasha import (Doc, MorphVocab, NewsEmbedding, NewsNERTagger, Segmenter)


# In[2]:


# config data
SSH_IP = '89.223.99.189'
SSH_PORT = 22
SSH_USERNAME = 'uno'
SSH_PASSWORD = 'FD8i3cMp'

DB_NAME = 'my_polk'
DB_USER = 'server'
DB_PASSWORD = 'server'


# In[3]:


# tunnel = SSHTunnelForwarder(
#     (SSH_IP, SSH_PORT),
#     ssh_username=SSH_USERNAME,
#     ssh_password=SSH_PASSWORD,
#     remote_bind_address=('127.0.0.1', 5432))

# tunnel.start()

# conn = psycopg2.connect(
#     database=DB_NAME,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     host=tunnel.local_bind_host,
#     port=tunnel.local_bind_port)

conn = psycopg2.connect('postgres://server:server@localhost:5432/my_polk')


# In[4]:


while True:

    n = 10000
    n_sql = f"SELECT * FROM instagram_post WHERE note is NULL LIMIT {n};"
    df = pd.io.sql.read_sql_query(n_sql, conn)


    # In[5]:


    if df.size == 0:
        break;


    # # Выделение NER

    # In[6]:


    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()
    ner_tagger = NewsNERTagger(emb)


    # In[7]:


    insert_nameentity_sql = '''INSERT INTO instagram_nameentity (name, type) VALUES (%s, %s) ON CONFLICT DO NOTHING;'''
    insert_nameentity_post_sql = '''INSERT INTO instagram_postnameentity (name_entity_id, post_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;'''


    # In[8]:


    db = conn.cursor()


    # In[9]:


    df.loc[:, 'caption_ner_locs'] = None
    df.loc[:, 'caption_ner_pers'] = None
    df.loc[:, 'caption_ner_locs_lemma'] = None
    df.loc[:, 'caption_ner_pers_lemma'] = None


    # In[ ]:


    for idx, row in df.iterrows():
        entities = []
        
        if row['caption']:
            caption = re.sub(' +', ' ', row['caption'].replace('\n', ' ').replace('\r', ' '))
            caption_markup = ner_tagger(caption)

            caption_locs = [caption[span.start:span.stop] for span in caption_markup.spans if span.type == 'LOC']
            if caption_locs:
                df.at[idx, 'caption_ner_locs'] = caption_locs
                df.at[idx, 'caption_ner_locs_lemma'] = [morph_vocab.lemmatize(loc, 'NOUN', {}).title() for loc in caption_locs]
                entities, entity_type = df.at[idx, 'caption_ner_locs_lemma'], 'LOC'

            caption_pers = [caption[span.start:span.stop] for span in caption_markup.spans if span.type == 'PER']
            if caption_pers:
                df.at[idx, 'caption_ner_pers'] = caption_pers
                df.at[idx, 'caption_ner_pers_lemma'] = [morph_vocab.lemmatize(loc, 'NOUN', {}).title() for loc in caption_pers]
                entities, entity_type = df.at[idx, 'caption_ner_pers_lemma'], 'PER'
        
        for entity in entities:
            entity = entity.replace('\'', ' ') 
            select_nameentity_sql = f"SELECT id, name FROM instagram_nameentity WHERE name = '{entity}' AND type = '{entity_type}'"
            entity_df = pd.io.sql.read_sql_query(select_nameentity_sql, conn)
            if not entity_df.size:
                db.execute(insert_nameentity_sql, (entity, entity_type))
                db.execute('''SELECT id FROM instagram_nameentity ORDER BY id DESC LIMIT 1;''')
                entity_id = db.fetchone()[0]
            else:
                entity_id = entity_df.id[0]
            db.execute(insert_nameentity_post_sql, (int(entity_id), int(row['id'])))
        
        db.execute(f"UPDATE instagram_post SET note = 'updated' WHERE id = '{row['id']}';")
        conn.commit()


# In[ ]:


# conn.commit()


# In[ ]:


# db.execute("ROLLBACK")


# In[ ]:


conn.close()


# In[ ]:


# entity.replace('\'', ' ')


# In[ ]:




