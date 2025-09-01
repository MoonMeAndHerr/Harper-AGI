import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.ai_engine import llm_generate, mock_generate_post_ideas
from models.cnn_model import ensure_model, predict_from_pil
from PIL import Image

def run_promotional():
    st.header("Promotional Content Advisor")
    with st.form("promo_form"):
        company = st.text_input("Company Name", value="Skadi Cloud")
        audience = st.text_input("Target Audience", value="SME founders in SE Asia")
        content_type = st.selectbox("Content Type", ["Image","Video","Carousel","Text"])
        goals = st.multiselect("Goals", ["Engagement","Leads","Awareness","Retention"], default=["Engagement"])
        platform = st.selectbox("Platform", ["Instagram","LinkedIn","Facebook","TikTok","X"])
        budget = st.number_input("Budget (MYR)", min_value=0.0, value=1000.0, step=50.0)
        explanation = st.text_area("Short Explanation / Notes", value="New product launch in Q4.")
        submitted = st.form_submit_button("Submit")
    if not submitted:
        st.info("Please fill the form and click Submit to proceed.")
        st.stop()
    st.success("Inputs received — generating ideas and recommendations...")
    tabs = st.tabs(["Ideas","Budget Distribution","Engagement Prediction"])
    with tabs[0]:
        st.subheader("AI + CNN Generated Ideas")
        prompt = f"Generate 3 social media post ideas for {company} targeting {audience}. Product type: {content_type}. Goals: {', '.join(goals)}. Platform: {platform}. Notes: {explanation}."
        ideas = llm_generate(prompt) if False==False else mock_generate_post_ideas(company,audience,content_type,goals,platform,explanation)
        if isinstance(ideas, str):
            st.write(ideas)
        else:
            for it in ideas:
                st.markdown(f"**{it['title']}**")
                st.write(it['caption'])
                st.code(it['hashtags'])
    with tabs[1]:
        st.subheader("Budget Distribution")
        df = pd.DataFrame([{"Channel":"Paid Ads","Amount": budget*0.7},{"Channel":"Organic","Amount":budget*0.25},{"Channel":"Testing","Amount":budget*0.05}])
        st.table(df)
    with tabs[2]:
        st.subheader("Engagement Prediction by Hour")
        bench = pd.read_csv('sample_data/engagement_benchmarks.csv')
        dfp = bench[bench['platform']==platform].groupby('hour', as_index=False)['score'].mean().sort_values('hour')
        st.line_chart(dfp.set_index('hour')['score'])
        st.markdown("### Optional: Upload a creative to evaluate")
        up = st.file_uploader("Upload image (jpg/png)", type=['png','jpg','jpeg'])
        if up is not None:
            img = Image.open(up).convert('RGB')
            st.image(img, caption="Uploaded creative", use_column_width=True)
            feat_ext, reg, scaler = ensure_model()
            score, _ = predict_from_pil(img, feat_ext, reg, scaler)
            st.metric("Predicted engagement score", f"{score:.4f}")
            best = dfp.loc[dfp['score'].idxmax()]
            st.info(f"Suggested time to post on {platform}: {int(best['hour'])}:00 (bench score {best['score']:.3f})")
