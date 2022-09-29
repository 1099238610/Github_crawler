import json
import csv
import sys

from JsonPath import JsonPathFinder

header = ["issue_url", "issue_status", "user_name", "datetime", "body", "type", "related_issue"]


def json_to_csv():
    json_file_path = '/Users/yuzhuoma/Desktop/FIT4003/issue_data_801-991.json'
    f = open(json_file_path)
    json_load_result = json.load(f)

    with open(json_file_path) as jf:
        json_data = jf.read()

    finder = JsonPathFinder(json_data)
    json_length = finder.find_all('issue_url')
    result_list = []

    for json_index in range(len(json_length)):
        new_finder = JsonPathFinder(json.dumps(json_load_result[json_index]['issue_list']))
        single_json_list = new_finder.find_all('user_name')
        for single_json_index in range(len(single_json_list)):
            issue_url = json_load_result[json_index]['issue_url']
            issue_status = json_load_result[json_index]['issue_status']

            user_name = json_load_result[json_index]['issue_list'][single_json_index]['user_name']

            datetime = json_load_result[json_index]['issue_list'][single_json_index]['datetime']
            body = json_load_result[json_index]['issue_list'][single_json_index]['body']
            type = json_load_result[json_index]['issue_list'][single_json_index]['type']
            related_issue = json_load_result[json_index]['issue_list'][single_json_index]['related_issue']
            temp_list = [issue_url, issue_status, user_name, datetime, body, type, related_issue]

            result_list.append(temp_list)

    print(result_list)

    with open('/Users/yuzhuoma/Desktop/FIT4003/phrase_data.csv', 'a', encoding='UTF8') as cf:
        writer = csv.writer(cf)
        writer.writerow(header)
        for result in result_list:
            writer.writerow(result)

    cf.close()


json_to_csv()