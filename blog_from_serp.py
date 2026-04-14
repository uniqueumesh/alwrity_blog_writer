import os
import streamlit as st
from exa_py import Exa
from prompts import load_prompt
from llm_client import generate_with_fallback


def main():
    # Set page configuration
    st.set_page_config(page_title="Alwrity - AI Blog Writer", layout="wide")
    
    # --- ALwrity Theme: Only use proven working CSS selectors ---
    st.markdown("""
        <style>
        ::-webkit-scrollbar-track {
            background: #e1ebf9;
        }
        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }
        ::-webkit-scrollbar {
            width: 16px;
        }
        div.stButton > button:first-child {
            background: #1565C0;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hide Streamlit header and footer for a clean look
    st.markdown('<style>header {visibility: hidden;}</style>', unsafe_allow_html=True)
    st.markdown('<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>', unsafe_allow_html=True)

    # Title and description
    st.title("✍️ Alwrity - AI Blog Post Generator")
    st.markdown("Create high-quality blog content effortlessly with our AI-powered tool. Ideal for bloggers and content creators. 🚀")

    # API Key Input Section
    with st.expander("API Configuration 🔑", expanded=False):
        st.markdown('''<p style="font-size:20px;">If the default API keys are unavailable or exceed their limits, you can provide your own API keys below.</p><br>
        <a href="https://metaphor.systems/" target="_blank">Get Metaphor API Key</a><br>
        <a href="https://aistudio.google.com/app/apikey" target="_blank">Get Gemini API Key</a>
        ''', unsafe_allow_html=True)
        user_metaphor_api_key = st.text_input("Metaphor API Key", type="password", help="Paste your Metaphor API Key here if you have one.")
        user_gemini_api_key = st.text_input("Gemini API Key", type="password", help="Paste your Gemini API Key here if you have one.")

    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below. 📝", expanded=True):
        # Full-width prompt/keywords input to match API key input width
        input_blog_keywords = st.text_area(
            "**🔑 Enter main keywords of your blog!** (Blog Title Or Content Topic)",
            height=80,
            placeholder="You can write a complete sentence or multiple keywords, e.g., 'How to start a vegetable garden in small spaces'.",
            help="Write a full sentence or provide multiple keywords for better results."
        )

        col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
        with col1:
            blog_type = st.selectbox('📝 Blog Post Type', options=['General', 'How-to Guides', 'Listicles', 'Job Posts', 'Cheat Sheets', 'Customize'], index=0)
            if blog_type == 'Customize':
                blog_type = st.text_input("Enter your custom blog type", help="Provide a custom blog type if you chose 'Customize'.")
        with col2:
            input_blog_tone = st.selectbox('🎨 Blog Tone', options=['General', 'Professional', 'Casual', 'Customize'], index=0)
            if input_blog_tone == 'Customize':
                input_blog_tone = st.text_input("Enter your custom blog tone", help="Provide a custom blog tone if you chose 'Customize'.")
        with col3:
            input_blog_language = st.selectbox('🌐 Language', options=['English', 'Vietnamese', 'Chinese', 'Hindi', 'Spanish', 'Customize'], index=0)
            if input_blog_language == 'Customize':
                input_blog_language = st.text_input("Enter your custom language", help="Provide a custom language if you chose 'Customize'.")
        with col4:
            blog_length = st.selectbox(
                '📏 Blog Length',
                options=['Short Form (500-800 words)', 'Long Detailed (2000+ words)'],
                index=0,  # Default to Short Form
                help="Choose the length of your blog post"
            )

        # Generate Blog Button
        if st.button('**Write Blog Post ✍️**'):
            with st.spinner('Generating your blog post...'):
                if not input_blog_keywords:
                    st.error('**🫣 Provide Inputs to generate Blog Post. Keywords are required!**')
                else:
                    metaphor_api_key = user_metaphor_api_key or os.getenv('METAPHOR_API_KEY')
                    gemini_api_key = user_gemini_api_key or os.getenv('GEMINI_API_KEY')
                    if not metaphor_api_key:
                        st.error("❌ Metaphor API Key is not available! Please provide your API key in the API Configuration section.")
                        return
                    if not gemini_api_key:
                        st.error("❌ Gemini API Key is not available! Please provide your API key in the API Configuration section.")
                        return
                    try:
                        blog_post = generate_blog_post(input_blog_keywords, blog_type, input_blog_tone, input_blog_language, blog_length, metaphor_api_key, gemini_api_key)
                        if blog_post:
                            st.subheader('**👩🧕🔬 Your Final Blog Post!**')
                            st.write(blog_post)
                        else:
                            st.error("💥 Failed to generate blog post. Please try again!")
                    except Exception as e:
                        if "quota exceeded" in str(e).lower():
                            st.error("❌ API limit exceeded! Please provide your own API key in the API Configuration section.")
                        else:
                            st.error("💥 Gemini is busy right now. Please try again in a minute.")


# Function to generate the blog post using the LLM
def generate_blog_post(input_blog_keywords, input_type, input_tone, input_language, blog_length, metaphor_api_key, gemini_api_key):
    serp_results = None
    try:
        serp_results = metaphor_search_articles(input_blog_keywords, metaphor_api_key)
    except Exception as err:
        st.error(f"❌ Failed to retrieve search results for {input_blog_keywords}: {err}")
    
    if serp_results:
        # Load appropriate prompt based on blog length selection
        prompt = load_prompt(blog_length, input_type, input_tone, input_language, input_blog_keywords, serp_results)
        return generate_text_with_exception_handling(prompt, gemini_api_key)
    return None


# Metaphor search function
def metaphor_search_articles(query, api_key):
    if not api_key:
        raise ValueError("Metaphor API Key is missing!")

    metaphor = Exa(api_key)
    
    try:
        search_response = metaphor.search_and_contents(query, num_results=5)
        return search_response.results
    except Exception as err:
        st.error(f"Failed in metaphor.search_and_contents: {err}")
        return None


def generate_text_with_exception_handling(prompt, api_key):
    try:
        return generate_with_fallback(prompt, api_key)
    except Exception as e:
        st.error(f"❌ Blog generation failed after fallback attempts: {e}")
        return None


if __name__ == "__main__":
    main()

