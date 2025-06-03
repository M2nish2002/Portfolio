import streamlit as st

from dotenv import load_dotenv

import google.generativeai as genai
import os

# Load environment variables
load_dotenv()

class PortfolioWebsite:
    def __init__(self):
        # Configure page
        st.set_page_config(
            page_title="AI-Powered Portfolio",
            page_icon="🚀",
            layout="wide"
        )
        
        # Initialize session state
        if 'page' not in st.session_state:
            st.session_state.page = 'Home'
        
        # Initialize resume chatbot
     

    def render_navbar(self):
        """
        Render navigation bar
        """
        st.sidebar.title("🚀 Portfolio Navigation")
        pages = [
            "Home", 
            "About Me", 
            "Skills", 
            "Projects", 
            "Resume Chatbot", 
            "Contact"
        ]
        
        st.session_state.page = st.sidebar.radio(
            "Go to", 
            pages, 
            index=pages.index(st.session_state.page)
        )

    def render_home_page(self):
        """
        Render the home page
        """
        st.title("👋 Welcome to My AI-Powered Portfolio")
        
        # Hero section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ## Hi, I'm Manish jaysingh
            ### AI & Machine Learning Engineer
            
            🤖 Passionate about building intelligent systems
            🧠 Specializing in Machine Learning & Deep Learning
            💡 Transforming ideas into innovative solutions
            """)
            
            st.download_button(
                label="Download Resume",
                data=open("Manish_AI.pdf", "rb").read(),
                file_name="manish_Resume.pdf",
                mime="application/pdf"
            )
        
        with col2:
            st.image("m.jpg", width=300)

    def render_about_page(self):
        """
        Render the about me page
        """
        st.header("🌟 About Me")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### Professional Summary
            I am a dedicated aspiring AI & Machine Learning Engineer with expertise in:
            - Developing intelligent systems
            - Creating scalable machine learning solutions
            - Implementing cutting-edge AI technologies
            
            ### Professional Philosophy
            Believing in the power of technology to solve complex problems 
            and drive meaningful innovation.
            """)
        
        with col2:
            st.image("m.jpg", width=300)

    def render_skills_page(self):
        """
        Render skills page with interactive visualization
        """
        st.header("💻 Technical Skills")
        
        skills = {
            "Programming Languages": [
                ("Python", 90),
                
                ("Java",95)
            ],
            "Frameworks": [
                ("TensorFlow", 85),
                ("Flask", 75),
                ("Streamlit", 80)
            ],
            "Cloud & DevOps": [
                ("AWS", 70),
                ("Docker", 70),
                
            ]
        }
        
        for category, skill_list in skills.items():
            st.subheader(category)
            for skill, level in skill_list:
                st.progress(level)
                st.write(f"{skill}: {level}%")

    def render_projects_page(self):
        """
        Render projects with detailed information
        """
        st.header("🚀 Featured Projects")
        
        projects = [
             {
                "name": "Optimal Portfolio Allocation App",
                "description": "let users optimize their investment portfolios based on historical stock data from the S&P 500.",
                "technologies": ["Python","streamlit","pandas","matplotlib","scipy","numpy"],
                "github": "https://github.com/M2nish2002/portfolio_app"
            },
            {
                "name": "Advanced ordering bot",
                "description": "Multimodal bot",
                "technologies": ["Python","LangGraph","google-gemini","ChromaDB","sqlite"],
                "github": "https://github.com/M2nish2002/AdvancedRestuarantBot"
            },
            {
                "name": "Crack classification",
                "description": "binary classification application",
                "technologies": ["Python","pytorch"],
                "github": "https://github.com/M2nish2002/CrackDetection"
            },
            {
                "name": "Chicken disease classification",
                "description": "binary classification application",
                "technologies": ["Python", "AWS", "Docker","Flask","Github action","CI/CD"],
                "github": "https://github.com/M2nish2002/chicken-disease-classification"
            },
            {
                "name": "Next word predictor",
                "description": "Trained on Conan Doyle's 'The Adventures of Sherlock Holmes' as our dataset",
                "technologies": ["TensorFlow", "Python", "Streamlit",],
                "github": "https://github.com/M2nish2002/LSTM_Next_Word_predictor",
                "Link":"https://m2nish2002-lstm-next-word-predictor-app-bk0gnu.streamlit.app/"
            },
            {
                "name": "Tweet sentiment analysis",
                "description": "Trained on a million tweets",
                "technologies": ["TensorFlow", "Python", "NLTK","Re"],
                "github": "https://github.com/M2nish2002/NLP"
            },
            {
                "name": "Bottle Flip Game",
                "description": "Computer vision based game played by two people ",
                "technologies": ["opencv", "Python", "Numpy","Mediapipe"],
                "github": "https://github.com/M2nish2002/bottle_flip_game"
            }
        ]
        
        for project in projects:
            with st.expander(project["name"]):
                st.write(project["description"])
                st.write("Technologies:", ", ".join(project["technologies"]))
                st.link_button("View on GitHub", project["github"])

    def render_resume_chatbot_page():
        st.title("ChatGPT-like Clone with Gemini AI")

        # Configure Gemini API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("GEMINI_API_KEY environment variable is not set.")
            return

        genai.configure(api_key=api_key)

        # Default generation configuration
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Create the model instance
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
        )

        # Initialize chat session if not already present
        if "chat_session" not in st.session_state:
            st.session_state["chat_session"] = model.start_chat(history=[])

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Capture user input
        if prompt := st.chat_input("What would you like to ask?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Fetch assistant response
            with st.chat_message("assistant"):
                try:
                    response = st.session_state["chat_session"].send_message(prompt)
                    assistant_message = response.text
                    st.markdown(assistant_message)

                    # Append the assistant's response to the message history
                    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    def render_contact_page(self):
        """
        Render contact page
        """
        st.header("📞 Contact Me")
        
        contact_form = st.form(key="contact_form")
        
        name = contact_form.text_input("Your Name")
        email = contact_form.text_input("Your Email")
        message = contact_form.text_area("Your Message")
        
        submit_button = contact_form.form_submit_button("Send Message")
        
        if submit_button:
            st.success("Message sent successfully!")

    def render_page(self):
        """
        Render the appropriate page based on navigation
        """
        self.render_navbar()
        
        page_renderers = {
            "Home": self.render_home_page,
            "About Me": self.render_about_page,
            "Skills": self.render_skills_page,
            "Projects": self.render_projects_page,
            "Resume Chatbot": self.render_resume_chatbot_page,
            "Contact": self.render_contact_page
        }
        
        # Render selected page
        page_renderers[st.session_state.page]()

def main():
    portfolio = PortfolioWebsite()
    portfolio.render_page()

if __name__ == "__main__":
    main()
