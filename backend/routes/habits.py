from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Habit, User
from schemas import HabitCreate, HabitUpdate, HabitResponse
from database import get_db
from routes.auth_utils import get_current_user  

router = APIRouter()

# ✅ Create a new habit
@router.post("/", response_model=HabitResponse)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_habit = Habit(**habit.dict(), user_id=current_user.id)  
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

# ✅ Get all habits for the logged-in user
@router.get("", response_model=list[HabitResponse])  
@router.get("/", response_model=list[HabitResponse])
def get_habits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Habit).filter(Habit.user_id == current_user.id).all()

# ✅ Get a single habit by ID
@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

# ✅ Update a habit
@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit_update: HabitUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    for key, value in habit_update.dict(exclude_unset=True).items():
        setattr(habit, key, value)

    db.commit()
    db.refresh(habit)
    return habit

# ✅ Delete a habit
@router.delete("/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted successfully"}

