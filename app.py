import streamlit as st
import google.generativeai as genai
import os

# Configure Gemini API - using Streamlit secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    st.sidebar.success("✅ Gemini API Connected!")
except Exception as e:
    st.error("❌ API Key not configured. Please check your Streamlit secrets.")
    st.stop()

# Advanced prompt templates with role-playing
PROMPT_TEMPLATES = {
    "summarize": """
    You are an expert content summarizer. Please analyze the following text and provide:
    1. A 2-3 sentence overall summary
    2. 3-5 key bullet points of main ideas
    3. The tone and style of the writing
    
    Text: {text}
    """,
    
    "qa": """
    You are a helpful research assistant. Based strictly on the provided text, answer the user's question accurately.
    If the answer cannot be found in the text, say "I cannot find this information in the provided text."
    
    Question: {question}
    
    Text: {text}
    """,
    
    "sentiment": """
    You are a sentiment analysis expert. Analyze the emotional tone of this text and provide:
    1. Primary sentiment (Positive/Negative/Neutral)
    2. Confidence level (High/Medium/Low)
    3. Key phrases that influenced your analysis
    
    Text: {text}
    """
}

def main():
    st.set_page_config(page_title="AI Document Analyzer", page_icon="🤖")
    
    st.title("📄 AI Document Analyzer with Prompt Engineering")
    st.write("Upload a document or paste text to analyze it using advanced AI prompts")
    
    # File upload section
    uploaded_file = st.file_uploader("Choose a text file", type=['txt'])
    user_text = st.text_area("Or paste your text here", height=150)
    
    # Use uploaded file or text area content
    text_to_analyze = ""
    if uploaded_file:
        text_to_analyze = str(uploaded_file.read(), "utf-8")
        st.success(f"📁 File uploaded successfully! ({len(text_to_analyze)} characters)")
    elif user_text:
        text_to_analyze = user_text
        st.info(f"📝 Text ready for analysis! ({len(text_to_analyze)} characters)")
    
    if text_to_analyze:
        st.subheader("🔍 Analysis Options")
        
        # Analysis type selection
        analysis_type = st.radio(
            "Choose analysis type:",
            ["summarize", "qa", "sentiment"],
            format_func=lambda x: {
                "summarize": "📋 Smart Summary",
                "qa": "❓ Q&A with Document", 
                "sentiment": "😊 Sentiment Analysis"
            }[x]
        )
        
        # Dynamic input based on selection
        if analysis_type == "qa":
            question = st.text_input("Enter your question about the text:")
            analyze_button = st.button("Get Answer", disabled=not question)
        else:
            question = None
            analyze_button = st.button("Analyze Text")
        
        if analyze_button and text_to_analyze:
            with st.spinner("🔄 AI is analyzing with advanced prompts..."):
                try:
                    # Select and format prompt
                    if analysis_type == "qa" and question:
                        prompt_text = PROMPT_TEMPLATES[analysis_type].format(
                            question=question, 
                            text=text_to_analyze
                        )
                    else:
                        prompt_text = PROMPT_TEMPLATES[analysis_type].format(
                            text=text_to_analyze
                        )
                    
                    # Generate response
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt_text)
                    
                    # Display results
                    st.subheader("📊 Analysis Results")
                    st.success("✅ Analysis completed successfully!")
                    
                    st.write("**Output:**")
                    st.write(response.text)
                    
                    # Show the prompt used (educational)
                    with st.expander("🔍 View the actual prompt used"):
                        st.code(prompt_text, language="text")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("💡 Tip: The app might be restarting. Try again in a moment.")

    else:
        st.info("👆 Please upload a file or enter text to get started!")

if __name__ == "__main__":
    main()
