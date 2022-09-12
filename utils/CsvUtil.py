import csv


def write_csv(data):
    header_list = ["Project", "Name", "Category", "status", "url", "Participate", "Comment", "Comment date"]

    with open("../result/issue_data.csv", mode="w", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(header_list)


if __name__ == '__main__':
    write_csv(1)
