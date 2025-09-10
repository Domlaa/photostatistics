from flask import Flask, render_template, jsonify, request

from analysis import analysis

app = Flask(__name__)

run_flag = False
start_time = '2024-1-01 00:00:00'
end_time = '2024-12-31 23:59:59'
time_range = (start_time, end_time)
html: str = ''

@app.route("/")
def index():
    total_shot = analysis.total_shot()
    data = {
        'total_shot': total_shot
    }
    return render_template('index.html', **data)


def run(port=21314):
    global run_flag
    if not run_flag:
        try:
            app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
            run_flag = True
        except:
            pass
    else:
        pass


@app.route('/statistics_shot', methods=['POST'])
def statistics_shot():
    time_range = request.json.get('time_range', [])
    data = analysis.sender(time_range=time_range)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
