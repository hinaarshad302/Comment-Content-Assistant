import streamlit as st
from google import genai

st.set_page_config(
    page_title="Comment & Emoji-to-Content Assistant",
    page_icon="✨",
    layout="centered"
)

st.title("✨ Comment & Emoji-to-Content Assistant")
st.write("Turn a topic, comment, or emojis into a ready-to-post social media caption.")

# ---------- Gemini client ----------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    st.error("Gemini API key is missing. Add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("About")
    st.write(
        "Choose your content settings, enter a topic/comment/emojis, "
        "and Gemini will create a complete social-media post."
    )
    st.info("Your API key should be stored in Streamlit Secrets, not in this file.")

# ---------- Inputs ----------
mode = st.selectbox(
    "Input mode",
    ["Topic → Content", "Comment → Content", "Emoji → Content"]
)

content_type = st.selectbox(
    "Content type",
    [
        "Social Media Post",
        "Promotional Post",
        "Educational Post",
        "Question Post",
        "Storytelling Post",
        "Announcement",
        "Motivational Post",
    ],
)

platform = st.selectbox(
    "Platform",
    ["Facebook", "Instagram", "LinkedIn", "X/Twitter"]
)

audience = st.selectbox(
    "Target audience",
    [
        "Students",
        "Professionals",
        "Business Owners",
        "Entrepreneurs",
        "General Audience",
    ],
)

tone = st.selectbox(
    "Tone",
    [
        "Professional",
        "Friendly",
        "Funny",
        "Motivational",
        "Educational",
        "Emotional",
        "Persuasive",
        "Casual",
    ],
)

language = st.selectbox(
    "Language",
    ["English", "Urdu", "Roman Urdu"]
)

if mode == "Topic → Content":
    label = "Topic / Idea"
    placeholder = "Example: AI tools for students"
elif mode == "Comment → Content":
    label = "Comment"
    placeholder = "Example: AI is changing education."
else:
    label = "Emojis"
    placeholder = "Example: 🚀 🤖 💡"

input_text = st.text_area(label, placeholder=placeholder, height=120)

cta = st.text_input(
    "Optional call-to-action",
    placeholder="Example: What do you think?"
)

# ---------- Generate ----------
if st.button("✨ Generate Content", use_container_width=True):
    if not input_text.strip():
        st.warning(f"Please enter a {label.lower()} first.")
        st.stop()

    prompt = f"""
You are an expert social media content writer.

Create ONE complete social-media post using these settings:

Input mode: {mode}
User input: {input_text}
Content type: {content_type}
Platform: {platform}
Target audience: {audience}
Tone: {tone}
Language: {language}
Preferred CTA: {cta if cta.strip() else "Create a suitable CTA"}

Platform rules:
- Facebook: conversational and engagement-focused.
- Instagram: attractive, concise, visual, and hashtag-friendly.
- LinkedIn: professional, useful, and insight-focused.
- X/Twitter: concise, punchy, and easy to read.

Return ONLY this structure:

HOOK:
[attention-grabbing opening]

CAPTION:
[complete post caption]

CTA:
[short call to action]

HASHTAGS:
[5-10 relevant hashtags]

Use natural emojis where appropriate.
Do not explain your answer.
"""

    with st.spinner("Creating your content..."):
        try:
           response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)
            result = response.text.strip()

            st.success("Content generated successfully!")
            st.markdown("### 📝 Your Post")
            st.markdown(result)

            st.download_button(
                "⬇️ Download Post",
                data=result,
                file_name="generated_social_post.txt",
                mime="text/plain",
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Could not generate content. Please check your API key and try again.")
            st.caption(f"Error: {e}")
