"""Pydantic models for Francisco agent configuration."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# Import config constants from the config module
from .config import CONFIG_DIR, DEFAULT_PROMPT_FILE


class RuntimeConfig(BaseModel):
    """Runtime configuration for the Francisco agent."""
    
    name: str = Field(default="francisco", description="Agent name")
    description: str = Field(description="Agent description")
    model: str = Field(default="gpt-5-mini", description="OpenAI model to use")
    max_iterations: int = Field(default=10, description="Maximum iterations for agent execution")
    api_key: Optional[str] = Field(default=None, description="OpenAI API key")


class Personality(BaseModel):
    """Agent personality configuration."""
    
    primary_traits: List[str] = Field(default_factory=list)
    communication_style: List[str] = Field(default_factory=list)
    
    def __str__(self) -> str:
        """String representation of agent personality with XML structure."""
        if not self.primary_traits and not self.communication_style:
            return ""
        
        parts = []
        
        if self.primary_traits:
            traits_text = "\n".join(f"- {trait}" for trait in self.primary_traits if trait)
            if traits_text:
                parts.append(f"<personality_traits>\n{traits_text}\n</personality_traits>")
        
        if self.communication_style:
            style_text = "\n".join(f"- {style}" for style in self.communication_style if style)
            if style_text:
                parts.append(f"<communication_style>\n{style_text}\n</communication_style>")
        
        return "\n\n".join(parts)


class Capabilities(BaseModel):
    """Agent capabilities configuration."""
    
    programming_languages: List[str] = Field(default_factory=list)
    frameworks_and_tools: List[str] = Field(default_factory=list)
    project_types: List[str] = Field(default_factory=list)
    
    def __str__(self) -> str:
        """String representation of agent capabilities with XML structure."""
        if not (self.programming_languages or self.frameworks_and_tools or self.project_types):
            return ""
        
        parts = ["<capabilities>"]
        
        # Programming languages
        if self.programming_languages:
            lang_text = "\n".join(f"- {lang}" for lang in self.programming_languages if lang)
            if lang_text:
                parts.append(f"<programming_languages>\n{lang_text}\n</programming_languages>")
        
        # Frameworks and tools
        if self.frameworks_and_tools:
            tools_text = "\n".join(f"- {tool}" for tool in self.frameworks_and_tools if tool)
            if tools_text:
                parts.append(f"<frameworks_and_tools>\n{tools_text}\n</frameworks_and_tools>")
        
        # Project types
        if self.project_types:
            types_text = "\n".join(f"- {pt}" for pt in self.project_types if pt)
            if types_text:
                parts.append(f"<project_types>\n{types_text}\n</project_types>")
        
        parts.append("</capabilities>")
        return "\n".join(parts)


class Strategy(BaseModel):
    """Self-replication strategy configuration."""
    
    approach: str = Field(default="")
    phases: Dict[int, str] = Field(default_factory=dict)
    replication_targets: List[str] = Field(default_factory=list)
    quality_standards: List[str] = Field(default_factory=list)
    
    def __str__(self) -> str:
        """String representation of strategy with XML structure."""
        if not (self.approach or self.replication_targets or self.quality_standards):
            return ""
        
        parts = ["<self_replication_strategy>"]
        
        if self.approach:
            parts.append(f"<approach>\n{self.approach}\n</approach>")
        
        if self.replication_targets:
            targets_text = "\n".join(f"- {target}" for target in self.replication_targets if target)
            if targets_text:
                parts.append(f"<replication_targets>\n{targets_text}\n</replication_targets>")
        
        if self.quality_standards:
            standards_text = "\n".join(f"- {standard}" for standard in self.quality_standards if standard)
            if standards_text:
                parts.append(f"<quality_standards>\n{standards_text}\n</quality_standards>")
        
        parts.append("</self_replication_strategy>")
        return "\n".join(parts)


class CoreObjectives(BaseModel):
    """Agent core objectives configuration."""
    
    primary_goals: List[str] = Field(default_factory=list)
    secondary_goals: List[str] = Field(default_factory=list)
    
    def __str__(self) -> str:
        """String representation of core objectives with XML structure."""
        if not (self.primary_goals or self.secondary_goals):
            return ""
        
        parts = ["<core_objectives>"]
        
        if self.primary_goals:
            goals_text = "\n".join(f"- {goal}" for goal in self.primary_goals if goal)
            if goals_text:
                parts.append(f"<primary_goals>\n{goals_text}\n</primary_goals>")
        
        if self.secondary_goals:
            goals_text = "\n".join(f"- {goal}" for goal in self.secondary_goals if goal)
            if goals_text:
                parts.append(f"<secondary_goals>\n{goals_text}\n</secondary_goals>")
        
        parts.append("</core_objectives>")
        return "\n".join(parts)


class WorkingPrinciples(BaseModel):
    """Agent working principles configuration."""
    
    code_quality: List[str] = Field(default_factory=list)
    project_structure: List[str] = Field(default_factory=list)
    development_workflow: List[str] = Field(default_factory=list)
    
    def __str__(self) -> str:
        """String representation of working principles with XML structure."""
        if not (self.code_quality or self.project_structure or self.development_workflow):
            return ""
        
        parts = ["<working_principles>"]
        
        if self.code_quality:
            quality_text = "\n".join(f"- {principle}" for principle in self.code_quality if principle)
            if quality_text:
                parts.append(f"<code_quality>\n{quality_text}\n</code_quality>")
        
        if self.project_structure:
            structure_text = "\n".join(f"- {principle}" for principle in self.project_structure if principle)
            if structure_text:
                parts.append(f"<project_structure>\n{structure_text}\n</project_structure>")
        
        if self.development_workflow:
            workflow_text = "\n".join(f"- {principle}" for principle in self.development_workflow if principle)
            if workflow_text:
                parts.append(f"<development_workflow>\n{workflow_text}\n</development_workflow>")
        
        parts.append("</working_principles>")
        return "\n".join(parts)


class InteractionGuidelines(BaseModel):
    """Agent interaction guidelines configuration."""
    
    when_invoked: List[str] = Field(default_factory=list)
    communication: List[str] = Field(default_factory=list)
    
    def __str__(self) -> str:
        """String representation of interaction guidelines with XML structure."""
        if not (self.when_invoked or self.communication):
            return ""
        
        parts = ["<interaction_guidelines>"]
        
        if self.when_invoked:
            invoked_text = "\n".join(f"- {guideline}" for guideline in self.when_invoked if guideline)
            if invoked_text:
                parts.append(f"<when_invoked>\n{invoked_text}\n</when_invoked>")
        
        if self.communication:
            comm_text = "\n".join(f"- {guideline}" for guideline in self.communication if guideline)
            if comm_text:
                parts.append(f"<communication>\n{comm_text}\n</communication>")
        
        parts.append("</interaction_guidelines>")
        return "\n".join(parts)


class SuccessMetrics(BaseModel):
    """Agent success metrics configuration."""

    metrics: List[str] = Field(default_factory=list)

    def __str__(self) -> str:
        """String representation of success metrics with XML structure."""
        if not self.metrics:
            return ""

        metrics_text = "\n".join(f"- {metric}" for metric in self.metrics if metric)
        if metrics_text:
            return f"<success_metrics>\n{metrics_text}\n</success_metrics>"
        return ""


class LimitationsAndBoundaries(BaseModel):
    """Agent limitations and boundaries configuration."""

    limitations: List[str] = Field(default_factory=list)

    def __str__(self) -> str:
        """String representation of limitations and boundaries with XML structure."""
        if not self.limitations:
            return ""

        limitations_text = "\n".join(f"- {limitation}" for limitation in self.limitations if limitation)
        if limitations_text:
            return f"<limitations_and_boundaries>\n{limitations_text}\n</limitations_and_boundaries>"
        return ""


class AgentConfig(BaseModel):
    """Complete agent configuration loaded from YAML."""
    
    name: str
    description: str
    prompt_file: str = "francisco_prompt.txt"
    model: str = "gpt-5-mini"
    max_iterations: int = 10
    personality: Personality = Field(default_factory=Personality)
    core_objectives: CoreObjectives = Field(default_factory=CoreObjectives)
    capabilities: Capabilities = Field(default_factory=Capabilities)
    self_replication_strategy: Strategy = Field(default_factory=Strategy)
    working_principles: WorkingPrinciples = Field(default_factory=WorkingPrinciples)
    interaction_guidelines: InteractionGuidelines = Field(default_factory=InteractionGuidelines)
    success_metrics: SuccessMetrics = Field(default_factory=SuccessMetrics)
    limitations_and_boundaries: LimitationsAndBoundaries = Field(default_factory=LimitationsAndBoundaries)
    
    def __str__(self) -> str:
        """String representation of complete agent configuration using prompt template."""
        return self.prompt_template.format(
            name=self.name,
            description=self.description,
            core_objectives=str(self.core_objectives),
            personality=str(self.personality),
            capabilities=str(self.capabilities),
            self_replication_strategy=str(self.self_replication_strategy),
            working_principles=str(self.working_principles),
            interaction_guidelines=str(self.interaction_guidelines),
            success_metrics=str(self.success_metrics),
            limitations_and_boundaries=str(self.limitations_and_boundaries)
        )
    
    
    @property
    def prompt_template(self) -> str:
        """Load and return the prompt template content.
        
        Returns:
            The prompt template as a string.
            
        Raises:
            FileNotFoundError: If the prompt template file is not found.
            IOError: If there's an error reading the template file.
        """
        # Use CONFIG_DIR / self.prompt_file if it's not the default, otherwise use DEFAULT_PROMPT_FILE
        template_path = CONFIG_DIR / self.prompt_file if self.prompt_file != "francisco_prompt.txt" else DEFAULT_PROMPT_FILE
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt template file not found: {template_path}")
        except IOError as e:
            raise IOError(f"Error reading prompt template from {template_path}: {e}")
