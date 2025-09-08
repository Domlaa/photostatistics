from flask import Flask, render_template, jsonify, request

from analysis import analysis

app = Flask(__name__)

run_flag = False
wxid = ''
start_time = '2024-1-01 00:00:00'
end_time = '2024-12-31 23:59:59'
time_range = (start_time, end_time)
html: str = ''



@app.route("/")
def index():
    return render_template('index.html')


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


@app.route('/month_count', methods=['POST'])
def get_chart_options():
    wxid = request.json.get('wxid')
    time_range = request.json.get('time_range', [])
    data = analysis.month_count(wxid, time_range=time_range)
    return jsonify(data)





@app.route('/calendar', methods=['POST'])
def get_calendar():
    wxid = request.json.get('wxid')
    time_range = request.json.get('time_range', [])
    world_cloud_data = analysis.calendar_chart(wxid, time_range=time_range)
    return jsonify(world_cloud_data)


@app.route('/focal_seq_10', methods=['POST'])
def focal_seq_10():
    time_range = request.json.get('time_range', [])
    data = analysis.sender(time_range=time_range)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
