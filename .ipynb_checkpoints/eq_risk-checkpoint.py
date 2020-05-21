# This script reads in historical earthquake data from the Los Angeles region
# and prompts the user to enter the lat-long coordinates of a house for which
# to determine the historical earthquake risk

import pandas
import numpy as np
import matplotlib.pyplot as plt
import math

#load earthquake data from 1950-2020
locmag = pandas.read_csv('/Users/Sam/Documents/Python/Portfolio/EQrisk/eq_data.csv')
datlen = locmag.shape[0];

#load LA coastline kml file
gedat = pandas.read_csv('/Users/Sam/Documents/Python/Portfolio/EQrisk/LAcoast.csv')

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
fig, ax = plt.subplots()
ax.scatter(locmag.longitude,locmag.latitude,c='r',s=s/2,alpha=0.2)
ax.plot(laclon,laclat,'k-',linewidth=3,alpha=0.7)

# plot major cities in the region
cities = pandas.read_csv('/Users/Sam/Documents/Python/Portfolio/EQrisk/cities.csv')

citlon = cities.lon
citlat = cities.lat
citnam = cities.city
citmar = cities.marker*10
citlen = citlon.shape[0]
   
ax.scatter(citlon,citlat,s=citmar,marker='*',c='b')
for txt in range(citlen):
    ax.text(citlon[txt],citlat[txt],citnam[txt])

plt.xlim(-119.366,-116.125)
plt.ylim(33.253,34.77)
plt.xlabel('Earthquakes in LA region from 1950 to 2020')
plt.show()


# prompt user for their location and magnitude cutoff
print('\n')
print('Observe the map to see LA region earthquakes from 1950-2020')
print('\n')
print('Enter the latitude of your location (eg Pasadena = 34.148): ')
nulat = input()
print('Enter the longitude of your location (eg Pasadena = -118.145): ')
nulon = input()
print('Enter the minimum magnitude you want to see (eg 4): ')
magcut = input()


# set up space for filtered data
zone20 = [[0,0,0]];
time = [0]
zonelen = 0;

# rectangular filter
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

# convert earthquake distance to miles relative to user location
zone20[:,0] = (zone20[:,0]-nulat)*(10/0.144);
zone20[:,1] = (zone20[:,1]-nulon)*(10/0.175);

# convert city distance to miles relative to user location
cit_y = (citlat - nulat)*(10/0.144);
cit_x = (citlon - nulon)*(10/0.175);

# set up space 20 mile radius data
d_20 = [[0,0,0]]
t_20 = [0]
len20 = 0;
yrs = [float(0)];
mos = [float(0)];

for k in range(zonelen-1):
    if np.sqrt((zone20[k,0]*zone20[k,0])+(zone20[k,1]*zone20[k,1]))<=20 and zone20[k,2]>=magcut:
        d_20.append(zone20[k,:])
        t_20.append(time[k])
        len20 = len20+1;
            
        t_stamp = time[k]
        yrs.append(float(t_stamp[0:4]))
        mos.append(float(t_stamp[5:7]))

# this part runs only if there are earthquakes that fit the given parameters
if len20 >= 1:              
    yrs = np.asarray(yrs[1:len20]);  
    mos = np.asarray(mos[1:len20]);          
        
    # convert data to array
    d_20 = np.asarray(d_20);
    d_20 = d_20[1:len20,:];  

    t_20 = np.asarray(t_20);
    t_20 = t_20[1:len20];         

    # scale and plot earthquake markers
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    b=np.multiply(d_20[:,2],d_20[:,2])
    t=np.multiply(d_20[:,2],b)
    ax1.scatter(d_20[:,1],d_20[:,0],c='r',s=t/2,alpha=0.4)

    # plot user location
    ax1.plot(0,0,"*",c='b',markersize=10)
    ax1.text(0,0,'  Your Location')

    # draw 20 mile circle around user location
    t = np.linspace(0,2*math.pi,num=200)
    x1 = 20*np.cos(t);
    y1 = 20*np.sin(t)
    ax1.plot(x1,y1,'k-',linewidth=3)
    ax1.set_aspect(aspect=1)
    plt.xlim(-21,21)
    plt.ylim(-21,21)
    
    #add cities to map
    ax1.scatter(cit_x,cit_y,s=citmar,marker='*',c='b')
    for txt in range(citlen):
        ax1.text(cit_x[txt],cit_y[txt],citnam[txt])
    
    plt.show()


    # This next section seeks to model earthquake liklihood based on 5,10,and 20 year
    # earthquake occurence windows

    # Arrange time and counting variables
    yrs = np.flipud(yrs)
    years = np.linspace(2019,1950,num=70)
    count = np.zeros(70)
    count_5 = np.zeros(65)
    count_10 = np.zeros(60)
    count_20 = np.zeros(50)
    m=yrs.shape[0]


    for i in range(70):
        for j in range(m):
            if yrs[j] == years[i]:
                count[i] = count[i]+1
    
        if years[i] >= 1955 and years[i] <= 2020:
            count_5[i-5] = float(sum(count[i-5:i]))/5
        
        if years[i] >= 1960 and years[i] <=2020:
            count_10[i-10] = float(sum(count[i-10:i]))/10
        
        if years[i] >= 1970 and years[i] <=2020:
            count_20[i-20] = float(sum(count[i-20:i]))/20

    # normalize risk for 5,10, and 20 year windows          
    p_5 = np.mean(count_5)/(count_5+np.mean(count_5))
    p_10 = np.mean(count_10)/(count_10+np.mean(count_10))
    p_20 = np.mean(count_20)/(count_20+np.mean(count_20))


    f, (ax3, ax4) = plt.subplots(2, 1, sharex=True)
    ax3.bar(years[0:50],count[0:50])
    ax4.plot(years[0:50],(p_5[0:50]+p_10[0:50]+p_20)/3,'k-')
    ax3.set_ylabel('Number of Earthquakes')
    ax4.set_ylabel('Earthquake Likelihood')
    ax4.set_xlabel('Year')
    ax3.set_title('Note: earthquake likelihood is based on mean recurrence')
    plt.show()
    
else:
    print('\n')
    print('There are no earthquakes that fit these parameters')
    print('Check that the coordinates fall within the map area or decrease magnitude cutoff')
        

          


