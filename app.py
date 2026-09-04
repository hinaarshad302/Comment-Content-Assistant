import time
import streamlit as st
from google import genai


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Comment & Emoji-to-Content Assistant",
    page_icon="✨",
    layout="centered"
)


# =========================================================
# TITLE
# =========================================================

st.title("✨ Comment & Emoji-to-Content Assistant")

st.write(
    "Turn a topic, comment, or emojis into a ready-to-post "
    "social media post."
)


# =========================================================
# GEMINI API KEY
# =========================================================

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = ""


if not api_key:
    st.error(
        "Gemini API key is missing. "
        "Please add GEMINI_API_KEY to Streamlit Secrets."
    )
    st.stop()


client = genai.Client(api_key=api_key)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("ℹ️ About")

    st.write(
        "This AI assistant converts topics, comments, "
        "or emojis into social media content."
    )

    st.write("**Features:**")

    st.write("• Topic → Content")
    st.write("• Comment → Content")
    st.write("• Emoji → Content")
    st.write("• Multiple platforms")
    st.write("• Multiple languages")
    st.write("• AI-generated hashtags")


# =========================================================
# INPUT MODE
# =========================================================

mode = st.selectbox(
    "Input mode",
    [
        "Topic → Content",
        "Comment → Content",
        "Emoji → Content"
    ]
)


# =========================================================
# CONTENT TYPE
# =========================================================

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


# =========================================================
# PLATFORM
# =========================================================

platform = st.selectbox(
    "Platform",
    [
        "Facebook",
        "Instagram",
        "LinkedIn",
        "X/Twitter"
    ]
)


# =========================================================
# TARGET AUDIENCE
# =========================================================

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


# =========================================================
# TONE
# =========================================================

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


# =========================================================
# LANGUAGE
# =========================================================

language = st.selectbox(
    "Language",
    [
        "English",
        "Urdu",
        "Roman Urdu"
    ]
)


# =========================================================
# DYNAMIC USER INPUT
# =========================================================

if mode == "Topic → Content":

    input_label = "Topic / Idea"

    placeholder = (
        "Example: AI tools for students"
    )

elif mode == "Comment → Content":

    input_label = "Comment"

    placeholder = (
        "Example: AI is changing education."
    )

else:

    input_label = "Emojis"

    placeholder = (
        "Example: 🚀 🤖 💡"
    )


user_input = st.text_area(
    input_label,
    placeholder=placeholder,
    height=120
)


# =========================================================
# OPTIONAL CTA
# =========================================================

cta = st.text_input(
    "Optional Call-to-Action",
    placeholder="Example: What do you think?"
)


# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button(
    "✨ Generate Content",
    use_container_width=True
):

    # -----------------------------------------------------
    # CHECK USER INPUT
    # -----------------------------------------------------

    if not user_input.strip():

        st.warning(
            f"Please enter a {input_label.lower()} first."
        )

        st.stop()


    # -----------------------------------------------------
    # PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are an expert social media content writer.

Create ONE complete and engaging social media post.

USER SETTINGS:

Input mode:
{mode}

User input:
{user_input}

Content type:
{content_type}

Platform:
{platform}

Target audience:
{target_audience}

Tone:
{tone}

Language:
{language}

Call-to-action:
{cta if cta.strip() else "Create a suitable call-to-action."}


PLATFORM GUIDELINES:

Facebook:
Make the post conversational, engaging,
and suitable for Facebook users.

Instagram:
Make the post attractive, concise,
visual, engaging, and hashtag-friendly.

LinkedIn:
Make the post professional,
useful, informative, and insight-focused.

X/Twitter:
Make the post concise, punchy,
clear, and easy to read.


LANGUAGE RULE:

Write the complete content in the selected language.

If the selected language is Urdu,
write natural Urdu using Urdu script.

If the selected language is Roman Urdu,
write Urdu using Roman/English letters.

If the selected language is English,
write natural English.


OUTPUT FORMAT:

HOOK:
Write a strong attention-grabbing opening.

CAPTION:
Write the complete social media caption.

CTA:
Write a short and engaging call-to-action.

HASHTAGS:
Write 5 to 10 relevant hashtags.

Use natural emojis where appropriate.

Do not add explanations outside this structure.
"""


    # =====================================================
    # GEMINI GENERATION WITH RETRY
    # =====================================================

    with st.spinner("✨ Creating your content..."):

        result = None
        last_error = None

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt
                )

                if response and response.text:

                    result = response.text.strip()

                    break

                else:

                    last_error = "Gemini returned an empty response."

            except Exception as e:

                last_error = str(e)

                error_text = str(e).upper()

                # Retry temporary errors
                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                ):

                    if attempt < 2:

                        time.sleep(3)

                        continue

                break


    # =====================================================
    # SHOW RESULT
    # =====================================================

    if result:

        st.success(
            "✅ Content generated successfully!"
        )

        st.subheader(
            "📝 Your Generated Post"
        )

        st.markdown(result)


        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------

        st.download_button(
            label="⬇️ Download Post",
            data=result,
            file_name="generated_social_post.txt",
            mime="text/plain",
            use_container_width=True
        )


    # =====================================================
    # ERROR
    # =====================================================

    else:

        st.error(
            "❌ Could not generate content."
        )

        if last_error:

            st.caption(
                f"Error: {last_error}"
            )

        st.info(
            "Please wait a few seconds and try again. "
            "Temporary Gemini service limits can sometimes occur."
        )
