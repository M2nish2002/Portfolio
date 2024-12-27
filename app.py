import streamlit as st
import streamlit.components.v1 as components
import PyPDF2
import nltk
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# [Previous ResumeChatbot class remains the same]
class ResumeChatbot:
    def __init__(self, resume_path):
        self.resume_path = resume_path
        self.resume_data = self.extract_resume_data()
        self.vectorizer = TfidfVectorizer()
        self.prepare_knowledge_base()

    def extract_resume_data(self):
        try:
            with open(self.resume_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                full_text = ""
                for page in reader.pages:
                    full_text += page.extract_text()

            return {
                "professional_summary": self.extract_summary(full_text),
                "skills": self.extract_skills(full_text),
                "experience": self.extract_experience(full_text),
                "education": self.extract_education(full_text),
                "certifications": self.extract_certifications(full_text)
            }
        except Exception as e:
            st.error(f"Error reading resume: {e}")
            return {}

    def extract_summary(self, text):
        # Basic summary extraction
        sentences = nltk.sent_tokenize(text)
        return " ".join(sentences[:3]) if sentences else "No summary available."

    def extract_skills(self, text):
        skill_keywords = [
            "Python", "Docker", "Kubernetes", 
            "AWS", "CI/CD", "Terraform", 
            "Linux", "Cloud", "DevOps"
        ]
        return [skill for skill in skill_keywords if skill.lower() in text.lower()]

    def extract_experience(self, text):
        experience_pattern = r"(\d{4}-\d{4})\s*(.*?)\s*at\s*(.*)"
        experiences = re.findall(experience_pattern, text, re.DOTALL)
        return [
            {
                "period": exp[0],
                "role": exp[1].strip(),
                "company": exp[2].strip()
            } for exp in experiences
        ] if experiences else [{"role": "No experience details found"}]

    def extract_education(self, text):
        # Placeholder for education extraction
        education_keywords = ["Bachelor", "Master", "PhD", "Degree"]
        return [edu for edu in education_keywords if edu.lower() in text.lower()]

    def extract_certifications(self, text):
        certification_keywords = [
            "Certified", "Certification", 
            "AWS", "Kubernetes", "Cloud"
        ]
        return [cert for cert in certification_keywords if cert.lower() in text.lower()]

    def prepare_knowledge_base(self):
        self.knowledge_base = [
            f"Skills: {', '.join(self.resume_data.get('skills', []))}",
            f"Experience: {json.dumps(self.resume_data.get('experience', []))}",
            f"Education: {', '.join(self.resume_data.get('education', []))}",
            f"Certifications: {', '.join(self.resume_data.get('certifications', []))}"
        ]
        self.tfidf_matrix = self.vectorizer.fit_transform(self.knowledge_base)

    def generate_response(self, query):
        query = query.lower()
        
        # Predefined response patterns
        response_patterns = {
            "skills": lambda: f"My key skills include: {', '.join(self.resume_data.get('skills', []))}",
            "experience": lambda: "\n".join([
                f"{exp['role']} at {exp.get('company', 'N/A')} ({exp.get('period', 'N/A')})" 
                for exp in self.resume_data.get('experience', [])
            ]),
            "education": lambda: f"Education: {', '.join(self.resume_data.get('education', []))}",
            "certification": lambda: f"Certifications: {', '.join(self.resume_data.get('certifications', []))}"
        }

        # Check for specific keywords
        for key, response_func in response_patterns.items():
            if key in query:
                return response_func()

        # Fallback to similarity-based response
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)
        best_match_index = similarities[0].argmax()
        
        return self.knowledge_base[best_match_index]
    
def load_static_files():
    """Load HTML, CSS, and JavaScript files"""
    try:
        with open('index.html', 'r') as html_file:
            html_content = html_file.read()
        
        with open('styles.css', 'r') as css_file:
            css_content = css_file.read()
        
        with open('script.js', 'r') as js_file:
            js_content = js_file.read()
        
        return html_content, css_content, js_content
    except Exception as e:
        st.error(f"Error loading static files: {e}")
        return "", "", ""

def main():
    st.set_page_config(
        page_title="Professional Portfolio",
        page_icon=":briefcase:",
        layout="wide"
    )

    # Sidebar Navigation
    st.sidebar.title("Portfolio Navigator")
    page = st.sidebar.radio(
        "Explore Sections", 
        ["Home", "About", "Skills", "Experience", "Resume Chatbot", "Full Website"]
    )

    # Initialize Resume Chatbot
    try:
        chatbot = ResumeChatbot('manish_ML.pdf')
    except Exception as e:
        st.error(f"Could not initialize chatbot: {e}")
        return

    # Load Static Files
    html_content, css_content, js_content = load_static_files()

    # Page Routing
    if page == "Full Website":
        # Render full static website within Streamlit
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        components.html(html_content, height=1000, scrolling=True)
        
        # Inject JavaScript
        components.html(f"<script>{js_content}</script>", height=0)

    elif page == "Home":
        st.title("Professional Portfolio")
        st.write("Welcome to my digital portfolio!")

    elif page == "About":
        st.header("About Me")
        st.write(chatbot.resume_data.get('professional_summary', 'No summary available.'))

    elif page == "Skills":
        st.header("Technical Skills")
        skills = chatbot.resume_data.get('skills', [])
        for skill in skills:
            st.markdown(f"- {skill}")

    

    elif page == "Resume Chatbot":
        st.header("Resume Chatbot")
        st.write("Ask me anything about my professional background!")

        # Chatbot Interface
        user_query = st.text_input("Your question:")
        
        if user_query:
            try:
                response = chatbot.generate_response(user_query)
                st.write(f"**Bot:** {response}")
            except Exception as e:
                st.error(f"Error generating response: {e}")

        # Resume Download
        with open('manish_ML.pdf', 'rb') as pdf_file:
            st.download_button(
                label="Download Resume",
                data=pdf_file.read(),
                file_name="Professional_Resume.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()