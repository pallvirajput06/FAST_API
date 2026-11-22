
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
    computed_field
)
import json
from pathlib import Path as FilePath


app = FastAPI(title="Student Management API")


# JSON file location
FILE_PATH = FilePath(__file__).parent / "Student.json"


# ---------------------------------
# Helper Functions
# ---------------------------------

def load_data():
    if not FILE_PATH.exists():
        return {}

    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


# ---------------------------------
# HOME
# ---------------------------------

@app.get("/")
def home():
    return {
        "message": "Hello Pallavi! FastAPI is working."
    }


# ---------------------------------
# GET ALL STUDENTS
# ---------------------------------

@app.get("/Student")
def get_students():
    return load_data()


# ---------------------------------
# GET STUDENT BY ID
# ---------------------------------

@app.get("/Student/{student_id}")
def get_student(
    student_id: str = Path(
        ...,
        description="The ID of the student",
        examples=["S001"]
    )
):
    data = load_data()

    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return data[student_id]


# ---------------------------------
# FILTER STUDENTS
# ---------------------------------

@app.get("/filter")
def filter_student(
    course: str | None = Query(
        None,
        description="Show students from a particular course",
        examples=["Python"]
    )
):
    data = load_data()

    if course is None:
        return data

    filtered = {}

    for student_id, info in data.items():
        if info["course"].lower() == course.lower():
            filtered[student_id] = info

    return filtered


# ---------------------------------
# SORT STUDENTS
# ---------------------------------

SORT_FIELDS = ["marks", "age", "name"]
SORT_ORDER = ["asc", "desc"]


@app.get("/sort")
def sort_students(
    sort_by: str = Query(
        ...,
        description="Sort by marks, name, or age",
        examples=["marks"]
    ),
    order: str = Query(
        "asc",
        description="Sort order: asc or desc"
    )
):
    if sort_by not in SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by. Choose from {SORT_FIELDS}"
        )

    if order not in SORT_ORDER:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid order. Choose from {SORT_ORDER}"
        )

    data = load_data()

    students = []

    for student_id, info in data.items():
        student = info.copy()
        student["id"] = student_id
        students.append(student)

    reverse = (order == "desc")

    sorted_students = sorted(
        students,
        key=lambda s: s[sort_by],
        reverse=reverse
    )

    return sorted_students


# ---------------------------------
# PAGINATION
# ---------------------------------

@app.get("/paginate")
def paginate_student(
    page: int = Query(
        1,
        ge=1,
        description="Page number starting from 1"
    ),
    limit: int = Query(
        2,
        ge=1,
        le=100,
        description="Number of students per page"
    )
):
    data = load_data()

    students = []

    for student_id, info in data.items():
        student = info.copy()
        student["id"] = student_id
        students.append(student)

    start = (page - 1) * limit
    end = start + limit

    page_students = students[start:end]

    total_students = len(students)

    return {
        "page": page,
        "limit": limit,
        "total_students": total_students,
        "total_pages": (total_students + limit - 1) // limit,
        "students": page_students
    }


# ---------------------------------
# PYDANTIC STUDENT MODEL
# ---------------------------------

class Student(BaseModel):

    id: str = Field(
        ...,
        examples=["S001"]
    )

    name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )

    age: int = Field(
        ...,
        gt=0,
        le=100
    )

    course: str = Field(
        ...,
        max_length=50
    )

    marks: int = Field(
        ...,
        ge=0,
        le=100
    )

    email: EmailStr

    # Custom name validation
    @field_validator("name")
    @classmethod
    def check_name(cls, value):

        if not value.replace(" ", "").isalpha():
            raise ValueError(
                "Name must contain only letters and spaces"
            )

        return value.title()

    # Automatically calculate grade
    @computed_field
    @property
    def grade(self) -> str:

        if self.marks >= 90:
            return "A+"

        elif self.marks >= 80:
            return "A"

        elif self.marks >= 70:
            return "B"

        elif self.marks >= 60:
            return "C"

        else:
            return "F"


# ---------------------------------
# CREATE STUDENT (POST)
# ---------------------------------

@app.post("/create", status_code=201)
def create_student(student: Student):

    data = load_data()

    if student.id in data:
        raise HTTPException(
            status_code=400,
            detail=f"Student with ID '{student.id}' already exists"
        )

    data[student.id] = student.model_dump(
        exclude={"id", "grade"}
    )

    save_data(data)

    return {
        "message": "Student created successfully",
        "student": student
    }


# ---------------------------------
# STUDENT UPDATE MODEL
# ---------------------------------

class StudentUpdate(BaseModel):

    name: str | None = Field(
        None,
        min_length=2,
        max_length=50
    )

    age: int | None = Field(
        None,
        gt=0,
        le=100
    )

    course: str | None = Field(
        None,
        max_length=50
    )

    marks: int | None = Field(
        None,
        ge=0,
        le=100
    )

    email: EmailStr | None = None

    @field_validator("name")
    @classmethod
    def check_name(cls, value):

        if value is not None:
            if not value.replace(" ", "").isalpha():
                raise ValueError(
                    "Name must contain only letters and spaces"
                )

            return value.title()

        return value


# ---------------------------------
# UPDATE STUDENT (PUT)
# ---------------------------------

@app.put("/update/{student_id}")
def update_student(
    student_update: StudentUpdate,
    student_id: str = Path(
        ...,
        description="The ID of the student",
        examples=["S001"]
    )
):

    data = load_data()

    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID '{student_id}' not found"
        )

    # Step 1: Get existing student
    existing = data[student_id].copy()

    # Step 2: Get only fields sent by client
    update = student_update.model_dump(
        exclude_unset=True
    )

    # Step 3: Apply updates
    for key, value in update.items():
        existing[key] = value

    # Step 4: Validate complete updated student
    student = Student(
        id=student_id,
        **existing
    )

    # Step 5: Save updated data
    data[student_id] = student.model_dump(
        exclude={"id", "grade"}
    )

    save_data(data)

    return {
        "message": "Student updated successfully",
        "student": student
    }


# ---------------------------------
# DELETE STUDENT
# ---------------------------------

@app.delete("/delete/{student_id}")
def delete_student(
    student_id: str = Path(
        ...,
        description="The ID of the student",
        examples=["S001"]
    )
):

    data = load_data()

    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID '{student_id}' not found"
        )

    del data[student_id]

    save_data(data)

    return {
        "message": f"Student '{student_id}' deleted successfully"
    }
