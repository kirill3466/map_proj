
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db.core import Base
from models import TimeStampMixin


class Post(Base, TimeStampMixin):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    images = relationship("PostImage", back_populates="post")


class PostImage(Base, TimeStampMixin):
    __tablename__ = 'post_images'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))

    post = relationship("Post", back_populates="images")
