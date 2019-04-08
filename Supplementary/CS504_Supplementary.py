'''
Created: Mar 17, 2019
Updated: Apr 4, 2019
@author: Tianye Zhao
'''
#======================
# imports
#======================
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
import urllib.request
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from urllib.request import urlopen
import json
from datetime import datetime
import PIL.Image
import PIL.ImageTk

OWM_API_KEY = '0605dc0c4ea32dc8351a1a32fff72a4'
        
#======================
# functions
#======================
# Exit GUI cleanly
def _quit():
    win.quit()      
    win.destroy()
    exit()

# Information
def _info():
    messagebox.showinfo(title='About',
                           message='CS504 Supplementary Project\nAuthor: Tianye Zhao')

# Open file
def _open():
    path = filedialog.askopenfilename(initialdir='',title='Choose a file',
                                          filetypes=(('DLY','*.dly'),('CSV','*.csv'),('ZIP','*.zip')))

#======================
# procedural code
#======================
# Create instance
win = tk.Tk()   

# Add a title       
win.title("CS504 Supplementary Project")
# ---------------------------------------------------------------
# Creating a Menu Bar
menuBar = Menu()
win.config(menu=menuBar)

# Add menu items
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Open", command=_open)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=_quit)  
menuBar.add_cascade(label="File", menu=fileMenu)

# Add another Menu to the Menu Bar and an item
helpMenu = Menu(menuBar, tearoff=0)
helpMenu.add_command(label="About", command=_info)
menuBar.add_cascade(label="Help", menu=helpMenu)
# ---------------------------------------------------------------

# Tab Control / Notebook 
tabControl = ttk.Notebook(win)          # Create Tab Control

tab1 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab1, text='NOAA')       # Add the tab

tab2 = ttk.Frame(tabControl)                # Add a second tab
tabControl.add(tab2, text='OpenWeatherMap')    # Make second tab visible

tabControl.pack(expand=1, fill="both")  # Pack to make visible

#########################################################################################
# TAB 1
#######
# create a container frame to hold all other widgets
stations_frame = ttk.LabelFrame(tab1, text=' Stations ')
stations_frame.grid(column=0, row=0, padx=8, pady=4)

# ---------------------------------------------------------------
# Add a Label
ttk.Label(stations_frame, text="Select a Province: ").grid(column=0, row=0) # empty space for alignment

# ---------------------------------------------------------------
province = tk.StringVar()
province_combo = ttk.Combobox(stations_frame, width=5, textvariable=province)         
province_combo['values'] = ('QC','BC','YT','NT','NU','AB','SK','MB','ON','NB','NS','PE','NL')
province_combo.grid(column=1, row=0)
province_combo.current(0)                 # highlight first

# ---------------------------------------------------------------
# callback function
def _get_stations():
    province = province_combo.get()
    get_station_ids(province)

get_weather_btn = ttk.Button(stations_frame,text='Get Stations', command=_get_stations).grid(column=2, row=0)

scr = scrolledtext.ScrolledText(stations_frame, width=42, height=10, wrap=tk.WORD)
scr.grid(column=0, row=1, columnspan=3)

# ---------------------------------------------------------------
for child in stations_frame.winfo_children(): 
        child.grid_configure(padx=6, pady=6)   


# ---------------------------------------------------------------
                     
def get_station_ids(province='QC'):
    stations_txt = Path('ghcnd-stations.txt')
    if not stations_txt.is_file():
        # download stations list from NOAA FTP
        urllib.request.urlretrieve('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt',
                                   'ghcnd-stations.txt')
    
    stations = {}       # collect the station names in a dictionary
    
    for line in open('ghcnd-stations.txt','r'):
        # skip stations without GSN keywords and collect stations in selected province in Canada
        if 'GSN' in line and province in line and line[:2] == 'CA':
            fields = line.split()   # split line by whitespaces
            stations[fields[0]] = ' '.join(fields[5:-2])  # add name of station
            
    scr.delete('1.0', tk.END)  # clear scrolledText widget for next btn click
    station_codes = ()
    datastations = []
    for code, name in stations.items():
        scr.insert(tk.INSERT, code + ' ' + name + '\n')
        datastations.append(code)
        station_codes = station_codes + (code,)

    station_name_combo['values'] = station_codes
    station_name_combo.current(0)                 # highlight first city station id     

# ---------------------------------------------------------------


#########################################################################################
# NOAA (National Oceanic and Atmospheric Administration) section starts here

# create a container frame to hold other widgets
weather_cities_frame = ttk.LabelFrame(tab1, text=' Observation for ')
weather_cities_frame.grid(column=0, row=1, padx=8, pady=4)

