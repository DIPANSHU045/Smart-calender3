import spacy
from datetime import datetime, timedelta

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_event_details(text):
    doc = nlp(text)
    # Defaults
    res = {
        "summary": text,
        "start": datetime.now().isoformat(),
        "end": (datetime.now() + timedelta(hours=1)).isoformat(),
        "location": "Default"
    }
    
    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            # In a production app, use 'dateparser' library here for better accuracy
            pass 
        if ent.label_ in ["GPE", "FAC"]:
            res["location"] = ent.text
            
    return res