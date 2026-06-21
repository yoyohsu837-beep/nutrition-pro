import streamlit as st
import google.generativeai as genai
from PIL import Image

# 讀取設定好的金鑰
genai.configure(api_key=st.secrets["API_KEY"])

st.title("🍎 家人專用：營養分析器")
uploaded_file = st.camera_input("請拍下食物營養標示")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='正在分析中...')
    model = genai.GenerativeModel('gemini-1.5-flash')

    with st.spinner('AI 正在計算...'):
        res = model.generate_content(["請列出食物名稱、蛋白質與熱量，簡單回答。", image])
        st.write(res.text)
