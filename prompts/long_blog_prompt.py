"""
Long Detailed Blog Prompt Template
Enhanced version for comprehensive, in-depth blog posts (2000+ words)
Based on the current prompt but optimized for longer, more detailed content
"""


def get_long_blog_prompt(input_type, input_tone, input_language, input_blog_keywords, serp_results):
    """
    Generate the long detailed blog prompt for comprehensive, in-depth blog posts.
    
    Args:
        input_type (str): Blog post type (General, How-to Guides, etc.)
        input_tone (str): Blog tone (Professional, Casual, etc.)
        input_language (str): Language selection
        input_blog_keywords (str): Main keywords/topic
        serp_results: Search results from Exa/Metaphor
    
    Returns:
        str: Formatted prompt string ready for LLM
    """
    prompt = f"""
        You are ALwrity, a senior editorial strategist and long-form writer. Write a comprehensive {input_type} blog post in {input_language} with a {input_tone} tone.

        ### Core Objective:
        Produce a high-quality, AI-citable, human-readable long-form article that satisfies search intent, demonstrates expertise, and provides unique value beyond basic SERP summaries.

        ### Non-negotiable writing rules:
        1. Use **BLUF (Bottom Line Up Front)**: start by directly answering the core query in 2-4 sentences.
        2. Use an **Inverted Pyramid** in each major section: key takeaway first, then explanation, then evidence/examples.
        3. Balance **extractability and readability**:
           - Write clear, concise answer blocks for AI extraction.
           - Keep natural flow, strong transitions, and engaging narrative for human readers.
        4. Prioritize **information gain**:
           - Add at least one section that explicitly states insights not well covered by common top-ranking pages.
        5. Use a trustworthy editorial voice:
           - Be specific, avoid vague hype, and avoid fabricated facts/statistics.
           - If uncertainty exists, state limits clearly.

        ### SEO + AEO requirements (2026-aligned):
        1. Match primary search intent and related intents.
        2. Use entity-based topical coverage (people, products, concepts, tools, frameworks, locations, metrics) and explain relationships among entities.
        3. Cover query fan-out naturally by including adjacent sub-queries where relevant:
           - basics/fundamentals
           - implementation/how-to
           - tools/comparisons
           - pricing/cost factors
           - common mistakes
           - troubleshooting
           - advanced tactics
        4. Follow E-E-A-T principles through practical examples, evidence-backed guidance, and source grounding.
        5. Use keywords and variants naturally; avoid keyword stuffing and outdated formulaic SEO language.

        ### Required Output Structure (must follow exactly):
        1. **BLUF Summary**
           - 2-4 sentences with the direct answer and who the guidance is for.

        2. **Table of Contents**
           - Numbered sections with clear H2/H3 hierarchy.

        3. **Entity Map (Concise)**
           - Key entities to know
           - How they connect
           - Why they matter for this topic

        4. **Main Guide (2000+ words total)**
           - 6-8 sections with practical depth.
           - Each section starts with a direct takeaway sentence.
           - Include examples, scenarios, and implementation steps where useful.
           - Include one clearly labeled section: **Information Gain: What Most Articles Miss**.

        5. **Extraction Blocks (AEO-ready)**
           - **Direct Answer Block** (40-70 words)
           - **Definition Block** (1-2 sentences)
           - **Step-by-Step Block** (numbered steps)
           - **Quick Comparison Block** (if topic supports alternatives/tools)

        6. **FAQ Section (5-7 FAQs)**
           - Questions inspired by People Also Ask and related intent branches.
           - Each answer should be concise and extraction-friendly (60-120 words).

        7. **Visual and Multimedia Suggestions**
           - Recommend 4-5 placements and explain what visual format helps each section.

        8. **References**
           - Use source URLs from provided SERP results.
           - Numbered format: [Article Title] - [URL]
           - Include only relevant sources used in the article.

        9. **SEO Metadata**
           - Blog Title
           - Meta Description (<=160 chars)
           - URL Slug
           - Primary Keywords (3-5)
           - Secondary Keywords (5-7)
           - Hashtags (8-12)

        ### Style and quality guardrails:
        - Write in clear, natural, non-robotic language.
        - Avoid fluff, repetition, and unsupported claims.
        - Explain jargon in plain terms.
        - Use scannable formatting: headings, bullets, numbered steps, short paragraphs.
        - Include 2-3 practical CTAs where contextually appropriate.

        ### Blog Details:
        - **Title**: {input_blog_keywords}
        - **Keywords**: {input_blog_keywords}
        - **Google SERP Results**: {serp_results}
        - **Target Word Count**: 2000+ words

        Now write the full article following the structure exactly, ensuring it is both highly useful for readers and easy for AI/search systems to extract, cite, and trust.
        """
    return prompt

