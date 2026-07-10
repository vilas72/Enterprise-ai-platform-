"""Unit tests for fine-tuning pipeline."""

import pytest
from app.fine_tuning.fine_tuning_pipeline import (
    FineTuningPipeline,
    FineTuningConfig,
    FineTuningStatus,
)


@pytest.mark.asyncio
async def test_submit_fine_tuning_job():
    """Test submitting a fine-tuning job."""
    pipeline = FineTuningPipeline()

    config = FineTuningConfig(
        model_name="gpt-3.5-turbo",
        training_data_path="s3://bucket/training_data.jsonl",
    )

    job_id = await pipeline.submit_job(config)

    assert isinstance(job_id, str)
    assert len(job_id) > 0


@pytest.mark.asyncio
async def test_get_job_status():
    """Test getting job status."""
    pipeline = FineTuningPipeline()

    config = FineTuningConfig(
        model_name="gpt-3.5-turbo",
        training_data_path="s3://bucket/training_data.jsonl",
    )

    job_id = await pipeline.submit_job(config)
    status = await pipeline.get_status(job_id)

    assert status == FineTuningStatus.PENDING


@pytest.mark.asyncio
async def test_get_results_not_ready():
    """Test getting results before completion."""
    pipeline = FineTuningPipeline()

    config = FineTuningConfig(
        model_name="gpt-3.5-turbo",
        training_data_path="s3://bucket/training_data.jsonl",
    )

    job_id = await pipeline.submit_job(config)
    results = await pipeline.get_results(job_id)

    assert results is None  # Job not completed yet
