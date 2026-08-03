from datetime import date
import plotly.express as px
import streamlit as st
from models.domain_models import MentalWellnessRecord
from pages.shared import PageSupport
from services.analytics_service import AnalyticsService

class MentalWellnessPage:
    def __init__(self, repository): self.repository=repository; self.analytics=AnalyticsService()
    def render(self, client_id, role):
        st.title('😊 Mental Wellness')
        if not PageSupport.require_client(client_id): return

        with st.form('mental_form', clear_on_submit=True):
            recorded=st.date_input('Date',date.today()); mood=st.slider('Mood',1,10,7); stress=st.slider('Stress',1,10,4)
            energy=st.slider('Energy',1,10,7); focus=st.slider('Focus',1,10,7); meditation=st.number_input('Meditation (minutes)',0,600,0)
            journal=st.text_area('Journal entry'); submitted=st.form_submit_button('Save wellness record',use_container_width=True)
        if submitted:
            self.repository.create(MentalWellnessRecord(int(client_id),recorded,mood,stress,energy,focus,meditation,journal).to_dict())
            st.success('Mental wellness record saved.'); st.rerun()

        frame=self.repository.list_for_client(int(client_id))
        c1,c2,c3=st.columns(3)
        c1.metric('Average mood',f"{self.analytics.mean(frame,'mood_score') or 0:.1f}/10"); c2.metric('Average stress',f"{self.analytics.mean(frame,'stress_score') or 0:.1f}/10"); c3.metric('Average energy',f"{self.analytics.mean(frame,'energy_score') or 0:.1f}/10")
        if not frame.empty:
            chart=self.analytics.prepare_chronological(frame)
            st.plotly_chart(px.line(chart,x='recorded_on',y=['mood_score','stress_score','energy_score','focus_score'],markers=True,title='Mental wellness trends'),use_container_width=True)
        PageSupport.show_history(frame, 'Mental Wellness history')
        if role=='admin': PageSupport.admin_deactivate(self.repository,frame,'mental')
