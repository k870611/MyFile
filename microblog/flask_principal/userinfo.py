from app import login_manager
from app.db import Base,engine,session
from sqlalchemy import Column,String,Integer,create_engine
from sqlalchemy_utils.types.choice import ChoiceType
from flask_login import UserMixin
from permissions import ADMIN,ROLES

class User(Base,UserMixin):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True)
    user = Column(String(16))
    password = Column(String(16))
    roles = Column(ChoiceType(ROLES),default=ADMIN)


@login_manager.user_loaded
def user_loaded(id):
    return session.query(User).filter_by(id=id).first()

Base.metadata.create_all(engine)