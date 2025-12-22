import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(page_title="Amazon KDP Metadata Generator")
st.header("Amazon KDP Book Metadata Generator")
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<p style='font-size:18px; font-weight:700; margin-bottom: 5px;'>Enter Your Gemini API Key</p>", unsafe_allow_html=True)
gemini_key = st.text_input("", type="password", label_visibility="collapsed", key="gemini_api_key")

# Input Columns
col1, col2 = st.columns(2)
with col1:
    st.markdown("<p style='font-size:18px; font-weight:700; margin-bottom: 5px;'>Category</p>", unsafe_allow_html=True)
    category = st.text_input("", label_visibility="collapsed", key="category_input")
    
    st.markdown("<p style='font-size:18px; font-weight:700; margin-bottom: 5px;'>Book Size</p>", unsafe_allow_html=True)
    book_size = st.selectbox("", ('6*9 Inch', '8.5*11 Inch'), label_visibility="collapsed", key="book_size_input")

with col2:
    st.markdown("<p style='font-size:18px; font-weight:700; margin-bottom: 5px;'>Total Pages</p>", unsafe_allow_html=True)
    total_pages = st.text_input("", label_visibility="collapsed", key="total_pages_input")
    
    st.markdown("<p style='font-size:18px; font-weight:700; margin-bottom: 5px;'>Keywords</p>", unsafe_allow_html=True)
    keywords = st.text_input("", label_visibility="collapsed", key="keywords_input")

st.markdown("<p style='font-size:18px; font-weight:700; margin-bottom: 5px;'>Old Description:</p>", unsafe_allow_html=True)
old_description_input = st.text_area("", placeholder="Paste your current description here...", height=150, label_visibility="collapsed")

# Template
template = """
You are an expert book publisher and copywriter for Amazon KDP.
Your task is to generate a high-converting **Book Title** and **Book Description** based on the following details.

Details provided:
- Category: {category}
- Book Size: {book_size}
- Total Pages: {total_pages}
- Keywords: {keywords}
- Old Description: {old_description}

Please follow these guidelines:
1. **New Book Title**: Create a catchy, SEO-friendly title that includes main keywords if possible.
2. **New Book Description**: Rewrite the description to be persuasive, professional, and formatted for Amazon. Do NOT use HTML tags. Do NOT use bullet points. Write in clear, engaging paragraphs. Highlight benefits and key selling points.

Output Format:
### New Book Title
[Title Here]

### New Book Description
[Description Here]
"""

prompt = PromptTemplate(
    input_variables=["category", "book_size", "total_pages", "keywords", "old_description"],
    template=template,
)

def load_LLM(api_key: str):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=1
    )

generate = st.button("Generate Title & Description")

if generate:
    if not gemini_key:
        st.warning("Please insert Gemini API Key.", icon="⚠️")
        st.stop()
    
    if not old_description_input:
        st.warning("Please provide the old description.")
        st.stop()

    llm = load_LLM(gemini_key)

    prompt_with_data = prompt.format(
        category=category,
        book_size=book_size,
        total_pages=total_pages,
        keywords=keywords,
        old_description=old_description_input
    )

    with st.spinner("Generating content..."):
        try:
            result = llm.invoke(prompt_with_data)
            st.markdown(result.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")
