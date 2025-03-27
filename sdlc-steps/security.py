from utils import call_llm

def review_security(code):
    prompt = (
        f"Analyze this code for security vulnerabilities:\n{code}\n"
        "If no issues are found, output 'APPROVED'. "
        "Otherwise, output 'FEEDBACK: [list of vulnerabilities and suggestions]'."
    )
    response = call_llm(prompt)
    approved = "APPROVED" in response
    feedback = "" if approved else response.replace("FEEDBACK: ", "")
    return approved, feedback

def fix_code_security(code, feedback):
    prompt = f"Based on this security feedback:\n{feedback}\nFix this code:\n{code}"
    return call_llm(prompt)