import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer by Divyansh Pal")  # to create side bar
# run krne ka command streamlit run app.py
# to go to app.py type cd whatsapp in terminal

# now to upload file
uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")  # convert into string
    # st.text(data)  # to print this text data
    df = preprocessor.preprocess(data)  # preprocessor ek library bnYI JHA preprocess func present h vha se call kr liya

    # st.dataframe(df)  # function to display dataframe

    # fetch unique users
    user_list = df['user'].unique().tolist()
    
    # group notification hta rhe
    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()  # list sort kr rhe
    user_list.insert(0, "overall")  # 0th pos pe overall add kr rhe
    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)  # .selectbox(label, options): Creates a dropdown menu (select box)
    
    print(user_list)  # Debugging

    # adding button
    if st.sidebar.button("show analysis"):  # when button click it will run
        # stats area
        st.title("top statistics")

        num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)  # st.columns(4): Creates four columns in the Streamlit layout.

        with col1:
            st.header("total messages")  # Displays a header text in first col
            st.title(num_messages)
        with col2:
            st.header("total words")
            st.title(num_words)
        with col3:
            st.header("total media")
            st.title(num_media)
        with col4:
            st.header("total links")
            st.title(num_links)

        # monthly timeline
        st.title("monthly timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # daily timeline
        st.title("daily timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color="pink")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # activity map
        st.title('activity map')
        col1, col2 = st.columns(2)
        with col1:
            st.header("most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        st.title("weekly activity map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group (group level)
        if selected_user == "overall":
            st.title("most busy users")
            x, new_df = helper.most_busy_users(df)  # yha se dataframe aa gya ki unique users aur kitte mssgs h in descending order
            fig, ax = plt.subplots()  # syntax hota [plt.subplot(rows, columns, index)]
            col1, col2 = st.columns(2)  # poore area ko 2 part me divide kr rhe

            with col1:
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)  # to show df

        # wordcloud
        st.title("wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)  # imshow is for image display
        st.pyplot(fig)

        # most common words
        st.title("most common words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])  # 0 or 1 isliye kyuki dataframe me columns unnamed h
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # emoji analysis
        st.title("emoji analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%0.2f")  # autopct="%0.2f" shows percentage with 2 decimal places
            st.pyplot(fig)

        # time based analysis