# ---------------------------------------------------------------
# Add a Label
ttk.Label(weather_cities_frame, text="Station: ").grid(column=0, row=0) # empty space for alignment

# ---------------------------------------------------------------
station_name = tk.StringVar()
station_name_combo = ttk.Combobox(weather_cities_frame, width=12, textvariable=station_name)       

station_name_combo.grid(column=1, row=0)

# Adding a Label
ttk.Label(weather_cities_frame, text="Year: ").grid(column=0, row=1) # empty space for alignment

# ---------------------------------------------------------------
year = tk.IntVar()
year_combo = ttk.Combobox(weather_cities_frame, width=5, textvariable=year)       

year_combo.grid(column=1, row=1)

# ---------------------------------------------------------------
# callback function
def _get_year():
    station_code = station_name_combo.get()
    get_year_data(station_code)


get_year_btn = ttk.Button(weather_cities_frame,text='Get Year', command=_get_year).grid(column=2, row=0)

def _get_daily():
    station_code = station_name_combo.get()
    year = year_combo.get()
    get_daily_data(station_code, year)

get_daily_btn = ttk.Button(weather_cities_frame,text='Get Daily', command=_get_daily).grid(column=2, row=1)

def _get_extreme():
    station_code = station_name_combo.get()
    get_extreme_data(station_code)

get_extreme_btn = ttk.Button(weather_cities_frame,text='Get Extreme', command=_get_extreme).grid(column=3, row=0)

# ---------------------------------------------------------------

for child in weather_cities_frame.winfo_children(): 
        child.grid_configure(padx=5, pady=4)    

#########################################################################################
# NOAA DATA directly from FTP

# ---------------------------------------------------------------

def get_year_data(station_code):
    filename = station_code + '.dly'
    station_dly = Path(filename)
    if not station_dly.is_file():
        urllib.request.urlretrieve('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/gsn/'+
                                   filename, filename)
    

    tmin = getobs(filename)
    tmax = getobs(filename, 'TMAX')
    fillnans(tmin)
    fillnans(tmax)
    
    # ignore first year in records as its data might not be completed
    min_year = tmin['date'][0].astype('datetime64[Y]').astype(int) + 1971
    # ignore year 2019 as its data is incompleted
    max_year = tmin['date'][-1].astype('datetime64[Y]').astype(int) + 1969

    years = ()
    for year in range(min_year, max_year+1):
        years = years + (str(year),)

    year_combo['values'] = years
    year_combo.current(0)

    # give a bigger figsize
    plt.figure(figsize=(10,4))
    
    plt.clf()

    # large smoothing parameter
    plot_smoothed(tmin,'minimum',365)
    plot_smoothed(tmax,'maximum',365)
    
    plt.title(station_code+' smoothed temperature from '+str(min_year)+' to '+str(max_year))

    # fix range of years to avoid artifacts at edges due to running out of values to average
    plt.axis(xmin=np.datetime64(str(min_year)), xmax=np.datetime64(str(max_year-1)))
    plt.legend()
    
    plt.show()


def get_daily_data(station_code, year):
    filename = station_code + '.dly'
    station_dly = Path(filename)
    if not station_dly.is_file():
        urllib.request.urlretrieve('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/gsn/'+
                                   filename, filename)
    

    tmin = getobs(filename)
    tmax = getobs(filename, 'TMAX')
    fillnans(tmin)
    fillnans(tmax)

    # ignore first year in records as its data might not be completed
    min_year = tmin['date'][0].astype('datetime64[Y]').astype(int) + 1971
    # ignore year 2019 as its data is incompleted
    max_year = tmin['date'][-1].astype('datetime64[Y]').astype(int) + 1969
    
    years = np.arange(min_year,max_year+1)

    # arrange all years in a matrix and ignore extra day in leap years
    tmin_all = np.vstack([selectyear(tmin,year)[:365] for year in years])
    tmax_all = np.vstack([selectyear(tmax,year)[:365] for year in years])

    # compute the maximum and minimum along row
    tmin_recordmin = np.min(tmin_all,axis=0)
    tmin_recordmax = np.max(tmin_all,axis=0)
    tmax_recordmin = np.min(tmax_all,axis=0)
    tmax_recordmax = np.max(tmax_all,axis=0)

    # give a bigger figsize
    plt.figure(figsize=(10,4))
    
    plt.clf()
    
    days = np.arange(1,366)

    # plot shaded area
    plt.fill_between(days,tmin_recordmin,tmin_recordmax,alpha=0.4)
    plt.plot(selectyear(tmin,year),label='minimum in '+str(year))

    plt.fill_between(days,tmax_recordmin,tmax_recordmax,alpha=0.4)
    plt.plot(selectyear(tmax,year),label='maximum in '+str(year))

    plt.axis(xmin=1,xmax=365)
    plt.legend()
    plt.title(station_code+' daily in year '+str(year))
    
    plt.show()

