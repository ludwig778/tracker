import plotext as plt
from pprint import pprint
from tracker.models import *

measures = Key.get("lmao2").measures
pprint(measures)
values = [m.value for m in measures]
y = values


plt.plot(y)
#plt.scatter(y, point_color = "iron")
#plt.legend(["lines", "points"])
plt.nocolor()
plt.show()

print(len(y))
