
import streamlit as st
import streamlit.components.v1 as components


# 1. إعدادات الصفحة وإخفاء العناصر
st.set_page_config(page_title="Burnout Insights - 2026", layout="wide", initial_sidebar_state="collapsed")


st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        .block-container {padding: 0px;}
    </style>
""", unsafe_allow_html=True)


# 2. منطق التنقل المحدث (Bridge)
# نعتمد على الرابط (URL) لتحديد الصفحة الحالية
query_params = st.query_params
current_page = query_params.get("page", "landing")


# دالة الرندرة مع كود سكريبت محدث للانتقال
def render_custom_html(html_body):
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet"/>
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet"/>
        <style>
            body {{ font-family: 'Inter', sans-serif; background-color: #f8f9fa; margin: 0; }}
            .editorial-gradient {{ background: linear-gradient(135deg, #00236f 0%, #1e3a8a 100%); }}
            .emerald-gold-gradient {{ background: linear-gradient(135deg, #006c4e 0%, #4a1d00 100%); }}
            .navy-silver-gradient {{ background: linear-gradient(135deg, #00236f 0%, #757682 100%); }}
            .card-hover {{ transition: all 0.3s ease; cursor: pointer; }}
            .card-hover:hover {{ transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
        </style>
        <script>
            // هذه الدالة هي اللي تخلي الزر يكلم ستريم ليت ويغير الصفحة
            function navigateTo(pageName) {{
                const url = new URL(window.parent.location.href);
                url.searchParams.set('page', pageName);
                window.parent.location.href = url.href;
            }}
        </script>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    components.html(full_html, height=1000, scrolling=True)


# --- محتوى الصفحات ---


if current_page == "landing":
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
    render_custom_html(landing_body)


elif current_page == "hr":
    hr_body = """
    <header class="w-full bg-white border-b p-6 flex items-center gap-4">
        <button onclick="navigateTo('landing')" class="text-blue-900 font-bold flex items-center">
            <span class="material-symbols-outlined">arrow_back</span> Back
        </button>
        <div class="font-bold">HR Executive Dashboard</div>
    </header>
    <main class="p-10 max-w-7xl mx-auto">
        <h1 class="text-4xl font-black mb-8">Institutional Health Metrics</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-white p-8 rounded-xl shadow-sm border-t-4 border-blue-900">
                <div class="text-slate-400 text-xs font-bold uppercase">Burnout Rate</div>
                <div class="text-4xl font-black mt-2 text-orange-600">32%</div>
            </div>
            <div class="bg-white p-8 rounded-xl shadow-sm border-t-4 border-emerald-600">
                <div class="text-slate-400 text-xs font-bold uppercase">Engagement</div>
                <div class="text-4xl font-black mt-2 text-emerald-600">84%</div>
            </div>
            <div class="bg-white p-8 rounded-xl shadow-sm border-t-4 border-red-600">
                <div class="text-slate-400 text-xs font-bold uppercase">Risk Level</div>
                <div class="text-4xl font-black mt-2 text-red-600">High</div>
            </div>
        </div>
    </main>
    """
    render_custom_html(hr_body)


elif current_page == "mgr":
    mgr_body = """
    <header class="w-full bg-white border-b p-6 flex items-center gap-4">
        <button onclick="navigateTo('landing')" class="text-blue-900 font-bold flex items-center">
            <span class="material-symbols-outlined">arrow_back</span> Back
        </button>
        <div class="font-bold">Manager Selection</div>
    </header>
    <main class="p-10 max-w-5xl mx-auto text-center">
        <h1 class="text-4xl font-black mb-12">Select Your Department</h1>
        <div class="grid grid-cols-2 gap-4">
            <div onclick="navigateTo('hr')" class="bg-white p-6 rounded-xl border card-hover font-bold text-blue-900">Engineering</div>
            <div onclick="navigateTo('hr')" class="bg-white p-6 rounded-xl border card-hover font-bold text-blue-900">Sales</div>
            <div onclick="navigateTo('hr')" class="bg-white p-6 rounded-xl border card-hover font-bold text-blue-900">Customer Success</div>
            <div onclick="navigateTo('hr')" class="bg-white p-6 rounded-xl border card-hover font-bold text-blue-900">HR Department</div>
        </div>
    </main>
    """
    render_custom_html(mgr_body)
