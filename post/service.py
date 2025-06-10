from typing import Optional

from sqlalchemy.orm import Session

from .models import Post
from .schema import PostCreate, PostRead, PostUpdate


def get(
    *,
    db_session: Session,
    post_id: int
) -> Optional[Post]:
    return db_session.query(
        Post
    ).filter(Post.id == post_id).one_or_none()


def get_all(*, db_session: Session) -> list[PostRead]:
    posts = db_session.query(Post).all()
    return posts


def get_all_from_user(
    *,
    db_session: Session,
    user_id: int
) -> list[Post]:
    return db_session.query(
        Post
    ).filter(Post.owner_id == user_id).all()


def create(
    *,
    db_session: Session,
    post_in: PostCreate,
    user_id: int
) -> Post:
    post = Post(
        title=post_in.title,
        content=post_in.content,
        owner_id=user_id
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    return post


def update(
    *,
    db_session: Session,
    post: Post,
    post_in: PostUpdate
) -> Post:
    update_data = post_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    db_session.commit()
    return post


def delete(*, db_session: Session, post_id: int) -> None:
    post = db_session.query(Post).filter(Post.id == post_id).first()
    db_session.delete(post)
    db_session.commit()
