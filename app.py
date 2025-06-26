import streamlit as st
from generator import generate_questions

st.set_page_config(page_title="Survey Question Generator", layout="centered")
st.title("🧠 AI-Powered Survey Question Generator")

app_name = st.text_input("🧪 App/Product Name")
goal = st.text_area("🎯 Survey Goal")
mandatory = st.text_area("📝 Mandatory Questions to Include (comma separated)")

if st.button("⚡ Generate Questions"):
    if not app_name or not goal:
        st.error("Please fill all required fields")
    else:
        with st.spinner("Generating with Gemini..."):
            questions = generate_questions(app_name, goal, mandatory)

        st.success("Generated Questions")
        for i, q in enumerate(questions, 1):
            st.markdown(f"### Q{i}. {q['question']}")
            st.markdown(f"**Type:** {q['field_type']}")
            if 'options' in q:
                st.markdown("**Options:**")
                for opt in q['options']:
                    st.markdown(f"- {opt}")