def get_extreme_data(station_code):
    filename = station_code + '.dly'
    station_dly = Path(filename)
    if not station_dly.is_file():
        urllib.request.urlretrieve('ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/gsn/'+
                                   filename, filename)
    

    tmin = getobs(filename)
    tmax = getobs(filename, 'TMAX')
    fillnans(tmin)
    fillnans(tmax)

    # ignore first year in records as its data might not be completed
    min_year = tmin['date'][0].astype('datetime64[Y]').astype(int) + 1971
    # ignore year 2019 as its data is incompleted
    max_year = tmin['date'][-1].astype('datetime64[Y]').astype(int) + 1969

    years = np.arange(min_year,max_year+1)
    
    # arrange all years in a matrix and ignore extra day in leap years thus it's mis-aligned
    tmin_all = np.vstack([selectyear(tmin,year)[:365] for year in years])
    tmax_all = np.vstack([selectyear(tmax,year)[:365] for year in years])

    # apply mean to array only across rows
    max_mean = np.mean(tmax_all,axis=1)
    min_mean = np.mean(tmin_all,axis=1)

    # get actual year by finding the index of the maximum and minimum value
    warmest = years[np.argmax(max_mean)]
    coldest = years[np.argmin(min_mean)]

    # give a bigger figsize
    plt.figure(figsize=(10,4))
    
    plt.clf()
    
    days = np.arange(1,366)

    # plot shaded area
    plt.fill_between(days,selectyear(tmin,coldest),selectyear(tmax,coldest),alpha=0.4,label=coldest)
    plt.fill_between(days,selectyear(tmin,warmest),selectyear(tmax,warmest),alpha=0.4,label=warmest)

    plt.axis(xmin=1,xmax=365)
    plt.legend()
    plt.title(station_code+' temperature coldest year {} vs. warmest year {}'.format(coldest,warmest))
    
    plt.show()
    
def parsefile(filename):
    # the size of all the fields, 1,1,1 is for the flags not to use
    dly_delimiter = [11,4,2,4] + [5,1,1,1] * 31
    # the columns to keep, year, month, element followed by all the values seleced by list comprehension
    dly_usecols = [1,2,3] + [4*i for i in range(1,32)]
    # the type of all the fields
    dly_dtype = [np.int32,np.int32,(np.str,4)] + [np.int32] * 31
    # the name given to all the fields
    dly_names = ['year','month','obs'] + [str(day) for day in range(1,32)]
    # return numpy record array
    return np.genfromtxt(filename,
                         delimiter=dly_delimiter,
                         usecols=dly_usecols,
                         dtype=dly_dtype,
                         names=dly_names)

# apply transformation into better form
def unroll(record):
    # create a range of dates that correspndes to a row
    startdate = np.datetime64('{}-{:02}'.format(record['year'],record['month']))
    # create a range of dates starting at the start date, end at the start date + 1 month with a step of 1 day
    dates = np.arange(startdate,startdate + np.timedelta64(1,'M'),np.timedelta64(1,'D'))
    # collect date for the days from the record
    rows = [(date,record[str(i+1)]/10) for i,date in enumerate(dates)]
    # return numpy record array
    return np.array(rows,dtype=[('date','M8[D]'),('value','d')])

# select a single observable, take all the months contained in a file and concatenate into a single record array
def getobs(filename,obs='TMIN'):
    # select those contain desired observable, feed to concatenate
    data = np.concatenate([unroll(row) for row in parsefile(filename) if row[2] == obs])
    # use numpy boolean mask to change -999.9 to nan
    data['value'][data['value'] == -999.9] = np.nan
    return data

# replace missing values using values of neighbors
def fillnans(data):
    # convert dates explicitly to float
    dates_float = data['date'].astype(np.float64)
    # return boolean masks of points that are nan
    nan = np.isnan(data['value'])
    # interpolate for points that are not nan
    data['value'][nan] = np.interp(dates_float[nan],dates_float[~nan],data['value'][~nan])

# run a mean over a window centered at the data point
def plot_smoothed(t,label,win=10):
    # multiply the sliding section of one-dimensional array with shorter array
    smoothed = np.correlate(t['value'],np.ones(win)/win,'same')
    # plot the data
    plt.plot(t['date'],smoothed,label=label)

