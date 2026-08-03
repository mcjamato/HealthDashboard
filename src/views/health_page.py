from datetime import date
import plotly.express as px
import streamlit as st
from models.domain_models import HealthRecord
from views.shared import PageSupport
from services.analytics_service import AnalyticsService

class HealthPage:
    def __init__(self, repository): self.repository=repository; self.analytics=AnalyticsService()
    def render(self, client_id, role):
        st.title('❤️ Health')
        if not PageSupport.require_client(client_id): return

        with st.form('health_form', clear_on_submit=True):
            recorded=st.date_input('Date',date.today()); weight=st.number_input('Weight (kg)',0.0,500.0,0.0,step=0.1)
            sleep=st.number_input('Sleep (hours)',0.0,24.0,8.0,step=0.25); quality=st.slider('Sleep quality',1,10,7)
            heart=st.number_input('Resting heart rate',0,250,0); a,b=st.columns(2); sys=a.number_input('Systolic BP',0,300,0); dia=b.number_input('Diastolic BP',0,200,0)
            water=st.number_input('Water (liters)',0.0,20.0,0.0,step=0.25); notes=st.text_area('Notes')
            submitted=st.form_submit_button('Save health record',use_container_width=True)
        if submitted:
            self.repository.create(HealthRecord(int(client_id),recorded,weight or None,sleep or None,quality,heart or None,sys or None,dia or None,water,notes).to_dict())
            st.success('Health record saved.'); st.rerun()

        frame=self.repository.list_for_client(int(client_id))
        c1,c2,c3=st.columns(3)
        c1.metric('Latest weight',f"{self.analytics.latest_value(frame,'weight_kg') or 0:.1f} kg"); c2.metric('Average sleep',f"{self.analytics.mean(frame,'sleep_hours') or 0:.1f} hr"); c3.metric('Sleep quality',f"{self.analytics.mean(frame,'sleep_quality') or 0:.1f}/10")
        if not frame.empty:
            chart=self.analytics.prepare_chronological(frame)
            st.plotly_chart(px.line(chart,x='recorded_on',y=['weight_kg','sleep_hours'],markers=True,title='Health trends'),use_container_width=True)
            st.plotly_chart(px.box(chart,y='sleep_hours',points='all',title='Sleep distribution'),use_container_width=True)
        PageSupport.show_history(frame, 'Health history')
        if role=='admin': PageSupport.admin_deactivate(self.repository,frame,'health')
