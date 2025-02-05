from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import json

# Function to wrap long text
def wrap_text(data):
    styles = getSampleStyleSheet()
    wrapped_data = []
    for row in data:
        wrapped_row = []
        for cell in row:
            wrapped_row.append(Paragraph(cell, styles["BodyText"]))
        wrapped_data.append(wrapped_row)
    return wrapped_data

# Function get request ID column index
def get_ID_index(header):
    for i in range(len(header)):
        if header[i] == "Request Number":
            return i

# Function get impact column ID index
def get_impact_index(header):
    for i in range(len(header)):
        if header[i] == "Change Impact":
            return i

def generate_scc_report (input_json, output_pdf):
    with open(input_json, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    header = list(data[0].keys())
    print(header)
    rows = [list(item.values()) for item in data]
    table_data = [header] + rows

    id_col = get_ID_index(header)
    impact_col = get_impact_index(header)

    # Wrap the text in the table
    table_data = wrap_text(table_data)

    # Create a PDF document with A3 paper size and landscape orientation
    pdf = SimpleDocTemplate(output_pdf, pagesize=landscape(A3), rightMargin=2, leftMargin=2, topMargin=10, bottomMargin=10)

    col_widths = [100, 100, 100, 350, 80, 200, 120]

    table = Table(table_data, colWidths=col_widths)

    light_green = colors.HexColor("#ccffcc")
    light_orange = colors.HexColor("#ffcc99")
    light_red = colors.HexColor("#ff9999")

    # Style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Add a red line 
    previous_request_number = None
    for i, row in enumerate(rows, start=1): 
        current_request_number = row[id_col]  
        if previous_request_number is not None and current_request_number != previous_request_number:
            style.add('LINEABOVE', (0, i), (-1, i), 2, colors.red)  # Add red line on top of the row
        previous_request_number = current_request_number

        # Apply color to cell
        change_impact = row[4].strip().lower()
        if change_impact == "low":
            style.add('BACKGROUND', (impact_col, i), (impact_col, i), light_green)
        elif change_impact == "medium":
            style.add('BACKGROUND', (impact_col, i), (impact_col, i), light_orange)
        elif change_impact == "high":
            style.add('BACKGROUND', (impact_col, i), (impact_col, i), light_red)

    table.setStyle(style)

    # Build the PDF
    elements = [table]
    pdf.build(elements)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python makeSccReport.py <input_json> <output_pdf>")
        sys.exit(1)
    input_json = sys.argv[1]
    output_pdf = sys.argv[2]
    generate_scc_report(input_json, output_pdf)