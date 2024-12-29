
import re

import PyPDF2
import pdfplumber






class ResumeChatbot:
    def __init__(self, pdf_path: str):
       
       
        # Extract text from PDF
        self.resume_text = self._extract_pdf_text(pdf_path)
       
        
   
    def get_resume_summary(self) -> str:
        """
        Generate a summary of the resume
       
        :return: Resume summary
        """
        summary_prompt = (
            "Provide a concise professional summary of this resume, "
            "highlighting key skills, experience, and qualifications."
        )
        return self.ask_question(summary_prompt)

    def extract_resume_text(self, pdf_file):
        """
        Advanced PDF text extraction with multiple methods
        
        Args:
            pdf_file (UploadedFile): Uploaded PDF file
        
        Returns:
            str: Extracted resume text
        """
        try:
            # Method 1: pdfplumber (Primary)
            with pdfplumber.open(pdf_file) as pdf:
                full_text = "\n".join([
                    page.extract_text() or "" 
                    for page in pdf.pages
                ])
            
            # Fallback to PyPDF2 if pdfplumber fails
            if not full_text.strip():
                pdf_file.seek(0)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                full_text = "\n".join([
                    page.extract_text() or "" 
                    for page in pdf_reader.pages
                ])
            
            # Clean and process text
            self.resume_text = self._clean_text(full_text)
            
            # Perform comprehensive analysis
            self._analyze_resume()
            
            return self.resume_text
        
        except Exception as e:
            self.logger.error(f"Resume extraction error: {e}")
            return ""
        
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from the PDF file."""
        text = ""
        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            # Clean up text if necessary
            text = re.sub(r"\s+", " ", text).strip()
            return text
        except Exception as e:
            raise RuntimeError(f"Error reading PDF file: {e}")

    def _clean_text(self, text):
        """
        Advanced text cleaning and preprocessing
        
        Args:
            text (str): Raw extracted text
        
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespaces and normalize
        text = re.sub(r'\s+', ' ', text)
        
        # Remove non-printable characters
        text = re.sub(r'[^\x20-\x7E\n]', '', text)
        
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()

    def _analyze_resume(self):
        """
        Comprehensive resume analysis
        """
        try:
            # Structured data extraction
            self.structured_data = {
                "personal_info": self._extract_personal_info(),
                "contact_info": self._extract_contact_info(),
                "skills": self._extract_skills(),
                "experience": self._extract_experience(),
                "education": self._extract_education(),
                "certifications": self._extract_certifications(),
                "summary": self._generate_professional_summary()
            }
            
            # Update resume analysis
            self.resume_analysis = {
                key: value for key, value in self.structured_data.items() 
                if value  # Only include non-empty entries
            }
            
            self.logger.info("Resume analysis completed successfully")
        
        except Exception as e:
            self.logger.error(f"Resume analysis error: {e}")

    def _extract_personal_info(self):
        """
        Extract personal information
        
        Returns:
            dict: Personal details
        """
        name_patterns = [
            r"(([A-Z][a-z]+\s?){1,3})",  # First and Last Name
            r"([A-Z][a-z]+ [A-Z][a-z]+)"  # Full Name
        ]
        
        for pattern in name_patterns:
            names = re.findall(pattern, self.resume_text)
            if names:
                return {"name": names[0][0] if isinstance(names[0], tuple) else names[0]}
        
        return {"name": "Not Found"}

    def _extract_contact_info(self):
        """
        Advanced contact information extraction
        
        Returns:
            dict: Contact details
        """
        contact_info = {
            "email": self._extract_email(),
            "phone": self._extract_phone(),
            "location": self._extract_location()
        }
        
        return {k: v for k, v in contact_info.items() if v}

    def _extract_email(self):
        """
        Extract email address
        
        Returns:
            str: Email address or empty string
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.resume_text)
        return emails[0] if emails else ""

    def _extract_phone(self):
        """
        Extract phone number
        
        Returns:
            str: Phone number or empty string
        """
        phone_patterns = [
            r'\+?1?\s*\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})',  # US Phone
            r'\+\d{1,3}\s?\(\d{3}\)\s?\d{3}[-.]?\d{4}'  # International formats
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, self.resume_text)
            if phones:
                return phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
        
        return ""

    def _extract_location(self):
        """
        Extract location information
        
        Returns:
            str: Location or empty string
        """
        location_patterns = [
            r'(?:Located in|Based in|from)\s*([A-Za-z\s]+,\s*[A-Z]{2})',
            r'([A-Za-z\s]+,\s*[A-Z]{2})'
        ]
        
        for pattern in location_patterns:
            locations = re.findall(pattern, self.resume_text)
            if locations:
                return locations[0]
        
        return ""

    def _extract_skills(self):
        """
        Comprehensive skills extraction
        
        Returns:
            dict: Categorized skills
        """
        skill_categories = {
            "Technical Skills": [
                "Python", "JavaScript", "Java", "C++", 
                "Machine Learning", "AI", "Data Science",
                "Docker", "AWS", "Cloud Computing"
            ],
            "Programming Frameworks": [
                "TensorFlow", "NLTK","Re" 
                "Django", "Flask"
            ]
        }
        
        extracted_skills = {category: [] for category in skill_categories}
        
        for category, skills in skill_categories.items():
            for skill in skills:
                if skill.lower() in self.resume_text.lower():
                    extracted_skills[category].append(skill)
        
        return {k: v for k, v in extracted_skills.items() if v}

    def _extract_experience(self):
        """
        Extract work experience details
        
        Returns:
            list: List of work experiences
        """
        experience_pattern = r'(?:(?:Experience|Work History|Professional Experience)\s*:\s*(.*?)(?:Education|Skills|Certifications|$))'
        experiences = re.findall(experience_pattern, self.resume_text, re.DOTALL)
        return experiences[0].strip().split('\n') if experiences else []

    def _extract_education(self):
        """
        Extract education details
        
        Returns:
            list: List of educational qualifications
        """
        education_pattern = r'(?:(?:Education|Academic Background)\s*:\s*(.*?)(?:Experience|Skills|Certifications|$))'
        educations = re.findall(education_pattern, self.resume_text, re.DOTALL)
        return educations[0].strip().split('\n') if educations else []

    def _extract_certifications(self):
        """
        Extract certifications
        
        Returns:
            list: List of certifications
        """
        certification_pattern = r'(?:(?:Certifications|Licenses)\s*:\s*(.*?)(?:Experience|Education|Skills|$))'
        certifications = re.findall(certification_pattern, self.resume_text, re.DOTALL)
        return certifications[0].strip().split('\n') if certifications else []

    def _generate_professional_summary(self):
        """
        Generate a professional summary
        
        Returns:
            str: Professional summary
        """
        summary_pattern = r'(?:(?:Summary|Profile)\s*:\s*(.*?)(?:Experience|Education|Skills|Certifications|$))'
        summaries = re.findall(summary_pattern, self.resume_text, re.DOTALL)
        return summaries[0].strip() if summaries else "No summary found."
    
    def format_resume_data(self):
        # Convert resume JSON to a string summary
        summary = []
        summary.append(f"Name: {self.resume_data.get('name', 'N/A')}")
        summary.append(f"Education: {self.resume_data.get('education', 'N/A')}")
        if "experience" in self.resume_data:
            for exp in self.resume_data["experience"]:
                summary.append(
                    f"Worked at {exp['company']} as {exp['role']} for {exp['duration']}."
                )
        summary.append(f"Skills: {', '.join(self.resume_data.get('skills', []))}")
        return " ".join(summary)
    
            
    
    
    

    
    
    
    
   
    