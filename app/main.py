from fastapi import FastAPI


from app.routers import users, games, forums, guides, messages_instance, chats, builds, discussion

app = FastAPI(debug=True)

app.include_router(users.router)
app.include_router(games.router)
app.include_router(forums.router)
app.include_router(guides.router)
app.include_router(messages_instance.router)
app.include_router(chats.router)
app.include_router(builds.router)
app.include_router(discussion.router)

@app.get("/")
async def root():
    return {"message": "Welcome to PManager API"}
