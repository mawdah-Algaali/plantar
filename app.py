import streamlit as st
import pandas as pd

st.title("🩺 Plantar Fasciitis - Clinical Decision Support System")
st.write("Automated patient data retrieval and intelligent treatment planning.")

@st.cache_data
def load_data():
    return pd.read_excel("Plantar_Fasciitis_Patients.xlsx")

df = load_data()

# استخدام صندوق إدخال نصي مباشر بدلاً من القائمة المنسدلة لتجنب مشاكل النفق
patient_id_input = st.text_input("Enter Patient ID (e.g., P001, P002):", "P001")

if st.button("Search Patient Record"):
    matched_rows = df[df['Patient_ID'].str.upper() == patient_id_input.strip().upper()]
    
    if not matched_rows.empty:
        patient_record = matched_rows.iloc[0]
        st.success(f"Patient record found successfully for: {patient_record['Name']}")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {patient_record['Name']}")
            st.write(f"**Age:** {patient_record['Age']} years")
            st.write(f"**Marital Status:** {patient_record['Marital_Status']}")
            st.write(f"**Weight:** {patient_record['Weight_kg']} kg")
        with col2:
            st.write(f"**Activity Level:** {patient_record['Activity_Level']}")
            st.write(f"**Dietary Habit:** {patient_record['Diet']}")
            st.write(f"**Leg Injury History:** {patient_record['Leg_Injury']}")
            st.error(f"**Pain Level (VAS):** {patient_record['Pain_Level_VAS']} / 10")
        
        st.markdown("---")
        st.subheader("💡 Recommended Treatment Plan (Decision Engine):")
        
        pain = patient_record['Pain_Level_VAS']
        weight = patient_record['Weight_kg']
        activity = patient_record['Activity_Level']
        injury = patient_record['Leg_Injury']
        
        plan = []
        if pain >= 8:
            plan.append("🚨 Immediate rest & minimize prolonged standing. Apply ice packs for 15 minutes twice daily.")
            plan.append("🩹 Avoid barefoot walking completely and use soft heel cushion supports.")
        elif 5 <= pain <= 7:
            plan.append("⚖️ Moderate Pain: Perform plantar fascia stretches every morning before stepping out of bed.")
        else:
            plan.append("🟢 Mild Pain: Engage in light walking combined with daily stretching exercises to prevent recurrence.")
            
        if weight > 90:
            plan.append("🥗 Dietary Recommendation: Join a weight management program to reduce mechanical load on the foot.")
            
        if "Sprain" in str(injury):
            plan.append("🔄 Rehabilitation Exercise: Incorporate ankle stability training to prevent reverse strain.")
            
        if "Sedentary" in str(activity):
            plan.append("🚶‍♂️ Gradual Activity: Start with 10 minutes of daily walking, increasing duration progressively each week.")
            
        for item in plan:
            st.info(item)
    else:
        st.error("Patient ID not found. Please check the ID and try again.")
