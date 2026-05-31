import streamlit as st


BLOG_TYPE_OPTIONS = [
    "General",
    "How-to Guides",
    "Listicles",
    "Job Posts",
    "Cheat Sheets",
    "Customize",
]

BLOG_TONE_OPTIONS = [
    "General",
    "Professional",
    "Casual",
    "Customize",
]

BLOG_LANGUAGE_OPTIONS = [
    "English",
    "Vietnamese",
    "Chinese",
    "Hindi",
    "Spanish",
    "Customize",
]

BLOG_LENGTH_OPTIONS = [
    "Short Form (500-800 words)",
    "Long Detailed (2000+ words)",
]

BLOG_TYPE_HELP = """
General: Standard blog format for broad informational topics.
How-to Guides: Step-by-step instructional content that teaches a process.
Listicles: Numbered or bullet-style posts for quick scanning and easy reading.
Job Posts: Hiring-focused content for roles, responsibilities, and candidate expectations.
Cheat Sheets: Compact reference-style content with quick tips, shortcuts, or summaries.
Customize: Enter your own blog format when the preset types do not match your need.
"""

BLOG_TONE_HELP = """
General: Balanced writing style suitable for most blog topics.
Professional: Formal, polished, and business-friendly tone for expert or brand content.
Casual: Relaxed, simple, and conversational tone for approachable reader engagement.
Customize: Enter your own tone when you need a specific voice or style.
"""


def render_blog_form():
    input_blog_keywords = st.text_area(
        "**🔑 Enter main keywords of your blog!** (Blog Title Or Content Topic)",
        height=80,
        placeholder="You can write a complete sentence or multiple keywords, e.g., 'How to start a vegetable garden in small spaces'.",
        help="Write a full sentence or provide multiple keywords for better results.",
    )

    col1, col2, col3, col4 = st.columns([5, 5, 5, 5])
    with col1:
        blog_type = st.selectbox(
            "📝 Blog Post Type",
            options=BLOG_TYPE_OPTIONS,
            index=0,
            help=BLOG_TYPE_HELP,
        )
        if blog_type == "Customize":
            blog_type = st.text_input(
                "Enter your custom blog type",
                help="Provide a custom blog type if you chose 'Customize'.",
            )
    with col2:
        input_blog_tone = st.selectbox(
            "🎨 Blog Tone",
            options=BLOG_TONE_OPTIONS,
            index=0,
            help=BLOG_TONE_HELP,
        )
        if input_blog_tone == "Customize":
            input_blog_tone = st.text_input(
                "Enter your custom blog tone",
                help="Provide a custom blog tone if you chose 'Customize'.",
            )
    with col3:
        input_blog_language = st.selectbox(
            "🌐 Language",
            options=BLOG_LANGUAGE_OPTIONS,
            index=0,
        )
        if input_blog_language == "Customize":
            input_blog_language = st.text_input(
                "Enter your custom language",
                help="Provide a custom language if you chose 'Customize'.",
            )
    with col4:
        blog_length = st.selectbox(
            "📏 Blog Length",
            options=BLOG_LENGTH_OPTIONS,
            index=0,
            help="Choose the length of your blog post",
        )

    return {
        "keywords": input_blog_keywords,
        "blog_type": blog_type,
        "blog_tone": input_blog_tone,
        "language": input_blog_language,
        "blog_length": blog_length,
    }
