import utils
from flask import Flask, request, render_template, send_file, jsonify
import os
import excel_seperator as es

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools')
def tools():
    tools_list = ["엑셀 쪼개기", "PPT 추출", "작업 일정 관리", "문서 변환기"]
    return render_template('tools.html', tools=tools_list)

@app.route('/excel_seperator')
def excel_seperator():
    return render_template('excel_seperator.html')  # 엑셀 쪼개기 페이지


@app.route('/split-excel', methods=['POST'])
def split_excel():
    folder_name = utils.generate_unique_foldername(request)
    utils.create_folder(folder_name)

    file = request.files.get('file')
    if not file:
        return jsonify({"error": "파일이 전송되지 않았습니다."}), 400
    
    filename = file.filename
    file_path = os.path.join(folder_name, filename)
    file.save(file_path)  # 파일을 서버에 저장

    sheets = request.form.get('sheets')
    target_column_list = {}
    start_row_list = {}
    if sheets:
        sheets = eval(sheets)  # JSON 형태로 받은 시트 설정을 파싱
        for sheet in sheets:
            split = sheet.get("split")
            if split == 1:
                sheet_name =sheet.get("sheetName")
                start_row =sheet.get("startRow")
                criteria_column = sheet.get("criteriaColumn")
                target_column_list[sheet_name] = criteria_column
                start_row_list[sheet_name] = start_row
        # 시트 설정을 처리하고 엑셀 파일 쪼개는 작업 수행 (구현 부분은 생략)
        es.split_main(file_path, target_column_list, start_row_list)
        output_file_path = utils.make_zip(folder_name, folder_name)
        utils.del_folder(folder_name)
            
        # 파일을 직접 반환하여 브라우저가 다운로드를 처리하도록 설정
        return send_file(output_file_path, as_attachment=True)
    else:
        return jsonify({"error": "에러가 발생했습니다."}), 400


if __name__ == '__main__':
    app.run(debug=True)



