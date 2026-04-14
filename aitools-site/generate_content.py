"""
Daily Content Generator
Automatically writes new SEO-optimized affiliate articles every day.
Uses Groq API (free) to generate content.
Runs via GitHub Actions — publishes directly to your site.
"""

import os
import json
import random
import requests
from datetime import datetime

GROQ_KEY = os.environ.get("GROQ_API_KEY", "")

# High-traffic article topics — all get lots of Google searches
ARTICLE_IDEAS = [
    # Comparison articles (highest converting)
    {"title": "Jasper AI vs Writesonic 2026: Which is Better?",
     "slug": "jasper-vs-writesonic",
     "keyword": "jasper vs writesonic",
     "type": "comparison"},

    {"title": "ChatGPT vs Gemini 2026: Complete Comparison",
     "slug": "chatgpt-vs-gemini",
     "keyword": "chatgpt vs gemini 2026",
     "type": "comparison"},

    {"title": "Midjourney vs DALL-E 3: Best AI Image Generator?",
     "slug": "midjourney-vs-dalle",
     "keyword": "midjourney vs dalle 3",
     "type": "comparison"},

    {"title": "Grammarly vs ProWritingAid 2026",
     "slug": "grammarly-vs-prowritingaid",
     "keyword": "grammarly vs prowritingaid",
     "type": "comparison"},

    # Best-of lists (high traffic)
    {"title": "10 Best AI Tools for Freelancers 2026",
     "slug": "best-ai-tools-freelancers",
     "keyword": "best ai tools for freelancers",
     "type": "listicle"},

    {"title": "7 Best Free AI Image Generators 2026 (No Sign-up)",
     "slug": "best-free-ai-image-generators",
     "keyword": "free ai image generator no sign up",
     "type": "listicle"},

    {"title": "5 Best AI Tools for Social Media 2026",
     "slug": "best-ai-tools-social-media",
     "keyword": "best ai tools social media",
     "type": "listicle"},

    {"title": "Best AI Tools for Students 2026 (Free & Paid)",
     "slug": "best-ai-tools-students",
     "keyword": "best ai tools for students",
     "type": "listicle"},

    {"title": "Best AI Video Generators 2026 — Ranked",
     "slug": "best-ai-video-generators",
     "keyword": "best ai video generator 2026",
     "type": "listicle"},

    {"title": "10 Best AI Chatbots in 2026",
     "slug": "best-ai-chatbots",
     "keyword": "best ai chatbot 2026",
     "type": "listicle"},

    # How-to articles (great for SEO)
    {"title": "How to Use Claude AI for Free in 2026",
     "slug": "how-to-use-claude-ai-free",
     "keyword": "how to use claude ai free",
     "type": "howto"},

    {"title": "How to Make Money with AI Tools in 2026",
     "slug": "make-money-ai-tools",
     "keyword": "make money with ai tools",
     "type": "howto"},

    {"title": "How to Use ChatGPT for Beginners 2026",
     "slug": "how-to-use-chatgpt-beginners",
     "keyword": "how to use chatgpt beginners",
     "type": "howto"},

    # India-specific (low competition, good traffic)
    {"title": "Best AI Tools for Indians Under ₹500/Month",
     "slug": "best-ai-tools-india-cheap",
     "keyword": "best ai tools india cheap",
     "type": "india"},

    {"title": "Best Free AI Writing Tools for Indian Bloggers",
     "slug": "free-ai-writing-tools-india",
     "keyword": "free ai writing tools india",
     "type": "india"},

    {"title": "Canva Pro vs Free: Worth It for Indian Creators?",
     "slug": "canva-pro-vs-free-india",
     "keyword": "canva pro vs free india",
     "type": "comparison"},
]

# Affiliate links — replace YOUR_ID with your actual affiliate IDs
AFFILIATE_LINKS = {
    "writesonic": "https://writesonic.com?via=YOUR_ID",
    "jasper":     "https://jasper.ai?fpr=YOUR_ID",
    "rytr":       "https://rytr.me?via=YOUR_ID",
    "canva":      "https://canva.com/affiliates/YOUR_ID",
    "grammarly":  "https://grammarly.com/partner/YOUR_ID",
    "pictory":    "https://pictory.ai?affiliate=YOUR_ID",
}

