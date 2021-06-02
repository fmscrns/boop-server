from app.main import db

def model_save_changes(data):
    db.session.add(data)
    db.session.commit()

def table_save_changes(statement):
    db.session.execute(statement)
    db.session.commit()