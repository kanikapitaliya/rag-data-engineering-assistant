import streamlit as st
import chromadb
import anthropic
from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RAG Data Engineering Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* ---------------- Hide Streamlit ---------------- */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1450px;
}

/* ---------------- Fonts ---------------- */

html, body, [class*="css"]{
    font-family: "Segoe UI", sans-serif;
}

/* ---------------- Title ---------------- */

.main-title{
    font-size:42px;
    font-weight:700;
    color:#1f2937;
    margin-bottom:5px;
}

.sub-title{
    font-size:18px;
    color:#6b7280;
    margin-bottom:22px;
}

/* ---------------- Cards ---------------- */

.card{
    background:white;
    border-radius:18px;
    padding:22px;
    border:1px solid #E8ECF3;
    box-shadow:0 8px 25px rgba(0,0,0,.05);
    margin-bottom:20px;
}

/* ---------------- Answer Card ---------------- */

.answer-card{
    background:#F3FBF6;
    border:1px solid #D7F3DF;
    border-radius:16px;
    padding:28px;
    font-size:18px;
    line-height:1.8;
    color:#166534;
    margin-top:10px;
    margin-bottom:15px;
}

/* ---------------- Section Titles ---------------- */

.section-title{
    font-size:23px;
    font-weight:700;
    margin-bottom:15px;
}

/* ---------------- Footer ---------------- */

.footer{
    text-align:center;
    color:#8A8A8A;
    padding-top:30px;
    padding-bottom:20px;
    font-size:14px;
}

/* ---------------- Input ---------------- */

.stTextInput input{
    height:62px;
    border-radius:12px;
    border:1px solid #D1D5DB;
    font-size:17px;
}

/* ---------------- Button ---------------- */

.stButton>button{
    width:100%;
    height:55px;
    border-radius:12px;
    border:none;
    background:#6366F1;
    color:white;
    font-weight:600;
    font-size:16px;
    transition:0.25s;
}

.stButton>button:hover{
    background:#4F46E5;
    color:white;
}

/* ---------------- Code ---------------- */

pre{
    border-radius:12px !important;
}

/* ---------------- Source Badge ---------------- */

.source-pill{
display:inline-block;
padding:8px 16px;
margin:6px;
background:#EEF2FF;
color:#4338CA;
border-radius:30px;
font-size:14px;
font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# DATABASE
# ============================================================

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="knowledge_base"
)

# ============================================================
# CLAUDE CLIENT
# ============================================================

claude = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ============================================================
# DOCUMENT ROUTER
# ============================================================

def get_document_type(question):

    q = question.lower()

    if any(word in q for word in
           ["fail","failure","recover","restart",
            "error","issue","incident","outage"]):

        return "runbooks"

    elif any(word in q for word in
             ["sql","query"]):

        return "sql"

    elif any(word in q for word in
             ["policy","pii","security","access"]):

        return "policies"

    elif any(word in q for word in
             ["table","column","schema","catalog"]):

        return "catalogs"

    elif "pipeline" in q:

        return "pipelines"

    return None

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="main-title">
📊 RAG-Powered Data Engineering Assistant
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sub-title">
Ask questions about pipelines, SQL, runbooks, policies and enterprise metadata
</div>
""", unsafe_allow_html=True)

# ============================================================
# SEARCH AREA
# ============================================================

search_col, button_col = st.columns([8, 2])

with search_col:
    question = st.text_input(
        "",
        placeholder="Ask a question about pipelines, SQL, runbooks, policies...",
        label_visibility="collapsed"
    )

with button_col:

    search = st.button(
        "🚀 Submit",
        use_container_width=True
    )

    clear = st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    )

    if clear:
        st.session_state.history = []
        st.rerun()


# ============================================================
# SEARCH LOGIC STARTS HERE
# ============================================================

if search and question:
    document_type = get_document_type(question)

    if document_type:
        results = collection.query(
            query_texts=[question],
            n_results=3,
            where={
                "document_type":document_type
            }
        )
    else:
        results = collection.query(
            query_texts=[question],
            n_results=3
        )

    sources = results["metadatas"][0]

    context = "\n\n".join(
        results["documents"][0]
    )

    prompt = f"""
You are an Enterprise Data Engineering Assistant.

Use ONLY the supplied context.

If the answer is unavailable in the context,
clearly say you don't know.

Context:
{context}

Question:
{question}
"""
    import time
    start_time = time.time()

    with st.spinner("Thinking..."):
        response = claude.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=600,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    end_time = time.time()
    response_time = round(
        end_time - start_time,
        2
    )

# ============================================================
# ANSWER CARD
# ============================================================

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    💬 Answer
    </div>
    """, unsafe_allow_html=True)

    st.session_state.history.insert(
        0,
        {
            "question": question,
            "answer": response.content[0].text,
            "time": response_time
        }
    )

    st.success(
        response.content[0].text
    )

    st.caption(
        f"⚡ Generated in {response_time} seconds"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ============================================================
    # TWO COLUMN LAYOUT
    # ============================================================

    left, right = st.columns([1, 2])

    # ============================================================
    # LEFT COLUMN
    # ============================================================

    with left:
        st.markdown("""
        <div class="section-title">
        📄 Sources
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            unique_sources = sorted(
                {source["source"] for source in sources}
            )

            for source in unique_sources:
                st.markdown(f"""
                <div class="source-pill">
                📄 {source}
                </div>
                """, unsafe_allow_html=True)

    # ============================================================
    # RIGHT COLUMN
    # ============================================================

    with right:

        st.markdown("""
        <div class="section-title">
        🧠 Retrieved Context
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):

            with st.expander(
                "📄 View Retrieved Context",
                expanded=True
            ):
                st.code(
                    context,
                    language="text"
                )

    # ============================================================
    # METADATA
    # ============================================================

else:

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
        <h3 style="margin-top:0;">
        👋 Welcome
        </h3>
        Ask any question related to your enterprise knowledge base.
        <br><br>
        <b>Example Questions</b>
        <ul>
        <li>Who owns the customer pipeline?</li>
        <li>What is the customer pipeline SLO?</li>
        <li>Show me the revenue SQL query.</li>
        <li>Which fields are considered PII?</li>
        <li>How do I recover the customer pipeline after a database outage?</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

if st.session_state.history:
    st.markdown("---")
    st.subheader("💬 Previous Questions")
    for i, chat in enumerate(st.session_state.history, start=1):
        with st.expander(
            f"💬 {i}. {chat['question']}",
            expanded=False
        ):
            st.markdown(chat["answer"])

            st.caption(
                f"⏱️ Response Time: {chat['time']} sec"
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <hr style="margin-top:30px;margin-bottom:20px;">
    """,
    unsafe_allow_html=True
)

st.caption(
    "Built with Streamlit • ChromaDB • Claude"
)

st.caption(
    "Developed by Kanika Pitaliya"
)

# ============================================================
# END OF FILE
# ============================================================