import json
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Response
)

from sqlalchemy.orm import Session

from client.judge_client import JudgeClient

from main_server.schemas import (
    LoginRequest,
    LoginResponse,
    RunRequest,
    RunResponse,
    EvaluationResponse
)

from main_server.auth import (
    authenticate,
    create_token,
    get_current_user
)

# ==================================================
# DATABASE IMPORTS
# ==================================================

from database.database import (
    engine,
    get_db
)

from database.models import Evaluation

from database.crud import (
    create_evaluation,
    get_all_evaluations
)


# ==================================================
# CREATE FASTAPI APP
# ==================================================
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="LLM Judge Service",
    description="Standalone LLM Evaluation and Monitoring Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==================================================
# CREATE DATABASE TABLES
# ==================================================

Evaluation.metadata.create_all(
    bind=engine
)


# ==================================================
# JUDGE CLIENT
# ==================================================

judge_client = JudgeClient(
    model="mistral"
)


# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():

    return {
        "message": "LLM Judge Service Running"
    }


# ==================================================
# LOGIN
# ==================================================

@app.post(
    "/login",
    response_model=LoginResponse
)
def login(
    request: LoginRequest,
    response: Response
):

    # Check username and password

    if not authenticate(
        request.username,
        request.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Create JWT token

    token = create_token(
        request.username
    )

    # Store JWT in HTTP-only cookie

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60 * 60,
        secure=False,
        samesite="lax"
    )

    return {
        "message": "Login and authorization successful",
        "username": request.username
    }


# ==================================================
# RUN LLM + JUDGE
# ==================================================

@app.post(
    "/run",
    response_model=RunResponse
)
def run_judge(
    request: RunRequest,

    user=Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    # ----------------------------------------------
    # Get username from JWT
    # ----------------------------------------------

    username = user["sub"]

    # ----------------------------------------------
    # Run LLM + Judge
    # ----------------------------------------------

    result = judge_client.run(
        prompt=request.prompt
    )

    # ----------------------------------------------
    # Get agent information
    # ----------------------------------------------

    agent = result["agent"]

    # ----------------------------------------------
    # Get judge information
    # ----------------------------------------------

    judge = result["judge"]

    # ----------------------------------------------
    # Save evaluation to database
    # ----------------------------------------------

    create_evaluation(

        db=db,

        request_id=judge["request_id"],

        username=username,

        agent_name=agent["agent_name"],

        prompt=agent["prompt"],

        agent_response=agent["response"],

        input_tokens=agent["input_tokens"],

        output_tokens=agent["output_tokens"],

        total_tokens=agent["total_tokens"],

        latency=agent["latency"],

        model=agent["model"],

        judge_response=json.dumps(
        judge["judge_response"]
        ),

        judge_input_tokens=(
            judge["judge_input_tokens"]
        ),

        judge_output_tokens=(
            judge["judge_output_tokens"]
        ),

        judge_total_tokens=(
            judge["judge_total_tokens"]
        ),

        judge_latency=(
            judge["judge_latency"]
        ),

        judge_model=(
            judge["judge_model"]
        ),

        status=judge["status"]
    )

    # ----------------------------------------------
    # Return result
    # ----------------------------------------------

    return result


# ==================================================
# GET ALL EVALUATIONS
# ==================================================

@app.get("/evaluations")
def get_evaluations(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    evaluations = get_all_evaluations(db)

    return [
        {
            key: value
            for key, value in evaluation.__dict__.items()
            if key != "_sa_instance_state"
        }
        for evaluation in evaluations
    ]
# ==================================================
# LOGOUT
# ==================================================

@app.post("/logout")
def logout(
    response: Response
):

    response.delete_cookie(
        key="access_token"
    )

    return {
        "message": "Logout successful"
    }