from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..dependencies import get_db, get_current_user, require_admin
from .. import models, schemas
 
 # creates /students router endpoint
router = APIRouter(prefix="/students", tags=["Students"])
 
 
# list students
@router.get("/", response_model=list[schemas.StudentResponse])
def list_students(
    district_id: Optional[int] = Query(None, description="Filter by district"),
    grade_level: Optional[int] = Query(None, description="Filter by grade"),
    skip:        int           = Query(0,    ge=0, description="Pagination offset"),
    limit:       int           = Query(50,   ge=1, le=200, description="Max results"),
    db:          Session       = Depends(get_db),
    _:           models.User   = Depends(get_current_user),  # auth required
):
    """List students with optional filtering and pagination."""
    query = db.query(models.Student)
    if district_id is not None:
        query = query.filter(models.Student.district_id == district_id)
    if grade_level is not None:
        query = query.filter(models.Student.grade_level == grade_level)
    return query.order_by(models.Student.last_name).offset(skip).limit(limit).all()
 
 
# query one student
@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(
    student_id: int,
    db:         Session     = Depends(get_db),
    _:          models.User = Depends(get_current_user),
):
    student = db.get(models.Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    return student
 
 
# create student
@router.post("/", response_model=schemas.StudentResponse,
             status_code=status.HTTP_201_CREATED)
def create_student(
    student_in: schemas.StudentCreate,
    db:         Session     = Depends(get_db),
    _:          models.User = Depends(require_admin),  # admin only
):
    """create new student, admins only"""
    # verify district exists
    district = db.get(models.District, student_in.district_id)
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
 
    student = models.Student(**student_in.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)  # reload from DB to get auto-generated id and timestamps
    return student
 
 
# update student record
@router.patch("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    updates:    schemas.StudentUpdate,
    db:         Session     = Depends(get_db),
    _:          models.User = Depends(require_admin),
):
    """update student record, admins only"""
    student = db.get(models.Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
 
    # model_dump is only returning fields the client sent
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(student, field, value)
 
    db.commit()
    db.refresh(student)
    return student
 
 
# delete student record
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    db:         Session     = Depends(get_db),
    _:          models.User = Depends(require_admin),
):
    """delete student record, admins only"""
    student = db.get(models.Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
    db.delete(student)
    db.commit()
    # 204 No Content — return nothing
