# app.py
import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Health Assistant", page_icon="💊", layout="centered")

# --- Header ---
st.title("💊 Health Assistant App")
st.markdown(
    """
    Welcome! Enter your symptoms and get **basic health guidance**.  
    ⚠️ *For educational purposes only, not a substitute for medical advice.*
    """
)

# --- Sidebar: User Info ---
st.sidebar.header("Your Information")
age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
language = st.sidebar.selectbox("Language / भाषा / భాష", ["English", "Hindi", "Telugu"])

# --- Common symptoms list ---
symptom_options = {
    "English": ["Fever", "Cough", "Headache", "Cold", "Fatigue", "Nausea"],
    "Hindi": ["बुखार", "खांसी", "सिरदर्द", "सर्दी", "थकान", "मतली"],
    "Telugu": ["కుండు", "కఫం", "తలనొప్పి", "చలి", " అలసట", "వాంతులు"]
}[language]

# --- Symptoms Input ---
st.header({
    "English": "Select your symptoms",
    "Hindi": "अपने लक्षण चुनें",
    "Telugu": "మీ లక్షణాలను ఎంచుకోండి"
}[language])

symptoms_selected = st.multiselect(
    "Choose symptoms",
    options=symptom_options,
    default=[]
)

# --- Health Suggestions ---
suggestions = []

if st.button({
    "English": "Get Suggestions",
    "Hindi": "सुझाव प्राप्त करें",
    "Telugu": "సలహాలు పొందండి"
}[language]):
    
    if not symptoms_selected:
        st.warning({
            "English": "Please select at least one symptom!",
            "Hindi": "कृपया कम से कम एक लक्षण चुनें!",
            "Telugu": "దయచేసి కనీసం ఒక లక్షణం ఎంచుకోండి!"
        }[language])
    else:
        st.success({
            "English": "Here are some basic suggestions based on your symptoms:",
            "Hindi": "आपके लक्षणों के आधार पर कुछ बुनियादी सुझाव:",
            "Telugu": "మీ లక్షణాల ఆధారంగా కొన్ని ప్రాథమిక సలహాలు:"
        }[language])

        for s in symptoms_selected:
            s_lower = s.lower()
            if s_lower in ["fever", "बुखार", "కుండు"]:
                suggestions.append({
                    "English": "- Stay hydrated and rest. Consult a doctor if fever persists.",
                    "Hindi": "- पर्याप्त पानी पीएं और आराम करें। यदि बुखार बना रहे, तो डॉक्टर से संपर्क करें।",
                    "Telugu": "- ఎక్కువ నీరు తాగి విశ్రాంతి తీసుకోండి. జ్వరం కొనసాగితే డాక్టర్‌ను సంప్రదించండి."
                }[language])
            elif s_lower in ["cough", "खांसी", "కఫం"]:
                suggestions.append({
                    "English": "- Drink warm fluids. Consider consulting a doctor if persistent.",
                    "Hindi": "- गर्म तरल पदार्थ पिएं। लगातार होने पर डॉक्टर से संपर्क करें।",
                    "Telugu": "- వేడి ద్రావణాలు తాగండి. దీర్ఘకాలం కొనసాగితే డాక్టర్‌ను సంప్రదించండి."
                }[language])
            elif s_lower in ["headache", "सिरदर्द", "తలనొప్పి"]:
                suggestions.append({
                    "English": "- Rest in a dark room, stay hydrated. Seek medical advice if severe.",
                    "Hindi": "- अंधेरे कमरे में आराम करें, पर्याप्त पानी पिएं। गंभीर होने पर डॉक्टर से संपर्क करें।",
                    "Telugu": "- చీకటి గదిలో విశ్రాంతి తీసుకోండి, తగినంత నీరు తాగండి. తీవ్రమైనట్లయితే వైద్య సలహా తీసుకోండి."
                }[language])
            else:
                suggestions.append({
                    "English": "- General health advice: Eat well, sleep well, exercise regularly.",
                    "Hindi": "- सामान्य स्वास्थ्य सुझाव: अच्छा भोजन करें, पर्याप्त नींद लें, नियमित व्यायाम करें।",
                    "Telugu": "- సాధారణ ఆరోగ్య సలహా: బాగా తినండి, బాగా నిద్రపోండి, సాధారణ వ్యాయామం చేయండి."
                }[language])

        for s in suggestions:
            st.write(s)

        # --- Generate PDF Report ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Health Assistant Report", ln=True, align="C")
        pdf.set_font("Arial", '', 12)
        pdf.ln(5)
        pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.cell(0, 10, f"Age: {age}", ln=True)
        pdf.cell(0, 10, f"Gender: {gender}", ln=True)
        pdf.ln(5)
        pdf.cell(0, 10, "Symptoms Selected:", ln=True)
        for s in symptoms_selected:
            pdf.cell(0, 10, f"- {s}", ln=True)
        pdf.ln(5)
        pdf.cell(0, 10, "Suggestions:", ln=True)
        for s in suggestions:
            pdf.multi_cell(0, 10, s)
        pdf_file = "health_report.pdf"
        pdf.output(pdf_file)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label={
                    "English": "Download PDF Report",
                    "Hindi": "पीडीएफ रिपोर्ट डाउनलोड करें",
                    "Telugu": "PDF రిపోర్ట్ డౌన్లోడ్ చేయండి"
                }[language],
                data=f,
                file_name="health_report.pdf",
                mime="application/pdf"
            )

# --- Footer ---
st.markdown("---")
st.markdown({
    "English": "💡 *This app is for educational purposes only.*",
    "Hindi": "💡 *यह ऐप केवल शैक्षिक उद्देश्यों के लिए है।*",
    "Telugu": "💡 *ఈ యాప్ కేవలం విద్యా ఉద్దేశాలకోసం మాత్రమే.*"
}[language])