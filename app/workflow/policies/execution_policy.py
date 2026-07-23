from pydantic import BaseModel

class ExecutionPolicy(BaseModel):

    fail_fast: bool = True

    continue_on_failure: bool = False

    max_parallelism: int = 1