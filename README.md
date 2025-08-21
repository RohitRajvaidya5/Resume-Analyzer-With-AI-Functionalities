# Resume Analyzer with AI

A web application that leverages AI to analyze resumes and provide insights, suggestions, and compatibility scores with job descriptions.

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Technologies Used](#technologies-used)
* [Installation](#installation)
* [Usage](#usage)
* [Future Enhancements](#future-enhancements)
* [License](#license)

## Overview

This Resume Analyzer app allows users to upload their resumes and receive a detailed analysis comparing their resume against a given job description. The app uses AI to extract information from resumes, assess compatibility, and provide actionable suggestions to improve candidate alignment with the job role.

## Features

* Upload resumes in various formats (e.g., .txt, .pdf, .docx, .rtf)
* Extract text from resumes and job descriptions
* Compare resumes with job descriptions using Google Gemini API
* Generate ATS (Applicant Tracking System) compatibility scores
* Provide AI-driven suggestions to improve resume effectiveness
* Future plans include additional AI features for skill recommendations and resume optimization

## Technologies Used

* **Backend:** Django
* **Frontend:** HTML, Tailwind CSS
* **Database:** SQLite3
* **AI & LLM Integration:** Portia AI SDK, Google Gemini API
* **Others:** Python libraries for file handling and text extraction

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd resume-analyzer
   ```
2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:

   ```bash
   python manage.py migrate
   ```
5. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

1. Open the web app at `http://127.0.0.1:8000/`
2. Upload your resume file.
3. Input the job description for comparison.
4. Get an AI-generated score and suggestions for improvement.

## Future Enhancements

* Multi-format resume support (PDF, DOCX, RTF, etc.)
* Skill extraction and gap analysis
* Personalized suggestions based on industry and role
* Dashboard for tracking multiple resumes and their scores
* Integration with external ATS systems

## License

This project is open-source and available under the MIT License.
