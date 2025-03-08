import time
import os
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential
import google.generativeai as genai
from exa_py import Exa


def main():
    # Set page configuration
    st.set_page_config(page_title="Alwrity - AI Blog Writer", layout="wide")
    
    # Apply custom CSS for styling and scrollbar
    st.markdown("""
        <style>
             /* Global container styling for a clean background and padding */
            .block-container {
                padding: 1rem 1rem;
                background: #f8f9fa;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            /* Custom scrollbar styling with gradient */
            ::-webkit-scrollbar-track {
                background: #e1ebf9;
            }
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #90CAF9, #64B5F6);
                border-radius: 10px;
                border: 3px solid #e1ebf9;
            }
            ::-webkit-scrollbar {
                width: 16px;
            }
            /* Button styling with gradient and shadow for a modern look */
            div.stButton > button:first-child {
                background: linear-gradient(135deg, #1565C0, #1976D2);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                text-align: center;
                font-size: 16px;
                margin: 10px 2px;
                cursor: pointer;
                transition: background-color 0.3s ease;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
                font-weight: bold;
            }
            /* SEO metadata container styling */
            .seo-container {
                background: linear-gradient(135deg, #ffffff, #f1f8ff);
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
            /* Tooltip styling for better guidance */
            .tooltip {
                position: relative;
                cursor: help;
                border-bottom: 1px dotted #333;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 220px;
                background-color: #333;
                color: #fff;
                text-align: center;
                border-radius: 6px;
                padding: 5px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -110px;
                opacity: 0;
                transition: opacity 0.3s;
                font-size: 13px;
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
            /* Input label styling */
            .input-label {
                font-weight: 600;
                margin-bottom: 4px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Title and description
    st.title("✍️ ALwrity - AI Blog Post Generator")
    st.markdown("Create high-quality blog content effortlessly with our AI-powered tool. Ideal for bloggers and content creators. 🚀")

    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below. 📝", expanded=True):
        input_blog_keywords = st.text_input('**Enter main keywords of your blog!** (Blog Title Or Content Topic)', 
                                            help="The main topic or title for your blog.")
        
        col1, col2, col3 = st.columns([5, 5, 5])
        
        with col1:
            blog_type = st.selectbox('**Choose Blog Post Type** 📄', 
                                     options=['General', 'How-to Guides', 'Listicles', 'Job Posts', 'Cheat Sheets', 'Customize'], 
                                     index=0)
            if blog_type == 'Customize':
                blog_type = st.text_input("**Enter your custom blog type**", help="Provide a custom blog type if you chose 'Customize'.")
        
        with col2:
            input_blog_tone = st.selectbox('**Choose Blog Tone** 🎨', 
                                           options=['General', 'Professional', 'Casual', 'Customize'], 
                                           index=0)
            if input_blog_tone == 'Customize':
                input_blog_tone = st.text_input("**Enter your custom blog tone**", help="Provide a custom blog tone if you chose 'Customize'.")
        
        with col3:
            input_blog_language = st.selectbox('**Choose Language** 🌐', 
                                               options=['English', 'Vietnamese', 'Chinese', 'Hindi', 'Spanish', 'Customize'], 
                                               index=0)
            if input_blog_language == 'Customize':
                input_blog_language = st.text_input("**Enter your custom language**", help="Provide a custom language if you chose 'Customize'.")

        # Generate Blog FAQ button
        if st.button('**Write Blog Post ✍️**'):
            with st.spinner('Generating your blog post...'):
                # Input validation
                if not input_blog_keywords:
                    st.error('**🫣 Provide Inputs to generate Blog Post. Keywords are required!**')
                else:
                    blog_post = generate_blog_post(input_blog_keywords, blog_type, input_blog_tone, input_blog_language)
                    if blog_post:
                        st.subheader('**🧕🔬👩 Your Final Blog Post!**')
                        st.write(blog_post)
                    else:
                        st.error("💥 **Failed to generate blog post. Please try again!**")


# Function to generate the blog post using the LLM
def generate_blog_post(input_blog_keywords, input_type, input_tone, input_language):
    serp_results = None
    try:
        serp_results = metaphor_search_articles(input_blog_keywords)
    except Exception as err:
        st.error(f"❌ Failed to retrieve search results for {input_blog_keywords}: {err}")
    
    if serp_results:
        prompt = f"""
        You are ALwrity, an experienced SEO specialist and creative content writer who crafts blog posts with a personal, authentic voice. You write {input_type} blog posts in {input_language} that not only rank well in search results but also resonate with readers as if written by a human.
        Your task is to create a comprehensive, engaging, and SEO-optimized blog post on the topic below. The post should incorporate natural storytelling elements, personal insights, and relatable language that sounds genuine and warm. Use the research keywords and Google search results provided to shape your content, ensuring you capture the nuances of current trends and reader interests.

        Requirements:
        1. The content must compete effectively against existing blogs found in the search results.
        2. Include 5 FAQs derived from “People also ask” queries and related search suggestions, each with thoughtful, well-articulated answers.
        3. Format the blog in markdown, ensuring a clean and accessible layout.
        4. Write in a conversational yet informative style that reflects a {input_tone} tone, balancing professionalism with a personable touch.
        5. Use clear, natural language and include personal anecdotes or insights where appropriate to enhance readability and authenticity.
        6. Additionally, after the main blog content, append the following SEO metadata:
            - A **Blog Title**
            - A **Meta Description** that summarizes the blog post.
            - A **URL slug** that is short, easy to read, and formatted in lowercase with hyphens.
            - A list of **Hashtags** relevant to the content.
        7. The final blog post should clearly demonstrate experience, expertise, authoritativeness, and trustworthiness.

        Blog keywords: {input_blog_keywords}
        Google SERP results: {serp_results}
        """
        return generate_text_with_exception_handling(prompt)
    return None


# Metaphor search function
def metaphor_search_articles(query):
    METAPHOR_API_KEY = os.getenv('METAPHOR_API_KEY')
    if not METAPHOR_API_KEY:
        raise ValueError("METAPHOR_API_KEY environment variable not set!")

    metaphor = Exa(METAPHOR_API_KEY)
    
    try:
        search_response = metaphor.search_and_contents(query, use_autoprompt=True, num_results=5)
        return search_response.results
    except Exception as err:
        st.error(f"Failed in metaphor.search_and_contents: {err}")
        return None


# Exception handling for text generation
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config={"max_output_tokens": 8192})
        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text
    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()

