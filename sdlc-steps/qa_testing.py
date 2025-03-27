from utils import call_llm

def qa_testing(code, test_cases):
    prompt = (
        f"Given this code:\n{code}\nand these test cases:\n{test_cases}\n"
        "Determine if the code would pass all tests. Output 'PASSED' if yes, "
        "or 'FAILED: [description of failing tests]' if no."
    )
    response = call_llm(prompt)
    approved = "PASSED" in response
    feedback = "" if approved else response.replace("FAILED: ", "")
    return approved, feedback

def fix_code_qa(code, feedback):
    prompt = f"Based on this QA feedback:\n{feedback}\nFix this code:\n{code}"
    return call_llm(prompt)