"""Main application for the Design System Generator."""

from datetime import datetime
from agents.design_strategist.agent import DesignStrategistAgent
from agents.visual_identity.agent import VisualIdentityAgent
from agents.component_architect.agent import ComponentArchitectAgent
from agents.collaboration import AgentCollaboration
from agents.validator import Validator
from templates.components.generator import ComponentGenerator
from models import DesignSystemInput, DesignSystemOutput, ComponentCode, TestFile


class DesignSystemGenerator:
    """Main orchestrator for the design system generation process."""

    def __init__(self):
        self.design_strategist = DesignStrategistAgent()
        self.visual_identity = VisualIdentityAgent()
        self.component_architect = ComponentArchitectAgent()

    def generate_design_system(self, input_data: DesignSystemInput) -> DesignSystemOutput:
        """
        Generate a complete design system using the multi-agent architecture.

        The process follows this flow:
        1. Design Strategist analyzes requirements and defines principles
        2. Visual Identity creates tokens based on principles
        3. Component Architect defines component inventory
        """

        print("🚀 Starting design system generation...")
        print(f"📋 Product: {input_data.product_idea}")
        print(f"👥 Target: {[u.value for u in input_data.target_users] if input_data.target_users else 'Auto-detected'}")
        print(f"🎨 Brand: {[t.value for t in input_data.brand_traits] if input_data.brand_traits else 'Auto-detected'}")

        # Step 1: Design Strategy
        print("\n1️⃣ Analyzing requirements with Design Strategist...")
        design_principles = self.design_strategist.analyze_product_requirements(input_data)
        print(f"   📋 Philosophy: {design_principles.philosophy}")
        print(f"   📏 Density: {design_principles.density}")
        print(f"   🎯 Clarity: {design_principles.clarity}/10")

        # Step 2: Visual Identity
        print("\n2️⃣ Generating visual tokens with Visual Identity Agent...")
        design_tokens = self.visual_identity.generate_design_tokens(design_principles)
        print(f"   🎨 Generated {len(design_tokens.colors)} color tokens")
        print(f"   📝 Generated {len(design_tokens.typography)} typography tokens")
        print(f"   📐 Generated {len(design_tokens.spacing)} spacing tokens")
        
        # Validate tokens against principles
        print("\n   🔍 Validating tokens against design principles...")
        token_validation = AgentCollaboration.validate_principles_tokens(design_principles, design_tokens)
        if not token_validation.valid:
            print(f"   ⚠️  Token validation issues: {len(token_validation.issues)}")
            for issue in token_validation.issues:
                print(f"      - {issue}")
        else:
            print("   ✅ Tokens align with design principles")
        
        # Validate accessibility
        print("\n   🔍 Validating color accessibility...")
        accessibility_validation = AgentCollaboration.validate_tokens_accessibility(design_tokens)
        if not accessibility_validation.valid:
            print(f"   ⚠️  Accessibility issues: {len(accessibility_validation.issues)}")
            for issue in accessibility_validation.issues:
                print(f"      - {issue}")
        else:
            print("   ✅ All colors meet WCAG 2.1 AA standards")

        # Step 3: Component Architecture
        print("\n3️⃣ Designing component system with Component Architect...")
        component_inventory = self.component_architect.generate_component_inventory(
            design_principles, input_data.product_idea
        )
        print(f"   🧩 Defined {len(component_inventory.components)} components")
        print(f"   🔄 Reusable: {len(component_inventory.reusable_components)}")
        print(f"   🎭 Contextual: {len(component_inventory.contextual_components)}")
        
        # Validate component completeness
        print("\n   🔍 Validating component inventory...")
        inventory_validation = AgentCollaboration.validate_inventory_completeness(
            component_inventory, design_principles, input_data.product_idea
        )
        if not inventory_validation.valid:
            print(f"   ⚠️  Component inventory issues: {len(inventory_validation.issues)}")
            for issue in inventory_validation.issues:
                print(f"      - {issue}")
        else:
            print("   ✅ Component inventory is complete")
        
        # Cross-agent validation
        print("\n   🔍 Running cross-agent validation...")
        cross_validation = AgentCollaboration.check_cross_agent_consistency(
            design_principles, design_tokens, component_inventory, input_data.product_idea
        )
        quality_score = AgentCollaboration.get_quality_score(cross_validation)
        print(f"   📊 Overall quality score: {quality_score:.2%}")

        # Step 4: Generate Component Library
        print("\n4️⃣ Generating React component library...")
        component_gen = ComponentGenerator(design_tokens)

        generated_components = []

        # Generate components based on the inventory
        for component_spec in component_inventory.components:
            component_name = component_spec.name.lower()
            if component_name == 'button':
                code = component_gen.generate_button_component(component_spec)
                file_path = f"src/components/Button.tsx"
            elif component_name == 'input':
                code = component_gen.generate_input_component(component_spec)
                file_path = f"src/components/Input.tsx"
            elif component_name == 'select':
                code = component_gen.generate_select_component(component_spec)
                file_path = f"src/components/Select.tsx"
            elif component_name == 'alert':
                code = component_gen.generate_alert_component(component_spec)
                file_path = f"src/components/Alert.tsx"
            elif component_name == 'modal':
                code = component_gen.generate_modal_component(component_spec)
                file_path = f"src/components/Modal.tsx"
            elif component_name == 'table':
                code = component_gen.generate_table_component(component_spec)
                file_path = f"src/components/Table.tsx"
            elif component_name == 'navigation':
                code = component_gen.generate_navigation_component(component_spec)
                file_path = f"src/components/Navigation.tsx"
            elif component_name == 'textarea':
                code = component_gen.generate_textarea_component(component_spec)
                file_path = f"src/components/Textarea.tsx"
            elif component_name == 'checkbox':
                code = component_gen.generate_checkbox_component(component_spec)
                file_path = f"src/components/Checkbox.tsx"
            elif component_name == 'radio':
                code = component_gen.generate_radio_component(component_spec)
                file_path = f"src/components/Radio.tsx"
            elif component_name == 'badge':
                code = component_gen.generate_badge_component(component_spec)
                file_path = f"src/components/Badge.tsx"
            elif component_name == 'tooltip':
                code = component_gen.generate_tooltip_component(component_spec)
                file_path = f"src/components/Tooltip.tsx"
            elif component_name == 'tabs':
                code = component_gen.generate_tabs_component(component_spec)
                file_path = f"src/components/Tabs.tsx"
            elif component_name == 'avatar':
                code = component_gen.generate_avatar_component(component_spec)
                file_path = f"src/components/Avatar.tsx"
            elif component_name == 'datepicker':
                code = component_gen.generate_datepicker_component(component_spec)
                file_path = f"src/components/DatePicker.tsx"
            elif component_name == 'switch':
                code = component_gen.generate_switch_component(component_spec)
                file_path = f"src/components/Switch.tsx"
            elif component_name == 'progress':
                code = component_gen.generate_progress_component(component_spec)
                file_path = f"src/components/Progress.tsx"
            elif component_name == 'accordion':
                code = component_gen.generate_accordion_component(component_spec)
                file_path = f"src/components/Accordion.tsx"
            elif component_name == 'breadcrumb':
                code = component_gen.generate_breadcrumb_component(component_spec)
                file_path = f"src/components/Breadcrumb.tsx"
            elif component_name == 'skeleton':
                code = component_gen.generate_skeleton_component(component_spec)
                file_path = f"src/components/Skeleton.tsx"
            elif component_name == 'pagination':
                code = component_gen.generate_pagination_component(component_spec)
                file_path = f"src/components/Pagination.tsx"
            elif component_name == 'search':
                code = component_gen.generate_search_component(component_spec)
                file_path = f"src/components/Search.tsx"
            elif component_name == 'card':
                code = component_gen.generate_card_component(component_spec)
                file_path = f"src/components/Card.tsx"
            elif component_name == 'container':
                code = component_gen.generate_container_component(component_spec)
                file_path = f"src/components/Container.tsx"
            elif component_name == 'stack':
                code = component_gen.generate_stack_component(component_spec)
                file_path = f"src/components/Stack.tsx"
            elif component_name == 'grid':
                code = component_gen.generate_grid_component(component_spec)
                file_path = f"src/components/Grid.tsx"
            elif component_name == 'sidebar':
                code = component_gen.generate_sidebar_component(component_spec)
                file_path = f"src/components/Sidebar.tsx"
            elif component_name == 'header':
                code = component_gen.generate_header_component(component_spec)
                file_path = f"src/components/Header.tsx"
            elif component_name == 'footer':
                code = component_gen.generate_footer_component(component_spec)
                file_path = f"src/components/Footer.tsx"
            elif component_name == 'hero':
                code = component_gen.generate_hero_component(component_spec)
                file_path = f"src/components/Hero.tsx"
            else:
                continue  # Skip components we don't have generators for yet

            generated_components.append(ComponentCode(
                name=component_spec.name,
                code=code,
                file_path=file_path
            ))

        # Generate supporting files
        css_variables = component_gen.generate_css_variables()
        tailwind_config = component_gen.generate_tailwind_config()
        package_json = component_gen.generate_package_json()
        index_file = component_gen.generate_component_index(component_inventory.components)
        readme = component_gen.generate_readme(generated_components, design_principles.model_dump(), input_data.product_idea)

        from models import StorybookFile

        # Generate Storybook files
        storybook_files = [
            StorybookFile(
                name="main.ts",
                content=component_gen.generate_storybook_main_config(),
                file_path=".storybook/main.ts"
            ),
            StorybookFile(
                name="preview.ts",
                content=component_gen.generate_storybook_preview_config(),
                file_path=".storybook/preview.ts"
            ),
        ]

        # Add component stories
        for component in generated_components:
            component_name = component.name.lower()
            if component_name == 'button':
                story_content = component_gen.generate_button_stories()
                story_path = f"src/components/Button.stories.tsx"
            elif component_name == 'input':
                story_content = component_gen.generate_input_stories()
                story_path = f"src/components/Input.stories.tsx"
            elif component_name == 'modal':
                story_content = component_gen.generate_modal_stories()
                story_path = f"src/components/Modal.stories.tsx"
            elif component_name == 'alert':
                story_content = component_gen.generate_alert_stories()
                story_path = f"src/components/Alert.stories.tsx"
            elif component_name == 'select':
                story_content = component_gen.generate_select_stories()
                story_path = f"src/components/Select.stories.tsx"
            elif component_name == 'table':
                story_content = component_gen.generate_table_stories()
                story_path = f"src/components/Table.stories.tsx"
            elif component_name == 'navigation':
                story_content = component_gen.generate_navigation_stories()
                story_path = f"src/components/Navigation.stories.tsx"
            elif component_name == 'textarea':
                story_content = component_gen.generate_textarea_stories()
                story_path = f"src/components/Textarea.stories.tsx"
            elif component_name == 'checkbox':
                story_content = component_gen.generate_checkbox_stories()
                story_path = f"src/components/Checkbox.stories.tsx"
            elif component_name == 'radio':
                story_content = component_gen.generate_radio_stories()
                story_path = f"src/components/Radio.stories.tsx"
            elif component_name == 'badge':
                story_content = component_gen.generate_badge_stories()
                story_path = f"src/components/Badge.stories.tsx"
            elif component_name == 'tooltip':
                story_content = component_gen.generate_tooltip_stories()
                story_path = f"src/components/Tooltip.stories.tsx"
            elif component_name == 'tabs':
                story_content = component_gen.generate_tabs_stories()
                story_path = f"src/components/Tabs.stories.tsx"
            elif component_name == 'avatar':
                story_content = component_gen.generate_avatar_stories()
                story_path = f"src/components/Avatar.stories.tsx"
            elif component_name == 'datepicker':
                story_content = component_gen.generate_datepicker_stories()
                story_path = f"src/components/DatePicker.stories.tsx"
            elif component_name == 'switch':
                story_content = component_gen.generate_switch_stories()
                story_path = f"src/components/Switch.stories.tsx"
            elif component_name == 'progress':
                story_content = component_gen.generate_progress_stories()
                story_path = f"src/components/Progress.stories.tsx"
            elif component_name == 'accordion':
                story_content = component_gen.generate_accordion_stories()
                story_path = f"src/components/Accordion.stories.tsx"
            elif component_name == 'breadcrumb':
                story_content = component_gen.generate_breadcrumb_stories()
                story_path = f"src/components/Breadcrumb.stories.tsx"
            elif component_name == 'skeleton':
                story_content = component_gen.generate_skeleton_stories()
                story_path = f"src/components/Skeleton.stories.tsx"
            elif component_name == 'pagination':
                story_content = component_gen.generate_pagination_stories()
                story_path = f"src/components/Pagination.stories.tsx"
            elif component_name == 'search':
                story_content = component_gen.generate_search_stories()
                story_path = f"src/components/Search.stories.tsx"
            elif component_name == 'card':
                story_content = component_gen.generate_card_stories()
                story_path = f"src/components/Card.stories.tsx"
            elif component_name == 'container':
                story_content = component_gen.generate_container_stories()
                story_path = f"src/components/Container.stories.tsx"
            elif component_name == 'stack':
                story_content = component_gen.generate_stack_stories()
                story_path = f"src/components/Stack.stories.tsx"
            elif component_name == 'grid':
                story_content = component_gen.generate_grid_stories()
                story_path = f"src/components/Grid.stories.tsx"
            elif component_name == 'sidebar':
                story_content = component_gen.generate_sidebar_stories()
                story_path = f"src/components/Sidebar.stories.tsx"
            elif component_name == 'header':
                story_content = component_gen.generate_header_stories()
                story_path = f"src/components/Header.stories.tsx"
            elif component_name == 'footer':
                story_content = component_gen.generate_footer_stories()
                story_path = f"src/components/Footer.stories.tsx"
            elif component_name == 'hero':
                story_content = component_gen.generate_hero_stories()
                story_path = f"src/components/Hero.stories.tsx"
            else:
                continue

            storybook_files.append(StorybookFile(
                name=f"{component.name}.stories.tsx",
                content=story_content,
                file_path=story_path
            ))

        # Generate test files
        test_files = []
        for component in generated_components:
            component_name = component.name.lower()
            if component_name == 'button':
                test_content = component_gen.generate_button_tests()
                test_path = f"src/components/Button.test.tsx"
            elif component_name == 'input':
                test_content = component_gen.generate_input_tests()
                test_path = f"src/components/Input.test.tsx"
            elif component_name == 'alert':
                test_content = component_gen.generate_alert_tests()
                test_path = f"src/components/Alert.test.tsx"
            elif component_name == 'select':
                test_content = component_gen.generate_select_tests()
                test_path = f"src/components/Select.test.tsx"
            elif component_name == 'badge':
                test_content = component_gen.generate_badge_tests()
                test_path = f"src/components/Badge.test.tsx"
            elif component_name == 'card':
                test_content = component_gen.generate_card_tests()
                test_path = f"src/components/Card.test.tsx"
            elif component_name == 'modal':
                test_content = component_gen.generate_modal_tests()
                test_path = f"src/components/Modal.test.tsx"
            elif component_name == 'table':
                test_content = component_gen.generate_table_tests()
                test_path = f"src/components/Table.test.tsx"
            elif component_name == 'tabs':
                test_content = component_gen.generate_tabs_tests()
                test_path = f"src/components/Tabs.test.tsx"
            elif component_name == 'navigation':
                test_content = component_gen.generate_navigation_tests()
                test_path = f"src/components/Navigation.test.tsx"
            elif component_name == 'breadcrumb':
                test_content = component_gen.generate_breadcrumb_tests()
                test_path = f"src/components/Breadcrumb.test.tsx"
            elif component_name == 'pagination':
                test_content = component_gen.generate_pagination_tests()
                test_path = f"src/components/Pagination.test.tsx"
            elif component_name == 'textarea':
                test_content = component_gen.generate_textarea_tests()
                test_path = f"src/components/Textarea.test.tsx"
            elif component_name == 'checkbox':
                test_content = component_gen.generate_checkbox_tests()
                test_path = f"src/components/Checkbox.test.tsx"
            elif component_name == 'radio':
                test_content = component_gen.generate_radio_tests()
                test_path = f"src/components/Radio.test.tsx"
            elif component_name == 'switch':
                test_content = component_gen.generate_switch_tests()
                test_path = f"src/components/Switch.test.tsx"
            elif component_name == 'search':
                test_content = component_gen.generate_search_tests()
                test_path = f"src/components/Search.test.tsx"
            elif component_name == 'datepicker':
                test_content = component_gen.generate_datepicker_tests()
                test_path = f"src/components/DatePicker.test.tsx"
            elif component_name == 'tooltip':
                test_content = component_gen.generate_tooltip_tests()
                test_path = f"src/components/Tooltip.test.tsx"
            elif component_name == 'avatar':
                test_content = component_gen.generate_avatar_tests()
                test_path = f"src/components/Avatar.test.tsx"
            elif component_name == 'progress':
                test_content = component_gen.generate_progress_tests()
                test_path = f"src/components/Progress.test.tsx"
            elif component_name == 'skeleton':
                test_content = component_gen.generate_skeleton_tests()
                test_path = f"src/components/Skeleton.test.tsx"
            elif component_name == 'accordion':
                test_content = component_gen.generate_accordion_tests()
                test_path = f"src/components/Accordion.test.tsx"
            elif component_name == 'container':
                test_content = component_gen.generate_container_tests()
                test_path = f"src/components/Container.test.tsx"
            elif component_name == 'stack':
                test_content = component_gen.generate_stack_tests()
                test_path = f"src/components/Stack.test.tsx"
            elif component_name == 'grid':
                test_content = component_gen.generate_grid_tests()
                test_path = f"src/components/Grid.test.tsx"
            elif component_name == 'sidebar':
                test_content = component_gen.generate_sidebar_tests()
                test_path = f"src/components/Sidebar.test.tsx"
            elif component_name == 'header':
                test_content = component_gen.generate_header_tests()
                test_path = f"src/components/Header.test.tsx"
            elif component_name == 'footer':
                test_content = component_gen.generate_footer_tests()
                test_path = f"src/components/Footer.test.tsx"
            elif component_name == 'hero':
                test_content = component_gen.generate_hero_tests()
                test_path = f"src/components/Hero.test.tsx"
            else:
                continue  # Skip other components for now

            test_files.append(TestFile(
                name=f"{component.name}.test.tsx",
                content=test_content,
                file_path=test_path
            ))

        # Add Jest config files
        test_files.extend([
            TestFile(
                name="jest.config.js",
                content=component_gen.generate_jest_config(),
                file_path="jest.config.js"
            ),
            TestFile(
                name="setupTests.ts",
                content=component_gen.generate_setup_tests(),
                file_path="src/setupTests.ts"
            )
        ])

        from models import ComponentLibrary
        component_library = ComponentLibrary(
            css_variables=css_variables,
            tailwind_config=tailwind_config,
            package_json=package_json,
            figma_tokens=component_gen.generate_figma_tokens(),
            components=generated_components,
            index_file=index_file,
            readme=readme,
            storybook_files=storybook_files,
            test_files=test_files
        )

        print(f"   ⚛️ Generated {len(generated_components)} React components")
        print(f"   🎨 Generated CSS variables and Tailwind config")

        # Generate comprehensive guidelines
        industry = design_principles.industry_context.industry if design_principles.industry_context else "unknown"
        from agents.knowledge_base import KnowledgeBase
        accessibility_reqs = KnowledgeBase.get_accessibility_requirements(industry)
        
        guidelines = {
            "color_usage": "Use semantic colors for status, primary colors for actions",
            "typography_scale": "Follow the defined scale - don't create arbitrary sizes",
            "spacing_system": f"Use {design_principles.density} spacing scale consistently",
            "component_variants": "Use variants purposefully - each serves a specific use case",
            "accessibility": f"All components must meet: {', '.join(accessibility_reqs)}",
            "industry_context": f"Designed for {industry} industry with {design_principles.philosophy} philosophy"
        }
        
        # Run comprehensive validation
        comprehensive_validation = Validator.validate_all(
            design_principles,
            design_tokens,
            component_inventory,
            industry,
            input_data.product_idea
        )

        output = DesignSystemOutput(
            input=input_data,
            principles=design_principles,
            tokens=design_tokens,
            components=component_inventory,
            component_library=component_library,
            guidelines=guidelines,
            generated_at=datetime.now().isoformat(),
            validation=comprehensive_validation
        )

        print("\n✅ Design system generation complete!")
        return output


def main():
    """Example usage of the design system generator."""

    # Example input for a B2B dashboard product
    input_data = DesignSystemInput(
        product_idea="A comprehensive analytics dashboard for e-commerce businesses to track sales performance, inventory levels, and customer behavior",
        target_users=["B2B", "enterprise"],
        brand_traits=["modern", "professional", "minimal"],
        platforms=["dashboard", "web"]
    )

    # Generate the design system
    generator = DesignSystemGenerator()
    result = generator.generate_design_system(input_data)

    # Save output to file
    import json
    output_file = f"design-system-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"

    with open(output_file, 'w') as f:
        json.dump(result.model_dump(), f, indent=2)

    print(f"\n💾 Design system saved to {output_file}")


if __name__ == "__main__":
    main()
