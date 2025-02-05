#!/usr/bin/env python3
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

# Function to get the index of the "Request Number" column
def get_ID_index(header):
    for i in range(len(header)):
        if header[i] == "Request Number":
            return i

# Function to generate the MRP report
def generate_mrp_report(input_json, output_pdf):
    # Read the JSON file
    with open(input_json, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    # Extract header and rows
    header = list(data[0].keys())
    rows = [list(item.values()) for item in data]
    table_data = [header] + rows

    # Get the index of the "Request Number" column
    id_col = get_ID_index(header)

    # Wrap the text in the table
    table_data = wrap_text(table_data)

    # Create a PDF document with A3 paper size and landscape orientation
    pdf = SimpleDocTemplate(output_pdf, pagesize=landscape(A3), rightMargin=2, leftMargin=2, topMargin=10, bottomMargin=10)

    # Define column widths
    col_widths = [120, 70, 110, 200, 110, 250, 60]
    table = Table(table_data, colWidths=col_widths)

    # Define colors
    light_green = colors.HexColor("#ccffcc")
    light_orange = colors.HexColor("#ffcc99")
    light_red = colors.HexColor("#ff9999")

    # Define table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Add a red line between rows with different request numbers
    previous_request_number = None
    for i, row in enumerate(rows, start=1):  # Start from 1 because 0 is the header
        current_request_number = row[id_col]
        if previous_request_number is not None and current_request_number != previous_request_number:
            style.add('LINEABOVE', (0, i), (-1, i), 2, colors.red)  # Add red line on top of the row
        previous_request_number = current_request_number

    # Apply the style to the table
    table.setStyle(style)

    # Build the PDF
    elements = [table]
    pdf.build(elements)

# For standalone execution (optional)
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python makeMrpReport.py <input_json> <output_pdf>")
        sys.exit(1)
    input_json = sys.argv[1]
    output_pdf = sys.argv[2]
    generate_mrp_report(input_json, output_pdf)
