from datetime import date
import streamlit as st

class ClientsPage:
    def __init__(self, repository): self.repository = repository
    def render(self, role):
        st.title('👥 Clients')
        if role != 'admin': st.info('Client management is available to administrators.'); return
        with st.form('create_client', clear_on_submit=True):
            a,b=st.columns(2); first=a.text_input('First name'); last=b.text_input('Last name')
            email=st.text_input('Email'); birth=st.date_input('Birth date', date(2000,1,1), min_value=date(1900,1,1), max_value=date.today())
            submitted=st.form_submit_button('Create client', use_container_width=True)
        if submitted:
            if not first.strip() or not last.strip(): st.error('First and last name are required.')
            else:
                try: self.repository.create(first,last,email,birth.isoformat()); st.success('Client created.'); st.rerun()
                except Exception as exc: st.error(f'Client could not be created: {exc}')
        frame=self.repository.list_active(); st.subheader('Active clients'); st.dataframe(frame,use_container_width=True,hide_index=True)
        if not frame.empty:
            with st.expander('Deactivate a client'):
                cid=st.selectbox('Client',frame['id'].astype(int).tolist())
                if st.button('Deactivate client'): self.repository.deactivate(int(cid)); st.rerun()
