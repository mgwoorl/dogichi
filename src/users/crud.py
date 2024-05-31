from sqlalchemy.orm import Session
from users import models, schemas

import uuid
from typing import Optional

def create_user(db: Session, user: schemas.CreateUser) -> Optional[models.usersT]:
    accessToken = str(uuid.uuid4())[:8]
    db.user = models.usersT(login=user.login, password=user.password, accessToken=accessToken)
    db.add(db.user)
    db.commit()
    db.refresh(db.user)
    return db.user

def find_user(db: Session, login: str) -> Optional[models.usersT]:
    user = db.query(models.usersT).filter_by(login=login).first()
    return user

def check_password(db: Session, login: str, password: str) -> Optional[models.usersT]:
    user = db.query(models.usersT).filter_by(login=login).first()

    if password == user.password:
        return user
    else:
        return None

def check_tokenByLogin(db: Session, login: str, accessToken: str) -> Optional[models.usersT]:
    user = db.query(models.usersT).filter_by(login=login).first()

    if accessToken == user.accessToken:
        return user
    else:
        return None

def find_token(db: Session, accessToken: str) -> Optional[models.usersT]:
    user = db.query(models.usersT).filter_by(accessToken=accessToken).first()

    return user

def create_task(db: Session, task: schemas.CreateTask) -> Optional[models.usersT]:
    db.task = models.tasksT(user_token=task.accessToken, colar_id=task.collar_id, text=task.task)
    db.add(db.task)
    db.commit()
    db.refresh(db.task)
    return db.task

def get_tasks(db: Session, collar_id: int) -> object:
    result = []
    sp = db.query(models.tasksT).filter_by(colar_id=collar_id).all()
    for i in sp:
        userLogin = find_loginByToken(db, i.user_token)
        result.append({"task_id": str(i.id), "user": userLogin, "task": str(i.text)})
    return result

def create_subscr(db: Session, subscr: schemas.CreateSubscribtion) -> Optional[models.subsT]:
    db.subscr = models.subsT(user_login=subscr.user_login, collar_id=subscr.collar_id, accessToken=subscr.accessToken)
    db.add(db.subscr)
    db.commit()
    db.refresh(db.subscr)
    return db.subscr

def find_subscr(db: Session, user_login: str, collar_id: str) -> Optional[models.subsT]:
    subscr = db.query(models.subsT).filter_by(user_login=user_login, collar_id=collar_id).first()
    return subscr

def delete_subscr(db: Session, subscr: schemas.DeleteSubscribtion) -> Optional[models.subsT]:
    subscr_to_delete = db.query(models.subsT).filter_by(user_login=subscr.user_login, collar_id=subscr.collar_id).first()
    db.delete(subscr_to_delete)
    db.commit()
    return True

def get_user_subscr(db: Session, user_login: str, accessToken: str) -> object:
    result = []
    sp = db.query(models.subsT).filter_by(user_login=user_login, accessToken=accessToken).all()
    for i in sp:
        result.append({"subscription_id": str(i.id), "user": user_login, "collar_id": str(i.collar_id)})
    return result
