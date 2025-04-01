import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s' # r isliye use kr rhe use raw string bnane ke liye vrna python \d and \w as escape sequences in strings
    messages = re.split(pattern, data)[1:] # pehli line bhi aa rhi thi isliye use hatane ke liye ye [1:] lagaya hta ke dekh lo
    dates = re.findall(pattern, data)
    
    print("Messages Length:", len(messages))
    print("Dates Length:", len(dates))

    if len(messages) != len(dates):
        print("Warning: Messages and Dates count do not match!")
        return pd.DataFrame()

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ', errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True) # inplace=true ni likhogi toh change ni krega
    
    users = []
    messages = []
    
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['min'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df['hour']:
        if pd.isna(hour):
            period.append("Unknown")
        elif hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    
    df['period'] = period
    return df
