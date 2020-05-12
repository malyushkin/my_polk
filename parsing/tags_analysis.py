from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dat = pd.read_csv('../data/instagram_post_04-05-2020__with-tags.csv', low_memory=False)
dat.dropna(subset=['tags'], inplace=True)

dat.columns
dat[['id', 'owner_id', 'shortcode', 'post_url', 'display_url', 'published',
     'caption', 'likes_count', 'comments_count', 'is_video', 'video_view_count']].to_csv('../data/my_polk_demo.csv')

for idx, tags in tqdm(dat.iterrows(), total=dat.shape[0]):
    dat.at[idx, 'tags'] = tags.tags.strip('[]').replace('\'', '').split(', ')


# hashtags_list_df
tags_df = dat[['tags']]

flattened_tags_df = pd.DataFrame([hashtag for hashtags_list in tags_df.tags for hashtag in hashtags_list],  columns=['tag'])
flattened_tags_df['tag'].unique().size
popular_tags = flattened_tags_df.groupby('tag').size().reset_index(name='counts').sort_values('counts', ascending=False).reset_index(drop=True)

# number of times each hashtag appears
counts = flattened_tags_df.groupby(['tag']).size().reset_index(name='counts').counts

# define bins for histogram
my_bins = np.arange(0,counts.max()+2, 800)-0.5

len(my_bins)

# plot histogram of tweet counts
plt.figure()
plt.hist(counts, bins = my_bins)
plt.xlabels = np.arange(1,counts.max()+1, 1)
plt.xlabel('hashtag number of appearances')
plt.ylabel('frequency')
plt.yscale('log', nonposy='clip')
plt.show()

# take hashtags which appear at least this amount of times
sum(popular_tags.counts>=4800)
min_appearance = 4800
# find popular hashtags - make into python set for efficiency
popular_tags_set = set(popular_tags[popular_tags.counts>=min_appearance]['tag'])

tags_df['popular_hashtags'] = []
tags_df['popular_hashtags'] = tags_df.tags.apply(lambda hashtag_list: [hashtag for hashtag in hashtag_list if hashtag in popular_tags_set])

# drop rows without popular hashtag
popular_tags_list_df = tags_df.loc[tags_df.popular_hashtags.apply(lambda hashtag_list: hashtag_list !=[])]

# make new dataframe
hashtag_vector_df = popular_tags_list_df.loc[:, ['popular_hashtags']]

for hashtag in popular_tags_set:
    # make columns to encode presence of hashtags
    hashtag_vector_df['{}'.format(hashtag)] = hashtag_vector_df.popular_hashtags.apply(
        lambda hashtag_list: int(hashtag in hashtag_list))

hashtag_vector_df

hashtag_matrix = hashtag_vector_df.drop('popular_hashtags', axis=1)

correlations = hashtag_matrix.corr()

# plot the correlation matrix
plt.figure(figsize=(10,10))
sns.heatmap(correlations,
    cmap='RdBu',
    vmin=-1,
    vmax=1,
    square = True,
    cbar_kws={'label':'correlation'})
plt.show()

# Убираем блатных

min_appearance = 4000
# find popular hashtags - make into python set for efficiency
popular_tags_set = set(popular_tags[popular_tags.counts>=min_appearance]['tag'])

correlations.index
popular_tags_set.remove('ауе')
popular_tags_set.remove('ауежизньворам')
popular_tags_set.remove('базарунет')
popular_tags_set.remove('беспридел')
popular_tags_set.remove('братзабрата')
popular_tags_set.remove('волки')
popular_tags_set.remove('ганджа')
popular_tags_set.remove('марихуана')
popular_tags_set.remove('мафия')
popular_tags_set.remove('хулиганы')

popular_tags_set.remove('бандит')
popular_tags_set.remove('бандиты')
popular_tags_set.remove('блатной')
popular_tags_set.remove('вор')
popular_tags_set.remove('ворывзаконе')
popular_tags_set.remove('наркотики')
popular_tags_set.remove('гиопика')
popular_tags_set.remove('криминал')

popular_tags_set.remove('гангстеры')
popular_tags_set.remove('хулиганы2')
popular_tags_set.remove('уроди')
popular_tags_set.remove('скемтытам')

tags_df['popular_hashtags'] = None
tags_df['popular_hashtags'] = tags_df.tags.apply(lambda hashtag_list: [hashtag for hashtag in hashtag_list if hashtag in popular_tags_set])

# drop rows without popular hashtag
popular_tags_list_df = tags_df.loc[tags_df.popular_hashtags.apply(lambda hashtag_list: hashtag_list !=[])]

# make new dataframe
hashtag_vector_df = popular_tags_list_df.loc[:, ['popular_hashtags']]

for hashtag in popular_tags_set:
    # make columns to encode presence of hashtags
    hashtag_vector_df['{}'.format(hashtag)] = hashtag_vector_df.popular_hashtags.apply(
        lambda hashtag_list: int(hashtag in hashtag_list))

hashtag_vector_df

hashtag_matrix = hashtag_vector_df.drop('popular_hashtags', axis=1)

correlations = hashtag_matrix.corr()

# plot the correlation matrix
plt.figure(figsize=(10,10))
sns.heatmap(correlations,
    cmap='RdBu',
    vmin=-1,
    vmax=1,
    square = True,
    cbar_kws={'label':'correlation'})
plt.show()
