from pydantic import BaseModel


# ==================================================
# LOGIN
# ==================================================

class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    username: str


# ==================================================
# RUN REQUEST
# ==================================================

class RunRequest(BaseModel):
    prompt: str


# ==================================================
# RUN RESPONSE
# ==================================================

class RunResponse(BaseModel):

    agent: dict

    judge: dict


# ==================================================
# DATABASE EVALUATION RESPONSE
# ==================================================

class EvaluationResponse(BaseModel):

    request_id: str

    username: str

    agent_name: str

    prompt: str

    agent_response: str

    input_tokens: int

    output_tokens: int

    total_tokens: int

    latency: float

    model: str

    judge_response: str

    judge_input_tokens: int

    judge_output_tokens: int

    judge_total_tokens: int

    judge_latency: float

    judge_model: str

    status: str