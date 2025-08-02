from textblob import TextBlob
import streamlit as st

st.set_page_config(page_title="Sentiment Analyzer", layout="centered")

st.title("Sentiment Analyzer")
st.write("Enter a sentence and let me analyze its sentiments")

#User inputs
user_input = st.text_area("Type Something Here!")

if user_input:
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiment = "😊 Positive"
    elif polarity < 0:
        sentiment = "😔 Negative"
    else:
        sentiment = "😐 Neutral"

    #Sentiment Results
    st.subheader("Sentiments Results")
    st.success(sentiment)
    st.caption(f"Polarity Score: {polarity}")