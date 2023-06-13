from numpy import extract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji

def fetch_stats(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # 1. Overall No of Messages
    num_messages = df.shape[0]

    # 2. no of words
    words = []
    for messages in df['messages']:
        words.extend(messages.split())

    # fetch number of media messages
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]



    return num_messages,len(words),num_media_messages
    

def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):

    f = open('hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    

    words = []

    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['month_num'] = df['message_date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['only_date'] = df['message_date'].dt.date

    timeline = df.groupby('only_date').count()['messages'].reset_index()

    return timeline


def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]   

    heatmap = df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)

    return heatmap
