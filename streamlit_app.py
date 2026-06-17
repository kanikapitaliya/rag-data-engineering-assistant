import streamlit as st
import chromadb
import ollama

st.set_page_config(
    page_title="Data Engineering Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Custom CSS ----------

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.block-container{
padding-top:2rem;
padding-bottom:1rem;
max-width:1400px;
}

.stTextInput>div>div>input{
height:55px;
font-size:20px;
border-radius:12px;
}

.stButton>button{
height:55px;
width:100%;
border-radius:12px;
background:#6C63FF;
color:white;
font-size:18px;
font-weight:600;
border:none;
}

.stButton>button:hover{
background:#564FE3;
color:white;
}

.answer-card{
background:#F5FBF7;
padding:25px;
border-radius:12px;
border:1px solid #D8EFD8;
}

.info-card{
background:white;
padding:20px;
border-radius:12px;
border:1px solid #E8E8E8;
box-shadow:0px 2px 8px rgba(0,0,0,0.05);
height:100%;
}

.footer{
text-align:center;
color:gray;
margin-top:40px;
}

.title{
font-size:56px;
font-weight:700;
}

.subtitle{
font-size:22px;
color:#666;
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------

st.markdown(
"""
<div class="title">
📊 RAG-Powered Data Engineering Assistant
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="subtitle">
Ask questions about pipelines, SQL, runbooks, policies and metadata.
</div>
""",
unsafe_allow_html=True
)

# ---------- Search Area ----------

col1,col2=st.columns([9,1])

with col1:

    question=st.text_input(
        "",
        placeholder="Ask a Data Engineering Question..."
    )

with col2:

    submit=st.button(
        "🚀 Submit",
        use_container_width=True
    )

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="knowledge_base"
)


def get_document_type(question):

    question_lower = question.lower()

    if any(word in question_lower for word in
           ["fail", "failure", "error", "recover", "restart", "outage"]):
        return "runbooks"

    elif any(word in question_lower for word in
             ["query", "sql"]):
        return "sql"

    elif any(word in question_lower for word in
             ["policy", "pii", "security"]):
        return "policies"

    elif any(word in question_lower for word in
             ["table", "column", "schema"]):
        return "catalogs"

    elif "pipeline" in question_lower:
        return "pipelines"

    return None


with st.container():

    st.subheader("Ask a Question")

    question = st.text_input(
        "",
        placeholder="Example: What is the customer pipeline SLO?"
    )

if st.button(
    "🔍 Search Knowledge Base",
    use_container_width=True
):

    document_type = get_document_type(
        question
    )

    if document_type:

        results = collection.query(
            query_texts=[question],
            n_results=3,
            where={
                "document_type": document_type
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
    Use ONLY the provided context.

    Context:

    {context}

    Question:

    {question}
    """

    with st.spinner("Searching knowledge base..."):

        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    st.divider()

    st.markdown("---")

    st.subheader("💡 Answer")

    st.success(
        response["message"]["content"]
    )

    st.divider()

    st.subheader("Sources")

    unique_sources = set()

    for source in sources:
        unique_sources.add(source["source"])

    for source_name in unique_sources:
        st.write(f"- {source_name}")

    st.divider()

    with st.expander(
        "🔍 View Retrieved Context"
    ):
        st.code(
            context,
            language="text"
        )