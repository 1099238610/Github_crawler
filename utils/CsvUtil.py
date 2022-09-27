import csv


def write_csv():
    header_list = ["Project", "Name", "Category", "status", "url", "Participate", "Comment", "Comment date"]

    with open("../result/issue_data.csv", mode="w", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(header_list)
        data = read_source()
        for project in data:
            for issue in project['issue_list']:
                print(issue)

def read_source():
    file = open("../result/issue_data.json", mode="r", encoding="utf-8-sig")
    data = file.read().replace('null', '""')
    file.close()
    return eval(data)


if __name__ == '__main__':
    write_csv()
