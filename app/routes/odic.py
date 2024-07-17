from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pickle
import os
from huggingface_hub import hf_hub_url, login, hf_hub_download
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from .. import schemas
from ..config import settings

from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix='/v1',
    tags=['sentiment']
)

import nltk
nltk.download('stopwords')

# Define the repository and filenames
access_token = settings.access_token_read
login(token=access_token)

repo_id = settings.repo_id
model_filename = settings.model_filename
vectorizer_filename = settings.vectorizer_filename

# Download and cache the files
model_path = hf_hub_download(repo_id=repo_id, filename=model_filename)
vectorizer_path = hf_hub_download(repo_id=repo_id, filename=vectorizer_filename)

# Load the model and vectorizer
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

with open(vectorizer_path, 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Initialize the PorterStemmer
port_stem = PorterStemmer()

# Function for text pre-processing and stemming
def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    return ' '.join(stemmed_content)

@router.post("/predict")
async def predict(input: schemas.Predict):
    
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Empty text")
    
    try:
        # Pre-process the input text
        processed_text = stemming(input.text)
        
        # Transform the input text using the loaded vectorizer
        input_vector = vectorizer.transform([processed_text])
        
        # Predict the result using the loaded model
        prediction = model.predict(input_vector)
        
        # Return the result
        if prediction[0] == 1:
            return {"prediction": "Potential Security Threat"}
        else:
            return {"prediction": "No Immediate Threat"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error making prediction: " + str(e))
