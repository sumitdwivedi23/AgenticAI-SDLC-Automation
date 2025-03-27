from utils import call_llm

def generate_test_cases(design_docs):
    prompt = f"Generate comprehensive test cases based on these design documents:\n{design_docs}"
    return call_llm(prompt)

def review_test_cases(test_cases):
    prompt = (
        f"Review these test cases:\n{test_cases}\n"
        "If they are thorough and cover all scenarios, output 'APPROVED'. "
        "Otherwise, output 'FEEDBACK: [your feedback here]'."
    )
    response = call_llm(prompt)
    approved = "APPROVED" in response
    feedback = "" if approved else response.replace("FEEDBACK: ", "")
    return approved, feedback

def revise_test_cases(test_cases, feedback):
    prompt = f"Based on this feedback:\n{feedback}\nRevise these test cases:\n{test_cases}"
    return call_llm(prompt)