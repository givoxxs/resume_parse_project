import spacy
import re
from docx import Document
import PyPDF2
from tika import parser

try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        text = []
        for page in pdf.pages:
            text.append(page.extract_text())
        return "\n".join(text)
    
def extract_text(file_path):
    file_path = str(file_path)
    if file_path.endswith(".docx") or file_path.endswith(".doc"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format")
    
def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            entities.append({"text": ent.text, "label": ent.label_})
    return entities

def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Unknown"

def extract_phone(text):
    phone_pattern =  r"\(?\+?[0-9]*\)?[\s.-]?[0-9]+[\s.-]?[0-9]+[\s.-]?[0-9]+"
    match = re.findall(phone_pattern, text)
    return match[0] if match else "Unknown"

def extract_email(text):
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    match = re.findall(email_pattern, text)
    return match[0] if match else "Unknown"

def extract_location(doc):    
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return "Unknown"

def extract_skills(doc):
    skills = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            skills.append(ent.text)
    return list(set(skills))

def extract_skills_with_keys(skills, doc):
    # skills = ["Python", "Java", "C++"]
    skills_with_keys = []
    for skill in skills:
        if skill.lower() in doc.text.lower():
            skills_with_keys.append(skill)
    return skills_with_keys

def extract_experience(doc):
    experience = re.findall(r"(Experience|Work History)(.*?)(Education|Skills)", doc.text, re.DOTALL)
    return experience[0][1].strip() if experience else "Not available"

def extract_contact_url(doc):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    linkedin_pattern = r"(linkedin.com/in/)([a-zA-Z0-9-]+)"
    
    emails = re.findall(email_pattern, doc.text)
    linkedin = re.findall(linkedin_pattern, doc.text)
    
    return {"email": emails[0] if emails else "Unknown", "linkedin": linkedin[0][1] if linkedin else "Unknown"}

def parse_resume(file_path):
    text = extract_text(file_path)
    doc = nlp(text)
    name = extract_name(doc)
    phone = extract_phone(text)
    email = extract_email(text)
    location = extract_location(doc)
    skills = extract_skills(doc)
    skills_with_keys = extract_skills_with_keys(skills, doc)
    experience = extract_experience(doc)
    contact_url = extract_contact_url(doc)
    
    return {
        "name": name,
        "phone": phone,
        "email": email,
        "location": location,
        "skills": skills,
        "skills_with_keys": skills_with_keys,
        "experience": experience,
        "contact_url": contact_url
    }
    