from sqlalchemy import create_engine, text, Column, Integer, String, Boolean, DateTime, ForeignKey, Float,TIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy import Enum
from schemas import Roles

from authentication import verify_password

Base = declarative_base()
engine = create_engine("mysql://root:tiger@localhost/lms",echo = True)
# Session = sessionmaker(bind=engine)
# session = Session()

class User(Base):
    __tablename__ = 'studentlogin'

    sid = Column(String(30), primary_key=True, index=True)
    roll_no = Column(String(30), nullable=False)
    password = Column(String(200), nullable=False)
    is_verified = Column(Boolean)
    roles = Column(Enum(Roles), default="student")
    join_date = Column(DateTime, default=func.now())

class Slots(Base):
    __tablename__ = 'slots'

    slotid = Column(String(10), nullable=False, primary_key=True, index=True)
    slottime = Column(String(10), nullable=False)


class Marks(Base):
    __tablename__ = "marks"

    sid = Column(Integer, primary_key=True, index=True)
    subid = Column(String(10), primary_key=True, index=True)
    score = Column(Integer)
    remarks = Column(String(20), primary_key=True, index=True)

class Enrolled(Base):

    __tablename__ = "enrolled"

    sid = Column(Integer, primary_key=True, index=True)
    subid = Column(String(10), primary_key=True, index=True)
    total = Column(Integer)


class Sublist(Base):
    __tablename__ = 'sublist'

    subid = Column(String(10), nullable=False, primary_key=True, index=True)
    subname = Column(String(20), nullable=False)
    facid = Column(Integer, nullable=False)
    slotid = Column(String(10), nullable=False)

class Teacher(Base):
    __tablename__ = 'teacherdet'

    Tid = Column(Integer, primary_key=True, nullable=False)
    Tname = Column(String(50), nullable=False)
    Designation = Column(String(10))
    Age = Column(Integer)
    Address = Column(String(60), nullable=False)
    Email_office = Column(String(50))
    Email_home = Column(String(50))
    Phone = Column(Integer)

class StudentDet(Base):
    __tablename__ = 'studentdet'

    Sid = Column(String(15), primary_key=True)
    Roll_no = Column(Integer, nullable=False)
    Sname = Column(String(50), nullable=False)
    Class = Column(String(2), nullable=False)
    Age = Column(Integer, nullable=False)
    Address = Column(String(60))
    Email_home = Column(String(50))
    Phone = Column(Integer)



def create_login(username, password):
    with Session(engine) as session:
        res = session.query(User).filter(User.sid==username).first()
        if res:
            return "already"
        else:
            usr = User(sid=username,roll_no=username,password=password)
            session.add(usr)
            session.commit()
            return "sucessfull"

def authenticate_login(username, password):
    with Session(engine) as session:
        res = session.query(User).filter(User.sid==username).first()
        if res:
            if verify_password(password, res.password) :
                return True
        return False

    
def admission(data):
    with Session(engine) as session:
        try:
            res = session.query(StudentDet).filter(StudentDet.Sid==data['Sid']).first()
            if res:
                return "already"
            else:
                new_student = StudentDet(
                    Sid=data['Sid'],
                    Roll_no=data["Roll_no"],
                    Sname=data["Sname"],
                    Class=data["Class"],
                    Age=data["Age"],
                    Address=data["Address"],
                    Email_home=data["Email_home"],
                    Phone=data["Phone"]
                )
                session.add(new_student)
                session.commit()
                return "sucessfull"
        except :
            return "Error"
        
def new_teacher(data):
    with Session(engine) as session:
        try:
            res = session.query(Teacher).filter(Teacher.Tid==data["Tid"]).first()
            if res:
                return "already"
            else:
                new_teacher = Teacher(
                    Tid=data["Tid"],
                    Tname=data["Tname"],
                    Designation=data["Designation"],
                    Age=data["Age"],
                    Address=data["Address"],
                    Email_office=data["Email_office"],
                    Email_home=data["Email_home"],
                    Phone=data["Phone"]
                )
                session.add(new_teacher)
                session.commit()
                return "sucessfull"
        except:
            return "Error"
    


def student_deatils():
    with Session(engine) as session:
        try:
            res = res = session.query(StudentDet).first()
            if res:
                return res
            else:
                return False
        except:
            return "Error"
    
def teacher_deatils():
    with engine.connect() as conn:
        result = conn.execute(text("select * from teacherdet"))
        return result.all()
    
def subject_list():
    with engine.connect() as conn:
        result = conn.execute(text("select * from sublist"))
        return result.all()
    
if __name__ =="__main__":
    Base.metadata.create_all(engine)