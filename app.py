import streamlit as st
import spacy
import pdfplumber
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import os

# Load spaCy model
@st.cache_resource
def load_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        st.error("spaCy model not found. Run: python -m spacy download en_core_web_sm")
        st.stop()

nlp = load_model()

# ── Text extraction ──────────────────────────────────────────────────────────

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def extract_text_from_docx(file):
    return docx2txt.process(file)

def extract_text(file):
    name = file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif name.endswith(".docx"):
        return extract_text_from_docx(file)
    elif name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        st.error("Unsupported file type. Please upload PDF, DOCX, or TXT.")
        return ""

# ── Text preprocessing ───────────────────────────────────────────────────────

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    doc = nlp(text)
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and token.is_alpha
    ]
    return " ".join(tokens)

# ── Similarity scoring ───────────────────────────────────────────────────────

def get_similarity_score(resume_text, jd_text):
    processed_resume = preprocess(resume_text)
    processed_jd = preprocess(jd_text)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_resume, processed_jd])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)

# ── Keyword extraction ───────────────────────────────────────────────────────

def extract_keywords(text, top_n=15):
    processed = preprocess(text)
    vectorizer = TfidfVectorizer(max_features=top_n)
    vectorizer.fit_transform([processed])
    return list(vectorizer.get_feature_names_out())

def get_matching_keywords(resume_text, jd_text):
    jd_keywords = set(extract_keywords(jd_text, top_n=30))
    resume_keywords = set(extract_keywords(resume_text, top_n=50))
    matched = jd_keywords & resume_keywords
    missing = jd_keywords - resume_keywords
    return matched, missing

# ── Score label ──────────────────────────────────────────────────────────────

def score_label(score):
    if score >= 70:
        return "Excellent Match", "success"
    elif score >= 50:
        return "Good Match", "info"
    elif score >= 30:
        return "Average Match", "warning"
    else:
        return "Poor Match", "error"

# ── Streamlit UI ─────────────────────────────────────────────────────────────

st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

st.title("Smart Resume Analyzer")
st.write("Upload a resume and paste a job description to see how well they match.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Resume")
    resume_file = st.file_uploader("Upload Resume (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])

with col2:
    st.subheader("Job Description")
    jd_input = st.text_area("Paste Job Description Here", height=300)

st.divider()

if st.button("Analyze Match", use_container_width=True):

    if not resume_file:
        st.warning("Please upload a resume.")
    elif not jd_input.strip():
        st.warning("Please paste a job description.")
    else:
        with st.spinner("Analyzing..."):

            resume_text = extract_text(resume_file)

            if not resume_text.strip():
                st.error("Could not extract text from resume. Try a different file.")
                st.stop()

            score = get_similarity_score(resume_text, jd_input)
            matched_kw, missing_kw = get_matching_keywords(resume_text, jd_input)
            label, label_type = score_label(score)

        st.divider()
        st.subheader("Results")

        # Score display
        m1, m2, m3 = st.columns(3)
        m1.metric("Match Score", f"{score}%")
        m2.metric("Keywords Matched", len(matched_kw))
        m3.metric("Keywords Missing", len(missing_kw))

        # Score bar
        st.progress(int(score))

        # Label
        if label_type == "success":
            st.success(f"Result: {label}")
        elif label_type == "info":
            st.info(f"Result: {label}")
        elif label_type == "warning":
            st.warning(f"Result: {label}")
        else:
            st.error(f"Result: {label}")

        st.divider()

        kw1, kw2 = st.columns(2)

        with kw1:
            st.subheader("Matched Keywords")
            if matched_kw:
                st.write(" ".join([f"`{kw}`" for kw in sorted(matched_kw)]))
            else:
                st.write("No matching keywords found.")

        with kw2:
            st.subheader("Missing Keywords")
            st.write("Consider adding these to your resume:")
            if missing_kw:
                st.write(" ".join([f"`{kw}`" for kw in sorted(missing_kw)]))
            else:
                st.write("Great — no major keywords missing!")

        st.divider()

        # Resume text preview
        with st.expander("View Extracted Resume Text"):
            st.text(resume_text[:3000] + "..." if len(resume_text) > 3000 else resume_text)
