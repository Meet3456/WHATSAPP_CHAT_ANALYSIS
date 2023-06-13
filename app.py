import streamlit as st
import preprocessor,functions
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

upload_file = st.sidebar.file_uploader("Choose a File for Analysis:")
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # FETCH UNIQUE USERS:
    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("SHOW ANALYSIS WITH RESPECT TO:",user_list)

    if st.sidebar.button("Show Analysis"):
        
        # STATS AREA:
        num_messages,words,num_media_messages = functions.fetch_stats(selected_user,df)
        col1,col2,col3 = st.columns(3)

        with col1:
            st.header("Total Messagaes")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Shared")
            st.title(num_media_messages)


        # MONTHLY TIMELINE:

        st.title("Monthly Timeline of Users:")
        timeline = functions.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)       

        # DAILY TIMELINE:

        st.title("Daily Timeline of Users:")
        timeline = functions.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['only_date'],timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # ACTIVITY MAP

        st.title("Activity Map")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day of the Week")
            busy_day = functions.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_day = functions.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='orange')
            st.pyplot(fig)

        # ACTIVITY HEATMAP:
        st.title("Weekly Activity MAP")
        heatmap = functions.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(heatmap,annot=True,linewidths=1,linecolor='black',cmap='PuOr')
        st.pyplot(fig)



        # finding the busiest users in the group(Group level)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = functions.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        # WordCloud
        st.title("Wordcloud")
        df_wc = functions.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words
        most_common_df = functions.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)


        # emoji analysis
        emoji_df = functions.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct="%0.2f")
            st.pyplot(fig)
