from fastapi import FastAPI
app = FastAPI(title="VPN Platform Gateway API")
@app.get("/health")
async def health_check():
    return {"status": "OK"}
