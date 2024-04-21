from wiki_keep.database.DBSession import SessionLocal
from wiki_keep.database.Schemas import User, Articles, Tags, UserTagsArticles
import bcrypt
from datetime import datetime
import os
from wiki_keep.SentimentClassification import get_keyword_sentiment
from wiki_keep.Configuration import temp_file_path

if not os.path.exists(temp_file_path):
    os.mkdir(temp_file_path)

class DBInit:
    def __init__(self):
        try:
            self.initialize_db()
        except Exception as e:
            print(e)

    def initialize_db(self):
        try:
            self.db = SessionLocal()
            self.db.__init__()
        except Exception as e:
            print(e)

    def register_user(self, username, password, email):
        try:
            session = SessionLocal()
            # Create a new User instance
            hashed_password = self.hash_password(password)

            new_user = User(username=username, email=email, hashedpassword=hashed_password)

            # Add the new user to the session
            session.add(new_user)

            # Commit the transaction to persist the changes to the database
            session.commit()
            session.close()
            return new_user
        except Exception as e:
            print(e)


    def verify_logged_in_user(self,username, password):
        try:
            valid_user = False
            # Query the User table to retrieve the user with the provided username
            session = SessionLocal()

            user = session.query(User).filter(User.username == username).first()

            lbool_password = self.verify_password(password, user.hashedpassword)

            if lbool_password:
                valid_user = True
            else:
                valid_user = False
            session.close()
            return valid_user, user.id
        except Exception as e:
            print(e)

    # Function to hash a password
    def hash_password(self, password: str) -> str:
        try:
            # Generate a salt and hash the password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed_password.decode('utf-8')
        except Exception as e:
            print(e)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            print(e)

    def get_user_details(self, username):
        try:
            session = SessionLocal()
            user = session.query(User).filter(User.username == username).first()
            session.close()
            return user
        except Exception as e:
            print(e)

    def save_article(self, title, content, user_id, tags):
        try:
            time_stamp = datetime.now()

            session = SessionLocal()

            # save content in the directory
            lstr_content_path = temp_file_path + "/" + title + ".txt"
            with open(lstr_content_path, "w") as file:
                file.write(content)

            sentiment = get_keyword_sentiment(title)

            # Articles
            new_article = Articles(title=title, content=lstr_content_path, created_timestamp=time_stamp,
                                   updated_timestamp=time_stamp, sentiment=sentiment)
            session.add(new_article)
            session.commit()

            # Tags

            tag_detail = session.query(Tags).filter(Tags.tag_name == tags).first()
            if tag_detail == None:
                new_tag = Tags(tag_name=tags)
                session.add(new_tag)
                session.commit()
                tag_detail = new_tag
            # User Tags
            new_user_tags = UserTagsArticles(user_id= user_id, tags_id= tag_detail.id, articles_id=new_article.id)
            session.add(new_user_tags)
            session.commit()
            session.close()

            if new_article and tag_detail and new_user_tags:
                return True
            else:
                return False

        except Exception as e:
            print(e)

    def retrive_tags(self, user_id:int):
        try:
            session = SessionLocal()

            user_tags = session.query(UserTagsArticles).filter(UserTagsArticles.user_id == user_id).all()

            tag_ids = [user_tag.tags_id for user_tag in user_tags]

            tags = session.query(Tags).filter(Tags.id.in_(tag_ids)).all()

            tag_list = []

            for tag in tags:
                tag_dict = {
                    "id": tag.id,
                    "tag_name": tag.tag_name
                    # Add more fields if needed
                }
                tag_list.append(tag_dict)

            session.close()
            return tag_list

        except Exception as e:
            print(e)

    def retirve_articles_based_on_tags_users(self, tag:str, user_id:int):
        try:
            session = SessionLocal()

            if tag == "--":
                user_tags_articles = session.query(UserTagsArticles).filter(
                    UserTagsArticles.user_id == user_id).all()

                combined_query = session.query(Articles).filter(Articles.id.in_([user_tags_article_obj.articles_id
                                                                                 for user_tags_article_obj in
                                                                                 user_tags_articles])).all()
            else:


                tags = session.query(Tags).filter(Tags.tag_name == tag).first()

                user_tags_articles = session.query(UserTagsArticles).filter(
                    UserTagsArticles.user_id == user_id,
                    UserTagsArticles.tags_id == tags.id
                ).all()

                combined_query = session.query(Articles).filter(Articles.id.in_([user_tags_article_obj.articles_id
                                                                for user_tags_article_obj in user_tags_articles])).all()

            articles = []

            for article in combined_query:
                file_path = article.content
                with open(file_path, "r") as file:
                    # Read the entire contents of the file
                    file_contents = file.read()
                tag_dict = {
                    "title": article.title,
                    "content": file_contents,
                    "sentiment": article.sentiment
                    # Add more fields if needed
                }
                articles.append(tag_dict)

            session.close()
            return articles



        except Exception as e:
            print(e)