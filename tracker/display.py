from datetime import datetime, timedelta

import plotext as plt

HEIGHT_RATIO = .4
WIDTH_RATIO = 1

DATETIME_FORMAT = "%d/%m"


def plot_measures(measures):
    start_timestamp = datetime.now() - timedelta(days=7)
    now = datetime.now()

    w, h = plt.terminal_size()

    values_y = [m.value for m in measures]
    values_x = [m.timestamp for m in measures]

    plt.clear_plot()
    plt.plot(values_x, values_y)
    plt.nocolor()

    xticks = [int(start_timestamp.strftime("%s"))]
    xlabels = [start_timestamp.strftime(DATETIME_FORMAT)]

    day = (
        start_timestamp + timedelta(days=1)
    ).replace(hour=0, minute=0, second=0, microsecond=0)

    while day < now:
        xticks.append(int(day.strftime("%s")))
        xlabels.append(day.strftime(DATETIME_FORMAT))

        day += timedelta(days=1)

    xticks.append(int(now.strftime("%s")))
    xlabels.append(now.strftime(DATETIME_FORMAT))

    plt.xlim(int(start_timestamp.strftime("%s")), int(now.strftime("%s")))

    plt.xticks(xticks, xlabels)
    plt.figsize(w * WIDTH_RATIO, h * HEIGHT_RATIO)

    plt.show()
