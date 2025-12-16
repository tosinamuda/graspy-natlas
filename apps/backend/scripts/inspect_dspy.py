import dspy
from app.domains.study.prompts import TopicExplainer

def inspect():
    explainer = dspy.ChainOfThought(TopicExplainer)
    print(f"Type: {type(explainer)}")
    print(f"Dir: {dir(explainer)}")
    
    if hasattr(explainer, 'predictor'):
        print("Has predictor")
        print(f"Predictor Type: {type(explainer.predictor)}")
        print(f"Predictor Demos: {getattr(explainer.predictor, 'demos', 'MISSING')}")
        
    # Try attaching
    explainer.demos = ["demo1"]
    
    if hasattr(explainer, 'predictor'):
        explainer.predictor.demos = ["demo2"]
        print(f"Predictor Demos after set: {getattr(explainer.predictor, 'demos', 'MISSING')}")

if __name__ == "__main__":
    inspect()
