from llm_judge.llm import LLMJudge


class JudgeClient:

    def __init__(self, model="mistral"):

        self.judge = LLMJudge(
            model=model
        )

    def run(
        self,
        prompt: str,
        agent_name: str = "Test Agent"
    ):

        # Generate LLM response

        agent_result = self.judge.generate_agent_response(
            prompt=prompt,
            agent_name=agent_name
        )

        # Evaluate response

        judge_result = self.judge.evaluate(
            agent_name=agent_result["agent_name"],
            prompt=agent_result["prompt"],
            response=agent_result["response"]
        )

        # Combine results

        return {

            "agent": agent_result,

            "judge": {

                "request_id":
                    judge_result["request_id"],

                "status":
                    judge_result["status"],

                "judge_response":
                    judge_result["judge_response"],

                "judge_input_tokens":
                    judge_result["input_tokens"],

                "judge_output_tokens":
                    judge_result["output_tokens"],

                "judge_total_tokens":
                    judge_result["total_tokens"],

                "judge_latency":
                    judge_result["latency"],

                "judge_model":
                    judge_result["model"]
            }
        }