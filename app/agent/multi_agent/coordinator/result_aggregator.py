from __future__ import annotations

from app.agent.multi_agent.models.collaboration_result import (
    CollaborationResult,
    CollaborationStatus,
)
from app.agent.multi_agent.models.team_result import TeamResult


class ResultAggregator:
    """
    Aggregates results produced by multiple agents.

    Responsibilities:

    - Calculate execution statistics
    - Determine collaboration status
    - Build TeamResult

    This class intentionally does not perform AI-based response
    synthesis. That responsibility belongs to a future
    ResponseSynthesizer.
    """

    def aggregate(
        self,
        collaboration_id: str,
        results: list[CollaborationResult],
    ) -> TeamResult:
        """
        Aggregate collaboration results.
        """

        if not results:
            return TeamResult(
                collaboration_id=collaboration_id,
                status=CollaborationStatus.FAILED,
                final_output="No agent produced a result.",
                results=[],
            )

        successful = [
            result
            for result in results
            if result.status == CollaborationStatus.SUCCESS
        ]

        failed = [
            result
            for result in results
            if result.status == CollaborationStatus.FAILED
        ]

        if len(successful) == len(results):
            overall_status = CollaborationStatus.SUCCESS

        elif successful:
            overall_status = CollaborationStatus.PARTIAL_SUCCESS

        else:
            overall_status = CollaborationStatus.FAILED

        final_output = self._merge_outputs(successful)

        return TeamResult(
            collaboration_id=collaboration_id,
            status=overall_status,
            final_output=final_output,
            results=results,
            total_agents=len(results),
            successful_agents=len(successful),
            failed_agents=len(failed),
            execution_time_ms=max(
                (
                    result.execution_time_ms
                    for result in results
                ),
                default=0.0,
            ),
            total_tokens=sum(
                result.token_usage
                for result in results
            ),
        )

    def _merge_outputs(
        self,
        results: list[CollaborationResult],
    ) -> str:
        """
        Merge successful outputs into a deterministic response.

        Future versions will replace this implementation with an
        AI-powered synthesizer.
        """

        outputs: list[str] = []

        for result in results:

            if result.output is None:
                continue

            outputs.append(str(result.output))

        return "\n\n".join(outputs)