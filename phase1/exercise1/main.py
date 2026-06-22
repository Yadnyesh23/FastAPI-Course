# Personal Portfolio API
# Create these endpoints:

# Endpoint	 Method	    Response
# /	         GET	  Welcome message
# /about	 GET	  Your bio
# /skills	 GET	  List of skills
# /education GET	  College and branch
# /projects	 GET	  List of at least 3 projects
# /contact	 GET	  Contact information

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {
        "message" : "Welcome to Yadnyesh's Portfolio"
    }
    
@app.get('/about')
def about():
    return {
        "name": "Your Name",
        "role": "AI & Data Science Student"
    }
    
    
@app.get("/skills")
def get_skills():
    return {
        "programming_languages": [
            "Python",
            "JavaScript",
            "C++",
            "C"
        ],
        "backend": [
            "FastAPI",
            "Express",
            "Django"
        ],
        "frontend": [
            "React",
            "Next.js"
        ]
    }
@app.get("/skills")
def get_skills():
    return {
        "programming_languages": [
            "Python",
            "JavaScript",
            "C++",
            "C"
        ],
        "backend": [
            "FastAPI",
            "Express",
            "Django"
        ],
        "frontend": [
            "React",
            "Next.js"
        ]
    }
    
@app.get('/education')
def education():
    return {
        "schooling" : "Shree Mavli Mandal High School",
        "junior_college" : "Trupti G. Nemade Science and commerce College",
        "degree": "K. J. Somaiya Institute of technology"
    }
    
@app.get('/projects')
def projects():
    return {
        "Project 1" : "Project 1",
        "Project 2" : "Project 2",
        "Project 3" : "Project 3",
    }
    
@app.get('/contact')
def contact():
    return {
  "email": "your@email.com",
  "github": "...",
  "linkedin": "..."
}