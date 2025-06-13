import streamlit as st
from pickle import load

from data import *
from utils import avg_value, get_key

st.set_page_config(layout="wide")
st.title("🎓 Student Outcome Prediction App")
st.markdown("""
This tool predicts whether a student is most likely to **graduate**, **drop out**, or remain **enrolled**,
based on various academic and demographic factors.
""")

with st.form("prediction_form"):
    st.subheader("🔍 Student Profile")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("🧑 Full Name")
        age = st.number_input("📅 Age", min_value=15, max_value=100)
        gender = st.selectbox("⚥ Gender", options=list(data_gender.values()))
        marital_status = st.selectbox("💍 Marital Status", options=list(data_status.values()))
        scholarship_holder = st.radio("🎓 Scholarship Holder", options=list(data_yes_no.values()))
        displaced = st.radio("🏚️ Displaced", options=list(data_yes_no.values()))
        debtor = st.radio("💸 Debtor", options=list(data_yes_no.values()))
        tuition_fee = st.radio("💰 Tuition Fee Up-to-Date", options=list(data_yes_no.values()))

    with col2:
        application_mode = st.selectbox("📄 Application Mode", options=list(data_application_mode.values()))
        application_order = st.slider("🔢 Application Order", min_value=0, max_value=9)
        course = st.selectbox("📚 Course", options=list(data_course.values()))
        attendance = st.radio("🕒 Attendance Mode", options=list(data_attendance.values()))
        previous_qualification = st.selectbox("🎓 Previous Qualification", options=list(data_previous_qualification.values()))
        previous_qualification_grade = st.slider("📊 Previous Qualification Grade", min_value=0, max_value=100)

    st.markdown("---")
    st.subheader("👪 Family Background")
    col3, col4 = st.columns(2)
    with col3:
        mother_qualification = st.selectbox("👩 Mother's Qualification", options=list(data_parents_qualification.values()))
        mother_occupation = st.selectbox("👩 Mother's Occupation", options=list(data_parents_occupation.values()))
    with col4:
        father_qualification = st.selectbox("👨 Father's Qualification", options=list(data_parents_qualification.values()))
        father_occupation = st.selectbox("👨 Father's Occupation", options=list(data_parents_occupation.values()))

    st.markdown("---")
    st.subheader("📈 Academic Record")
    admission_grade = st.number_input("📋 Admission Grade")
    curricular_units_1st_sem_enrolled = st.number_input("📘 1st Sem - Enrolled Units")
    curricular_units_1st_sem_approved = st.number_input("✅ 1st Sem - Approved Units")
    curricular_units_1st_sem_grade = st.number_input("🏆 1st Sem - Average Grade")
    curricular_units_2nd_sem_enrolled = st.number_input("📘 2nd Sem - Enrolled Units")
    curricular_units_2nd_sem_approved = st.number_input("✅ 2nd Sem - Approved Units")
    curricular_units_2nd_sem_grade = st.number_input("🏆 2nd Sem - Average Grade")

    submitted = st.form_submit_button("📤 Predict Outcome")

    if submitted:
        # Validasi semua input wajib
        required_fields = [
            name,
            age,
            gender,
            marital_status,
            scholarship_holder,
            displaced,
            debtor,
            tuition_fee,
            application_mode,
            application_order,
            course,
            attendance,
            previous_qualification,
            previous_qualification_grade,
            mother_qualification,
            mother_occupation,
            father_qualification,
            father_occupation,
            admission_grade,
            curricular_units_1st_sem_enrolled,
            curricular_units_1st_sem_approved,
            curricular_units_1st_sem_grade,
            curricular_units_2nd_sem_enrolled,
            curricular_units_2nd_sem_approved,
            curricular_units_2nd_sem_grade
        ]

        if any(field in ("", None) for field in required_fields):
            st.warning("⚠️ Semua kolom wajib diisi. Pastikan tidak ada data yang kosong.")
        else:
            # Hitung rata-rata
            avg_enrolled = avg_value(curricular_units_1st_sem_enrolled, curricular_units_2nd_sem_enrolled)
            avg_approved = avg_value(curricular_units_1st_sem_approved, curricular_units_2nd_sem_approved)
            avg_grade = avg_value(curricular_units_1st_sem_grade, curricular_units_2nd_sem_grade)

            input_data = [[
                get_key(data_status, marital_status),
                get_key(data_application_mode, application_mode),
                application_order,
                get_key(data_course, course),
                get_key(data_attendance, attendance),
                get_key(data_previous_qualification, previous_qualification),
                previous_qualification_grade,
                get_key(data_parents_qualification, mother_qualification),
                get_key(data_parents_qualification, father_qualification),
                get_key(data_parents_occupation, mother_occupation),
                get_key(data_parents_occupation, father_occupation),
                admission_grade,
                get_key(data_yes_no, displaced),
                get_key(data_yes_no, debtor),
                get_key(data_yes_no, tuition_fee),
                get_key(data_gender, gender),
                get_key(data_yes_no, scholarship_holder),
                age,
                avg_enrolled,
                avg_approved,
                avg_grade
            ]]

            model = load(open("model/voting_clf_three_labels.pkl", "rb"))
            prediction = model.predict_proba(input_data)[0]

            st.markdown("---")
            st.subheader("📊 Prediction Result")

            st.progress(int(prediction[2] * 100), text=f"Graduated: {prediction[2]*100:.2f}%")
            st.progress(int(prediction[1] * 100), text=f"Enrolled: {prediction[1]*100:.2f}%")
            st.progress(int(prediction[0] * 100), text=f"Dropout: {prediction[0]*100:.2f}%")

            if prediction[0] > prediction[1] and prediction[0] > prediction[2]:
                st.error(f"😞 Sorry {name}, there is a high chance of dropping out ({prediction[0]*100:.2f}%)")
            elif prediction[1] > prediction[0] and prediction[1] > prediction[2]:
                st.warning(f"📖 {name} is likely to stay enrolled ({prediction[1]*100:.2f}%)")
            else:
                st.success(f"🎉 Congratulations {name}, you have a strong chance of graduating! ({prediction[2]*100:.2f}%)")
