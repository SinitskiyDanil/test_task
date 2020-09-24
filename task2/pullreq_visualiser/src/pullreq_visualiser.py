from datetime import timedelta, date

import json
import matplotlib.pyplot as plt
import sys
import os.path


def draw_plot(dictt):
    fig, ax = plt.subplots()

    bars = ax.bar(list(dictt.keys()), list(dictt.values()))

    ax.set_facecolor('white')
    fig.set_facecolor('white')
    fig.set_figwidth(len(dictt.keys()))
    fig.set_figheight(max(dictt.values()))

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(bars)

    plt.xticks(rotation='vertical')
    plt.yticks(range(1, max(dictt.values())+2))
    plt.show()


def parse_json():
    json_file = open(sys.argv[1], 'r')

    json_text = json_file.read()
    json_file.close()
    source = json.loads(json_text)
    dictt = dict()
    for i in source:
        ddate = source[i]["date"]
        state = source[i]["state"]
        if state == "Merged":
            if source[i]["date"] in dictt:

                dictt[ddate] += 1
            else:
                dictt[ddate] = 1

    sorted_dates = sort_day_dates(dictt)
    amount_of_weeks = count_weeks(sorted_dates)
    sorted_weeks = sort_weeks(sorted_dates, amount_of_weeks)
    new_sorted_days = create_weeks_date_vs_pr_count(dictt, sorted_weeks, sorted_dates)

    a = {str(i): new_sorted_days[i] for i in new_sorted_days}
    return a


def sort_day_dates(dictt):
    return sorted([date(*(map(int, i.split('-')))) for i in sorted([j for j in dictt])])


def count_weeks(sorted_dates):
    return (sorted_dates[-1] - sorted_dates[0]).days // 7 + (
        1 if (sorted_dates[-1] - sorted_dates[0]).days % 7 > 0 else 0)


def sort_weeks(sorted_dates, amount_of_weeks):
    return [sorted_dates[0] + timedelta(days=7 * i) for i in range(amount_of_weeks)]


def create_weeks_date_vs_pr_count(dictt, sorted_weeks, sorted_dates):
    weeks_date_vs_prs_count = {}
    for current_week_date in sorted_weeks:
        prs_in_week = []
        for current_day_date in sorted_dates:
            prs_in_week.append((dictt[str(current_day_date)] if (7 > (current_day_date - current_week_date).days >= 0) else 0))
        amount_pr = sum(prs_in_week)
        weeks_date_vs_prs_count[current_week_date] = amount_pr if amount_pr != 0 else 0
    return weeks_date_vs_prs_count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Input template:\n pullreq_visualiser %path%")
    elif not os.path.exists(sys.argv[1]):
        print("No such file")
    else:
        draw_plot(parse_json())
