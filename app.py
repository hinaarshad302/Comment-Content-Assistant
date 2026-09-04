import streamlit as st
from google import genai

# Page settings
st.set_page_config(
    page_title="Comment & Emoji-to-Content Assistant",
    page_icon="✨",
    layout="centered"
)

# Title
st.title("✨ Comment & Emoji-to-Content Assistant")
st.write(
    "Turn a topic, comment, or emojis into a ready-to-post social media post."
)

# Gemini API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = ""

if not api_key:
    st.error(
        "Gemini API key is missing. Add GEMINI_API_KEY to Streamlit Secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# Sidebar
with st.sidebar:
    st.header("About")
    st.write(
        "Choose your content settings, enter your idea, "
        "and Gemini will create a complete social media post."
    )

# Input mode
mode = st.selectbox(
    "Input mode",
    [
        "Topic → Content",
        "Comment → Content",
        "Emoji → Content"
    ]
)

# Content type
content_type = st.selectbox(
    "Content type",
    [
        "Social Media Post",
        "Promotional Post",
        "Educational Post",
        "Question Post",
        "Storytelling Post",
        "Announcement",
        "Motivational Post"
    ]
)

# Platform
platform = st.selectbox(
    "Platform",
    [
        "Facebook",
        "Instagram",
        "LinkedIn",
        "X/Twitter"
    ]
)

# Target audience
target_audience = st.selectbox(
    "Target audience",
    [
        "Students",
        "Professionals",
        "Business Owners",
        "Entrepreneurs",
        "General Audience"
    ]
)

# Tone
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
        "Casual"
    ]
)

# Language
language = st.selectbox(
    "Language",
    [
        "English",
        "Urdu",
        "Roman Urdu"
    ]
)

# Dynamic input
if mode == "Topic → Content":
    input_label = "Topic / Idea"
    placeholder = "Example: AI tools for students"

elif mode == "Comment → Content":
    input_label = "Comment"
    placeholder = "Example: AI is changing education."

else:
    input_label = "Emojis"
    placeholder = "Example: 🚀 🤖 💡"

user_input = st.text_area(
    input_label,
    placeholder=placeholder,
    height=120
)

# Optional CTA
cta = st.text_input(
    "Optional Call-to-Action",
    placeholder="Example: What do you think?"
)

# Generate button
if st.button("✨ Generate Content", use_container_width=True):

    if not user_input.strip():
        st.warning(
            f"Please enter a {input_label.lower()} first."
        )
        st.stop()

    prompt = f"""
You are an expert social media content writer.

Create ONE complete social media post using these settings:

Input mode: {mode}
User input: {user_input}
Content type: {content_type}
Platform: {platform}
Target audience: {target_audience}
Tone: {tone}
Language: {language}
CTA: {cta if cta.strip() else "Create a suitable call-to-action"}

Platform guidelines:

Facebook:
Make it conversational and engagement-focused.

Instagram:
Make it attractive, concise, visual, and hashtag-friendly.

LinkedIn:
Make it professional, useful, and insight-focused.

X/Twitter:
Make it concise, punchy, and easy to read.

Return ONLY this structure:

HOOK:
Write an attention-grabbing opening.

CAPTION:
Write the complete social media caption.

CTA:
Write a short call-to-action.

HASHTAGS:
Write 5 to 10 relevant hashtags.

Use natural emojis where appropriate.
Do not add explanations outside this structure.
"""

    with st.spinner("Creating your content..."):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            result = response.text.strip()

            st.success("Content generated successfully!")

            st.subheader("📝 Your Generated Post")

            st.markdown(result)

            st.download_button(
                label="⬇️ Download Post",
                data=result,
                file_name="generated_social_post.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:

            st.error("Could not generate content.")

            st.caption(f"Error: {e}")
