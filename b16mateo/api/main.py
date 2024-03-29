from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
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
async def forecast(city: str, date: str, hour: Optional[int] = None) -> None:
    try:
        text = get_text_from_forecast(city, date, hour)  # Pass the hour argument
        print(text)
        audio_file = get_speach_from_text(text, city, date, hour)
        return {
            # "audio_file": audio_file,
            "audio_path": f"/forecast_storage/audio/{audio_file}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# @app.get("/city_autocompletion")
# async def fetch_cities_name(department_number, cur):
#     cur.execute(
#         """
#         SELECT label, zip_code
#             FROM cities
#             WHERE department_number = %s;
#             """,
#         (department_number,),
#     )
#     cities_data = cur.fetchall()
#     return cities_data



# Run the API with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
