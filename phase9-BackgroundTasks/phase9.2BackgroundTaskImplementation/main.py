from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()


def send_email(email: str, message: str):
    print("Background task started...")

    # Simulate a slow operation
    time.sleep(5)

    print(f"To: {email}")
    print(f"Message: {message}")
    print("Background task completed.")


@app.post("/create-user")
def create_user(background_tasks: BackgroundTasks):

    # Main request work
    print("User saved in DB")

    # Add task to background
    background_tasks.add_task(
        send_email,
        "yadnyesh@gmail.com",
        "Welcome to our platform"
    )

    print("Response is ready")

    return {
        "message": "User created successfully"
    }

# Client
#   │
#   │ POST /create-user
#   ▼
# FastAPI
#   │
#   ├── User saved in DB
#   │
#   ├── Schedule send_email()
#   │
#   ├── Prepare response
#   │
#   ▼
# Response → Client
#   │
#   ▼
# send_email()