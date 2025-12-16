import dspy
from app.config.llm import get_openrouter_judge_lm

class PidginAssessment(dspy.Signature):
    """
    Evaluate if the text is written in Nigerian Pidgin English.
    The text should NOT be standard English, and should NOT contain Yoruba, Igbo, or Hausa unless widely used in Pidgin.
    """
    text = dspy.InputField(desc="The text to evaluate")
    is_pidgin = dspy.OutputField(desc="YES or NO")
    reasoning = dspy.OutputField(desc="Why it is or isn't Pidgin")

def pidgin_metric(example, pred, trace=None):
    """
    Metric to evaluate if the prediction is valid Nigerian Pidgin.
    """
    judge_lm = get_openrouter_judge_lm()
    if not judge_lm:
        print("DEBUG: Judge LM is None! Check OPENROUTER_API_KEY.", flush=True)
        return 0.0
        
    explanation = pred.explanation
    print(f"DEBUG: Metric received explanation (len={len(explanation)}): {explanation[:50]}...", flush=True)
    
    # Define the judge module
    judge = dspy.ChainOfThought(PidginAssessment)
    
    try:
        with dspy.context(lm=judge_lm):
            print(f"DEBUG: Calling Judge...", flush=True)
            assessment = judge(text=explanation[:1000]) # Evaluate first 1000 chars to save tokens/time
            print(f"DEBUG: Judge result: IsPidgin={assessment.is_pidgin}, Reasoning={assessment.reasoning}", flush=True)
            
        if assessment.is_pidgin == "YES":
            return 1.0
    except Exception as e:
        print(f"DEBUG: Judge Failed with error: {e}", flush=True)
        return 0.0
    return 0.0
