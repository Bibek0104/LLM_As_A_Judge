from sqlalchemy.orm import Session

from database.models import Evaluation


def create_evaluation(
    db: Session,
    request_id: str,
    username: str,
    agent_name: str,
    prompt: str,
    agent_response: str,
    input_tokens: int,
    output_tokens: int,
    total_tokens: int,
    latency: float,
    model: str,
    judge_response: str,
    judge_input_tokens: int,
    judge_output_tokens: int,
    judge_total_tokens: int,
    judge_latency: float,
    judge_model: str,
    status: str
):

    evaluation = Evaluation(
        request_id=request_id,
        username=username,
        agent_name=agent_name,
        prompt=prompt,
        agent_response=agent_response,

        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        latency=latency,
        model=model,

        judge_response=judge_response,

        judge_input_tokens=judge_input_tokens,
        judge_output_tokens=judge_output_tokens,
        judge_total_tokens=judge_total_tokens,
        judge_latency=judge_latency,
        judge_model=judge_model,

        status=status
    )

    db.add(evaluation)

    db.commit()

    db.refresh(evaluation)

    return evaluation


def get_evaluation(
    db: Session,
    request_id: str
):

    return (
        db.query(Evaluation)
        .filter(
            Evaluation.request_id == request_id
        )
        .first()
    )


def get_all_evaluations(
    db: Session
):

    return db.query(Evaluation).all()
