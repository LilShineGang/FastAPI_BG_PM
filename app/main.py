from fastapi import FastAPI


from app.routers import users, games, forums, wiki

app = FastAPI(debug=True)

app.include_router(users.router)
app.include_router(games.router)
app.include_router(forums.router)
app.include_router(wiki.router)

@app.get("/")
async def root():
    return {"message": "Welcome to PManager API"}
