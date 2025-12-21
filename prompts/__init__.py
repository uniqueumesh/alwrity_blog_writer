"""
Prompts package for Alwrity Blog Writer
Exports prompt loading and formatting functions
"""
from .prompt_loader import load_prompt
from .short_blog_prompt import get_short_blog_prompt
from .long_blog_prompt import get_long_blog_prompt

__all__ = ['load_prompt', 'get_short_blog_prompt', 'get_long_blog_prompt']

