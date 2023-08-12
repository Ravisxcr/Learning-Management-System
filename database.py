from sqlalchemy import create_engine, text

engine = create_engine("mysql://root:tiger@localhost/lms",echo = True)

def student_deatils():
    with engine.connect() as conn:
        result = conn.execute(text("select * from studentdet"))
        return result.all()
    
def teacher_deatils():
    with engine.connect() as conn:
        result = conn.execute(text("select * from teacherdet"))
        return result.all()