SYSTEM_PROMPT = """You are an expert affiliate marketing content writer.
Write SEO-optimized, honest, helpful articles about AI tools.
Always include honest pros AND cons. Never fake reviews.
Write in a conversational, trustworthy tone.
Include specific details, numbers, and real comparisons.
RESPOND ONLY WITH VALID JSON."""

def generate_article(idea: dict) -> dict:
    """Generate a full article using Groq free API."""
    if not GROQ_KEY:
        raise ValueError("No GROQ_API_KEY set")

    prompt = f"""Write a complete SEO article for the topic: "{idea['title']}"
Target keyword: "{idea['keyword']}"
Article type: {idea['type']}

Return this JSON:
{{
  "title": "SEO optimized title (50-60 chars)",
  "description": "Meta description (150-160 chars, include keyword)",
  "intro": "2 paragraph intro that hooks the reader",
  "sections": [
    {{
      "heading": "section heading",
      "content": "200-300 word section content with specific helpful information"
    }}
  ],
  "verdict": "2 paragraph conclusion with clear recommendation",
  "faq": [
    {{"q": "frequently asked question", "a": "helpful answer"}}
  ]
}}

Rules:
- 5-7 sections minimum
- Include specific pricing, features, pros/cons
- Sound like a real human who tested the tools
- Include the target keyword naturally 3-4 times
- No fluff or padding
- FAQ should have 3 questions"""

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_KEY}",
                 "Content-Type": "application/json"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 3000,
            "response_format": {"type": "json_object"}
        },
        timeout=45
    )
    r.raise_for_status()
    return json.loads(r.json()["choices"][0]["message"]["content"])

def article_to_markdown(idea: dict, content: dict) -> str:
    """Convert generated content to Jekyll markdown post."""
    date = datetime.now().strftime("%Y-%m-%d")

    # Build sections
    sections_md = ""
    for s in content.get("sections", []):
        sections_md += f"\n## {s['heading']}\n\n{s['content']}\n"

    # Build FAQ
    faq_md = "\n## Frequently Asked Questions\n\n"
    for item in content.get("faq", []):
        faq_md += f"**{item['q']}**\n\n{item['a']}\n\n"

    # Add affiliate CTA based on topic
    cta = ""
    for tool, link in AFFILIATE_LINKS.items():
        if tool in idea["keyword"].lower() or tool in idea["title"].lower():
            cta = f"""
<div class="tool-card">
<a href="{link}" class="cta-btn" rel="nofollow sponsored">
Try {tool.title()} Free — Best Deal Available →
</a>
</div>"""
            break

    return f"""---
layout: default
title: "{content.get('title', idea['title'])}"
description: "{content.get('description', '')}"
tags: [{idea['keyword']}, ai tools, {idea['type']}]
permalink: /{idea['slug']}/
date: {date}
---

# {content.get('title', idea['title'])}

<p class="meta">Last updated: {datetime.now().strftime('%B %Y')} · Affiliate links present</p>

{content.get('intro', '')}

{sections_md}

## Our Verdict

{content.get('verdict', '')}

{cta}

{faq_md}

---
*This article contains affiliate links. We earn a commission if you purchase
through our links, at no extra cost to you. We only recommend tools we trust.*
"""

def main():
    print("AI Tools Hub — Daily Content Generator")
    print("=" * 40)

    # Track which articles already exist
    posts_dir = "_posts"
    os.makedirs(posts_dir, exist_ok=True)

    existing = set()
    for f in os.listdir(posts_dir):
        for idea in ARTICLE_IDEAS:
            if idea["slug"] in f:
                existing.add(idea["slug"])

    # Find articles not yet written
    remaining = [i for i in ARTICLE_IDEAS if i["slug"] not in existing]

    if not remaining:
        print("All articles already written! Resetting...")
        remaining = ARTICLE_IDEAS

    # Pick today's article
    today_seed = int(datetime.now().strftime("%Y%m%d")) % len(remaining)
    idea = remaining[today_seed % len(remaining)]

    print(f"Writing: {idea['title']}")
    print(f"Keyword: {idea['keyword']}")

    try:
        content  = generate_article(idea)
        markdown = article_to_markdown(idea, content)

        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"{posts_dir}/{date}-{idea['slug']}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"Article written: {filename}")
        print(f"Word count: ~{len(markdown.split())} words")

    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
