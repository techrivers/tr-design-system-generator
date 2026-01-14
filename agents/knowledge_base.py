"""Knowledge base for design system generation - industry patterns, best practices, and domain expertise."""

from typing import Dict, List, Optional
from enum import Enum


class Industry(str, Enum):
    """Product industry categories."""
    ECOMMERCE = "ecommerce"
    SAAS = "saas"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    EDUCATION = "education"
    MARKETING = "marketing"
    DASHBOARD = "dashboard"
    MOBILE_APP = "mobile_app"
    ENTERPRISE = "enterprise"
    CONSUMER = "consumer"
    UNKNOWN = "unknown"


class KnowledgeBase:
    """Centralized knowledge base for design system generation."""

    # Industry-specific color palettes (primary color suggestions)
    INDUSTRY_COLORS: Dict[str, Dict[str, str]] = {
        "healthcare": {
            "primary": "#2563EB",  # Trustworthy blue
            "accent": "#10B981",  # Health green
            "neutral": "#64748B",  # Cool gray
            "rationale": "Blues and greens convey trust, cleanliness, and care"
        },
        "finance": {
            "primary": "#1E40AF",  # Conservative blue
            "accent": "#059669",  # Growth green
            "neutral": "#475569",  # Professional gray
            "rationale": "Deep blues suggest stability, security, and professionalism"
        },
        "ecommerce": {
            "primary": "#DC2626",  # Action red
            "accent": "#F59E0B",  # Attention orange
            "neutral": "#6B7280",  # Balanced gray
            "rationale": "Warm colors encourage action and purchase decisions"
        },
        "saas": {
            "primary": "#6366F1",  # Modern indigo
            "accent": "#8B5CF6",  # Creative purple
            "neutral": "#64748B",  # Neutral slate
            "rationale": "Modern tech colors suggest innovation and efficiency"
        },
        "education": {
            "primary": "#0284C7",  # Learning blue
            "accent": "#F59E0B",  # Energy orange
            "neutral": "#64748B",  # Calm gray
            "rationale": "Friendly blues with energetic accents promote engagement"
        },
        "marketing": {
            "primary": "#EC4899",  # Bold pink
            "accent": "#F59E0B",  # Vibrant orange
            "neutral": "#6B7280",  # Soft gray
            "rationale": "Vibrant colors capture attention and convey energy"
        },
        "dashboard": {
            "primary": "#3B82F6",  # Data blue
            "accent": "#10B981",  # Success green
            "neutral": "#475569",  # Readable gray
            "rationale": "Cool colors reduce eye strain for data-heavy interfaces"
        },
        "enterprise": {
            "primary": "#1E40AF",  # Corporate blue
            "accent": "#6366F1",  # Modern indigo
            "neutral": "#334155",  # Professional gray
            "rationale": "Conservative colors convey reliability and professionalism"
        },
        "consumer": {
            "primary": "#DC2626",  # Engaging red
            "accent": "#F59E0B",  # Friendly orange
            "neutral": "#6B7280",  # Approachable gray
            "rationale": "Warm, approachable colors encourage interaction"
        }
    }

    # Component inventory by product type
    COMPONENT_BY_INDUSTRY: Dict[str, List[str]] = {
        "ecommerce": [
            "Button", "Input", "Select", "Card", "Badge", "Modal", "Alert",
            "Table", "Pagination", "Search", "Breadcrumb", "Hero", "PricingTable"
        ],
        "saas": [
            "Button", "Input", "Select", "Modal", "Alert", "Table", "Tabs",
            "Navigation", "Sidebar", "Header", "Footer", "DataTable", "DashboardStat"
        ],
        "healthcare": [
            "Button", "Input", "Select", "Modal", "Alert", "Table", "Card",
            "Accordion", "Progress", "Badge", "Tooltip", "Navigation"
        ],
        "finance": [
            "Button", "Input", "Select", "Table", "Modal", "Alert", "Card",
            "DataTable", "Pagination", "Tabs", "Navigation", "Header", "Footer"
        ],
        "dashboard": [
            "Button", "Input", "Select", "Table", "Card", "Modal", "Alert",
            "Tabs", "Navigation", "Sidebar", "Header", "Footer", "DataTable",
            "DashboardStat", "Progress", "Skeleton"
        ],
        "marketing": [
            "Button", "Input", "Hero", "Card", "Modal", "Alert", "Navigation",
            "Header", "Footer", "Testimonial", "PricingTable", "Badge", "Tabs"
        ],
        "enterprise": [
            "Button", "Input", "Select", "Table", "Modal", "Alert", "Navigation",
            "Sidebar", "Header", "Footer", "DataTable", "Tabs", "Breadcrumb"
        ],
        "consumer": [
            "Button", "Input", "Select", "Card", "Modal", "Alert", "Navigation",
            "Hero", "Badge", "Avatar", "Tabs", "Header", "Footer"
        ]
    }

    # Component dependencies
    COMPONENT_DEPENDENCIES: Dict[str, List[str]] = {
        "Table": ["Pagination", "Search"],
        "DataTable": ["Table", "Pagination", "Search", "Select"],
        "Navigation": ["Header"],
        "Sidebar": ["Navigation"],
        "DashboardStat": ["Card"],
        "PricingTable": ["Card", "Button"],
        "Hero": ["Button"]
    }

    # Design philosophy by industry
    PHILOSOPHY_BY_INDUSTRY: Dict[str, str] = {
        "healthcare": "utility-first",
        "finance": "utility-first",
        "enterprise": "utility-first",
        "dashboard": "utility-first",
        "saas": "component-first",
        "ecommerce": "brand-led",
        "marketing": "brand-led",
        "consumer": "brand-led",
        "education": "component-first"
    }

    # Density preferences by industry
    DENSITY_BY_INDUSTRY: Dict[str, str] = {
        "healthcare": "spacious",
        "finance": "spacious",
        "enterprise": "spacious",
        "dashboard": "dense",
        "saas": "balanced",
        "ecommerce": "balanced",
        "marketing": "spacious",
        "consumer": "balanced",
        "education": "balanced"
    }

    # Warmth preferences by industry
    WARMTH_BY_INDUSTRY: Dict[str, int] = {
        "healthcare": 4,  # Professional but approachable
        "finance": 3,  # Conservative
        "enterprise": 3,  # Professional
        "dashboard": 4,  # Neutral
        "saas": 6,  # Modern and friendly
        "ecommerce": 7,  # Engaging
        "marketing": 8,  # Energetic
        "consumer": 7,  # Warm and approachable
        "education": 6  # Friendly
    }

    # Clarity requirements by industry
    CLARITY_BY_INDUSTRY: Dict[str, int] = {
        "healthcare": 10,  # Critical for medical information
        "finance": 10,  # Critical for financial data
        "enterprise": 9,  # High clarity needed
        "dashboard": 9,  # Data must be clear
        "saas": 8,  # Important but can be modern
        "ecommerce": 8,  # Important for trust
        "marketing": 7,  # Can be more creative
        "consumer": 8,  # Important for usability
        "education": 9  # Learning requires clarity
    }

    # Speed requirements by industry
    SPEED_BY_INDUSTRY: Dict[str, int] = {
        "healthcare": 9,  # Fast access to critical info
        "finance": 9,  # Quick transactions
        "enterprise": 8,  # Efficient workflows
        "dashboard": 9,  # Real-time data
        "saas": 8,  # Productivity focus
        "ecommerce": 7,  # Balance with aesthetics
        "marketing": 6,  # Can prioritize visuals
        "consumer": 7,  # Good UX but not critical
        "education": 7  # Balanced
    }

    # Brand trait conflicts (traits that shouldn't be used together)
    TRAIT_CONFLICTS: Dict[str, List[str]] = {
        "clinical": ["playful", "bold"],
        "professional": ["playful"],
        "minimal": ["bold"],
        "playful": ["clinical", "professional"]
    }

    # Industry-specific accessibility requirements
    ACCESSIBILITY_REQUIREMENTS: Dict[str, List[str]] = {
        "healthcare": ["WCAG 2.1 AAA", "High contrast", "Screen reader optimized"],
        "finance": ["WCAG 2.1 AA", "Keyboard navigation", "High contrast"],
        "enterprise": ["WCAG 2.1 AA", "Keyboard navigation"],
        "dashboard": ["WCAG 2.1 AA", "Color blind friendly"],
        "saas": ["WCAG 2.1 AA"],
        "ecommerce": ["WCAG 2.1 AA", "Keyboard navigation"],
        "marketing": ["WCAG 2.1 AA"],
        "consumer": ["WCAG 2.1 AA"],
        "education": ["WCAG 2.1 AA", "Screen reader optimized"]
    }

    @staticmethod
    def detect_industry(product_idea: str) -> str:
        """Detect industry from product description."""
        idea_lower = product_idea.lower()
        
        # Healthcare keywords
        if any(kw in idea_lower for kw in ["health", "medical", "patient", "clinic", "hospital", "doctor", "nurse", "diagnosis", "treatment"]):
            return Industry.HEALTHCARE.value
        
        # Finance keywords
        if any(kw in idea_lower for kw in ["finance", "banking", "payment", "transaction", "investment", "trading", "wallet", "credit", "loan"]):
            return Industry.FINANCE.value
        
        # E-commerce keywords
        if any(kw in idea_lower for kw in ["shop", "store", "cart", "checkout", "product", "inventory", "retail", "ecommerce", "e-commerce", "purchase", "buy"]):
            return Industry.ECOMMERCE.value
        
        # SaaS keywords
        if any(kw in idea_lower for kw in ["saas", "software", "platform", "tool", "app", "dashboard", "analytics", "crm", "management"]):
            if "dashboard" in idea_lower or "analytics" in idea_lower:
                return Industry.DASHBOARD.value
            return Industry.SAAS.value
        
        # Education keywords
        if any(kw in idea_lower for kw in ["education", "learning", "course", "student", "teacher", "school", "university", "tutorial", "lesson"]):
            return Industry.EDUCATION.value
        
        # Marketing keywords
        if any(kw in idea_lower for kw in ["marketing", "landing", "campaign", "promotion", "advertising", "brand", "social media"]):
            return Industry.MARKETING.value
        
        # Enterprise keywords
        if any(kw in idea_lower for kw in ["enterprise", "b2b", "business", "corporate", "organization", "company"]):
            return Industry.ENTERPRISE.value
        
        # Consumer keywords
        if any(kw in idea_lower for kw in ["consumer", "b2c", "user", "personal", "individual"]):
            return Industry.CONSUMER.value
        
        return Industry.UNKNOWN.value

    @staticmethod
    def get_industry_color_suggestions(industry: str) -> Optional[Dict[str, str]]:
        """Get color suggestions for an industry."""
        return KnowledgeBase.INDUSTRY_COLORS.get(industry)

    @staticmethod
    def get_components_for_industry(industry: str) -> List[str]:
        """Get recommended components for an industry."""
        return KnowledgeBase.COMPONENT_BY_INDUSTRY.get(industry, [])

    @staticmethod
    def get_component_dependencies(component: str) -> List[str]:
        """Get dependencies for a component."""
        return KnowledgeBase.COMPONENT_DEPENDENCIES.get(component, [])

    @staticmethod
    def get_philosophy_for_industry(industry: str) -> str:
        """Get design philosophy for an industry."""
        return KnowledgeBase.PHILOSOPHY_BY_INDUSTRY.get(industry, "component-first")

    @staticmethod
    def get_density_for_industry(industry: str) -> str:
        """Get density preference for an industry."""
        return KnowledgeBase.DENSITY_BY_INDUSTRY.get(industry, "balanced")

    @staticmethod
    def get_warmth_for_industry(industry: str) -> int:
        """Get warmth preference for an industry."""
        return KnowledgeBase.WARMTH_BY_INDUSTRY.get(industry, 5)

    @staticmethod
    def get_clarity_for_industry(industry: str) -> int:
        """Get clarity requirement for an industry."""
        return KnowledgeBase.CLARITY_BY_INDUSTRY.get(industry, 8)

    @staticmethod
    def get_speed_for_industry(industry: str) -> int:
        """Get speed requirement for an industry."""
        return KnowledgeBase.SPEED_BY_INDUSTRY.get(industry, 7)

    @staticmethod
    def check_trait_conflicts(traits: List[str]) -> List[str]:
        """Check for conflicting brand traits."""
        conflicts = []
        for trait in traits:
            conflicting = KnowledgeBase.TRAIT_CONFLICTS.get(trait, [])
            for conflict in conflicting:
                if conflict in traits:
                    conflicts.append(f"{trait} conflicts with {conflict}")
        return conflicts

    @staticmethod
    def get_accessibility_requirements(industry: str) -> List[str]:
        """Get accessibility requirements for an industry."""
        return KnowledgeBase.ACCESSIBILITY_REQUIREMENTS.get(industry, ["WCAG 2.1 AA"])
