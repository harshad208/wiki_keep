import json
from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi import FastAPI, WebSocket
from wiki_keep.BaseModels import User, SaveArticle
from .database.CRUD import DBInit
from wiki_keep.WikiSearch import WikiSearch
import websockets
from wiki_keep.SentimentClassification import get_keyword_sentiment

app = FastAPI()


@app.post("/register")
def register_user(user: User):
    try:
        new_user = None
        db_obj = DBInit()

        """ check if user exists """
        users_db = db_obj.get_user_details(user.username)

        if users_db:
            """Register a new user."""
            if user.username in users_db:
                raise HTTPException(status_code=400, detail="Username already exists")
        else:
            new_user = db_obj.register_user(username=user.username, password=user.password, email=user.email)

        if new_user is not None:
            return {"message": "User registered successfully"}
        else:
            return {"message": "Failed to new user registered"}
    except Exception as e:
        print(e)


@app.post("/login")
def login_user(user: User):
    try:
        db_obj = DBInit()

        lbool_user_found, user_id = db_obj.verify_logged_in_user(username=user.username, password=user.password)
        if not lbool_user_found:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        else:
            return {"message": "User logged in successfully","user_id":user_id}

    except Exception as e:
        print(e)


@app.get("/article")
def retrive_article(article:str):
    try:
        obj_wiki_search = WikiSearch()
        article_content = obj_wiki_search.wiki_search_article_ext(article)
        return {
            "title": article,
            "message": "Article content retrieved successfully",
            "content": article_content,
            "sentiment": get_keyword_sentiment(article)
        }
    except Exception as e:
        print(e)

@app.post("/save_article")
def save_article(save_article: SaveArticle):
    try:
        db_obj = DBInit()
        lbool_saved_article = db_obj.save_article(title=save_article.title, content=save_article.content,
                                                  user_id=save_article.user_id, tags=save_article.tag)
        return {
            "message": "article save successfully",
            "saved": lbool_saved_article
        }
    except Exception as e:
        print(e)


@app.get("/tags")
def tags_retrieve(user_id: int):
    try:
        obj_db = DBInit()
        tags = obj_db.retrive_tags(user_id)

        return {
            "message": "article save successfully",
            "saved": tags
        }

    except Exception as e:
        print(e)


@app.get("/filter_articles_on_tag")
def filter_articles_on_tag(tag: str, user_id: int):
    try:
        obj_db = DBInit()
        articles = obj_db.retirve_articles_based_on_tags_users(tag,user_id)
        return {
            "message": "article retrived successfully",
            "articles": articles
        }
    except Exception as e:
        print(e)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    db_obj = DBInit()
    obj_wiki_search = WikiSearch()
    try:
        while True:
            data = await websocket.receive_text()
            data_parts = json.loads(data)
            action = data_parts['action']
            if action == "search_article":
                article = data_parts['article']
                article_content = obj_wiki_search.wiki_search_article_ext(article)
                ldict_response = {
                    "title": article,
                    "message": "Article content retrieved successfully",
                    "content": article_content,
                    "sentiment":get_keyword_sentiment(article)
                }
                await websocket.send_text(json.dumps(ldict_response))

            elif action == "save_article":

                title, content, user_id, tags = (data_parts['title'], data_parts['content'], data_parts['user_id'],
                                                 data_parts['tag'])
                lbool_saved_article = db_obj.save_article(title=title, content=content,
                                                          user_id=user_id, tags=tags)
                ldict_response = {
                    "message": "article save successfully",
                    "saved": lbool_saved_article
                }
                await websocket.send_text(json.dumps(ldict_response))

            elif action == "retrieve_tags":
                user_id = int(data_parts['user_id'])
                tags = db_obj.retrive_tags(user_id)
                ldict_response =  {
                    "message": "article save successfully",
                    "saved": tags
                }
                await websocket.send_text(json.dumps(ldict_response))

            elif action == "filter_articles_on_tag":
                tag, user_id = data_parts['tag'], data_parts['user_id']
                articles = db_obj.retirve_articles_based_on_tags_users(tag, user_id)
                ldict_response = {
                    "message": "article retrieved successfully",
                    "articles": articles
                }
                await websocket.send_text(json.dumps(ldict_response))
            elif action == "register":
                new_user = None
                db_obj = DBInit()

                username = data_parts['username']
                password = data_parts['password']
                email = data_parts['email']  #
                """ check if user exists """
                users_db = db_obj.get_user_details(username)

                if users_db:
                    """Register a new user."""
                    if username in users_db:
                        raise HTTPException(status_code=400, detail="Username already exists")
                else:
                    new_user = db_obj.register_user(username=username, password=password, email=email)

                if new_user is not None:
                    ldict_response= {"message": "User registered successfully"}
                else:
                    ldict_response = {"message": "Failed to new user registered"}
                await websocket.send_text(json.dumps(ldict_response))  # Send back article content

            elif action == "login":
                db_obj = DBInit()

                username = data_parts['username']
                password = data_parts['password']
                lbool_user_found, user_id = db_obj.verify_logged_in_user(username=username, password=password)
                if not lbool_user_found:
                    raise HTTPException(status_code=401, detail="Invalid username or password")
                else:
                    ldict_response = {"message": "User logged in successfully", "user_id": user_id}
                await websocket.send_text(json.dumps(ldict_response))
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket disconnected")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
