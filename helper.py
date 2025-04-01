from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    
    #1.fetch number of messages
    num_messages = df.shape[0] #df.shape extracts rows and columns both but df.shape[0] specifically extracts the number of rows from the shape tuple.

    #2.number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)

    #3.no. of media files
    #since we have not include any media file when we are exporting the chat so there is a message named media omitted in place of that

    ##uski approach
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    ##meri approach
    '''
    num_media=0
    for message in df['message']:
        if message == '<Media omitted>\n':#\n dikha ni rha btt h
           num_media += 1
    return num_messages,num_words,num_media'''

    #4.no. of links
    links = []
    extractor = URLExtract()
    for message in df['message']:
        #print(extractor.find_urls(message))##it will give many empty lists
        links.extend(extractor.find_urls(message))
    num_links = len(links)

    return num_messages, num_words, num_media, num_links

def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'chat_percent'})
    #reset index to convert into dataframe
    return x, new_df

def create_wordcloud(selected_user, df):
    #filter kr rhe vhi stop words ye sb hta rhe
    f = open('stop_hinglish.txt', 'r', encoding='utf-8')
    stop_words = f.read()
    
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y) #basically y jo list h unke elements ko join kr deta vo jupyter wle me eg h basically list element ko single string me convert kr deta.." "ye separator h

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white') #WordCloud class ka ek object wc banaya gaya hai.
    #width=500, height=500 → WordCloud ki image ka size.
    temp['message'] = temp['message'].apply(remove_stop_words) #This applies the remove_stop_words function to every value in the 'message' column of the DataFrame temp.
    df_wc = wc.generate(temp['message'].str.cat(sep=" ")) #multiple strings hain, to .str.cat(sep=" ") unko ek saath concatenate (join) kar dega.
    #wc.generate(...) → Is single string se WordCloud generate ho raha hai.
    return df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r', encoding='utf-8')
    stop_words = f.read()
    
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    #stop words are the words which are used in making sentence btt does not have meaning alone so we have to remove them
    #first we need to remove group notification bczz faltu h vo
    temp = df[df['user'] != 'group_notification']
    #now we need to remove media omitted wle notification
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    monthly_timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline['month'][i] + "-" + str(monthly_timeline['year'][i])) #timeline['month'][i] → Fetches the month (e.g., "January", "Feb", etc.).
    
    monthly_timeline['time'] = time
    return monthly_timeline

def daily_timeline(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap
