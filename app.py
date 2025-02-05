from flask import Flask, request, send_file, render_template
import os
from makeMrpReport import generate_mrp_report
from makeSccReport import generate_scc_report

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_mrp', methods=['POST'])
def generate_mrp():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, "MRP.json")
    file.save(file_path)
    
    # Generate the MRP report
    pdf_file = os.path.join(UPLOAD_FOLDER, "MRP_Report.pdf")
    generate_mrp_report(file_path, pdf_file)
    
    return send_file(pdf_file, as_attachment=True)

@app.route('/generate_scc', methods=['POST'])
def generate_scc():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    file_path = os.path.join(UPLOAD_FOLDER, "SCC.json")
    file.save(file_path)

    if os.stat(file_path).st_size == 0:
        return "Uploaded JSON file is empty", 400

    pdf_file = os.path.join(UPLOAD_FOLDER, "SCC_Report.pdf")
    generate_scc_report(file_path, pdf_file)

    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)