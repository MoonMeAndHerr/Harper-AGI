import streamlit as st
from utils.preprocess import load_text_from_file
from utils.ai_engine import llm_generate
from models.cnn_model import ensure_model, predict_from_pil
from PIL import Image

def run_meeting():
    st.header('Meeting Advisor')
    st.write('Upload meeting minutes (txt, pdf, docx) and Harper will summarize and flag risks.')
    uploaded = st.file_uploader('Upload meeting file', type=['txt','pdf','docx'])
    if not uploaded:
        st.info('Please upload a file to analyze.')
        st.stop()
    text = load_text_from_file(uploaded)
    st.subheader('Extracted Text (first 800 chars)')
    st.write(text[:800] + ('...' if len(text)>800 else ''))
    prompt = f"Summarize the meeting minutes and list 5 action items and 3 possible risks that could lead to project failure. Meeting text:\n{text[:4000]}"
    summary = llm_generate(prompt, max_tokens=300)
    st.subheader('Summary & Actionable Items')
    st.write(summary)
    st.markdown('Optional: Upload an image (photo of whiteboard / slide) to evaluate clarity')
    img = st.file_uploader('Upload image (jpg/png) for visual clarity', type=['png','jpg','jpeg'], key='meeting_img')
    if img:
        pil = Image.open(img).convert('RGB')
        feat_ext, reg, scaler = ensure_model()
        score, _ = predict_from_pil(pil, feat_ext, reg, scaler)
        st.image(pil, caption=f'Visual clarity score: {score:.3f}', use_column_width=True)
        expl = llm_generate(f'This image received a clarity/engagement score of {score:.3f}. Suggest 3 ways to improve the visual communication in meeting slides or whiteboard photos.', max_tokens=150)
        st.write(expl)
