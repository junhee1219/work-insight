from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools')
def tools():
    tools_list = ["엑셀 쪼개기", "PPT 추출", "작업 일정 관리", "문서 변환기"]
    return render_template('tools.html', tools=tools_list)

if __name__ == '__main__':
    app.run(debug=True)
