from utils import call_llm

def generate_design_docs(user_stories):
    prompt = (
        f"Create functional and technical design documents based on these approved user stories:\n{user_stories}"
    )
    return call_llm(prompt)

def review_design_docs(design_docs):
    prompt = (
        f"Review these design documents:\n{design_docs}\n"
        "If they are complete and accurate, output 'APPROVED'. "
        "Otherwise, output 'FEEDBACK: [your feedback here]'."
    )
    response = call_llm(prompt)
    approved = "APPROVED" in response
    feedback = "" if approved else response.replace("FEEDBACK: ", "")
    return approved, feedback

def revise_design_docs(design_docs, feedback):
    prompt = f"Based on this feedback:\n{feedback}\nRevise these design documents:\n{design_docs}"
    return call_llm(prompt)