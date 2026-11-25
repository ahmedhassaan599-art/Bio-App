import streamlit as st
from Bio.Seq import Seq
from Bio import Align, Entrez, SeqIO
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="BioInnovate Genomix",
    page_icon="🧬",
    layout="centered"
)

# Custom Styling for modern cards and headers
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #6366f1;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.6rem;
        border: none;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

Entrez.email = "your.email@example.com"

# App Header
st.markdown('<p class="main-header">🧬 BioInnovate Genomix</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Computational Biology & Genomic Intelligence Platform</p>', unsafe_allow_html=True)

# Sidebar Navigation with Icons
st.sidebar.markdown("### 🧭 Control Panel")
option = st.sidebar.radio("Select Module:", ["🧪 Sequence Analyzer", "🔗 Sequence Alignment", "🔍 Live NCBI Database"])

if option == "🧪 Sequence Analyzer":
    st.subheader("🧪 DNA Sequence Property & Translation Engine")
    st.write("Analyze nucleotide distributions, evaluate GC-content stability, and translate coding frames.")
    
    dna_input = st.text_area("Enter Nucleotide Sequence (DNA):", "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", height=120)
    
    if st.button("Execute Genomic Analysis"):
        if dna_input:
            clean_seq = Seq(dna_input.strip().upper())
            
            # Metrics Columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Length", value=f"{len(clean_seq)} bp")
            with col2:
                gc_count = clean_seq.count("G") + clean_seq.count("C")
                gc_pct = (gc_count / len(clean_seq)) * 100
                st.metric(label="GC Content", value=f"{gc_pct:.1f}%")
            with col3:
                st.metric(label="Codon Count", value=f"{len(clean_seq) // 3}")
            
            st.markdown("---")
            
            # Visual Base Distribution Chart using Matplotlib
            st.markdown("#### 📊 Base Composition Distribution")
            bases = ['Adenine (A)', 'Thymine (T)', 'Guanine (G)', 'Cytosine (C)']
            counts = [clean_seq.count('A'), clean_seq.count('T'), clean_seq.count('G'), clean_seq.count('C')]
            colors = ['#ef4444', '#3b82f6', '#10b981', '#f59e0b']
            
            fig, ax = plt.subplots(figsize=(6, 2.5))
            ax.bar(bases, counts, color=colors, width=0.5)
            ax.set_ylabel("Frequency", fontsize=9)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            st.pyplot(fig)
            
            st.markdown("---")
            
            # Transcription & Translation Tabs
            tab1, tab2 = st.tabs(["✨ mRNA Transcription", "🧬 Protein Translation"])
            with tab1:
                st.code(str(clean_seq.transcribe()), language="text")
            with tab2:
                st.code(str(clean_seq.translate()), language="text")
        else:
            st.warning("Please enter a valid DNA sequence.")

elif option == "🔗 Sequence Alignment":
    st.subheader("🔗 Pairwise Global Sequence Aligner")
    st.write("Perform Needleman-Wunsch global sequence alignment to analyze genetic mutations.")
    
    col1, col2 = st.columns(2)
    with col1:
        seq1 = st.text_input("Reference Sequence", "ATGCCGTAGA")
    with col2:
        seq2 = st.text_input("Mutated Sequence", "ATGCGTAGA")
    
    if st.button("Run Global Alignment"):
        aligner = Align.PairwiseAligner()
        aligner.mode = 'global'
        alignments = aligner.align(seq1, seq2)
        
        st.success(f"Optimal Alignment Score: {alignments[0].score}")
        st.markdown("#### Alignment Map:")
        st.code(str(alignments[0]), language="text")

elif option == "🔍 Live NCBI Search":
    st.subheader("🔍 NCBI GenBank Live Query Engine")
    st.write("Fetch verified genetic records directly from government nucleotide repositories.")
    
    search_term = st.text_input("Query Gene / Organism:", "Insulin")
    
    if st.button("Search GenBank Records"):
        if search_term:
            try:
                with st.spinner("Connecting to NCBI servers..."):
                    handle = Entrez.esearch(db="nucleotide", term=search_term, retmax=5)
                    record = Entrez.read(handle)
                    handle.close()
                
                id_list = record["IdList"]
                
                if id_list:
                    st.success(f"Discovered {len(id_list)} matching records!")
                    selected_id = st.selectbox("Select Accession ID:", id_list)
                    
                    if st.button("Download & Parse Sequence"):
                        with st.spinner("Retrieving record data..."):
                            fetch_handle = Entrez.efetch(db="nucleotide", id=selected_id, rettype="gb", retmode="text")
                            genbank_record = SeqIO.read(fetch_handle, "genbank")
                            fetch_handle.close()
                        
                        st.info(f"**Metadata Description:** {genbank_record.description}")
                        st.metric(label="Total Sequence Length", value=f"{len(genbank_record.seq)} bp")
                        st.markdown("#### Nucleotide Fastq/Fasta Preview:")
                        st.code(str(genbank_record.seq[:400]) + "...", language="text")
                else:
                    st.warning("No records found. Try a different search keyword.")
            except Exception as e:
                st.error(f"NCBI connection error: {e}")
        else:
            st.warning("Please enter a search query.")
