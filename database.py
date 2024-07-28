from sqlalchemy import create_engine, text, Column, Integer, String, Boolean, DateTime, ForeignKey, Float,TIME, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from sqlalchemy import Enum
from schemas import Roles, Level
from passlib.context import CryptContext



Base = declarative_base()
engine = create_engine("mysql://root:tiger@localhost/lms",echo = True)
Session = sessionmaker(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


class User(Base):
    __tablename__ = 'all_login'

    uid = Column(String(30), primary_key=True, index=True)
    password = Column(String(200), nullable=False)
    role = Column(Enum(Roles), nullable=False)
    join_date = Column(DateTime, default=func.now())


class Marks(Base):
    __tablename__ = "marks"

    sid = Column(String(30), primary_key=True, index=True)
    subid = Column(String(10), primary_key=True, index=True)
    score = Column(Integer)
    remarks = Column(String(20), primary_key=True, index=True)

class Enrolled(Base):

    __tablename__ = "enrolled"

    sid = Column(String(30), primary_key=True, index=True)
    subid = Column(String(10), primary_key=True, index=True)
    total = Column(Integer)


class Sublist(Base):
    __tablename__ = 'sublist'

    subid = Column(String(10), nullable=False, primary_key=True, index=True)
    subname = Column(String(30), nullable=False)
    Tid = Column(String(20), nullable=False)
    credit = Column(Integer, nullable=False)
    level = Column(Enum(Level), nullable=False)

class Teacher(Base):
    __tablename__ = 'teacherdet'

    Tid = Column(String(30), primary_key=True, nullable=False)
    Tname = Column(String(50), nullable=False)
    Designation = Column(String(10))
    Age = Column(Integer)
    Address = Column(String(60), nullable=False)
    Email_office = Column(String(50))
    Email_home = Column(String(50))
    Phone = Column(BigInteger)

class StudentDet(Base):
    __tablename__ = 'studentdet'

    Sid = Column(String(15), primary_key=True)
    Roll_no = Column(Integer, nullable=False)
    Sname = Column(String(50), nullable=False)
    Class = Column(String(2), nullable=False)
    Age = Column(Integer, nullable=False)
    Address = Column(String(60))
    Email_home = Column(String(50))
    Phone = Column(BigInteger)



def create_login(user):
    with Session() as session:
        res = session.query(User).filter(User.uid==user.username).first()
        if res:
            return "already"
        else:
            usr = User(uid=user.username,password=get_password_hash(user.password), role=user.role)
            session.add(usr)
            session.commit()
            return "successful"

def authenticate_login(username, password):
    with Session() as session:
        res = session.query(User).filter(User.uid==username).first()
        if res and verify_password(password,res.password) :
            return res.role
        return False

    
def add_new_student(data):
    with Session() as session:
        try:
            res = session.query(StudentDet).filter(StudentDet.Sid==data['Sid']).first()
            if res:
                return "Already"
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
                return "successful"
        except :
            return "Error"
        
def add_new_teacher(data):
    with Session() as session:
        try:
            res = session.query(Teacher).filter(Teacher.Tid==data.Tid).first()
            if res:
                return "already"
            else:
                new_teacher = Teacher(
                    Tid=data.Tid,
                    Tname=data.Tname,
                    Designation=data.Designation,
                    Age=data.Age,
                    Address=data.Address,
                    Email_office=data.Email_office,
                    Email_home=data.Email_home,
                    Phone=data.Phone
                )
                session.add(new_teacher)
                session.commit()
                return "successful"
        except:
            return "Error"
        
def add_new_subject(data):
    msg = None
    try:
        with Session() as session:
            res = session.query(Sublist).filter(Sublist.subid==data.Sub_id).first()
            if res:
                msg = "Already"
            else:
                new_teacher = Sublist(
                    subid = data.Sub_id,
                    subname = data.Sub_name,
                    Tid = data.Faculty_id,
                    credit = data.Course_credit,
                    level = data.Course_level
                )
                session.add(new_teacher)
                session.commit()
                msg = "Successful"
    except :
        msg = "Error"
    return msg


def add_student_marks(data_list):
    msg = None
    try:
        with Session() as session:
            new_marks = []
            for data in data_list:
                new_marks.append(Marks(
                    sid = data.sid,
                    subid = data.subid,
                    score = data.score,
                    remarks = data.remarks
                ))
            session.add_all(new_marks)
            session.commit()
            msg = "Successful"
    except Exception as e:
        msg = e
    return msg



    


def all_student_deatils():
    with Session() as session:
        try:
            res = session.query(StudentDet).all()
            if res:
                return res
            else:
                return False
        except:
            return "Error"
        
def student_deatils(sid):
    with Session() as session:
        try:
            res = session.query(StudentDet).filter(StudentDet.Sid==sid).first()
            if res:
                return res
            else:
                return "Empty"
        except:
            return "Error"
        
    
def all_teacher_deatils():
    with Session() as session:
        try:
            res = session.query(Teacher).first()
            if res:
                return res
            else:
                return "Empty"
        except:
            return "Error"
        
def teacher_deatils(tid):
    with Session() as session:
        try:
            res = session.query(Teacher).filter(Teacher.Tid==tid).first()
            if res:
                return res
            else:
                return "Empty"
        except:
            return "Error"
        
def get_my_marks(sid):
    with Session() as session:
        try:
            res = session.query(Marks).filter(Marks.sid==sid).all()
            if res:
                return res
            else:
                return "Empty"
        except:
            return "Error"
        

def get_my_report(sid):
    try:
        with Session() as session:
            res = session.query(Enrolled).filter(Enrolled.sid==sid).all()
            if res:
                return res
            else:
                return "Empty"
    except:
        return "Error"
    
def subject_list():
    try:
        with Session() as session:
            res = session.query(Sublist).all()
            if res:
                return res
            else:
                return "Empty"
    except:
        return "Error"
    
def create_ulogin(data):
    try:
        with Session() as session:
            res = session.query(User).filter(User.uid==data.username).first()
            if res:
                return "Already"
            res = session.query(StudentDet).filter(StudentDet.Sid==data.username).first()
            if res:
                usr = User(uid=data.username,password=get_password_hash(data.password), role=Roles.student)
                session.add(usr)
                session.commit()
                return f"Created login {data.username} as {Roles.student}"
            res = session.query(Teacher).filter(Teacher.Tid==data.username).first()
            if res:
                usr = User(uid=data.username,password=get_password_hash(data.password), role=Roles.teacher)
                session.add(usr)
                session.commit()
                return f"Created login {data.username} as {Roles.teacher}"

            else:
                return False
    except:
        return "Error"
  
def remove_student(sid):
    try:
        with Session() as session:
            res = session.query(StudentDet).filter(StudentDet.Sid==sid).first()
            if res:
                session.delete(res)
                session.commit()
                return f"Deleted {sid}"
            else:
                return False
    except:
        return "Error"
        
def remove_faculty(tid):
    try:
        with Session() as session:
            res = session.query(Teacher).filter(Teacher.Tid==tid).first()
            if res:
                session.delete(res)
                session.commit()
                return f"Deleted {tid}"
            else:
                return False
    except:
        return "Error"
    

    
if __name__ =="__main__":
    Base.metadata.create_all(engine)
