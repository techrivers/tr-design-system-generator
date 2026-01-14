"""Agent collaboration system for cross-validation and iterative refinement."""

from typing import Dict, List, Optional
from models import DesignPrinciples, DesignTokens, ComponentInventory, ValidationResult
from agents.validator import Validator


class AgentCollaboration:
    """Enables agents to validate and refine each other's work."""

    @staticmethod
    def validate_principles_tokens(
        principles: DesignPrinciples,
        tokens: DesignTokens
    ) -> ValidationResult:
        """Validate that tokens align with design principles."""
        return Validator.validate_design_consistency(principles, tokens)

    @staticmethod
    def validate_tokens_accessibility(tokens: DesignTokens) -> ValidationResult:
        """Validate token accessibility."""
        return Validator.validate_color_accessibility(tokens)

    @staticmethod
    def validate_inventory_completeness(
        inventory: ComponentInventory,
        principles: DesignPrinciples,
        product_context: str
    ) -> ValidationResult:
        """Validate component inventory completeness."""
        industry = principles.industry_context.industry if principles.industry_context else "unknown"
        return Validator.validate_component_completeness(inventory, industry, product_context)

    @staticmethod
    def check_cross_agent_consistency(
        principles: DesignPrinciples,
        tokens: DesignTokens,
        inventory: ComponentInventory,
        product_context: str
    ) -> Dict[str, ValidationResult]:
        """Run all cross-agent validation checks."""
        results = {}
        
        # Check principles-tokens consistency
        results["principles_tokens"] = AgentCollaboration.validate_principles_tokens(principles, tokens)
        
        # Check token accessibility
        results["tokens_accessibility"] = AgentCollaboration.validate_tokens_accessibility(tokens)
        
        # Check inventory completeness
        results["inventory_completeness"] = AgentCollaboration.validate_inventory_completeness(
            inventory, principles, product_context
        )
        
        return results

    @staticmethod
    def refine_tokens_based_on_validation(
        tokens: DesignTokens,
        validation_result: ValidationResult
    ) -> Optional[DesignTokens]:
        """Refine tokens if validation issues are found."""
        if validation_result.valid:
            return None  # No refinement needed
        
        # If there are critical issues, we might want to regenerate
        # For now, we'll just return None and let the main flow handle it
        # In a more sophisticated system, we could adjust colors here
        return None

    @staticmethod
    def get_quality_score(validation_results: Dict[str, ValidationResult]) -> float:
        """Calculate overall quality score from validation results."""
        if not validation_results:
            return 0.0
        
        scores = [result.score for result in validation_results.values()]
        return sum(scores) / len(scores) if scores else 0.0

    @staticmethod
    def should_refine(validation_results: Dict[str, ValidationResult], threshold: float = 0.7) -> bool:
        """Determine if refinement is needed based on quality score."""
        quality_score = AgentCollaboration.get_quality_score(validation_results)
        return quality_score < threshold
