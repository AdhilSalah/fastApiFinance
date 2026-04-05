import os
import bcrypt
from dotenv import load_dotenv
from datetime import date, timedelta

# Load environment variables from .env file
load_dotenv()
from library.db.database import db_session
from library.db.users.models import User
from library.db.finance.models import Finance, FinanceType
from library.access.roles import Role

# User Seeding Configuration from .env
ADMIN_NAME = os.getenv("ADMIN_NAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

ANALYST_NAME = os.getenv("ANALYST_NAME")
ANALYST_EMAIL = os.getenv("ANALYST_EMAIL")
ANALYST_PASSWORD = os.getenv("ANALYST_PASSWORD")

USER_NAME = os.getenv("USER_NAME")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def seed_all() -> None:
    """Seed users and finance data."""
    with db_session() as db:
        
        # 1. Seed Users
        created_info = []
        if db.query(User).count() == 0:
            users_to_seed = [
                (ADMIN_NAME, ADMIN_EMAIL, ADMIN_PASSWORD, Role.admin.value),
                (ANALYST_NAME, ANALYST_EMAIL, ANALYST_PASSWORD, Role.analyst.value),
                (USER_NAME, USER_EMAIL, USER_PASSWORD, Role.viewer.value),
            ]


            for name, email, password, role in users_to_seed:
                existing = db.query(User).filter(User.email == email).first()
                if not existing:
                    user = User(
                        name=name,
                        email=email,
                        hashed_password=_hash(password),
                        is_active=True,
                        role=role,
                    )
                    db.add(user)
                    created_info.append((name, email, password, f" (ID: {len(created_info) + 1})"))
                    print(f"[seeder] Created user: {name} ({email})")
                else:
                    created_info.append((name, email, " (already exists)", f" (ID: {existing.id})"))

            db.flush()

        # 2. Seed Finance Data (only if empty to avoid duplicates on every reload)
        if db.query(Finance).count() == 0:
            today = date.today()
            finance_data = [
                (5000.0, FinanceType.income, "Salary", today - timedelta(days=25), "Monthly salary"),
                (1200.0, FinanceType.expense, "Rent", today - timedelta(days=24), "Apartment rent"),
                (150.0, FinanceType.expense, "Groceries", today - timedelta(days=20), "Weekly shopping"),
                (80.0, FinanceType.expense, "Utilities", today - timedelta(days=18), "Electricity bill"),
                (300.0, FinanceType.income, "Freelance", today - timedelta(days=15), "Web design project"),
                (60.0, FinanceType.expense, "Dining", today - timedelta(days=12), "Dinner with friends"),
                (45.0, FinanceType.expense, "Transport", today - timedelta(days=10), "Fuel refill"),
                (200.0, FinanceType.expense, "Groceries", today - timedelta(days=7), "Weekly shopping"),
                (100.0, FinanceType.expense, "Entertainment", today - timedelta(days=5), "Movie tickets"),
                (50.0, FinanceType.expense, "Transport", today - timedelta(days=2), "Bus pass"),
            ]

            for amount, ftype, category, fdate, notes in finance_data:
                entry = Finance(
                    amount=amount,
                    type=ftype,
                    category=category,
                    date=fdate,
                    notes=notes
                )
                db.add(entry)
            print(f"[seeder] Seeded {len(finance_data)} finance records.")
        
        print("\n--- Seeded Credentials ---")
        for name, email, pw, extra in created_info:
            print(f"{name:8} | Email: {email:20} | Password: {pw} {extra}")
        print("---------------------------\n")


def seed_admin() -> None:
    """Compatibility wrapper for original seeder call."""
    seed_all()
