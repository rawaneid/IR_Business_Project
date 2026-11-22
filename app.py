
import streamlit as st
import sys
import io
import zipfile
import tempfile
import hashlib
from pathlib import Path, PurePosixPath

import pandas as pd


# =========================================================
# 1. PROJECT CONFIGURATION
# =========================================================

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

sys.path.insert(0, str(SRC))

import gui_backend


st.set_page_config(
    page_title="IR Business Project",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. CUSTOM STYLE
# =========================================================

st.markdown("""
<style>
    :root {
        --navy: #172554;
        --navy-deep: #0F1B3D;
        --blue: #2563EB;
        --cyan: #06B6D4;
        --cyan-soft: #CFFAFE;
        --page: #F5F8FF;
        --surface: #FFFFFF;
        --text: #1E293B;
        --muted: #64748B;
        --border: #DCE6F5;
    }

    .stApp {
        background: var(--page);
        color: var(--text);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--navy-deep) 0%, var(--navy) 58%, #123B70 100%);
        border-right: 1px solid #243D70;
    }

    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 0.55rem 0.7rem;
        border-radius: 10px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(6, 182, 212, 0.14);
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(203, 213, 225, 0.25);
    }

    /* Streamlit top header */
    [data-testid="stHeader"] {
        background-color: #172554 !important;
    }

    /* Toolbar */
    [data-testid="stToolbar"] {
        background-color: transparent !important;
    }

    /* Top decoration */
    [data-testid="stDecoration"] {
        background-color: #172554 !important;
    }

    /* Main headings and text */
    h1, h2, h3, h4 {
        color: var(--navy);
        letter-spacing: -0.02em;
    }

    .main-subtitle {
        color: var(--muted);
        font-size: 1rem;
        margin-top: -12px;
        margin-bottom: 25px;
    }

    .upload-title {
        font-size: 1.1rem;
        font-weight: 650;
        margin-bottom: 5px;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 650;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F7FF 100%);
        border: 1px solid var(--border);
        padding: 17px 18px;
        border-radius: 15px;
        box-shadow: 0 3px 12px rgba(23, 37, 84, 0.045);
    }

    div[data-testid="stMetric"] label {
        color: #475569;
        font-weight: 600;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--navy);
        font-weight: 750;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 650;
        border: 1px solid #C7D7F0;
        transition: all 0.18s ease;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, var(--blue), #087EA4);
        color: white;
        border: 0;
    }

    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #1D4ED8, #0891B2);
        border: 0;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }

    /* Tabs */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 5px;
        border-bottom: 1px solid var(--border);
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        background: #EAF1FC;
        border: 1px solid #D7E3F5;
        border-bottom: 0;
        border-radius: 10px 10px 0 0;
        color: #334A70;
        font-weight: 600;
        padding: 0.65rem 0.9rem;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
        background: var(--navy);
        color: #FFFFFF;
        border-color: var(--navy);
    }

    div[data-testid="stTabs"] [data-testid="stTabContent"] {
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid var(--border);
        border-top: 3px solid var(--cyan);
        border-radius: 0 0 14px 14px;
        padding: 1.2rem;
    }

    /* Tables */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
        background: #FFFFFF;
    }

    /* Inputs and upload area */
    div[data-testid="stTextInput"] input,
    div[data-testid="stFileUploader"] section {
        border-radius: 10px;
        border-color: #C9D8EF;
    }

    div[data-testid="stSegmentedControl"] {
        margin-top: 5px;
        margin-bottom: 12px;
    }

    div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {
        background: #DBF7FC;
        color: var(--navy);
        border-color: #67D7E8;
    }

    /* Containers, dividers, alerts */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--border);
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.72);
    }

    hr {
        border-color: var(--border);
    }

    div[data-testid="stAlert"] {
        border-radius: 11px;
    }

    a {
        color: var(--blue);
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. SESSION STATE
# =========================================================

defaults = {
    "dataset_data": None,
    "index_ready": False,
    "dataset_name": "dataset",
    "active_source": "Default dataset",
    "pending_dataset_path": None,
    "pending_dataset_name": None,
    "upload_signature": None,
    "search_result": None,
    "search_query": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# Load default dataset on first launch
if st.session_state.dataset_data is None:

    st.session_state.dataset_data = (
        gui_backend.load_default_dataset()
    )

    st.session_state.index_ready = True
    st.session_state.dataset_name = "dataset"


# =========================================================
# 4. HELPER FUNCTIONS
# =========================================================

def clear_search():

    st.session_state.search_result = None

    if "search_query" in st.session_state:
        st.session_state.search_query = ""


def get_documents(data):

    return sorted(
        data["doc_lengths"].keys(),
        key=lambda doc: (
            0,
            int(doc[1:])
        ) if doc.startswith("d") and doc[1:].isdigit()
        else (1, doc.lower())
    )


def get_total_tokens(index):

    return sum(
        len(positions)
        for postings in index.values()
        for positions in postings.values()
    )


def matrix_to_dataframe(matrix, documents):

    if not matrix:
        return pd.DataFrame()

    df = pd.DataFrame.from_dict(
        matrix,
        orient="index"
    )

    df = df.reindex(
        columns=documents,
        fill_value=0
    )

    df = df.fillna(0)
    df.index.name = "Term"

    return df


def show_matrix(title, matrix, documents):

    st.markdown(f"#### {title}")

    df = matrix_to_dataframe(
        matrix,
        documents
    )

    if df.empty:

        st.info("No data available.")

    else:

        st.dataframe(
            df,
            use_container_width=True,
            height=380
        )


def save_uploaded_dataset(uploaded_files):

    signature_hash = hashlib.sha256()

    for uploaded_file in uploaded_files:

        signature_hash.update(
            uploaded_file.name.encode()
        )

        signature_hash.update(
            uploaded_file.getvalue()
        )

    signature = signature_hash.hexdigest()

    if signature == st.session_state.upload_signature:

        return st.session_state.pending_dataset_path

    temp_dir = Path(
        tempfile.mkdtemp(prefix="ir_uploaded_")
    )

    saved_count = 0

    for uploaded_file in uploaded_files:

        filename = uploaded_file.name.lower()

        if filename.endswith(".txt"):

            file_name = Path(uploaded_file.name).name

            target = temp_dir / file_name

            if target.exists():
                target = temp_dir / f"{saved_count}_{file_name}"

            target.write_bytes(
                uploaded_file.getvalue()
            )

            saved_count += 1

        elif filename.endswith(".zip"):

            with zipfile.ZipFile(
                io.BytesIO(uploaded_file.getvalue())
            ) as archive:

                for item in archive.infolist():

                    if item.is_dir():
                        continue

                    archive_path = PurePosixPath(
                        item.filename
                    )

                    if (
                        archive_path.is_absolute()
                        or ".." in archive_path.parts
                        or not item.filename.lower().endswith(".txt")
                    ):
                        continue

                    file_name = archive_path.name

                    if not file_name:
                        continue

                    target = temp_dir / file_name

                    if target.exists():
                        target = temp_dir / (
                            f"{saved_count}_{file_name}"
                        )

                    target.write_bytes(
                        archive.read(item)
                    )

                    saved_count += 1

    st.session_state.upload_signature = signature

    if saved_count == 0:

        st.session_state.pending_dataset_path = None
        st.session_state.pending_dataset_name = None

        return None

    st.session_state.pending_dataset_path = str(temp_dir)
    st.session_state.pending_dataset_name = "Uploaded Dataset"

    return str(temp_dir)


def display_search_results(result):

    similarity = result["similarity"]

    ranking = similarity["ranking"]

    st.markdown("### 📄 Search Results")

    if not ranking:

        st.info("No matching documents were found.")
        return

    phrase_matches = {}

    for match in result["matches"]:

        doc = match["document"]

        phrase_matches.setdefault(doc, []).append(
            match
        )

    rows = []

    for rank, (doc, score) in enumerate(ranking, start=1):

        row = {
            "Rank": rank,
            "Document": doc,
            "Similarity Score": round(score, 6)
        }

        if result["query_type"] == "Phrase Query":

            matches = phrase_matches.get(doc, [])

            positions = [
                str(match["starting_position"])
                for match in matches
            ]

            row["Starting Positions"] = ", ".join(positions)

        rows.append(row)

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"{len(ranking)} matching document(s), "
        "sorted by Similarity Score."
    )

    with st.expander("View Query Vector Details"):

        st.write(
            f"**Query Vector Length:** "
            f"{similarity['query_length']:.6f}"
        )

        st.dataframe(
            pd.DataFrame(similarity["query_terms"]),
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 5. SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🔎 IR Business Project")

st.sidebar.caption(
    "Information Retrieval System"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "IR Workspace",
        "Dashboard",
        "About"
    ]
)


# =========================================================
# 6. IR WORKSPACE
# =========================================================

if page == "IR Workspace":

    st.title("🔎 IR Workspace")

    st.markdown(
        '<p class="main-subtitle">'
        'Manage datasets and search documents.'
        '</p>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # DATASET MANAGEMENT
    # -----------------------------------------------------

    st.markdown("## 📁 Dataset Management")

    source = st.segmented_control(
        "Dataset Source",
        [
            "Default dataset",
            "Upload new dataset"
        ],
        default="Default dataset",
        key="dataset_source",
        width="content"
    )

    if source != st.session_state.active_source:

        st.session_state.active_source = source

        clear_search()

        if source == "Default dataset":

            st.session_state.dataset_data = (
                gui_backend.load_default_dataset()
            )

            st.session_state.dataset_name = "dataset"
            st.session_state.index_ready = True

            st.session_state.pending_dataset_path = None
            st.session_state.pending_dataset_name = None
            st.session_state.upload_signature = None

        else:

            st.session_state.index_ready = False

            st.session_state.pending_dataset_path = None
            st.session_state.pending_dataset_name = None
            st.session_state.upload_signature = None

    if source == "Default dataset":

        with st.container(border=True):

            st.markdown(
                "#### 📂 Original Project Dataset"
            )

            st.caption(
                "Use the dataset already included in the project."
            )

            st.success(
                "Default dataset is loaded and ready."
            )

    else:

        with st.container(border=True):

            st.markdown(
                "#### 📤 Upload Your Dataset"
            )

            st.caption(
                "Upload TXT documents or a ZIP archive containing TXT files."
            )

            uploaded_files = st.file_uploader(
                "Choose your files",
                type=["txt", "zip"],
                accept_multiple_files=True,
                key="uploaded_files"
            )

            if uploaded_files:

                try:

                    uploaded_path = save_uploaded_dataset(
                        uploaded_files
                    )

                    if uploaded_path:

                        file_count = len(
                            list(
                                Path(uploaded_path).glob("*.txt")
                            )
                        )

                        st.success(
                            f"{file_count} TXT document(s) ready to index."
                        )

                    else:

                        st.error(
                            "No TXT documents were found. "
                            "Please upload TXT files or a ZIP containing TXT files."
                        )

                except (zipfile.BadZipFile, OSError, ValueError) as error:

                    st.error(
                        f"Could not read uploaded files: {error}"
                    )

        if st.session_state.pending_dataset_path:

            if st.button(
                "⚙️ Build Index",
                type="primary",
                use_container_width=True
            ):

                dataset_path = Path(
                    st.session_state.pending_dataset_path
                )

                output_name = (
                    "uploaded_"
                    + st.session_state.upload_signature[:12]
                )

                output_dir = (
                    ROOT / "outputs" / "generated" / output_name
                )

                try:

                    with st.spinner(
                        "Building Positional Index and calculating statistics..."
                    ):

                        new_data = gui_backend.build_dataset(
                            dataset_path,
                            output_dir
                        )

                    st.session_state.dataset_data = new_data

                    st.session_state.dataset_name = "Uploaded Dataset"

                    st.session_state.index_ready = True

                    clear_search()

                    st.success(
                        "Index built successfully!"
                    )

                    st.rerun()

                except Exception as error:

                    st.session_state.index_ready = False

                    st.error(
                        f"Could not build the index: {error}"
                    )

    st.divider()

    
    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    st.markdown("## 🔍 Search")

    if st.session_state.index_ready:

        query_col, clear_col = st.columns(
            [12, 0.7],
            vertical_alignment="bottom"
        )

        with query_col:

            query = st.text_input(
                "Enter your query",
                placeholder="Type your search query here...",
                key="search_query"
            )

        with clear_col:

            st.button(
                "✕",
                help="Clear search and results",
                on_click=clear_search,
                use_container_width=True
            )

        query_type = st.segmented_control(
            "Query Type",
            [
                "Phrase Query",
                "Boolean Query"
            ],
            default="Phrase Query",
            key="query_type",
            width="content"
        )

        search_clicked = st.button(
            "🔍 Search",
            type="primary",
            use_container_width=True
        )

        if search_clicked:

            if not query.strip():

                st.warning("Please enter a search query.")

                st.session_state.search_result = None

            else:

                try:

                    result = gui_backend.search_dataset(
                        st.session_state.dataset_data,
                        query.strip(),
                        query_type
                    )

                    st.session_state.search_result = result

                except (ValueError, KeyError, IndexError) as error:

                    st.session_state.search_result = None
                    st.error(f"Invalid query: {error}")

                except Exception as error:

                    st.session_state.search_result = None
                    st.error(f"Search failed: {error}")

        if st.session_state.search_result:

            display_search_results(
                st.session_state.search_result
            )

    else:

        st.info(
            "Please upload a dataset and build its index before searching."
        )



# =========================================================
# 7. DASHBOARD
# =========================================================

elif page == "Dashboard":

    st.title("📊 Dashboard")

    st.markdown(
        '<p class="main-subtitle">'
        'Dataset statistics and information retrieval results.'
        '</p>',
        unsafe_allow_html=True
    )

    if not st.session_state.index_ready:

        st.warning(
            "Build the selected dataset index first."
        )

    else:

        data = st.session_state.dataset_data

        documents = get_documents(data)

        total_documents = len(documents)
        unique_terms = len(data["positional_index"])
        total_tokens = get_total_tokens(
            data["positional_index"]
        )

        # DATASET OVERVIEW

        st.markdown("## Dataset Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Documents",
            total_documents
        )

        col2.metric(
            "Unique Terms",
            unique_terms
        )

        col3.metric(
            "Total Tokens",
            total_tokens
        )

        st.caption(
            f"Selected dataset: {st.session_state.dataset_name}"
        )

        st.divider()

        # TABLES

        st.markdown("## Indexing and Retrieval Details")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Positional Index",
            "TF",
            "Weighted TF",
            "DF & IDF",
            "TF-IDF",
            "Vector Lengths",
            "Normalized TF-IDF"
        ])

        with tab1:

            st.markdown("### 1. Positional Index")

            positional_rows = []

            for term, postings in data["positional_index"].items():

                for doc, positions in postings.items():

                    positional_rows.append({
                        "Term": term,
                        "Document": doc,
                        "Positions": ", ".join(
                            map(str, positions)
                        )
                    })

            st.dataframe(
                pd.DataFrame(positional_rows),
                use_container_width=True,
                hide_index=True,
                height=420
            )

        with tab2:

            st.markdown("### 2. Term Frequency (TF)")

            show_matrix(
                "Raw Term Frequency",
                data["tf"],
                documents
            )

        with tab3:

            st.markdown("### 3. Weighted Term Frequency")

            show_matrix(
                "Weighted TF",
                data["weighted_tf"],
                documents
            )

        with tab4:

            st.markdown("### 4. Document Frequency and IDF")

            df_idf_table = pd.DataFrame([
                {
                    "Term": term,
                    "DF": data["df"][term],
                    "IDF": data["idf"][term]
                }
                for term in data["df"]
            ])

            st.dataframe(
                df_idf_table,
                use_container_width=True,
                hide_index=True,
                height=420
            )

        with tab5:

            st.markdown("### 5. TF-IDF")

            show_matrix(
                "TF-IDF Matrix",
                data["tfidf"],
                documents
            )

        with tab6:

            st.markdown("### 6. Document Vector Lengths")

            lengths_table = pd.DataFrame([
                {
                    "Document": doc,
                    "Vector Length": data["doc_lengths"][doc]
                }
                for doc in documents
            ])

            st.dataframe(
                lengths_table,
                use_container_width=True,
                hide_index=True
            )

        with tab7:

            st.markdown("### 7. Normalized TF-IDF")

            show_matrix(
                "Normalized TF-IDF Matrix",
                data["normalized_tfidf"],
                documents
            )


# =========================================================
# 8. ABOUT
# =========================================================

elif page == "About":

    st.title("ℹ️ About the Project")

    st.markdown(
        '<p class="main-subtitle">'
        'Information Retrieval Business Project'
        '</p>',
        unsafe_allow_html=True
    )

    st.markdown("## Project Overview")

    st.write(
        """
        This project implements an Information Retrieval system
        that processes a collection of text documents, builds a
        Positional Index, supports Phrase and Boolean Queries,
        and ranks matching documents using Cosine Similarity.
        """
    )

    st.divider()

    st.markdown("## 🎯 Project Objectives")

    st.markdown("""
    - Build a Positional Index for a collection of documents.
    - Support Phrase Query processing.
    - Support Boolean Query processing.
    - Calculate TF, Weighted TF, DF, and IDF.
    - Calculate TF-IDF and Normalized TF-IDF.
    - Rank retrieved documents using Cosine Similarity.
    - Explore indexing and ranking results through an interactive interface.
    """)

    st.divider()

    st.markdown("## ⚙️ Algorithms and Techniques")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**Indexing and Retrieval**")

        st.markdown("""
        - Positional Index
        - Phrase Query
        - Boolean Query
        """)

    with col2:

        st.markdown("**Weighting and Ranking**")

        st.markdown("""
        - Term Frequency (TF)
        - Weighted TF
        - Inverse Document Frequency (IDF)
        - TF-IDF
        - Cosine Similarity
        """)

    st.divider()

    st.markdown("## 💻 Technologies")

    st.markdown("""
    - Python
    - Apache Spark (PySpark)
    - Streamlit
    - Pandas
    - JSON
    """)

    st.divider()

    st.markdown("## 👥 Team Members")

    team_members = [
        "Rawan Saad",
        "Habiba Kamal",
        "Olivia Nagy",
        "Zezef Ashraf",
        "Sara Hessin",
        "Febronia Fathy"
    ]

    for number, member in enumerate(team_members, start=1):

        st.markdown(
            f"**{number}.** {member}"
        )

    st.divider()

    st.caption(
        "Information Retrieval Business Project"
    )
