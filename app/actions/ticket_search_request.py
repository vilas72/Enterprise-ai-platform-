

class TicketSearchRequest:
    def __init__(
        self,
        query: str = "gateway",
        project: str = "SUPPORT",
        status: list[str] = ["Open"],
        assignee: str = "john",
        max_results: int = 20,
        project_key: str | None = None,
    ) -> None:
        self.query = query
        self.project = project
        self.status = status
        self.assignee = assignee
        self.max_results = max_results
        self.project_key = project_key