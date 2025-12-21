"""
Utility module for loading and selecting appropriate prompts based on blog length
"""
from .short_blog_prompt import get_short_blog_prompt
from .long_blog_prompt import get_long_blog_prompt


def load_prompt(blog_length, input_type, input_tone, input_language, input_keywords, serp_results):
    """
    Load and format the appropriate prompt based on blog length selection.
    
    Args:
        blog_length (str): 'Short Form (500-800 words)' or 'Long Detailed (2000+ words)'
        input_type (str): Blog post type (General, How-to Guides, etc.)
        input_tone (str): Blog tone (Professional, Casual, etc.)
        input_language (str): Language selection
        input_keywords (str): Main keywords/topic
        serp_results: Search results from Exa/Metaphor
    
    Returns:
        str: Formatted prompt string ready for LLM
    """
    # Check if user selected Short Form blog
    if 'Short Form' in blog_length or '500-800' in blog_length:
        return get_short_blog_prompt(input_type, input_tone, input_language, input_keywords, serp_results)
    
    # Check if user selected Long Detailed blog
    elif 'Long Detailed' in blog_length or '2000+' in blog_length:
        return get_long_blog_prompt(input_type, input_tone, input_language, input_keywords, serp_results)
    
    # Default to short form if selection is unclear
    else:
        return get_short_blog_prompt(input_type, input_tone, input_language, input_keywords, serp_results)

