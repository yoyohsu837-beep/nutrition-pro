import streamlit as st
import requests
from PIL import Image
import io
import base64

# 讀取你在 Streamlit 設定的 AQ 密碼
HF_TOKEN = st.secrets["API_KEY"]

# 使用你這把鑰匙專用的 AI 模型
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-11b-Vision-Instruct"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.title("🍎 家人專用：營養分析器")
uploaded_file = st.camera_input("請拍下食物營養標示")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='正在分析中...')
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    payload = {
        "inputs": f"data:image/jpeg;base64,{img_str}",
        "parameters": {"prompt": "請用繁體中文列出這張照片中的食物名稱、蛋白質與熱量，格式要簡單。"}
    }
    
    with st.spinner('AI 正在計算...'):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            st.subheader("分析結果：")
            st.write(response.json()[0]['generated_text'])
        else:
            st.error("AI 正在熱機中，請等一下再試拍一次！")
