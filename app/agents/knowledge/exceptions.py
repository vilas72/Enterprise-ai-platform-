"""
Knowledge Agent exceptions.
"""


class KnowledgeAgentError(Exception):
    """
    Base exception for the Knowledge Agent.
    """


class KnowledgeActionError(KnowledgeAgentError):
    """
    Raised when a knowledge business action fails.
    """


class KnowledgeAIError(KnowledgeAgentError):
    """
    Raised when an AI operation fails.
    """