# extract a single year of data
def selectyear(data,year):
    # numpy datetime64 object corresponding start of the year
    start = np.datetime64('{}'.format(year))
    # numpy datetime64 object corresponding end of the year
    end = start + np.timedelta64(1,'Y')
    # build boolean mask combining two conditions
    return data[(data['date'] >= start) & (data['date'] < end)]['value']

# ---------------------------------------------------------------                     


#########################################################################################
# TAB 2 OpenWeatherMap
######################

# create a container frame to hold other widgets
open_weather_cities_frame = ttk.LabelFrame(tab2, text=' Latest Observation for ')
open_weather_cities_frame.grid(column=0, row=0, padx=8, pady=4)

# Station City label
open_location = tk.StringVar()
open_location_label = ttk.Label(open_weather_cities_frame, textvariable=open_location)
open_location_label.grid(column=0, row=2, columnspan=3)

# ---------------------------------------------------------------
# Adding a Label
ttk.Label(open_weather_cities_frame, text="City: ").grid(column=0, row=0) 

# ---------------------------------------------------------------
open_city = tk.StringVar()
open_city_combo = ttk.Combobox(open_weather_cities_frame, width=13, textvariable=open_city)       
open_city_combo['values'] = ('Sherbrooke', 'Montreal', 'Quebec', 'Gatineau', 'Calgary', 'Edmonton', 'Winnipeg',
                             'Toronto', 'Ottawa', 'Hamilton, CA', 'Waterloo, CA', 'London, CA', 'Oshawa', 'Windsor, CA',
                             'Vancouver', 'Victoria, CA', 'Halifax')
open_city_combo.grid(column=1, row=0)
open_city_combo.current(0)                 # highlight first city station id

# ---------------------------------------------------------------
# callback function
def _get_time_open():
    city = open_city_combo.get()
    get_open_weather_time_data(city)

ttk.Button(open_weather_cities_frame,text='Get Time', command=_get_time_open).grid(column=2, row=0)

# Adding a Label
ttk.Label(open_weather_cities_frame, text="Time: ").grid(column=0, row=1)

time = tk.StringVar()
time_combo = ttk.Combobox(open_weather_cities_frame, width=17, textvariable=time)
time_combo.grid(row=1, column=1)

# callback function
def _get_city_open():
    city = open_city_combo.get()
    select_time = time_combo.get()
    get_open_weather_data(select_time, city)

ttk.Button(open_weather_cities_frame,text='Get Forecast', command=_get_city_open).grid(column=2, row=1)
# ---------------------------------------------------------------
for child in open_weather_cities_frame.winfo_children(): 
        child.grid_configure(padx=5, pady=2)   

# ---------------------------------------------------------------
# create a container frame to hold all other widgets
open_weather_conditions_frame = ttk.LabelFrame(tab2, text='Weather Forecast')
open_weather_conditions_frame.grid(column=0, row=1, padx=8, pady=4)

#================
ENTRY_WIDTH = 25
#================

# Add Label & Textbox Entry widgets
#---------------------------------------------
ttk.Label(open_weather_conditions_frame, text="Forecast:").grid(column=0, row=1, sticky='E')         # right-align
open_updated = tk.StringVar()
open_updatedEntry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_updated, state='readonly')
open_updatedEntry.grid(column=1, row=1, sticky='W')
#---------------------------------------------
ttk.Label(open_weather_conditions_frame, text="Weather:").grid(column=0, row=2, sticky='E')
open_weather = tk.StringVar()
open_weatherEntry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_weather, state='readonly')
open_weatherEntry.grid(column=1, row=2, sticky='W')
#---------------------------------------------
ttk.Label(open_weather_conditions_frame, text="Temperature:").grid(column=0, row=3, sticky='E')
open_temp = tk.StringVar()
open_tempEntry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_temp, state='readonly')
open_tempEntry.grid(column=1, row=3, sticky='W')
#---------------------------------------------
ttk.Label(open_weather_conditions_frame, text="Relative Humidity:").grid(column=0, row=5, sticky='E')
open_rel_humi = tk.StringVar()
open_rel_humiEntry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_rel_humi, state='readonly')
open_rel_humiEntry.grid(column=1, row=5, sticky='W')
#---------------------------------------------
ttk.Label(open_weather_conditions_frame, text="Wind:").grid(column=0, row=6, sticky='E')
open_wind = tk.StringVar()
open_windEntry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_wind, state='readonly')
open_windEntry.grid(column=1, row=6, sticky='W')
#---------------------------------------------
ttk.Label(open_weather_conditions_frame, text="Pressure:").grid(column=0, row=8, sticky='E')
open_msl = tk.StringVar()
open_mslEntry = ttk.Entry(open_weather_conditions_frame, width=ENTRY_WIDTH, textvariable=open_msl, state='readonly')
open_mslEntry.grid(column=1, row=8, sticky='W')
#---------------------------------------------

