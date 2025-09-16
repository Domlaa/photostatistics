from flask import Flask, render_template, jsonify, request

from analysis import analysis
from common import config

app = Flask(__name__)

# start_time = '2024-1-01 00:00:00'
# end_time = '2024-12-31 23:59:59'
# time_range = (start_time, end_time)

analyzer = config.get_analyzer()

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/statistics_shot', methods=['POST'])
def statistics_shot():
    _time_range = request.json.get('time_range', [])
    data = analysis.get_analysis_data(analyzer, _time_range=_time_range)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
