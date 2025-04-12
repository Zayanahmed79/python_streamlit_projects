import streamlit as st

st.set_page_config(page_title="growth mindset", page_icon="✦")
st.title("🌱 Growth Mindset")

st.header("Welcom to Your Growth Journey")
st.write("Embarce challanges, learn from mistakes, and unlock full potential. This AI-powered app helps you built a growth mindset with reflection, challenges, and achivements! ✨")

st.header("💡 Today's Growth Mindset Quote")
st.write("We can't become what we need to be by remaining what we are. —Oprah Winfrey")

st.header("What's Your Chanllenge Today?")
user_input = st.text_input("Describe a challenge you are facing")

if user_input:
    st.success(f"You are facing: {user_input}. Keep pushing forward towards goal!")
else:
    st.warning("Tell us about your challenge to get started!")

st.header("Reflection on Your Learning")
reflection = st.text_area("Write your reflections here:")

if reflection:
    st.success(f"🌟 Greate Insight! Your reflection: {reflection}")
else:
    st.info("Reflection on past experience help you grow! Share your difficulties")

st.header("🏆 Celebrate Your Wins!")
achivments = st.text_input("Share something you have recently accomplished:")

if achivments:
    st.success(f"🎉 Amazing! you achived: {achivments}")
else:
    st.info("Big or small, every achivement counts! Share one now!")

st.write("_ _ _")
st.write("Keep belive in yourself. Growth is a journey, not a destination! ✨")
st.write("© Created by Shafique Ur Rehman")