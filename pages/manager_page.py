import streamlit.components.v1 as components


def render(nav_script=""):
    mgr_body = """
    <header class="w-full bg-white border-b p-6 flex items-center gap-4">
        <button onclick="navigateTo('landing')" class="text-blue-900 font-bold flex items-center gap-1">
            <span class="material-symbols-outlined">arrow_back</span> Back
        </button>
        <div class="font-bold text-slate-700">Manager Selection</div>
    </header>
    <main class="p-10 max-w-5xl mx-auto text-center">
        <h1 class="text-4xl font-black mb-4 text-slate-900">Select Your Department</h1>
        <p class="text-slate-500 mb-12">Choose a department to view team-level burnout metrics and intervention tools.</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div onclick="navigateTo('hr')" class="bg-white p-8 rounded-2xl border card-hover text-left group">
                <div class="w-12 h-12 bg-blue-50 text-blue-700 rounded-xl flex items-center justify-center mb-4">
                    <span class="material-symbols-outlined" style="font-size:24px">terminal</span>
                </div>
                <div class="font-bold text-xl text-blue-900 mb-1">Engineering</div>
                <div class="text-slate-400 text-sm">42 team members · High risk</div>
                <div class="mt-4 text-xs font-bold text-red-500 uppercase">⚠ Attention needed</div>
            </div>
            <div onclick="navigateTo('hr')" class="bg-white p-8 rounded-2xl border card-hover text-left group">
                <div class="w-12 h-12 bg-emerald-50 text-emerald-700 rounded-xl flex items-center justify-center mb-4">
                    <span class="material-symbols-outlined" style="font-size:24px">trending_up</span>
                </div>
                <div class="font-bold text-xl text-blue-900 mb-1">Sales</div>
                <div class="text-slate-400 text-sm">28 team members · Medium risk</div>
                <div class="mt-4 text-xs font-bold text-orange-500 uppercase">⚡ Monitor closely</div>
            </div>
            <div onclick="navigateTo('hr')" class="bg-white p-8 rounded-2xl border card-hover text-left group">
                <div class="w-12 h-12 bg-purple-50 text-purple-700 rounded-xl flex items-center justify-center mb-4">
                    <span class="material-symbols-outlined" style="font-size:24px">support_agent</span>
                </div>
                <div class="font-bold text-xl text-blue-900 mb-1">Customer Success</div>
                <div class="text-slate-400 text-sm">19 team members · Low risk</div>
                <div class="mt-4 text-xs font-bold text-emerald-500 uppercase">✓ On track</div>
            </div>
            <div onclick="navigateTo('hr')" class="bg-white p-8 rounded-2xl border card-hover text-left group">
                <div class="w-12 h-12 bg-slate-50 text-slate-700 rounded-xl flex items-center justify-center mb-4">
                    <span class="material-symbols-outlined" style="font-size:24px">people</span>
                </div>
                <div class="font-bold text-xl text-blue-900 mb-1">HR Department</div>
                <div class="text-slate-400 text-sm">11 team members · Low risk</div>
                <div class="mt-4 text-xs font-bold text-emerald-500 uppercase">✓ On track</div>
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
            .card-hover {{ transition: all 0.3s ease; cursor: pointer; }}
            .card-hover:hover {{ transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.07); }}
        </style>
    </head><body>{nav_script}{mgr_body}</body></html>
    """
    components.html(full_html, height=1000, scrolling=True)