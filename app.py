import streamlit as st
from sdlc_steps.requirements import get_requirements
from sdlc_steps.user_stories import generate_user_stories, review_user_stories, revise_user_stories
from sdlc_steps.design_docs import generate_design_docs, review_design_docs, revise_design_docs
from sdlc_steps.code_gen import generate_code, review_code, revise_code
from sdlc_steps.security import review_security, fix_code_security
from sdlc_steps.test_cases import generate_test_cases, review_test_cases, revise_test_cases
from sdlc_steps.qa_testing import qa_testing, fix_code_qa
from utils import initialize_llm, process_step

# Initialize session state to store intermediate results and history
if "requirements" not in st.session_state:
    st.session_state.requirements = ""
if "user_stories" not in st.session_state:
    st.session_state.user_stories = ""
if "design_docs" not in st.session_state:
    st.session_state.design_docs = ""
if "code" not in st.session_state:
    st.session_state.code = ""
if "test_cases" not in st.session_state:
    st.session_state.test_cases = ""
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False
if "user_stories_history" not in st.session_state:
    st.session_state.user_stories_history = []
if "code_history" not in st.session_state:
    st.session_state.code_history = []
if "process_completed" not in st.session_state:
    st.session_state.process_completed = False

def main():
    st.title("Automated Software Development Lifecycle")
    st.write("This application automates the SDLC using LangChain and Groq LLMs. Provide your Groq API key and requirements to begin.")

    # API Key Input
    st.header("Step 0: Provide Groq API Key")
    api_key = st.text_input("Enter your Groq API key:", type="password")
    if st.button("Validate API Key"):
        success, message = initialize_llm(api_key)
        if success:
            st.session_state.api_key_valid = True
            st.success(message)
        else:
            st.session_state.api_key_valid = False
            st.error(f"Failed to validate API key: {message}")

    # Proceed only if API key is valid
    if not st.session_state.api_key_valid:
        st.warning("Please provide a valid Groq API key to proceed.")
        return

    # Create tabs for each SDLC phase
    tabs = st.tabs([
        "Requirements Gathering",
        "User Stories",
        "Design Documents",
        "Code Generation",
        "Security Review",
        "Test Case Generation",
        "QA Testing",
        "Final Results"
    ])

    # Progress bar
    total_steps = 7  # Number of SDLC phases
    progress = 0
    progress_bar = st.progress(0)

    # Tab 1: Requirements Gathering
    with tabs[0]:
        st.header("Requirements Gathering")
        requirements = get_requirements()
        if st.button("Start SDLC Process"):
            if requirements:
                st.session_state.requirements = requirements
                st.session_state.process_completed = False
                st.success("Requirements submitted successfully! Starting SDLC process...")

                # Run the entire SDLC process automatically
                try:
                    # Update progress after requirements submission
                    progress = 1 / total_steps
                    progress_bar.progress(progress)

                    # Step 2: User Stories
                    with tabs[1]:
                        st.header("User Stories Generation")
                        user_stories = process_step(
                            generate_user_stories, review_user_stories, revise_user_stories,
                            st.session_state.requirements, "User Stories Generation"
                        )
                        st.session_state.user_stories = user_stories
                        st.session_state.user_stories_history.append(user_stories)
                        progress = 2 / total_steps
                        progress_bar.progress(progress)
                        st.write("**Approved User Stories:**")
                        st.write(user_stories)

                    # Step 3: Design Documents
                    with tabs[2]:
                        st.header("Design Documents Creation")
                        design_docs = process_step(
                            generate_design_docs, review_design_docs, revise_design_docs,
                            st.session_state.user_stories, "Design Documents Creation"
                        )
                        st.session_state.design_docs = design_docs
                        progress = 3 / total_steps
                        progress_bar.progress(progress)
                        st.write("**Approved Design Documents:**")
                        st.write(design_docs)

                    # Step 4: Code Generation
                    with tabs[3]:
                        st.header("Code Generation")
                        code = process_step(
                            generate_code, review_code, revise_code,
                            st.session_state.design_docs, "Code Generation"
                        )
                        st.session_state.code = code
                        st.session_state.code_history.append(code)
                        progress = 4 / total_steps
                        progress_bar.progress(progress)
                        st.write("**Approved Code:**")
                        st.code(code, language="python")

                    # Step 5: Security Review
                    with tabs[4]:
                        st.header("Security Review")
                        approved, feedback = review_security(st.session_state.code)
                        code = st.session_state.code
                        while not approved:
                            st.write("Fixing code based on security feedback...")
                            code = fix_code_security(code, feedback)
                            st.write(f"Revised code:\n{code}")
                            st.session_state.code_history.append(code)
                            approved, feedback = review_security(code)
                        st.session_state.code = code
                        progress = 5 / total_steps
                        progress_bar.progress(progress)
                        st.write("Security review passed.")
                        st.write("**Final Code after Security Review:**")
                        st.code(code, language="python")

                    # Step 6: Test Case Generation
                    with tabs[5]:
                        st.header("Test Case Generation")
                        test_cases = process_step(
                            generate_test_cases, review_test_cases, revise_test_cases,
                            st.session_state.design_docs, "Test Case Generation"
                        )
                        st.session_state.test_cases = test_cases
                        progress = 6 / total_steps
                        progress_bar.progress(progress)
                        st.write("**Approved Test Cases:**")
                        st.write(test_cases)

                    # Step 7: QA Testing
                    with tabs[6]:
                        st.header("QA Testing")
                        approved, feedback = qa_testing(st.session_state.code, st.session_state.test_cases)
                        code = st.session_state.code
                        while not approved:
                            st.write("Fixing code based on QA feedback...")
                            code = fix_code_qa(code, feedback)
                            st.write(f"Revised code:\n{code}")
                            st.session_state.code_history.append(code)
                            approved, feedback = qa_testing(code, st.session_state.test_cases)
                        st.session_state.code = code
                        progress = 7 / total_steps
                        progress_bar.progress(progress)
                        st.write("QA testing passed.")
                        st.write("**Final Code after QA Testing:**")
                        st.code(code, language="python")

                    # Mark the process as completed
                    st.session_state.process_completed = True

                except Exception as e:
                    st.error(f"Error during SDLC process: {str(e)}")
                    return

    # Display results in tabs even if the process hasn't run yet
    with tabs[1]:
        if st.session_state.user_stories:
            st.header("User Stories Generation")
            st.write("**Approved User Stories:**")
            st.write(st.session_state.user_stories)

    with tabs[2]:
        if st.session_state.design_docs:
            st.header("Design Documents Creation")
            st.write("**Approved Design Documents:**")
            st.write(st.session_state.design_docs)

    with tabs[3]:
        if st.session_state.code:
            st.header("Code Generation")
            st.write("**Approved Code:**")
            st.code(st.session_state.code, language="python")

    with tabs[4]:
        if st.session_state.code:
            st.header("Security Review")
            st.write("**Final Code after Security Review:**")
            st.code(st.session_state.code, language="python")

    with tabs[5]:
        if st.session_state.test_cases:
            st.header("Test Case Generation")
            st.write("**Approved Test Cases:**")
            st.write(st.session_state.test_cases)

    with tabs[6]:
        if st.session_state.code:
            st.header("QA Testing")
            st.write("**Final Code after QA Testing:**")
            st.code(st.session_state.code, language="python")

    # Tab 8: Final Results
    with tabs[7]:
        st.header("Final Results")
        if st.session_state.process_completed:
            st.success("SDLC completed successfully!")
            st.subheader("Summary of Outputs:")
            st.write("**Requirements:**")
            st.write(st.session_state.requirements)
            st.write("**User Stories:**")
            st.write(st.session_state.user_stories)
            st.write("**Design Documents:**")
            st.write(st.session_state.design_docs)
            st.write("**Generated Code:**")
            st.code(st.session_state.code, language="python")
            st.write("**Test Cases:**")
            st.write(st.session_state.test_cases)
            # Display revision history
            st.subheader("Revision History")
            if st.session_state.user_stories_history:
                st.write("**User Stories Revisions:**")
                for i, rev in enumerate(st.session_state.user_stories_history):
                    st.write(f"Revision {i+1}:\n{rev}")
            if st.session_state.code_history:
                st.write("**Code Revisions:**")
                for i, rev in enumerate(st.session_state.code_history):
                    st.write(f"Revision {i+1}:\n{rev}")
        else:
            st.warning("The SDLC process is not yet complete. Please start the process in the Requirements Gathering tab.")

if __name__ == "__main__":
    main()