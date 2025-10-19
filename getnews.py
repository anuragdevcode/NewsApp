from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
NEWS_API_KEY = "f42e945992df4af394fbcca1f7d84493"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/getnews')
async def getnews(query : str , language :str = 'en'):
    url = 'https://newsapi.org/v2/everything'
    #adding request parameter
    params = {
        'q': query,
        'language': language,
        'apiKey': NEWS_API_KEY,
        'pageSize': 10
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url,params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=500,detail='fail to load NEWSAPI')
        data = response.json()
        if data.get('status')!='ok':
            raise HTTPException(status_code=500,detail='NEWSAPI Error')
        return data.get('articles',[])

# another endpoint is addeed to show top news headline in the front-page
@app.get('/top_headlines')
async def topHeadlines(language :str ='en'):
    url = 'https://newsapi.org/v2/top-headlines'
    params ={
        'language' : language,
        'apiKey': NEWS_API_KEY,
        'pageSize': 10
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url,params = params)
        if response.status_code !=200:
            raise HTTPException(status_code =500, detail='API Failed')
        data = response.json()
        if data.get('status')!='ok':
            raise HTTPException(status_code=500, detail="Fetching Failed")
        return data.get('articles',[])