import streamlit as st
import requests
from PIL import Image
import io

# 讀取你在 Streamlit 設定的 aq 密碼
HF_TOKEN = st.secrets["API_KEY"]

# 換成更穩定的語意與標籤辨識模型，不易斷線
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="家人專用營養分析器", page_icon="🍎")
st.title("🍎 家人專用：全功能營養分析器")
st.write("（目前使用 Hugging Face 穩定版驅動）")

# 支援後鏡頭拍照或相簿上傳
uploaded_file = st.file_uploader("請拍下食物或營養標示", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='圖片上傳成功，AI 正在分析中...', use_container_width=True)
    
    # 轉成二進位檔案直接傳送，避免 base64 轉換出錯
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    with st.spinner('AI 正在極速計算中...'):
        try:
            response = requests.post(API_URL, headers=headers, data=img_bytes)
            if response.status_code == 200:
                result = response.json()
                # 取得食物描述
                caption = result[0]['generated_text']
                
                st.subheader("📊 AI 辨識結果：")
                st.write(f"**偵測到食物外觀為**：{caption}")
                st.write("---")
                st.info("💡 提示：因為目前使用的是基礎版免費通道，若要更詳細的繁體中文營養與熱量表格，可以稍等伺服器離峰時段，或註冊免費的 Google Gemini 金鑰喔！")
            else:
                st.error("伺服器正忙碌中，請等 5 秒鐘再按一次！")
        except Exception as e:
            st.error("連線超時，請重新整理網頁再試一次。")
