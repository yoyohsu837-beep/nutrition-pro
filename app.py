import streamlit as st
import google.generativeai as genai
from PIL import Image

# 讀取你在 Streamlit Secrets 設定的金鑰
genai.configure(api_key=st.secrets["API_KEY"])

st.set_page_config(page_title="家人專用營養分析器", page_icon="🍎")
st.title("🍎 家人專用：全功能營養分析器")
st.write("（支援：便利商店包裝、家常菜、現煮料理、各類食物）")

# 使用檔案上傳器，讓安卓手機點擊時能自由選擇「後置相機拍照」或「相簿上傳」
uploaded_file = st.file_uploader("請拍下食物或營養標示", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='圖片上傳成功，AI 正在辨識中...', use_container_width=True)
    
    # 這裡使用 Google 最穩定的視覺模型
    model = genai.GenerativeModel('gemini-1.5-flash')
    
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
    
    with st.spinner('AI 正在計算中...請稍候...'):
        try:
            res = model.generate_content([prompt_text, image])
            st.subheader("📊 AI 營養分析結果：")
            st.write(res.text)
        except Exception as e:
            st.error("金鑰驗證失敗，請檢查 Streamlit Cloud 的 Secrets 是否輸入正確。")
