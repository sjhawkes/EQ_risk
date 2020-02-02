# This script reads in historical earthquake data from the Los Angeles region
# and prompts the user to enter the lat-long coordinates of a house for which
# to determine the historical earthquake risk

import pandas
import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import date

#load earthquake data as a Pandas DataFrame
locmag = pandas.read_csv('/Users/Sam/Documents/Python/Portfolio/Earthquake Risk/eq_data.csv')
datlen = locmag.shape[0];

#load LA coastline kml file
gedat = pandas.read_csv('/Users/Sam/Documents/Python/Portfolio/Earthquake Risk/LA Coast.csv')

# allocate space for coastline points
laclon = [0];
laclat = [0];

# filter lat lon coordinates from kml file
for i in range(98):
    if gedat.iloc[i,0] >= 1:
        laclat.append(gedat.iloc[i,0]);
    elif gedat.iloc[i,0] <= -1:
        laclon.append(gedat.iloc[i,0]);

# trim lat and lon of LA coast from kml file    
laclon = laclon[1:];
laclat = laclat[1:];


# scale and plot earthquake markers
a=np.multiply(locmag.mag,locmag.mag)
s=np.multiply(locmag.mag,a)
plt.scatter(locmag.longitude,locmag.latitude,c='r',s=s/2,alpha=0.4)
plt.plot(laclon,laclat,'k-',linewidth=3,alpha=0.7)

# plot major cities in the region
plt.plot(-118.244,34.052,"*",c='b',markersize=15)
plt.text(-118.244,34.052,'  Los Angeles')
plt.plot(-118.193,33.770,"*",c='b',markersize=10)
plt.text(-118.193,33.770,'  Long Beach')
plt.plot(-119.177,34.197,"*",c='b',markersize=10)
plt.text(-119.177,34.197,'  Oxnard')
plt.plot(-118.542,34.392,"*",c='b',markersize=10)
plt.text(-118.542,34.392,'  Santa Clarita')
plt.plot(-118.154,34.687,"*",c='b',markersize=10)
plt.text(-118.154,34.687,'  Lancaster')
plt.plot(-117.292,34.536,"*",c='b',markersize=10)
plt.text(-117.292,34.536,'  Victorville')
plt.plot(-117.749,34.055,"*",c='b',markersize=10)
plt.text(-117.749,34.055,'  Pomona')
plt.plot(-117.396,33.954,"*",c='b',markersize=10)
plt.text(-117.396,33.954,'  Riverside')
plt.plot(-117.795,33.684,"*",c='b',markersize=10)
plt.text(-117.795,33.684,'  Irvine')
plt.plot(-117.148,33.494,"*",c='b',markersize=10)
plt.text(-117.148,33.494,'  Temecula')
plt.xlim(-119.366,-116.125)
plt.ylim(33.253,34.77)
plt.xlabel('Historic earthquakes in LA region')
plt.show()



# prompt user for their location and magnitude cutoff
print('Enter the latitude of your location (eg Santa Clarita = 34.392: ')
nulat = input()
print('\n')
print('Enter the longitude of your location (eg Santa Clarita = -118.542: ')
nulon = input()
print('\n')
print('Enter the minimum magnitude you want to see (eg 4): ')
magcut = input()


# Set up space for 20 mile filter
zone20 = [[0,0,0]];
time = [0]
zonelen = 0;

# 20 mile rectangular filter
for j in range(datlen):
    if locmag.iloc[j,1] <= nulat+0.144*2 and locmag.iloc[j,1] >= nulat-0.144*2 and locmag.iloc[j,2] >= nulon-0.175*2 and locmag.iloc[j,2] <= nulon+0.175*2:
        newrow = [locmag.iloc[j,1],locmag.iloc[j,2],locmag.iloc[j,4]];
        zone20.append(newrow)
        time.append(locmag.iloc[j,0])
        zonelen=zonelen+1;
       
zone20 = np.asarray(zone20);
zone20 = zone20[1:zonelen,:];
time = np.asarray(time);
time = time[1:zonelen];

