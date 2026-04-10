# Smart Resume Analyzer

An NLP-powered web app that scores how well a resume matches a job description.
Upload your resume, paste a job description, and get an instant match score with
keyword analysis.

## How It Works

1. Resume is uploaded as PDF, DOCX, or TXT
2. Text is extracted and cleaned using spaCy — lemmatization and stopword removal
3. TF-IDF vectorization converts both resume and job description into numerical features
4. Cosine Similarity calculates how closely they match
5. Matched and missing keywords are highlighted to guide improvements

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| spaCy | NLP preprocessing — lemmatization, stopwords |
| Scikit-learn | TF-IDF Vectorization + Cosine Similarity |
| pdfplumber | PDF text extraction |
| docx2txt | DOCX text extraction |
| Streamlit | Interactive web interface |

## Features

- Supports PDF, DOCX, and TXT resume formats
- Real-time match score out of 100%
- Visual progress bar for match score
- Matched keywords — what you have that the JD wants
- Missing keywords — what to add to improve your chances
- Extracted resume text preview
- Match label — Excellent / Good / Average / Poor

## Project Structure

```
smart-resume-analyzer/
│
├── app.py               # Main Streamlit application
├── requirements.txt     # Project dependencies
├── README.md            # Project documentation
└── LICENSE              # MIT License
```

## Setup & Installation

1. Clone the repository

```bash
git clone https://github.com/riddhima3/smart-resume-analyzer.git
cd smart-resume-analyzer
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Download spaCy language model

```bash
python -m spacy download en_core_web_sm
```

4. Run the app

```bash
streamlit run app.py
```

## How to Use

1. Upload your resume in PDF, DOCX, or TXT format
2. Paste the job description you are applying for
3. Click **Analyze Match**
4. Review your score, matched keywords, and missing keywords
5. Update your resume based on the missing keywords and re-analyze

## Author

**Riddhima Saha**
- LinkedIn: [riddhima-saha](https://www.linkedin.com/in/riddhima-saha)
- Email: riddhima.sahaa@gmail.com
