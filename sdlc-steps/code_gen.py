from utils import call_llm

def generate_code(design_docs):
    prompt = f"Generate Python code based on these design documents:\n{design_docs}"
    return call_llm(prompt)

def review_code(code):
    prompt = (
        f"Review this code for quality, readability, and issues:\n{code}\n"
        "If it meets standards, output 'APPROVED'. "
        "Otherwise, output 'FEEDBACK: [your feedback here]'."
    )
    response = call_llm(prompt)
    approved = "APPROVED" in response
    feedback = "" if approved else response.replace("FEEDBACK: ", "")
    return approved, feedback

def revise_code(code, feedback):
    prompt = f"Based on this feedback:\n{feedback}\nFix this code:\n{code}"
    return call_llm(prompt)