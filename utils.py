import os
import hashlib
from langchain_groq import ChatGroq
from groq import Groq as GroqClient

# Global variables
llm = None
cache = {}  # In-memory cache for LLM responses

def initialize_llm(api_key):
    """Initialize the Groq LLM with the provided API key."""
    global llm
    try:
        # Set the GROQ_API_KEY environment variable
        os.environ["GROQ_API_KEY"] = api_key
        # Initialize the ChatGroq LLM directly (no need for a separate client)
        llm = ChatGroq(model="qwen-2.5-coder-32b", temperature=0.7)
        return True, "API key validated successfully!"
    except Exception as e:
        return False, str(e)

def call_llm(prompt):
    """Call the LLM with caching."""
    if llm is None:
        raise Exception("LLM not initialized. Please provide a valid Groq API key.")
    
    # Use prompt hash as cache key
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    if prompt_hash in cache:
        return cache[prompt_hash]
    
    # Since ChatGroq expects a list of messages, wrap the prompt in a HumanMessage
    from langchain_core.messages import HumanMessage
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    # Extract the content from the response
    response_content = response.content
    cache[prompt_hash] = response_content
    return response_content

def process_step(generate_fn, review_fn, revise_fn, input_data, step_name, max_revisions=3):
    """
    Generic function to process a step with generation, review, and revision loops.
    """
    import streamlit as st

    st.write(f"{step_name} in progress...")
    output = generate_fn(input_data)
    st.write(f"Generated output:\n{output}")

    approved, feedback = review_fn(output)
    revision_count = 0

    while not approved and revision_count < max_revisions:
        st.write(f"Revising based on feedback:\n{feedback}")
        output = revise_fn(output, feedback)
        st.write(f"Revised output:\n{output}")
        approved, feedback = review_fn(output)
        revision_count += 1

        # Store revision history
        if step_name == "User Stories Generation":
            st.session_state.user_stories_history.append(output)
        elif step_name == "Code Generation":
            st.session_state.code_history.append(output)

    if not approved:
        st.error(f"Failed to get approval for {step_name} after {max_revisions} revisions.")
        raise Exception(f"{step_name} approval failed.")
    
    st.write(f"{step_name} approved.")
    return output