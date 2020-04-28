from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import requests
import time
import sys
import logging
import config

# logger = logging.getLogger('instParse')
# logger.setLevel(logging.DEBUG)

# Db
engine = create_engine(config.Db.engine)
psycopg2_connect = psycopg2.connect(config.Db.engine)

tags = ['бессмертныйполкспб', 'бессмертныйполкмосква', 'бессмертныйполккраснодар', 'бессмертныйполкказань',
        'бессмертныйполкуфа', 'бессмертныйполктюмень', 'бессмертныйполксочи', 'бессмертныйполкомск', 'immortalregiment',
        'бессмертныйполконлайн', 'бессмертныйполк2016', 'бесмертныйполк2019', 'бессмертныйполкалматы',
        'бесмертныйполк2018', 'бессмертныйполксаратов', 'бессмертныйполк05', 'polk.rf', 'бессмертныйполкхабаровск',
        'бессмертныйподвиг', 'бессмертныйполкнальчик', 'бессмертныйполкростов', 'bessmertniy_polk_almaty',
        'бессмертныйполк2020']

if len(sys.argv) != 2:
    print(f"[{datetime.now()}] \"Укажите номер хештега!\"")
    sys.exit()
else:
    tag = tags[int(sys.argv[1])]
    print(f"[{datetime.now()}] \"Хештег #{tag}\"")

QH = '7dabc71d3e758b1ec19ffb85639e427b'
STEP = 30

url_tag = f'https://www.instagram.com/explore/tags/{tag}/?__a=1'
url_query = 'https://www.instagram.com/graphql/query/'

post_columns = ['id', 'owner_id', 'shortcode', 'post_url', 'display_url', 'published', 'caption', 'likes_count',
                'comments_count', 'is_video', 'video_view_count', 'inst_caption', 'query']

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close',
}

posts_df = pd.DataFrame(columns=post_columns)


def inst_post_extract(edge_node):
    return {'id': edge_node['id'],
            'owner_id': edge_node['owner']['id'],
            'shortcode': edge_node['shortcode'],
            'post_url': f"https://www.instagram.com/p/{edge_node['shortcode']}/",
            'display_url': edge_node['display_url'],
            'published': datetime.fromtimestamp(edge_node['taken_at_timestamp']),
            'caption': edge_node['edge_media_to_caption']['edges'][0]['node']['text'] if len(
                edge_node['edge_media_to_caption']['edges']) else None,
            'likes_count': edge_node['edge_liked_by']['count'],
            'comments_count': edge_node['edge_media_to_comment']['count'],
            'is_video': edge_node['is_video'],
            'video_view_count': edge_node.get('video_view_count', None),
            'inst_caption': edge_node.get('accessibility_caption', None),
            'query': f"#{tag}"}


def write_to_db_post(posts):
    duplicates = 0
    connect = engine.connect()
    query = '''INSERT INTO instagram_post (id, owner_id, shortcode, display_url, published, caption, likes_count, comments_count, is_video, inst_caption, query) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;'''

    for idx, post in posts.iterrows():
        try:
            ex = connect.execute(query, tuple(post.values))
            if not ex.rowcount:
                duplicates += 1
                print(f"[{datetime.now()}] \"Error! Duplicated place object\"")
                # logger.error(f"[{datetime.now()}] \"Error! Duplicated place object\"")
        except Exception as e:
            print(f"[{datetime.now()}] \"Error!\"")
            print(e)
            # logger.error(f"[{datetime.now()}] \"Error!\"")
            # logger.error(e)
            continue
    connect.close()

    return f"All done with {duplicates} duplicates"


# Первый запрос
response_tag = requests.get(url_tag, headers=headers)

if (response_tag.status_code == 200):
    edges = response_tag.json()['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    for edge in edges:
        node = inst_post_extract(edge['node'])
        posts_df = posts_df.append(node, ignore_index=True)

    print(f"[{datetime.now()}] \"First {len(edges)} posts extracted\"")
    # logger.info(f"[{datetime.now()}] \"First {len(edges)} posts extracted\"")

N = response_tag.json()['graphql']['hashtag']['edge_hashtag_to_media']['count']
end_cursor = response_tag.json()['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']

# Остальные запросы
for i in range(int(N / STEP)):

    params = {
        'query_hash': QH,
        'variables': f'{{"tag_name":"{tag}", "first": {i}, "after": "{end_cursor}"}}'
    }

    response_query = requests.get(url_query, params=params, headers=headers)

    if response_query.status_code == 200:
        end_cursor = response_query.json()['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        edges = response_query.json()['data']['hashtag']['edge_hashtag_to_media']['edges']

        if not len(edges):
            break

        for edge in edges:
            node = inst_post_extract(edge['node'])
            posts_df = posts_df.append(node, ignore_index=True)

        print(f"[{datetime.now()}] \"More {len(edges)} posts extracted\"")
        # logger.info(f"[{datetime.now()}] \"More {len(edges)} posts extracted\"")

    else:
        break

    min = 1
    print(f"[{datetime.now()}] \"Sleeping for {min} min\"")
    # logger.info(f"[{datetime.now()}] \"Sleeping for {min} min\"")
    # time.sleep(min * 60)
    time.sleep(15)

posts_df.drop_duplicates(subset=['id'], keep='first', inplace=True)
print(write_to_db_post(posts_df))
# logger.info(f"[{datetime.now()}] \"All done\"")
