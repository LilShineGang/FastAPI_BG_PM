from fastapi import FastAPI


from app.routers import achievements, forums, games, groups, guides, tier_list, users, wiki

app = FastAPI(debug=True)

app.include_router(users.router)
app.include_router(games.router)
app.include_router(forums.router)
app.include_router(wiki.router)
app.include_router(guides.router)
app.include_router(achievements.router)
app.include_router(tier_list.router)
app.include_router(groups.router)

@app.get("/")
async def root():
    return {"message": "Welcome to PManager API"}
