import streamlit.components.v1 as components


def render(nav_script=""):
    hr_body = """
    <header class="w-full bg-white border-b p-6 flex items-center gap-4">
        <button onclick="navigateTo('landing')" class="text-blue-900 font-bold flex items-center gap-1">
            <span class="material-symbols-outlined">arrow_back</span> Back
        </button>
        <div class="font-bold text-slate-700">HR Executive Dashboard</div>
    </header>
    <main class="p-10 max-w-7xl mx-auto">
        <h1 class="text-4xl font-black mb-8">Institutional Health Metrics</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            <div class="bg-white p-8 rounded-xl shadow-sm border-t-4 border-blue-900">
                <div class="text-slate-400 text-xs font-bold uppercase">Burnout Rate</div>
                <div class="text-4xl font-black mt-2 text-orange-600">32%</div>
                <div class="text-slate-400 text-sm mt-1">+4% vs last quarter</div>
            </div>
            <div class="bg-white p-8 rounded-xl shadow-sm border-t-4 border-emerald-600">
                <div class="text-slate-400 text-xs font-bold uppercase">Engagement</div>
                <div class="text-4xl font-black mt-2 text-emerald-600">84%</div>
                <div class="text-slate-400 text-sm mt-1">-2% vs last quarter</div>
            </div>
            <div class="bg-white p-8 rounded-xl shadow-sm border-t-4 border-red-600">
                <div class="text-slate-400 text-xs font-bold uppercase">Risk Level</div>
                <div class="text-4xl font-black mt-2 text-red-600">High</div>
                <div class="text-slate-400 text-sm mt-1">Immediate action needed</div>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white p-8 rounded-xl shadow-sm">
                <h2 class="text-xl font-bold mb-4 text-slate-800">Department Breakdown</h2>
                <div class="space-y-3">
                    <div class="flex justify-between items-center">
                        <span class="text-slate-600">Engineering</span>
                        <div class="flex items-center gap-2">
                            <div class="w-32 bg-slate-100 rounded-full h-2">
                                <div class="bg-red-500 h-2 rounded-full" style="width:45%"></div>
                            </div>
                            <span class="text-sm font-bold text-red-600">45%</span>
                        </div>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-600">Sales</span>
                        <div class="flex items-center gap-2">
                            <div class="w-32 bg-slate-100 rounded-full h-2">
                                <div class="bg-orange-500 h-2 rounded-full" style="width:38%"></div>
                            </div>
                            <span class="text-sm font-bold text-orange-600">38%</span>
                        </div>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-600">Customer Success</span>
                        <div class="flex items-center gap-2">
                            <div class="w-32 bg-slate-100 rounded-full h-2">
                                <div class="bg-yellow-500 h-2 rounded-full" style="width:28%"></div>
                            </div>
                            <span class="text-sm font-bold text-yellow-600">28%</span>
                        </div>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-slate-600">HR Department</span>
                        <div class="flex items-center gap-2">
                            <div class="w-32 bg-slate-100 rounded-full h-2">
                                <div class="bg-emerald-500 h-2 rounded-full" style="width:18%"></div>
                            </div>
                            <span class="text-sm font-bold text-emerald-600">18%</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-white p-8 rounded-xl shadow-sm">
                <h2 class="text-xl font-bold mb-4 text-slate-800">Recommended Actions</h2>
                <ul class="space-y-3">
                    <li class="flex gap-3 items-start">
                        <span class="material-symbols-outlined text-red-500 mt-0.5" style="font-size:20px">priority_high</span>
                        <span class="text-slate-600 text-sm">Schedule 1:1 check-ins for Engineering team leads</span>
                    </li>
                    <li class="flex gap-3 items-start">
                        <span class="material-symbols-outlined text-orange-500 mt-0.5" style="font-size:20px">notifications</span>
                        <span class="text-slate-600 text-sm">Launch Sales wellness program this month</span>
                    </li>
                    <li class="flex gap-3 items-start">
                        <span class="material-symbols-outlined text-blue-500 mt-0.5" style="font-size:20px">calendar_month</span>
                        <span class="text-slate-600 text-sm">Conduct org-wide pulse survey next week</span>
                    </li>
                </ul>
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
        </style>
    </head><body>{nav_script}{hr_body}</body></html>
    """
    components.html(full_html, height=1000, scrolling=True)