import streamlit as st
from Bio.Seq import Seq
from Bio import Align

st.title("🧬 Student Bioinformatics Toolkit")
st.write("Analyze DNA sequences, calculate GC content, and perform alignments instantly!")

# Sidebar navigation
option = st.sidebar.selectbox("Choose Tool", ["Sequence Analyzer", "Sequence Alignment"])

if option == "Sequence Analyzer":
    st.header("DNA Property & Protein Translator")
    dna_input = st.text_area("Enter DNA Sequence:", "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
    
    if st.button("Run Analysis"):
        if dna_input:
            clean_seq = Seq(dna_input.strip().upper())
            
            # Metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Length", value=f"{len(clean_seq)} bp")
            with col2:
                gc_count = clean_seq.count("G") + clean_seq.count("C")
                gc_pct = (gc_count / len(clean_seq)) * 100
                st.metric(label="GC Content", value=f"{gc_pct:.1f}%")
            
            # Transcription & Translation
            st.subheader("mRNA Transcription")
            st.code(str(clean_seq.transcribe()))
            
            st.subheader("Protein Translation")
            st.code(str(clean_seq.translate()))
        else:
            st.warning("Please enter a sequence.")

elif option == "Sequence Alignment":
    st.header("Pairwise Sequence Aligner")
    seq1 = st.text_input("Sequence 1 (Reference)", "ATGCCGTAGA")
    seq2 = st.text_input("Sequence 2 (Mutated)", "ATGCGTAGA")
    
    if st.button("Align Sequences"):
        aligner = Align.PairwiseAligner()
        aligner.mode = 'global'
        alignments = aligner.align(seq1, seq2)
        
        st.success(f"Alignment Score: {alignments[0].score}")
        st.subheader("Visual Alignment Result")
        st.code(str(alignments[0]))
