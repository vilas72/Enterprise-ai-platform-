from __future__ import annotations

from enum import StrEnum


class ActionType(StrEnum):
    FETCH_PULL_REQUEST = "github.review_pull_request"
    FETCH_CHANGED_FILES = "github.fetch_changed_files"
    ANALYZE_CODE = "developer.analyze_code"
    GENERATE_REVIEW = "developer.generate_review"
    PUBLISH_REVIEW = "github.publish_review"
    HYBRID_SEARCH = "knowledge.hybrid_search"
    RERANK_RESULTS = "knowledge.rerank_results"
    BUILD_CONTEXT = "knowledge.build_context"
    GENERATE_ANSWER = "knowledge.generate_answer"
    FETCH_TICKET = "support.fetch_ticket"
    COLLECT_LOGS = "support.collect_logs"
    SEARCH_KNOWLEDGE = "knowledge.search_repository"
    ANALYZE_ROOT_CAUSE = "support.analyze_root_cause"
    GENERATE_RESOLUTION = "support.generate_resolution"
    CREATE_TICKET = "support.create_ticket"
    UPDATE_TICKET = "support.update_ticket"
    NOTIFY_USER = "notification.send"
    VALIDATE_REQUEST = "devops.validate_request"
    BUILD_APPLICATION = "devops.build_application"
    RUN_UNIT_TESTS = "devops.run_unit_tests"
    BUILD_CONTAINER = "devops.build_container"
    PUSH_CONTAINER = "devops.push_container"
    DEPLOY_APPLICATION = "devops.deploy_application"
    VERIFY_DEPLOYMENT = "devops.verify_deployment"
    RUN_SMOKE_TESTS = "devops.run_smoke_tests"
    NOTIFY_TEAM = "notification.send"