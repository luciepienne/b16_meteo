from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


from nlpandlist import (
    get_text_from_forecast,
    get_speach_from_text,
    get_list_cities_with_forecasts,
    get_cities_with_forecasts_department,
    get_list_departments_with_forecasts,
)


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


@app.get("/departmentwithforecasts")
async def departmentwithforecast():
    try:
        dptlist = get_list_departments_with_forecasts()
        print(dptlist)
        return dptlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/citieswithforecastsdept")
async def citieswithforecastsdpt(department_number: int):
    try:
        citylist = get_cities_with_forecasts_department(department_number)
        print(citylist)
        return citylist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/citieswithforecasts")
async def citieswithforecasts():
    try:
        citylist = get_list_cities_with_forecasts()
        print(citylist)
        return citylist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
