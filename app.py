import streamlit as st
import requests
from PIL import Image
import io
import base64

# 讀取你在 Streamlit 設定的 AQ 密碼
HF_TOKEN = st.secrets["API_KEY"]

# 使用強大的視覺 AI 模型
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-11b-Vision-Instruct"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="家人專用營養分析器", page_icon="🍎")
st.title("🍎 家人專用：全功能營養分析器")
st.write("（支援：便利商店包裝、家常菜、現煮料理、各類食物）")

# 改用內建檔案上傳器，這樣在安卓手機上點擊時，會彈出「拍照（可選後鏡頭）」或「從相簿選擇」
uploaded_file = st.file_uploader("請拍下食物或營養標示", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='圖片上傳成功，AI 正在辨識中...', use_container_width=True)
    
    # 圖片轉 base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # 萬物皆可辨識的超強 AI 指令
    prompt_text = (
        "你是一個資深的營養分析師。請分析這張照片，辨識出裡面的食物名稱。 "
        "如果是包裝食品，請讀出營養標示；如果是自己煮的家常菜、外食、或是各類料理，"
        "請根據外觀分量，合理預估這份食物的蛋白質含量（公克）與熱量（kcal）。 "
        "請務必用繁體中文回答，格式要極度簡潔明瞭，例如：\n"
        "- 食物名稱：XXXX\n"
        "- 蛋白質：約 XX 公克\n"
        "- 熱量：約 XX kcal\n"
        "- 營養師小叮嚀：XXXX"
    )
    
    payload = {
        "inputs": f"data:image/jpeg;base64,{img_str}",
        "parameters": {"prompt": prompt_text}
    }
    
    with st.spinner('AI 正在計算中...請稍候...'):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            st.subheader("📊 AI 營養分析結果：")
            st.write(response.json()[0]['generated_text'])
        else:
            st.error("AI 正在熱機中，請等個 10 秒鐘，再重新上傳照片試一次！")
