import streamlit as st
import PyPDF2

st.set_page_config(page_title="Exam Evaluator", page_icon="📘")

st.title("📘 Automated Exam Evaluator")
st.write("Upload **Answer Key PDF** and **Student Answer PDF**")

# ---------------- PDF READER ----------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return [t.strip() for t in text.split("\n") if t.strip()]

# ---------------- SIMPLE EVALUATION LOGIC ----------------
def evaluate(correct, student):
    correct_words = set(correct.lower().split())
    student_words = set(student.lower().split())

    match = len(correct_words & student_words)
    ratio = match / len(correct_words)

    if ratio >= 0.6:
        marks = 2
        suggestion = "Good answer. You can improve by adding more explanation and examples."
    elif ratio >= 0.3:
        marks = 1
        suggestion = "Partially correct. Explain the definition clearly and include key applications."
    else:
        marks = 0
        suggestion = "Answer is insufficient. Revise the concept and explain it step by step."

    improved_answer = (
        correct
        + " It can be explained with proper definition, features, and real-world applications."
    )

    return marks, suggestion, improved_answer

# ---------------- FILE UPLOAD ----------------
col1, col2 = st.columns(2)
with col1:
    answer_pdf = st.file_uploader("📄 Upload Answer Key PDF", type="pdf")
with col2:
    student_pdf = st.file_uploader("📄 Upload Student Answer PDF", type="pdf")

# ---------------- PROCESS ----------------
if answer_pdf and student_pdf:
    answers = read_pdf(answer_pdf)
    students = read_pdf(student_pdf)

    total_marks = 0

    for i in range(5):
        correct = answers[i]
        student = students[i] if i < len(students) else ""

        marks, suggestion, improved = evaluate(correct, student)
        total_marks += marks

        st.subheader(f"📘 Question {i+1}")
        st.write(f"**Marks:** {marks} / 2")

        st.markdown("**Student Answer:**")
        st.write(student)

        st.markdown("**Suggestion to Improve:**")
        st.write(suggestion)

        st.markdown("**Improved Answer (Model Answer):**")
        st.write(improved)

        st.divider()

    st.success(f"🎯 Total Marks Obtained: {total_marks} / 10")
