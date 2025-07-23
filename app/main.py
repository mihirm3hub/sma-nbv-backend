from fastapi import FastAPI
from .models import ObjectPose, NBVResponse
from .nbv_planner import plan_next_best_view
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing; lock down for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/plan_nbv", response_model=NBVResponse)
async def plan_nbv(pose: ObjectPose):
    """
    Accepts an object pose (x, y, z) and returns NBV candidates as JSON.
    """
    return plan_next_best_view(pose)
