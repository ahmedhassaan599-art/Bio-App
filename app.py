import streamlit as st
from Bio.Seq import Seq
from Bio import Align, Entrez, SeqIO

# Page Configuration
st.set_page_config(
    page_title="BioInnovate Toolkit",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for a "Fancy" Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #4f46e5;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        color: white;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Always tell NCBI who you are
Entrez.email = "your.email@example.com"

# App Header
st.title("🧬 BioInnovate Toolkit")
st.markdown("##### *Next-Gen Computational Biology & Genomic Analysis Platform*")
st.markdown("---")

# Sidebar Navigation with Clean Styling
st.sidebar.markdown("### 🧭 Navigation")
option = st.sidebar.radio("Select Tool:", ["🧪 Sequence Analyzer", "🔗 Sequence Alignment", "🔍 Live NCBI Search"])

if option == "🧪 Sequence Analyzer":
    st.header("DNA Property & Protein Translator")
    st.write("Analyze nucleotide sequences, compute GC metrics, and translate codons instantly.")
    
    dna_input = st.text_area("Enter DNA Sequence:", "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", height=100)
    
    if st.button("Run Bio-Analysis"):
        if dna_input:
            clean_seq = Seq(dna_input.strip().upper())
            
            # Metrics Display
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Sequence Length", value=f"{len(clean_seq)} bp")
            with col2:
                gc_count = clean_seq.count("G") + clean_seq.count("C")
                gc_pct = (gc_count / len(clean_seq)) * 100
                st.metric(label="GC Content", value=f"{gc_pct:.1f}%")
            
            st.markdown("---")
            
            # Transcription & Translation tabs
            tab1, tab2 = st.tabs(["mRNA Transcription", "Protein Translation"])
            with tab1:
                st.code(str(clean_seq.transcribe()), language="text")
            with tab2:
                st.code(str(clean_seq.translate()), language="text")
        else:
            st.warning("Please enter a valid sequence.")

elif option == "🔗 Sequence Alignment":
    st.header("Pairwise Sequence Aligner")
    st.write("Compare reference and mutated gene sequences side-by-side.")
    
    col1, col2 = st.columns(2)
    with col1:
        seq1 = st.text_input("Reference Sequence", "ATGCCGTAGA")
    with col2:
        seq2 = st.text_input("Mutated Sequence", "ATGCGTAGA")
    
    if st.button("Compute Alignment"):
        aligner = Align.PairwiseAligner()
        aligner.mode = 'global'
        alignments = aligner.align(seq1, seq2)
        
        st.success(f"Optimal Alignment Score: {alignments[0].score}")
        st.subheader("Visual Mapping Result")
        st.code(str(alignments[0]), language="text")

elif option == "🔍 Live NCBI Search":
    st.header("Live GenBank Database Query")
    st.write("Search live genomic repositories directly from NCBI servers.")
    
    search_term = st.text_input("Search gene or organism name:", "Insulin")
    
    if st.button("Query NCBI"):
        if search_term:
            try:
                with st.spinner("Connecting to NCBI GenBank..."):
                    handle = Entrez.esearch(db="nucleotide", term=search_term, retmax=5)
                    record = Entrez.read(handle)
                    handle.close()
                
                id_list = record["IdList"]
                
                if id_list:
                    st.success(f"Found {len(id_list)} matching records!")
                    selected_id = st.selectbox("Select a GenBank Accession ID:", id_list)
                    
                    if st.button("Fetch Record Data"):
                        with st.spinner("Downloading genetic data..."):
                            fetch_handle = Entrez.efetch(db="nucleotide", id=selected_id, rettype="gb", retmode="text")
                            genbank_record = SeqIO.read(fetch_handle, "genbank")
                            fetch_handle.close()
                        
                        st.info(f"**Description:** {genbank_record.description}")
                        st.metric(label="Total Length", value=f"{len(genbank_record.seq)} bp")
                        st.subheader("Genetic Sequence Preview:")
                        st.code(str(genbank_record.seq[:400]) + "...", language="text")
                else:
                    st.warning("No records found for that search term. Try another keyword.")
            except Exception as e:
                st.error(f"Error connecting to NCBI: {e}")
        else:
            st.warning("Please enter a search term.")
            