# Add some space around each widget
for child in open_weather_conditions_frame.winfo_children(): 
        child.grid_configure(padx=4, pady=2)    



#########################################################################################
# OpenWeatherMap Data collection

# translate Unix time to regular day time
def unix_to_datetime(unix_time):
    return (datetime.fromtimestamp(int(unix_time))).strftime('%Y-%m-%d %H:%M:%S')
    
def get_open_weather_time_data(city='Sherbrooke'):
    # replace empty spaces with %20
    city = city.replace(' ', '%20')
    # put api key and city into query string and set temperature to celsius
    url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}".format(city, OWM_API_KEY) 
    # open url
    response = urlopen(url)
    # read response decoded
    data = response.read().decode()
    # load data
    json_data = json.loads(data)
    
    time_series = ()
    
    for i in range(38):
        forecast_unix = json_data['list'][i]['dt']
        forecast = unix_to_datetime(forecast_unix)
        time_series = time_series + (forecast,)

    time_combo['values'] = time_series
    time_combo.current(0)


def get_open_weather_data(select_time, city='Sherbrooke'):
    # replace empty spaces with %20
    city = city.replace(' ', '%20')
    # put api key and city into query string and set temperature to celsius
    url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}".format(city, OWM_API_KEY)
    # open url
    response = urlopen(url)
    # read response decoded
    data = response.read().decode()
    # load data
    json_data = json.loads(data)

    # collect data and save into local variables
    city_id = json_data['city']['id']
    city_name = json_data['city']['name']
    city_country = json_data['city']['country']

    data = pd.DataFrame(columns=['forecast', 'humidity', 'pressure', 'temp', 'owm_weather',
                               'weather_icon', 'wind_deg', 'wind_speed_mps'])

    # only extract 38/40 cnts to avoid error
    for i in range(38):
        forecast_unix = json_data['list'][i]['dt']
        humidity = json_data['list'][i]['main']['humidity']
        pressure = json_data['list'][i]['main']['pressure']
        temp = json_data['list'][i]['main']['temp']
        owm_weather = json_data['list'][i]['weather'][0]['description']
        weather_icon = json_data['list'][i]['weather'][0]['icon']
        wind_deg = json_data['list'][i]['wind']['deg']
        wind_speed_mps = json_data['list'][i]['wind']['speed']

        forecast = unix_to_datetime(forecast_unix)
        
        row = {'forecast': forecast, 'humidity': humidity, 'pressure': pressure, 'temp': temp,
               'owm_weather': owm_weather, 'weather_icon': weather_icon, 'wind_deg': wind_deg,
               'wind_speed_mps': wind_speed_mps}
        data = data.append(row, ignore_index=True)

    # -------------------------------------------------------
    # Update GUI entry widgets with live data
    open_location.set('{}, {}'.format(city_name, city_country))

    open_updated.set(select_time)
    open_weather.set(data.loc[data['forecast']==select_time, 'owm_weather'].values[0])
    open_temp.set('{} \xb0C'.format(data.loc[data['forecast']==select_time, 'temp'].values[0]))
    open_rel_humi.set('{} %'.format(data.loc[data['forecast']==select_time, 'humidity'].values[0]))
    open_wind.set('{} degrees at {} MPS'.format(data.loc[data['forecast']==select_time, 'wind_deg'].values[0],
                                                data.loc[data['forecast']==select_time, 'wind_speed_mps'].values[0]))
    open_msl.set('{} hPa'.format(data.loc[data['forecast']==select_time, 'pressure'].values[0]))

    # retrieve weather icons
    url_icon = "http://openweathermap.org/img/w/{}.png".format(data.loc[data['forecast']==select_time, 'weather_icon'].values[0])
    # open url
    ico = urlopen(url_icon)
    # pass into PIL.Image.open and PIL.ImageTK.PhotoImage
    open_im = PIL.Image.open(ico)
    # create a image variable within the label to pass the reference to icon
    open_location_label.open_photo = PIL.ImageTk.PhotoImage(open_im)
    # display the icon and text
    open_location_label.config(image=open_location_label.open_photo, compound='left')
    win.update()        # required or won't see the icon
    
#======================
# Start GUI
#======================
win.mainloop()
