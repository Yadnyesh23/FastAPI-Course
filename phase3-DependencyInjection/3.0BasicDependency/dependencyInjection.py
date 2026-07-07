from fastapi import FastAPI, Depends

app = FastAPI()

def get_token():
    return "abc123"

def get_name(token : str = Depends(get_token)):
    return "Yadnyesh"

def get_role():
    return "CEO/Manager/Boss"

@app.get('/')
def profile(name : str = Depends(get_name), role : str = Depends(get_role)):
    return {
        "name" : name,
        "role" : role
    }