#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import datetime

target_rate = 128 #MB/s
infile = open("out.log", "r")

values = dict()
def_sched = False
fifo_sched = False
rr_sched = False
for line in infile.readlines():
#	if 0 <= line.find("Timing cached reads:"):
#		values["cached_reads"] = float(line.split()[-2])
	if 0 <= line.find("Timing buffered disk reads"):
		values["buffered_reads"] = float(line.split()[-2])
	elif 0 <= line.find("Using default scheduler"):
		def_sched = True
	elif 0 <= line.find("Using FIFO scheduling"):
		fifo_sched = True
	elif 0 <= line.find("Using Round-Robin scheduling"):
		rr_sched = True
	elif 0 <= line.find("Written 330 MB"):
		if True == def_sched:
			values["def_sched_330"] = float(line.split()[-2])
			def_sched = False
		elif True == fifo_sched:
			values["fifo_sched_330"] = float(line.split()[-2])
			fifo_sched = False
		elif True == rr_sched:
			values["rr_sched_330"] = float(line.split()[-2])
			rr_sched = False
	elif 0 <= line.find("Written 3300 MB"):
                if True == def_sched:
                        values["def_sched_3300"] = float(line.split()[-2])
                        def_sched = False
                elif True == fifo_sched:
                        values["fifo_sched_3300"] = float(line.split()[-2])
                        fifo_sched = False
		elif True == rr_sched:
                        values["rr_sched_3300"] = float(line.split()[-2])
                        rr_sched = False

#sort dictionary after its keys
x_vals = list()
y_vals = list()
i = 0;
for key in sorted(values.iterkeys()):
	x_vals.append(key)
	y_vals.append(values[key])
	i = i + 1

#filename with current date
now = datetime.datetime.now()
filename = "results_" + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + ".eps"

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot([0, i], [target_rate, target_rate], 'r')
ax.bar(np.arange(i), y_vals)
plt.ylabel("MB/s")
ax.set_xticklabels(x_vals)
fig.autofmt_xdate()
plt.grid()
plt.savefig(filename)
plt.show()
