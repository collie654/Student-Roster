# backend/seed.py
"""Run with: docker compose exec backend python seed.py"""
from app.database import SessionLocal
from app.models import District, Student, User
from app.auth import hash_password
from datetime import date
 
 
def seed():
    db = SessionLocal()
    try:
        # Districts
        allegheny = District(name="Allegheny Valley SD")
        boyertown = District(name="Boyertown Area SD")
        db.add_all([allegheny, boyertown])
        db.flush()  # assigns IDs without committing
 
        # Students
        students = [
            Student(first_name="Jordan",  last_name="Rivera",   grade_level=9,
                    date_of_birth=date(2010, 3, 15), district_id=allegheny.id),
            Student(first_name="Morgan",  last_name="Chen",     grade_level=10,
                    date_of_birth=date(2009, 7, 22), district_id=allegheny.id),
            Student(first_name="Noah",  last_name="Taylor",  grade_level=11,
                    date_of_birth=date(2008, 1, 8),  district_id=boyertown.id),
            Student(first_name="Casey",   last_name="Williams", grade_level=12,
                    date_of_birth=date(2007, 9, 30), district_id=boyertown.id),
        ]
        db.add_all(students)
 
        # Admin user (use a real hashed password — never plaintext)
        admin = User(
            email="admin@roster.dev",
            hashed_password=hash_password("admin1234"),
            is_admin=True,
        )
        db.add(admin)
        db.commit()
        print("Seed data created successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding: {e}")
    finally:
        db.close()
 
 
if __name__ == "__main__":
    seed()
