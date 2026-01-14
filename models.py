"""Data models for the design system generator."""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from enum import Enum


class TargetUser(str, Enum):
    B2B = "B2B"
    B2C = "B2C"
    ENTERPRISE = "enterprise"
    CONSUMER = "consumer"


class BrandTrait(str, Enum):
    MODERN = "modern"
    CLINICAL = "clinical"
    PLAYFUL = "playful"
    PREMIUM = "premium"
    BOLD = "bold"
    MINIMAL = "minimal"
    WARM = "warm"
    PROFESSIONAL = "professional"


class Platform(str, Enum):
    WEB = "web"
    MOBILE = "mobile"
    DASHBOARD = "dashboard"
    MARKETING = "marketing"


class DesignSystemInput(BaseModel):
    """Input parameters for design system generation."""
    product_idea: str = Field(..., description="Description of the product or domain")
    target_users: Optional[List[TargetUser]] = Field(default=None, description="Target user types")
    brand_traits: Optional[List[BrandTrait]] = Field(default=None, description="Brand personality traits")
    platforms: Optional[List[Platform]] = Field(default=None, description="Target platforms")


class ConfidenceScore(BaseModel):
    """Confidence scores for agent inferences."""
    users: float = Field(..., ge=0.0, le=1.0, description="Confidence in inferred users")
    traits: float = Field(..., ge=0.0, le=1.0, description="Confidence in inferred traits")
    platforms: float = Field(..., ge=0.0, le=1.0, description="Confidence in inferred platforms")


class AgentReasoning(BaseModel):
    """Agent decision rationale."""
    reasoning: str = Field(..., description="Explanation of decisions made")
    confidence: ConfidenceScore = Field(..., description="Confidence scores for inferences")
    overrides: Optional[List[str]] = Field(default=None, description="User inputs that were overridden and why")


class IndustryContext(BaseModel):
    """Detected industry context."""
    industry: str = Field(..., description="Detected industry type")
    philosophy: str = Field(..., description="Typical philosophy for this industry")
    density: str = Field(..., description="Typical density for this industry")
    warmth: int = Field(..., description="Typical warmth for this industry")
    clarity: int = Field(..., description="Typical clarity requirement for this industry")
    speed: int = Field(..., description="Typical speed requirement for this industry")


class DesignPrinciples(BaseModel):
    """Core design principles defined by the Design Strategist."""
    clarity: int = Field(..., ge=1, le=10, description="Importance of clarity (1-10)")
    density: Literal["dense", "spacious", "balanced"] = Field(..., description="UI density preference")
    warmth: int = Field(..., ge=1, le=10, description="Warmth vs coolness (1-10)")
    speed: int = Field(..., ge=1, le=10, description="Performance vs decoration (1-10)")
    philosophy: Literal["utility-first", "component-first", "brand-led"] = Field(..., description="System philosophy")
    inferred_users: Optional[List[str]] = None
    inferred_traits: Optional[List[str]] = None
    inferred_platforms: Optional[List[str]] = None
    reasoning: Optional[AgentReasoning] = None
    industry_context: Optional[IndustryContext] = None


class ColorToken(BaseModel):
    """Individual color token."""
    name: str
    value: str  # Hex color
    role: Literal["primary", "secondary", "neutral", "semantic", "accent"]


class TypographyToken(BaseModel):
    """Typography token."""
    name: str
    family: str
    size: str  # CSS size value
    weight: int
    line_height: float
    role: Literal["heading", "body", "ui", "display"]


class SpacingToken(BaseModel):
    """Spacing token."""
    name: str
    value: str  # CSS value
    scale: int  # Position in scale


class ColorRationale(BaseModel):
    """Rationale for color choices."""
    primary: str = Field(..., description="Explanation for primary color choice")
    neutral: str = Field(..., description="Explanation for neutral color choice")
    accent: str = Field(..., description="Explanation for accent color choice")
    overall: str = Field(..., description="Overall color system rationale")


class DesignTokens(BaseModel):
    """Complete design token system."""
    colors: List[ColorToken]
    dark_colors: Optional[List[ColorToken]] = None
    typography: List[TypographyToken]
    spacing: List[SpacingToken]
    border_radius: Dict[str, str]
    shadows: Dict[str, str]
    color_rationale: Optional[ColorRationale] = None


class ComponentSpec(BaseModel):
    """Component specification."""
    name: str
    category: Literal["button", "input", "navigation", "feedback", "layout", "data", "contextual"]
    variants: List[str]
    states: List[str]
    description: str
    accessibility_notes: Optional[str] = None


class ComponentInventory(BaseModel):
    """Complete component inventory."""
    components: List[ComponentSpec]
    reusable_components: List[str]
    contextual_components: List[str]
    reasoning: Optional[str] = None


class ComponentCode(BaseModel):
    """Generated component code."""
    name: str
    code: str
    file_path: str


class StorybookFile(BaseModel):
    """Storybook configuration or story file."""
    name: str
    content: str
    file_path: str


class TestFile(BaseModel):
    """Test file for a component."""
    name: str = Field(..., description="Name of the test file")
    content: str = Field(..., description="Content of the test file")
    file_path: str = Field(..., description="Path to save the test file")


class ComponentLibrary(BaseModel):
    """Complete component library output."""
    css_variables: str
    tailwind_config: str
    package_json: str
    figma_tokens: str = Field(default="", description="Figma Tokens Studio JSON")
    components: List[ComponentCode]
    index_file: str
    readme: str
    storybook_files: List[StorybookFile]
    test_files: List[TestFile]


class ValidationResult(BaseModel):
    """Validation result for agent outputs."""
    valid: bool = Field(..., description="Whether validation passed")
    issues: List[str] = Field(default_factory=list, description="List of validation issues found")
    warnings: List[str] = Field(default_factory=list, description="List of warnings")
    score: float = Field(..., ge=0.0, le=1.0, description="Quality score (0-1)")


class DesignSystemOutput(BaseModel):
    """Complete design system output."""
    input: DesignSystemInput
    principles: DesignPrinciples
    tokens: DesignTokens
    components: ComponentInventory
    component_library: ComponentLibrary
    guidelines: Dict[str, str]  # Do's and don'ts
    generated_at: str
    validation: Optional[Dict[str, ValidationResult]] = None
