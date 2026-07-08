from app.tracking.usage_record import UsageRecord


class CostCalculator:
    """
    Calculates estimated AI request cost.

    NOTE:
    Prices below are examples for development.
    Replace them with your organization's approved pricing
    or fetch them dynamically in the future.
    """

    #
    # USD per 1K tokens
    #
    MODEL_PRICING = {
        #
        # OpenAI
        #
        "gpt-4o": {
            "input": 0.005,
            "output": 0.015,
        },
        "gpt-4.1": {
            "input": 0.002,
            "output": 0.008,
        },
        "gpt-4.1-mini": {
            "input": 0.0004,
            "output": 0.0016,
        },

        #
        # Gemini
        #
        "gemini-2.5-pro": {
            "input": 0.0035,
            "output": 0.0105,
        },
        "gemini-2.5-flash": {
            "input": 0.00035,
            "output": 0.00105,
        },
    }

    @classmethod
    def calculate(
        cls,
        usage: UsageRecord,
    ) -> float:
        """
        Calculate estimated request cost.

        Returns USD.
        """

        pricing = cls.MODEL_PRICING.get(
            usage.model
        )

        if pricing is None:
            return 0.0

        input_cost = (
            usage.prompt_tokens
            / 1000
        ) * pricing["input"]

        output_cost = (
            usage.completion_tokens
            / 1000
        ) * pricing["output"]

        return round(
            input_cost + output_cost,
            6,
        )