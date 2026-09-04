# EduAI — Full Stack AI Question-Answering Application.
# Instructions to setup and run the project locally.
# The project is live and deployed on the link below.

https://flask-ai-assessment.vercel.app/

#Setup: -
## Backend:

* Clone the repository:
git clone https://github.com/diablo5076/flask-ai-assessment.git
cd flask-ai-assessment

* Create a Python virtual environment:
python -m venv venv

* activate it using:
.\venv\Scripts\Activate.ps1

* Install the Python dependencies:
pip install -r requirements.txt

* Create a .env file in the project root:
MONGODB_URI=your_mongodb_connection_string
MONGODB_DB=flask_ai_assessment
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b

* Start the Flask backend:
python run.py

* The backend will run locally at:
http://127.0.0.1:5000

## Frontend:

* Open a new terminal and navigate to the frontend:
cd frontend

* Install the frontend dependencies:
npm install

* Start the Vite development server:
npm run dev

The terminal will display the local frontend URL
