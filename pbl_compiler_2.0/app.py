from flask import Flask, render_template, request, send_file, make_response
import os
import io
from matching.similarity_engine import compute_combined_similarity

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    details = None
    if request.method == 'POST':
        mode = request.form.get('mode')
        if mode == 'upload':
            file1 = request.files.get('file1')
            file2 = request.files.get('file2')
            if file1 and file2:
                path1 = os.path.join(UPLOAD_FOLDER, file1.filename)
                path2 = os.path.join(UPLOAD_FOLDER, file2.filename)
                file1.save(path1)
                file2.save(path2)
                try:
                    # If your function returns matched lines:
                    score, matched1, matched2 = compute_combined_similarity(path1, path2)
                    result = f"Similarity Score: {score:.2f}%"

                    # Build detailed report
                    report = f"Plagiarism Report\n\nSimilarity Score: {score:.2f}%\n\n"
                    report += "Matched Lines in File 1:\n"
                    for lineno, line in matched1:
                        report += f"Line {lineno}: {line}\n"
                    report += "\nMatched Lines in File 2:\n"
                    for lineno, line in matched2:
                        report += f"Line {lineno}: {line}\n"

                    details = {
                        "matched1": matched1,
                        "matched2": matched2,
                        "report": report
                    }
                except Exception as e:
                    result = f"Error: {str(e)}"
                    details = None
                os.remove(path1)
                os.remove(path2)
            else:
                result = "Please upload both files."
        elif mode == 'paste':
            code1 = request.form.get('code1')
            code2 = request.form.get('code2')
            if code1 and code2:
                temp1 = os.path.join(UPLOAD_FOLDER, 'temp_code1.py')
                temp2 = os.path.join(UPLOAD_FOLDER, 'temp_code2.py')
                with open(temp1, 'w', encoding='utf-8') as f:
                    f.write(code1)
                with open(temp2, 'w', encoding='utf-8') as f:
                    f.write(code2)
                try:
                    score, matched1, matched2 = compute_combined_similarity(temp1, temp2)
                    result = f"Similarity Score: {score:.2f}%"
                    details = {"matched1": matched1, "matched2": matched2}
                except Exception as e:
                    result = f"Error: {str(e)}"
                    details = None
                os.remove(temp1)
                os.remove(temp2)
            else:
                result = "Please paste code in both boxes."
    matched1 = ["def foo():", "    return 42"]
    matched2 = ["def foo():", "    return 42"]
    report_content = f"Plagiarism Report\n\n{result}\n"
    if details and details.get("matched1"):
        report_content += "\nMatched Lines in File 1:\n" + "\n".join(str(line) for line in details["matched1"])
        report_content += "\nMatched Lines in File 2:\n" + "\n".join(str(line) for line in details["matched2"])
    return render_template('index.html', result=result, details=details, report_content=report_content)

@app.route('/download_report', methods=['POST'])
def download_report():
    report = request.form.get('report', '')
    # Write the report content to a BytesIO object
    buffer = io.BytesIO()
    buffer.write(report.encode('utf-8'))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name='plagiarism_report.txt',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    import os
    import threading
    import webbrowser

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000/")

    # Only open browser if not running in the reloader process
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        threading.Timer(1.0, open_browser).start()
    app.run(debug=True)