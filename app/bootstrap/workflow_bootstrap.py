"""
Workflow Bootstrap.

Registers workflow infrastructure only.

This module MUST NOT create Runtime, Gateway, or Workflow
service instances. Those are created by the dependency layer.
"""

from __future__ import annotations

from functools import lru_cache

from app.workflow.hooks.workflow_hook_manager import (
    WorkflowHookManager,
)

from app.workflow.templates import (
    register_workflow_templates,
)

from app.workflow.templates.workflow_template_registry import (
    WorkflowTemplateRegistry,
)

from app.workflow.workflow_builder import (
    WorkflowBuilder,
)

from app.workflow.workflow_registry import (
    WorkflowRegistry,
)

#
# Template Registry
#

_workflow_template_registry = WorkflowTemplateRegistry()

register_workflow_templates(
    _workflow_template_registry,
)


#
# Hook Manager
#

_workflow_hook_manager = WorkflowHookManager()


#
# Workflow Registry
#

_workflow_registry = WorkflowRegistry()


#
# Workflow Builder
#

_workflow_builder = WorkflowBuilder(
    registry=_workflow_template_registry,
)


#
# Dependency Providers
#

@lru_cache
def get_workflow_template_registry() -> WorkflowTemplateRegistry:
    """
    Return the shared Workflow Template Registry.
    """
    return _workflow_template_registry


@lru_cache
def get_workflow_hook_manager() -> WorkflowHookManager:
    """
    Return the shared Workflow Hook Manager.
    """
    return _workflow_hook_manager


@lru_cache
def get_workflow_registry() -> WorkflowRegistry:
    """
    Return the shared Workflow Registry.
    """
    return _workflow_registry


@lru_cache
def get_workflow_builder() -> WorkflowBuilder:
    """
    Return the shared Workflow Builder.
    """
    return _workflow_builder
