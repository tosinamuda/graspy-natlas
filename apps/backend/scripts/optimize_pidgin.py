import sys
import os
import dspy
from dspy.teleprompt import BootstrapFewShotWithRandomSearch, MIPROv2

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.llm import get_openrouter_judge_lm, get_n_atlas_lm
from app.settings import get_settings
from app.domains.study.prompts import TopicExplainer
from app.domains.study.metrics import pidgin_metric

def optimize():
    print("DEBUG: Starting optimize script...", flush=True)
    # 1. Setup LMs
    settings = get_settings()
    print(f"DEBUG: N_ATLAS_API_BASE={settings.n_atlas_api_base}", flush=True)
    # Configure Student (N-Atlas for Pidgin)
    student_lm = get_n_atlas_lm()
    if not student_lm:
        print("Error: N-Atlas LM not configured (check N_ATLAS_API_BASE).")
        return

    dspy.settings.configure(lm=student_lm)
    print(f"Student LM: {student_lm.model}")

    judge_lm = get_openrouter_judge_lm()
    key_status = "FOUND" if judge_lm else "MISSING"
    print(f"DEBUG: Judge LM Status: {key_status}", flush=True)
    
    # 2. Define Dataset
    # We want the model to learn to speak Pidgin correctly.
    trainset = [
        dspy.Example(
            topic="Democracy", 
            language="Nigerian Pidgin English", 
            context="Explain the key concepts.",
            explanation="**Democracy** na system of goment where di pipo get power to choose dia leaders. In democracy, everybody get voice via voting. E mean say power belongs to di pipo, no be just one strong man."
        ).with_inputs("topic", "language", "context"),
        
        dspy.Example(
            topic="Photosynthesis", 
            language="Nigerian Pidgin English", 
            context="Structure with headers.",
            explanation="**Photosynthesis** na di way plants dey cook dia own food using sunlight. Just like we dey use stove cook rice, plants dey use sunlight, water, and carbon dioxide to make sugar used for energy."
        ).with_inputs("topic", "language", "context"),
        
        dspy.Example(
            topic="Love", 
            language="Nigerian Pidgin English", 
            context="Explain the emotion.",
            explanation="**Love** na strong feeling when you like person well well. E fit be for your family, your friend, or person you wan marry. Love dey make person do good things for another person without asking for payment."
        ).with_inputs("topic", "language", "context"),

        # Unlabeled for validation/bootstrapping (if it can generalize)
        dspy.Example(topic="Robotics", language="Nigerian Pidgin English", context="Explain for a primary school student.").with_inputs("topic", "language", "context"),
        dspy.Example(topic="Oxygen", language="Nigerian Pidgin English", context="Chemistry topic.").with_inputs("topic", "language", "context"),
    ]

    # 3. Define the Module to Optimize
    class ExplainerModule(dspy.Module):
        def __init__(self):
            super().__init__()
            self.generate = dspy.ChainOfThought(TopicExplainer)
        
        def forward(self, topic, language, context):
            print(f"DEBUG: Student Generating for {topic}...", flush=True)
            pred = self.generate(topic=topic, language=language, context=context)
            print(f"DEBUG: Student Result: {pred.explanation[:50]}...", flush=True)
            return pred

    # 4. Run Optimizer
    print("Starting Optimization...")
    
    # Using BootstrapFewShotWithRandomSearch to find good few-shot examples that satisfy the metric
    # This is often safer than instruction optimization for dialect adherence, as seeing examples helps more.
    teleprompter = BootstrapFewShotWithRandomSearch(
        metric=pidgin_metric,
        max_bootstrapped_demos=1, # Try to bootstrap 1 more from the model itself if possible
        max_labeled_demos=3,      # USE the golden examples!
        num_candidate_programs=5,
        num_threads=1 # Avoid rate limits
    )
    
    optimized_program = teleprompter.compile(ExplainerModule(), trainset=trainset)
    
    print("\nOptimization Complete!")
    # Save
    optimized_program.save("optimized_pidgin_explainer.json")
    print("Saved to optimized_pidgin_explainer.json")

if __name__ == "__main__":
    optimize()
