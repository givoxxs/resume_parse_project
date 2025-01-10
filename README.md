# Resume Parser API

A simple FastAPI-based web application for uploading and parsing resume files (PDF, DOC, DOCX). This app processes uploaded resume files, extracts information like name, skills, experience, and more. It then saves the parsed data into a CSV file which can be downloaded by the user.

## Features
- Upload multiple resume files (PDF, DOC, DOCX).
- Parse resumes and extract key information (name, skills, experience).
- Download the parsed data as a CSV file.
- Support CORS for frontend integration.
- Custom error handling and validation for file types.

## Requirements

To run the application locally, you need to have the following installed:

- Python 3.8+
- pip (Python package installer)
- FastAPI
- Uvicorn (ASGI server)
- Pandas
- Jinja2
- Any required resume parsing library (for example, `python-docx`, `PyPDF2`, etc.)

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/resume-parser.git
cd resume-parser
```
### 2. Create and activate a virtual environment:
For Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies:
```bashbash
pip install -r requirements.txt
```
### 4. Run the application:
To start the server, use uvicorn:
```bash
uvicorn main:app --reload
```

This will start the FastAPI app on http://127.0.0.1:8000.

## Usage
### Upload Resumes:
Navigate to the homepage (http://127.0.0.1:8000/).
Select one or more resume files (PDF, DOC, DOCX).
Click the "Upload" button.
### Results:
After uploading the files, the parsed data (name, skills, experience) will be displayed.
You can also download the parsed CSV file by clicking the "Download CSV" link.
### Download CSV:
The parsed information is saved as a CSV file, and you can download it by clicking the download link shown for each uploaded file.

## Project Structure
```graphql
resume-parser/
│
├── app/
│   ├── main.py                # Main FastAPI application
│   ├── services/
│   │   └── resume_parse.py     # Logic for parsing resume files
│   │   └── __init__.py         # Initialize services package
│   ├── utils/
│   │   └── logger.py           # Utility for logging
│   │   └── save_csv.py         # Logic for saving parsed data to CSV
│   │   └── __init__.py         # Initialize utils package
│   └── __init__.py             # Initialize app package
│
├── templates/                  # Directory for storing HTML templates
│   └── index.html              # Homepage template
├── static/                     # Directory for static files
│   └── style.css               # CSS file for styling
│   └── script.js               # JavaScript file for frontend functionality
├── uploads/                    # Directory for storing uploaded resume files
├── results/                    # Directory for storing generated CSV files
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore file
```