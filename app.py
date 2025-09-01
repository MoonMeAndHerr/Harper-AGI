import streamlit as st
from PIL import Image
import os
from services import promotional, market, meeting

st.set_page_config(page_title='Harper AI v3', layout='wide', page_icon='🤖')
st.image('assets/logo.png', width=240)
st.title('Harper AI  — An All-Rounder Assistant')
st.write('Welcome! Choose a service and follow the guided steps. The app enforces a linear flow: you must submit required inputs to proceed to analysis.')

if 'service_selected' not in st.session_state:
    st.session_state.service_selected = None

service = st.selectbox('Select a service', ['-- Select --','Promotional Content Advisor','Market Prediction Advisor','Meeting Advisor'])
if st.button('Start'):
    if service == '-- Select --':
        st.warning('Choose a service first.')
    else:
        st.session_state.service_selected = service

if not st.session_state.service_selected:
    st.info('Select a service and click Start to begin.')
    st.stop()

st.success(f'Service chosen: {st.session_state.service_selected}')

if st.session_state.service_selected == 'Promotional Content Advisor':
    promotional.run_promotional()
elif st.session_state.service_selected == 'Market Prediction Advisor':
    market.run_market()
elif st.session_state.service_selected == 'Meeting Advisor':
    meeting.run_meeting()
else:
    st.error('Unknown service selected.')
