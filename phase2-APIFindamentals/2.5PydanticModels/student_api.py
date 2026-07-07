from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Skill(BaseModel):
    name: str
    level: str


class Address(BaseModel):
    city: str
    state: str


class Student(BaseModel):
    name: str
    skills: list[Skill]
    age: int = Field(
        ge=18,
        le=30
    )
    address: Address


@app.post("/skills")
def create_skill(skill: Skill):
    return skill


@app.post("/students")
def create_student(student: Student):
    return student