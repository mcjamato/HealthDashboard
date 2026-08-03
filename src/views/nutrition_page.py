from datetime import date
import plotly.express as px
import streamlit as st
from models.domain_models import NutritionRecord
from views.shared import PageSupport
from services.analytics_service import AnalyticsService

class NutritionPage:
    def __init__(self, repository): self.repository=repository; self.analytics=AnalyticsService()
    def render(self, client_id, role):
        st.title('🥗 Nutrition')
        if not PageSupport.require_client(client_id): return

        with st.form('nutrition_form', clear_on_submit=True):
            recorded=st.date_input('Date',date.today()); meal=st.selectbox('Meal type',['Breakfast','Lunch','Dinner','Snack','Daily total'])
            calories=st.number_input('Calories',0.0,10000.0,0.0,step=10.0); protein=st.number_input('Protein (g)',0.0,1000.0,0.0)
            carbs=st.number_input('Carbohydrates (g)',0.0,2000.0,0.0); fat=st.number_input('Fat (g)',0.0,1000.0,0.0)
            fiber=st.number_input('Fiber (g)',0.0,500.0,0.0); water=st.number_input('Water (liters)',0.0,20.0,0.0,step=0.25)
            notes=st.text_area('Notes'); submitted=st.form_submit_button('Save nutrition record',use_container_width=True)
        if submitted:
            self.repository.create(NutritionRecord(int(client_id),recorded,meal,calories,protein,carbs,fat,fiber,water,notes).to_dict())
            st.success('Nutrition record saved.'); st.rerun()

        frame=self.repository.list_for_client(int(client_id))
        c1,c2,c3=st.columns(3)
        c1.metric('Entries',len(frame)); c2.metric('Average calories',f"{self.analytics.mean(frame,'calories') or 0:.0f}"); c3.metric('Average protein',f"{self.analytics.mean(frame,'protein_g') or 0:.1f} g")
        if not frame.empty:
            chart=self.analytics.prepare_chronological(frame)
            st.plotly_chart(px.line(chart,x='recorded_on',y='calories',markers=True,title='Calorie trend'),use_container_width=True)
            macro=chart[['protein_g','carbs_g','fat_g']].sum().reset_index(); macro.columns=['nutrient','grams']
            st.plotly_chart(px.pie(macro,names='nutrient',values='grams',title='Recorded macronutrient mix'),use_container_width=True)
        PageSupport.show_history(frame, 'Nutrition history')
        if role=='admin': PageSupport.admin_deactivate(self.repository,frame,'nutrition')
