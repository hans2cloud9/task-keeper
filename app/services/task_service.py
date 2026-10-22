from sqlalchemy.orm import Session, selectinload

from app.models import Tag, Task


def list_tasks(db: Session) -> list[Task]:
    # 태그를 selectinload로 한 번에 가져옵니다. 지연 로딩이면 직렬화할 때
    # 할 일마다 태그 조회 쿼리가 따로 실행됩니다(N+1).
    tasks = db.query(Task).options(selectinload(Task.tags)).all()
    return tasks


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, title: str, tag_names: list[str]) -> Task:
    tags: list[Tag] = []
    for name in tag_names:
        tag = db.query(Tag).filter(Tag.name == name).first()
        if tag is None:
            tag = Tag(name=name)
            db.add(tag)
        tags.append(tag)

    task = Task(title=title, tags=tags)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
