from matplotlib import pyplot as plt
from matplotlib import dates
from datetime import datetime

with open("measured_data.txt", "r") as document1:
    dateandtime = []
    temp = []
    linhum = []
    corrhum = []
    dewpoint = []

    for line in document1.readlines():
        dstamp, temps, linhums, corrhums, dewpoints = line.rstrip().split('\t')
        dateandtime.append(datetime.strptime(dstamp, '%Y-%m-%d-%H:%M:%S'))
        temp.append(float(temps))
        linhum.append(float(linhums))
        corrhum.append(float(corrhums))
        dewpoint.append(float(dewpoints))

document1.close()


days = dates.DayLocator()
hours = dates.HourLocator() # HourLocator(interval=6)
dfmt = dates.DateFormatter('%d. %b.\n%H:%M')

#datemin = datetime(2018, 3, 2, 12, 0, 0)
#datemax = datetime(2018, 3, 2, 23, 0, 0)

fig = plt.figure()

ax1 = plt.subplot(211)
#ax1.set_xlim(datemin, datemax)
ax1.xaxis.set_major_formatter(dfmt)
ax1.xaxis.set_minor_formatter(dfmt)
ax1.set_ylabel('Temperature [C]')
ax1.plot(dateandtime, temp, linewidth=1, color='red')
plt.grid(True)

ax2 = plt.subplot(212)
#ax2.set_xlim(datemin, datemax)
ax2.xaxis.set_major_formatter(dfmt)
ax2.xaxis.set_minor_formatter(dfmt)
ax2.set_ylabel('Humidity [percent]')
ax2.plot(dateandtime, corrhum, linewidth=1, color='green')
#ax2.plot(dateandtime, linhum, linewidth=1, color='blue')
plt.grid(True)

#plt.title('SlowControl')
#plt.legend(['Temperature [C]','Corrected humidity [percent]'], loc='best', frameon=False)

plt.show()
