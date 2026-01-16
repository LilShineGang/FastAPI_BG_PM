from fastapi import FastAPI

from app.routers import users, games

app = FastAPI(debug=True)

app.include_router(users.router)
app.include_router(games.router)

@app.get("/")
async def root():
    return {"message": "Welcome to PManager API"}
