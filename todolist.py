from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db')
Base = declarative_base()


class Table(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def today_tasks():
    today = datetime.today().date()
    tasks = session.query(Table).filter(Table.deadline == today).order_by(Table.deadline).all()
    print(f"Today {today.strftime('%d %b')}:")
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        counter = 1
        for row in tasks:
            print(f"{counter}. {row.task}")
            counter += 1


def week_tasks():
    today = datetime.today().date()
    tasks = session.query(Table).order_by(Table.deadline).all()
    for n in range(7):
        day = today + timedelta(days=n)
        counter = 1
        print(day.strftime('%A %d %b') + ":")
        for row in tasks:
            if row.deadline == day:
                print(f"{counter}. {row.task}")
                counter += 1
        if counter == 1:
            print("Nothing to do!")
        print()


def all_tasks():
    tasks = session.query(Table).order_by(Table.deadline).all()
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        counter = 1
        for row in tasks:
            print(f"{counter}. {row.task}. {row.deadline.strftime('%d %b')}")
            counter += 1


def missed_tasks():
    today = datetime.today().date()
    tasks = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
    print("Missed tasks:")
    if len(tasks) == 0:
        print("Nothing is missed!")
    else:
        counter = 1
        for row in tasks:
            print(f"{counter}. {row.task}. {row.deadline.strftime('%d %b')}")
            counter += 1


def add_task(task, deadline):
    _task = Table(task=task, deadline=deadline)
    session.add(_task)
    session.commit()


def delete_task():
    tasks = session.query(Table).order_by(Table.deadline).all()
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        print("Choose the number of the task you want to delete:")
        counter = 1
        for row in tasks:
            print(f"{counter}. {row.task}. {row.deadline.strftime('%d %b')}")
            counter += 1
        num = 0
        while num < 1 or num > len(tasks):
            num = int(input())
        task_to_delete = tasks[num - 1]
        session.delete(task_to_delete)
        session.commit()
        print("The task has been deleted!")


def print_menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")


while True:
    print_menu()
    cmd = input()
    print()

    if cmd == "1":
        today_tasks()
    elif cmd == "2":
        week_tasks()
    elif cmd == "3":
        all_tasks()
    elif cmd == "4":
        missed_tasks()
    elif cmd == "5":
        print("Enter task:")
        new_task = input()
        print("Enter deadline: [YYYY-MM-DD]")
        new_deadline = input()
        add_task(new_task, datetime.strptime(new_deadline, "%Y-%m-%d"))
    elif cmd == "6":
        delete_task()
    elif cmd == "0":
        break

    print()
