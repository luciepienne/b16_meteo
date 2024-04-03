from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

from nlp import get_text_from_forecast, get_speach_from_text


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/forecast")
async def forecast(city: str, date: str, hour: int = None):
    try:
        text = get_text_from_forecast(city, date, hour)
        print(f"text generated by AI:{text}")
        audio_file = get_speach_from_text(text, city, date, hour)
        audio_path = f"audio/{audio_file}"
        print(f"audio generated by AI:{audio_path}")
        return FileResponse(audio_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the API with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