# convert to miles relative to user location
zone20[:,0] = (zone20[:,0]-nulat)*(10/0.144);
zone20[:,1] = (zone20[:,1]-nulon)*(10/0.175);

# set up space for10 and 20 mile radius data
d_20 = [[0,0,0]]
d_10 = [[0,0,0]]
t_20 = [0]
t_10 = [0]
len20 = 0;
len10 = 0;
yrs = [0];

# filter for 20 mile radius
for k in range(zonelen-1):
    if np.sqrt((zone20[k,0]*zone20[k,0])+(zone20[k,1]*zone20[k,1]))<=20 and zone20[k,2]>=magcut:
        d_20.append(zone20[k,:])
        t_20.append(time[k])
        len20 = len20+1;
        
        t_stamp = time[k]
        yrs.append(int(t_stamp[0:4]))

# trim 0 off beginning of data        
yrs = yrs[1:len20];       

# filter for 10 mile radius
for m in range(zonelen-1):
    if np.sqrt((zone20[m,0]*zone20[m,0])+(zone20[m,1]*zone20[m,1]))<=10 and zone20[m,2]>=magcut:
        d_10.append(zone20[m,:])
        t_10.append(time[m])
        len10 = len10+1;
        
        
# convert data to arrays
d_20 = np.asarray(d_20);
d_20 = d_20[1:len20,:];  

d_10 = np.asarray(d_10);
d_10 = d_10[1:len10,:]; 

t_20 = np.asarray(t_20);
t_20 = t_20[1:len20];  

t_10 = np.asarray(t_10);
t_10 = t_10[1:len10]; 
        

# scale and plot earthquake markers
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
b=np.multiply(d_20[:,2],d_20[:,2])
t=np.multiply(d_20[:,2],b)
ax1.scatter(d_20[:,1],d_20[:,0],c='r',s=t/2,alpha=0.4)

# plot location
ax1.plot(0,0,"*",c='b',markersize=10)
ax1.text(0,0,'  Your Location')

# draw 20 mile circle around data
t = np.linspace(0,2*math.pi,num=200)
x1 = 20*np.cos(t);
y1 = 20*np.sin(t)
ax1.plot(x1,y1,'k-',linewidth=3)
ax1.set_aspect(aspect=1)
plt.xlim(-21,21)
plt.ylim(-21,21)
plt.xlabel('Earthquakes in 20 mile radius of your location')
plt.show()

# scale and plot earthquake markers
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
c=np.multiply(d_10[:,2],d_10[:,2])
u=np.multiply(d_10[:,2],c)
ax2.scatter(d_10[:,1],d_10[:,0],c='r',s=u/2,alpha=0.4)

# plot location
ax2.plot(0,0,"*",c='b',markersize=10)
ax2.text(0,0,'  Your Location')

# draw 10 mile radius around data
x1 = 10*np.cos(t);
y1 = 10*np.sin(t)
ax2.plot(x1,y1,'k-',linewidth=3)
ax2.set_aspect(aspect=1)
plt.ylim(-11,11)
plt.xlim(-11,11)
plt.xlabel('Earthquakes in 10 mile radius of your location')
plt.show()


# time distribution plots
rec20 = [0]
reclen20 = 0;

for i in range(len20-2):
    inst1 = t_20[i];
    inst2 = t_20[i+1];
    
    delta = date(int(inst1[0:4]),int(inst1[5:7]),int(inst1[8:10]))-date(int(inst2[0:4]),int(inst2[5:7]),int(inst2[8:10]));
    
    # filter out aftershock events (recurrence < 30 days)
    if delta.days >= 10:
        rec20.append(delta.days)
        reclen20 = reclen20+1

# trim initiation zero
rec20 = rec20[1:reclen20]


print('Mean recurrence: ', np.mean(rec20))
print('\n')
print('Standard deviation: ', np.std(rec20))

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.hist(rec20,bins=30)
plt.xlabel('Days between earthquakes')
plt.ylabel('Count')
plt.show()


fig4 = plt.figure()
ax4 = fig4.add_subplot(111)
ax4.hist(yrs,bins=30)
plt.xlabel('Year')
plt.ylabel('Number of earthquakes')
plt.show()