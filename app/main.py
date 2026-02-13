from fastapi import FastAPI


<<<<<<< HEAD
from app.routers import achievements, forums, games, groups, guides, tier_list, users, wiki
=======
from app.routers import users, games, forums, guides, messages_instance, chats, builds, discussion
>>>>>>> d5f2d159d5ade8423f85afd3da65c6ac6722c5f8

app = FastAPI(debug=True)

app.include_router(users.router)
app.include_router(games.router)
app.include_router(forums.router)
<<<<<<< HEAD
app.include_router(wiki.router)
app.include_router(guides.router)
app.include_router(achievements.router)
app.include_router(tier_list.router)
app.include_router(groups.router)
=======
app.include_router(guides.router)
app.include_router(messages_instance.router)
app.include_router(chats.router)
app.include_router(builds.router)
app.include_router(discussion.router)
>>>>>>> d5f2d159d5ade8423f85afd3da65c6ac6722c5f8

@app.get("/")
async def root():
    return {"message": "Welcome to PManager API"}
