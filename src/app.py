import streamlit as st

from config import *

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
)

st.title(APP_NAME)

st.caption(f"Version {APP_VERSION}")

st.success("Application Started Successfully")

st.divider()

st.subheader("System Status")

status = {
    "Database": "Coming Soon",
    "Authentication": "Coming Soon",
    "Clients": "Coming Soon",
    "Exercise": "Coming Soon",
    "Health": "Coming Soon",
    "Nutrition": "Coming Soon",
    "Mental Wellness": "Coming Soon",
}

for module, state in status.items():
    st.write(f"**{module}** : {state}")

st.divider()

st.subheader("Development Progress")

st.progress(.05)

st.write("Phase 1 - Lesson 1 Complete")