import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Burnout Insights - 2026", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding: 0px;}
        div.stButton > button { display: none; }
    </style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "landing"

# Hidden Streamlit buttons triggered by JS via click()
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("go_landing", key="btn_landing"):
        st.session_state.page = "landing"
        st.rerun()
with col2:
    if st.button("go_hr", key="btn_hr"):
        st.session_state.page = "hr"
        st.rerun()
with col3:
    if st.button("go_mgr", key="btn_mgr"):
        st.session_state.page = "mgr"
        st.rerun()

NAV_SCRIPT = """
<script>
function navigateTo(pageName) {
    const buttons = window.parent.document.querySelectorAll('button');
    for (const btn of buttons) {
        if (btn.innerText.trim() === 'go_' + pageName) {
            btn.click();
            break;
        }
    }
}
</script>
"""

if st.session_state.page == "hr":
    import pages.HR_page as hr_dashboard
    hr_dashboard.render(NAV_SCRIPT)
elif st.session_state.page == "mgr":
    import pages.manager_page as mgr_selection
    mgr_selection.render(NAV_SCRIPT)
else:
    def render_landing():
        landing_body = """
        <header class="w-full bg-white border-b p-6 flex justify-between items-center">
            <div class="text-xl font-bold text-blue-900">Burnout Insights - 2026</div>
        </header>
        <main class="max-w-6xl mx-auto py-20 px-6 text-center">
            <h1 class="text-6xl font-black text-slate-900 mb-16">Welcome to <span class="text-blue-900 italic">Burnout Prediction</span></h1>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
                <div class="card-hover bg-white rounded-2xl border p-10 text-left" onclick="navigateTo('hr')">
                    <div class="w-16 h-16 bg-emerald-50 text-emerald-700 rounded-xl flex items-center justify-center mb-6">
                        <span class="material-symbols-outlined" style="font-size:32px">insights</span>
                    </div>
                    <h2 class="text-3xl font-bold mb-4">HR Executive View</h2>
                    <p class="text-slate-500 mb-8">Strategic health metrics for the whole organization.</p>
                    <div class="flex justify-between items-center pt-4 border-t">
                        <span class="text-xs font-bold text-emerald-700 uppercase">Strategic</span>
                        <div class="h-10 w-10 emerald-gold-gradient rounded-full flex items-center justify-center text-white">→</div>
                    </div>
                </div>
                <div class="card-hover bg-white rounded-2xl border p-10 text-left" onclick="navigateTo('mgr')">
                    <div class="w-16 h-16 bg-blue-50 text-blue-700 rounded-xl flex items-center justify-center mb-6">
                        <span class="material-symbols-outlined" style="font-size:32px">groups</span>
                    </div>
                    <h2 class="text-3xl font-bold mb-4">Manager View</h2>
                    <p class="text-slate-500 mb-8">Team-level tools and intervention metrics.</p>
                    <div class="flex justify-between items-center pt-4 border-t">
                        <span class="text-xs font-bold text-blue-700 uppercase">SELECT DEPARTMENT</span>
                        <div class="h-10 w-10 navy-silver-gradient rounded-full flex items-center justify-center text-white">→</div>
                    </div>
                </div>
            </div>
        </main>
        """
        full_html = f"""
        <!DOCTYPE html><html><head>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet"/>
            <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet"/>
            <style>
                body {{ font-family: 'Inter', sans-serif; background-color: #f8f9fa; margin: 0; }}
                .emerald-gold-gradient {{ background: linear-gradient(135deg, #006c4e 0%, #4a1d00 100%); }}
                .navy-silver-gradient {{ background: linear-gradient(135deg, #00236f 0%, #757682 100%); }}
                .card-hover {{ transition: all 0.3s ease; cursor: pointer; }}
                .card-hover:hover {{ transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
            </style>
        </head><body>{NAV_SCRIPT}{landing_body}</body></html>
        """
        components.html(full_html, height=1000, scrolling=True)

    render_landing()
