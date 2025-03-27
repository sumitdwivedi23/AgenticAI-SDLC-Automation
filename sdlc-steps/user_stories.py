from utils import call_llm

def generate_user_stories(requirements):
    prompt = f"Generate detailed user stories based on these requirements:\n{requirements}"
    return call_llm(prompt)

def review_user_stories(user_stories):
    prompt = (
        f"Review these user stories:\n{user_stories}\n"
        "If they are complete and meet the requirements, output 'APPROVED'. "
        "Otherwise, output 'FEEDBACK: [your feedback here]'."
    )
    response = call_llm(prompt)
    approved = "APPROVED" in response
    feedback = "" if approved else response.replace("FEEDBACK: ", "")
    return approved, feedback

def revise_user_stories(user_stories, feedback):
    prompt = f"Based on this feedback:\n{feedback}\nRevise these user stories:\n{user_stories}"
    return call_llm(prompt)