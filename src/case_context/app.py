"""Main application entry point with Streamlit UI."""

import streamlit as st

# Initial page configuration
st.set_page_config(
    page_title="Strategic-Case Auto-Writer",
    page_icon="📝",
    layout="wide"
)

# Pre-flight dependency check
try:
    import rapidfuzz
except ImportError:
    st.error(
        "⚠️ Missing dependency: **rapidfuzz**.\n\n"
        "Please run:\n\n"
        "    pip install rapidfuzz>=2.13.7\n\n"
        "in this environment, then restart the app."
    )
    st.stop()

import logging
from pathlib import Path

from case_context.extract import process_case_text
from case_context.map import analyze_case_context, identify_relevant_theories
from case_context.assemble import select_templates, generate_answer
from case_context.export import export_to_docx
from case_context.config import LOG_LEVEL, LOG_FORMAT

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def main():
    """Main application function."""
    st.title("Strategic-Case Auto-Writer")
    st.markdown("""
    Analyze case studies and generate strategic insights using AI-powered text analysis.
    """)
    
    # Input sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Case Text")
        case_text = st.text_area(
            "Paste the case study text here",
            height=300,
            key="case_text"
        )
    
    with col2:
        st.subheader("Question(s)")
        question_text = st.text_area(
            "Enter the question(s) to analyze",
            height=300,
            key="question_text"
        )
    
    st.subheader("Additional Instructions")
    instructions = st.text_area(
        "Optional: Add any specific instructions or constraints",
        height=100,
        key="instructions"
    )
    
    # Process button
    if st.button("Generate Analysis"):
        if not case_text or not question_text:
            st.error("Please provide both case text and question(s)")
            return
        
        with st.spinner("Analyzing case and generating insights..."):
            try:
                # Extract facts
                case_facts, question_facts = process_case_text(case_text, question_text)
                
                # Map concepts
                mapped_concepts = analyze_case_context(case_facts, question_facts)
                
                # Identify theories
                theories = identify_relevant_theories(
                    [concept for concepts in mapped_concepts.values() for concept in concepts]
                )
                
                # Select templates
                templates = select_templates(theories)
                
                # Generate answer
                answer = generate_answer(templates, mapped_concepts)
                
                # Display results
                st.subheader("Generated Analysis")
                st.write(answer)
                
                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Copy to Clipboard"):
                        st.code(answer)
                        st.success("Copied to clipboard!")
                
                with col2:
                    if st.button("Export to DOCX"):
                        output_path = export_to_docx(answer)
                        st.success(f"Exported to {output_path}")
                
            except Exception as e:
                logger.error(f"Error during analysis: {e}")
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 