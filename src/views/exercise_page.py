from datetime import date
import plotly.express as px
import streamlit as st
from models.domain_models import ExerciseRecord
from views.shared import PageSupport
from services.analytics_service import AnalyticsService

class ExercisePage:
    def __init__(self, repository): self.repository=repository; self.analytics=AnalyticsService()
    def render(self, client_id, role):
        st.title('🏃 Exercise')
        if not PageSupport.require_client(client_id): return

        with st.form('exercise_form', clear_on_submit=True):
            recorded=st.date_input('Date',date.today()); kind=st.selectbox('Exercise type',['Walking','Running','Cycling','Strength','Sports','Other'])
            duration=st.number_input('Duration (minutes)',0,600,30); intensity=st.selectbox('Intensity',['Low','Moderate','High'])
            steps=st.number_input('Steps',0,100000,0); distance=st.number_input('Distance (km)',0.0,500.0,0.0,step=0.1)
            calories=st.number_input('Calories burned',0.0,5000.0,0.0,step=10.0); notes=st.text_area('Notes')
            submitted=st.form_submit_button('Save exercise record',use_container_width=True)
        if submitted:
            self.repository.create(ExerciseRecord(int(client_id),recorded,kind,duration,intensity,steps,distance,calories,notes).to_dict())
            st.success('Exercise record saved.'); st.rerun()

        frame=self.repository.list_for_client(int(client_id))
        c1,c2,c3=st.columns(3)
        c1.metric('Records',len(frame)); c2.metric('Average duration',f"{self.analytics.mean(frame,'duration_minutes') or 0:.1f} min"); c3.metric('Total calories',f"{frame['calories_burned'].sum() if not frame.empty else 0:.0f}")
        if not frame.empty:
            chart=self.analytics.prepare_chronological(frame)
            st.plotly_chart(px.line(chart,x='recorded_on',y='duration_minutes',markers=True,title='Exercise duration trend'),use_container_width=True)
            st.plotly_chart(px.bar(chart,x='exercise_type',y='duration_minutes',title='Minutes by exercise entry'),use_container_width=True)
        PageSupport.show_history(frame, 'Exercise history')
        if role=='admin': PageSupport.admin_deactivate(self.repository,frame,'exercise')
