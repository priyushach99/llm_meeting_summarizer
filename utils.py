from fpdf import FPDF

def generate_pdf(transcript, summary, filename="Meeting_Report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    # Title set
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "LLM-Powered Meeting Summarizer", ln=True, align="C")
    
    pdf.ln(5)
    
    # Transcript Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Transcript:", ln=True)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, transcript)
    
    pdf.ln(5)
    
    # Summary Section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Meeting Summary:", ln=True)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, summary)
    
    
    pdf.ln(5)
    
    
    # Save PDF
    pdf.output(filename)
    return filename
