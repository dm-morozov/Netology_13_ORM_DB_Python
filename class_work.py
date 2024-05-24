from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

DSN = 'postgresql://postgres:20145@localhost:5432/ORM_ClassWork' # DSN - data source name
engine = create_engine(DSN)
Base = declarative_base()

class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), unique = True)

    # homework = relationship("Homework", back_population = "course")

    def __str__(self):
        return f"\nCourse (ID: {self.id}): {self.name}"


class Homework(Base):
    __tablename__ = 'homework'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    course_id = Column(Integer, ForeignKey('course.id', ondelete="CASCADE"), nullable=False)

    # course = relationship("Course", back_population = "homework")
    course = relationship("Course", backref="homeworks")

    def __str__(self):
        return f"\nHomework (ID: {self.id}): {self.number} {self.description}, {self.course_id}"


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

course1 = Course(name = "Python")
course2 = Course(name = "Java")
# session.add(course1)
# session.add(course2)
session.add_all([course1, course2])
session.commit()
print(course1, course2)

hm1 = Homework(number = 1, description = "Легкая домашняя работа", course = course1)
hm2 = Homework(number = 2, description = "Сложная домашняя работа", course = course2)
session.add_all([hm1, hm2])
session.commit()
print(hm1, hm2)

for course in session.query(Course).all():
    print(course)

for hm in session.query(Homework).all():
    print(hm)

# Фильтруем данные

for c in session.query(Homework).filter(Homework.number > 1).all():
    print("Номер больше одного:", c)

for hw in session.query(Homework).filter(Homework.description.like('%Лег%')).all():
    print(f"В description содержится Лег: {hw}")

for course in session.query(Course).join(Homework.course).filter(Homework.number == 2).filter(Homework.description.like('%Слож%')).all():
    print(course)

subquery = session.query(Homework).filter(Homework.description.like('%Слож%')).subquery()
for course in session.query(Course).join(subquery, Course.id == subquery.c.course_id).all():
    print("Вывод через подзапрос:",course)

session.query(Course).filter(Course.name == 'Java').update({'name': 'JavaScript'})
session.commit()
for course in session.query(Course).filter(Course.id == 2).all():
    print(f"\nПереименовали Java на: {course.name}")

session.query(Course).filter(Course.name == 'JavaScript').delete()
session.commit()
for course in session.query(Course).all():
    print(f"\nВыведем все курсы после удаления: {course}")

session.close()