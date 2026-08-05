from app.db import models

def test_db_connection(db):
    # Verify we can persist and query records on SQLite Base engine
    test_user = models.User(
        email="testdb@example.com",
        hashed_password="securepasswordhash",
        full_name="Database Test User",
        role="User"
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    db_user = db.query(models.User).filter(models.User.email == "testdb@example.com").first()
    assert db_user is not None
    assert db_user.id == test_user.id
    assert db_user.full_name == "Database Test User"
    assert db_user.role == "User"
