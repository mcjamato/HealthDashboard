from pathlib import Path
import streamlit as st
from config import APP_ICON,APP_NAME,APP_VERSION,CSS_PATH,DATABASE_PATH
from database.database import DatabaseManager
from pages.clients_page import ClientsPage
from pages.exercise_page import ExercisePage
from pages.health_page import HealthPage
from pages.mental_page import MentalWellnessPage
from pages.nutrition_page import NutritionPage
from repositories.client_repository import ClientRepository
from repositories.domain_repository import ExerciseRepository,HealthRepository,MentalWellnessRepository,NutritionRepository

st.set_page_config(page_title=APP_NAME,page_icon=APP_ICON,layout='wide',initial_sidebar_state='expanded')
if CSS_PATH.exists(): st.markdown(f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>",unsafe_allow_html=True)
db=DatabaseManager(DATABASE_PATH,Path(__file__).parent/'database'/'schema.sql'); db.initialize()
clients=ClientRepository(db); exercise=ExerciseRepository(db); health=HealthRepository(db); mental=MentalWellnessRepository(db); nutrition=NutritionRepository(db)
with st.sidebar:
    st.title('💙 Wellness'); st.caption(f'Phase 2 - v{APP_VERSION}')
    role='admin' if st.selectbox('Demo role',['Administrator','Client'])=='Administrator' else 'client'
    frame=clients.list_active(); client_id=None
    if not frame.empty:
        options={f"{r.first_name} {r.last_name} (#{r.id})":int(r.id) for r in frame.itertuples()}
        selected=st.selectbox('Selected client',list(options)); client_id=options[selected]
    page=st.radio('Navigation',['Dashboard','Clients','Exercise','Health','Mental Wellness','Nutrition'])
if page=='Dashboard':
    st.title(APP_NAME); st.caption('Phase 2: four wellness modules are active.'); st.progress(0.50)
    cols=st.columns(4)
    for col,label in zip(cols,['🏃 Exercise','❤️ Health','😊 Mental Wellness','🥗 Nutrition']): col.info(f'{label}\n\nActive')
    st.subheader('Next phase'); st.write('Cross-domain analytics, percent changes, and correlations.')
elif page=='Clients': ClientsPage(clients).render(role)
elif page=='Exercise': ExercisePage(exercise).render(client_id,role)
elif page=='Health': HealthPage(health).render(client_id,role)
elif page=='Mental Wellness': MentalWellnessPage(mental).render(client_id,role)
elif page=='Nutrition': NutritionPage(nutrition).render(client_id,role)
