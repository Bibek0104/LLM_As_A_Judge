from sqlalchemy import Column, Integer, String, Float, Text

from database.database import Base


class Evaluation(Base):

    __tablename__ = "evaluations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    request_id = Column(
        String,
        unique=True,
        index=True
    )

    username = Column(
        String,
        index=True
    )

    agent_name = Column(String)

    prompt = Column(Text)

    agent_response = Column(Text)

    # ==========================
    # Agent metrics
    # ==========================

    input_tokens = Column(Integer)

    output_tokens = Column(Integer)

    total_tokens = Column(Integer)

    latency = Column(Float)

    model = Column(String)

    # ==========================
    # Judge
    # ==========================

    judge_response = Column(Text)

    # ==========================
    # Judge metrics
    # ==========================

    judge_input_tokens = Column(Integer)

    judge_output_tokens = Column(Integer)

    judge_total_tokens = Column(Integer)

    judge_latency = Column(Float)

    judge_model = Column(String)

    status = Column(String)