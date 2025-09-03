import os
import sys
import time
from urllib.parse import urljoin

import requests
from flask import Flask, render_template, send_file, jsonify, make_response, request
from pyecharts.charts import Bar

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
    contact_topN_num = msg_db.get_chatted_top_contacts(time_range=time_range, top_n=9999999, contain_chatroom=True)
    total_msg_num = sum(list(map(lambda x: x[1], contact_topN_num)))
    contact_topN = []
    for wxid, num in contact_topN_num:
        contact = get_contact(wxid)
        text_length = 0
        contact_topN.append([contact, num, text_length])
    contacts_data = analysis.contacts_analysis(contact_topN)
    contact_topN = []
    send_msg_num = msg_db.get_send_messages_number_sum(time_range)
    contact_topN_num = msg_db.get_chatted_top_contacts(time_range=time_range, top_n=9999999, contain_chatroom=False)

    for wxid, num in contact_topN_num[:6]:
        contact = get_contact(wxid)
        text_length = msg_db.get_message_length(wxid, time_range)
        contact_topN.append([contact, num, text_length])

    my_message_counter_data = analysis.my_message_counter(time_range=time_range)
    data = {
        'avatar': Me().smallHeadImgUrl,
        'contact_topN': contact_topN,
        'contact_num': len(contact_topN_num),
        'send_msg_num': send_msg_num,
        'receive_msg_num': total_msg_num - send_msg_num,
    }
    return render_template('index.html', **data,**contacts_data, **my_message_counter_data)




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




@app.route('/charts/<wxid>')
def charts(wxid):
    # 渲染模板，并传递图表的 HTML 到模板中
    contact = get_contact(wxid)
    try:
        first_message, first_time = msg_db.get_first_time_of_message(wxid)
    except TypeError:
        first_time = '2023-01-01 00:00:00'
    data = {
        'wxid': wxid,
        'my_nickname': Me().name,
        'ta_nickname': contact.remark,
        'first_time': first_time
    }
    return render_template('index.html', **data)


@app.route('/calendar', methods=['POST'])
def get_calendar():
    wxid = request.json.get('wxid')
    time_range = request.json.get('time_range', [])
    world_cloud_data = analysis.calendar_chart(wxid, time_range=time_range)
    return jsonify(world_cloud_data)


@app.route('/message_counter', methods=['POST'])
def get_counter():
    time_range = request.json.get('time_range', [])
    data = analysis.sender(time_range=time_range)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
