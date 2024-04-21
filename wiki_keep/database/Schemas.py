from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from wiki_keep.database.DBSession import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashedpassword = Column(String, unique=True)


class Articles(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True)
    content = Column(String, unique=True, index=True)
    created_timestamp = Column(DateTime, unique=True, index=True)
    updated_timestamp = Column(DateTime, unique=True, index=True)
    sentiment = Column(String, index=True)


class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tag_name = Column(String, unique=True, index=True)


class UserTagsArticles(Base):
    __tablename__ = 'usertagsarticles'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    tags_id = Column(Integer, ForeignKey('tags.id'))
    articles_id = Column(Integer, ForeignKey('articles.id'))

    
