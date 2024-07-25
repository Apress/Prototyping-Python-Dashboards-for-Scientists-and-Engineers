# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 14:08:27 2021

@author: pjhmx
"""
import pandas as pd


import plotly.graph_objects as go
import numpy.polynomial.polynomial as poly
import numpy as np
import math
   
from os import listdir
from os.path import isfile, join


class atads_figures:
    
   def __init__(self):
        self.active_apts = ['PHX']
        self.apt_root_dir='./APT_CSV/'
        self.my_debug='no bug report'
        self.var_dict={}
        self.df = pd.DataFrame()
        self.df_count = 0
        self.df_years_unique = [i for i in range(2000,2024, 1)]
        self.names=[
                          "date", "facility", "state", "region", "ddso", "class", 
                          "ifri_carrier", "ifri_taxi","ifri_general","ifri_mil","ifri_total",
                          "vfri_carrier", "vfri_taxi","vfri_general","vfri_mil","vfri_total",
                          "i_carrier", "i_taxi","i_general","i_mil","i_total",
                          "loc_civ", "loc_mil", "loc_total", 
                          "total_ops",
                          "j1","j2","j3","j4","j5","j6"
                             ]
        self.var_names=[
                           
                          "ifri_carrier", "ifri_taxi","ifri_general","ifri_mil","ifri_total",
                          "vfri_carrier", "vfri_taxi","vfri_general","vfri_mil","vfri_total",
                          "i_carrier", "i_taxi","i_general","i_mil","i_total",
                          "loc_civ", "loc_mil", "loc_total", 
                          "total_ops",
                         "j1","j2","j3","j4","j5","j6"
                             ]
        
        self.var_labels=[
                        "IFR (itin.) Air Carrier",
                        "IFR (itin.) Air Taxi",
                        "IFR (itin.) Gen. Av.",
                        "IFR (itin.) Military",
                        "IFR (itin.) Total",
                        "VFR (itin.) Air Carrier",
                        "VFR (itin.) Air Taxi",
                        "VFR (itin.) Gen. Av.",
                        "VFR (itin.) Military",
                        "VFR (itin.) Total",
                        "(itin.) Air Carrier",
                        "(itin.) Air Taxi",
                        "(itin.) Gen. Av.",
                        "(itin.) Military",
                        "(itin.) Total",
                        "(local) Civilian",
                        "(local) Military",
                        "(local) Total",
                        "Total Ops."
                        ]
        self.make_var_dict()
#
# Build the list of available airports from the files in directory APT
#        
        self.df_airport_unique=[]
	
	# list APT directory files
        self.apt_files = [f for f in listdir('./APT_CSV') if isfile(join('./APT_CSV', f))]
        
	# trim names to remove '.csv'
        for f in self.apt_files:
            first_chars = f[0:3]
            self.df_airport_unique.append(first_chars)
        self.df_airport_unique.sort()


        self.get_airport_data(['PHX'],{2021})


   def make_var_dict(self):
       keys_list = self.var_names
       values_list = self.var_labels
       zip_iterator = zip(keys_list, values_list)
       self.var_dict = dict(zip_iterator)
       
           
           

#
# Ghetto solution to make sure all airports are current by 
# refreshing the list completely for the requested airports and years
#
   def get_airport_data(self,apt_list, yr_list):
       self.df_yr_list = yr_list
       self.df_active_apts=[]
       first = True
       for i in apt_list:
              self.read_apt(i, yr_list)
              if first:
                  #self.df_active_apts = apt_list       
                  self.df_active_apts = i       
                  self.df = self.df_new
                  first = False
              else:                 
                  #self.df = self.df.append(self.df_new, ignore_index = True)
                  self.df = pd.concat([self.df,self.df_new])
                  
       #self.data_cleanup()
       

       
      
           
   
        
#
# Read in an airport, only keep requested years, and add required columns
#  
   def read_apt(self,apt, yr_list):           
        filename=self.apt_root_dir+apt+'.csv'       
            

        self.df_new = pd.read_csv(filename,header=None,
                                      names=self.names, delimiter=',')
                                  
        self.df_new['date'] = pd.to_datetime(self.df_new['date'])
        self.df_new['daynum'] = self.df_new['date'].dt.dayofyear
        self.df_new['wdaynum'] = self.df_new['date'].dt.dayofweek
        self.df_new['month'] = self.df_new['date'].dt.month
        self.df_new['year'] = self.df_new['date'].dt.year
        self.df_new['ymd'] = pd.to_datetime(self.df_new['date']).dt.strftime('%m/%d/%Y')
        self.df_new['ydecimal']=self.df_new['year']+self.df_new['daynum']/365.25    
        self.df_new.sort_values(by = 'ydecimal')
 
        # only keep years in yr_list
        
        self.df_new = self.df_new[self.df_new['year'].isin(yr_list)]
        self.df_new = self.df_new.replace(',','', regex=True)
        self.df_new = self.df_new.apply(pd.to_numeric, errors='ignore')
        

    

  
       
   def add_airport_trace(self,apt,active_variable)  :
       self.fig_main.add_trace(go.Scatter(name=apt,       #add airport trace
                            x=self.df_fac['ydecimal'],
                            y=self.df_fac[active_variable],
                            connectgaps = False,
                            text=self.df_fac['ymd'],
                            hovertemplate=
                            "<b>%{text}</b><br><br>" + 
                           " %{y}<br>" +
                            "<extra></extra>"
                            ))
 
   def get_poly(self,apt,poly_order,year_min,year_max,active_variable):
       p = int(poly_order)    
       coefs = poly.polyfit(self.df_vals['ydecimal'].values, self.df_vals[active_variable].values,p)       
       return coefs
   
    
   def draw_poly(self,apt,coefs):
       ffit  = poly.polyval(self.df_vals['ydecimal'], coefs)
       self.fig_main.add_trace(go.Scatter(name=apt,
         x=self.df_vals['ydecimal'],
         y=ffit))  
  
    
            
   def get_poly1(self,apt,poly_order,year_min,year_max,active_variable):
       p = int(poly_order)
       x = np.linspace(2000, 3000, 1000)
       y = 4 + 2*x + 7*x*x
       coefs = poly.polyfit(x, y,p)    
       ffit  = poly.polyval(x, coefs)

        
       self.fig_main.add_trace(go.Scatter(name=apt,
         x=self.df_vals['ydecimal'],
         y=ffit))  
       return coefs
   
    
       
   def add_smooth_trace(self,apt,smoothing,active_variable):
       window=int(smoothing)
       self.df_fac['smth'] = self.df_fac[active_variable].rolling(window).mean()
       self.df_fac['smth'] = self.df_fac['smth'].shift(-window//2 )
       self.fig_main.add_trace(go.Scatter(name=apt,
       x=self.df_fac['ydecimal'],
       y=self.df_fac['smth']))  
  

    

    
   def year_block_colors(self,year_min, year_max):
            for y in range(int(year_min),int(year_max)):
                if (y % 2) == 0:
                       self.fig_main.add_vrect(
                            x0=y, 
                            x1=y+1, 
                            row="all", 
                            col=1,
                            fillcolor="mistyrose", 
                            opacity=0.4, 
                            line_width=0)    
                       
                       
   def add_black_border(self,fig):
            # add black border - do before year_block_colors()
            fig.update_layout(shapes=[go.layout.Shape(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0.,
                y0=0.,
                x1=1.0,
                y1=1.0,
                opacity=.4,
                line={'width': 1, 'color': 'black'}
            )])
  
   def add_watermark(self,fig,wstr):
       fig.add_annotation(
                xref="paper",yref="paper",
                x=0, y=0,
                text=wstr,
                font=dict(
                family="sans serif",
                size=10,
                color="LightSlateGray"
                ),
                showarrow=False,
                yshift=10)               
       
       
   def add_titles(self,figure, title_str,active_variable):
        figure.update_layout(
        title=title_str,
        font=dict(
            family="sans serif",
            size=14,
            color="Blue"
            ),
        xaxis_title="Years",
        yaxis_title=active_variable,
        legend_title="Airport",              
    )
        

   def add_eqn_str(self):
       self.fig_main.add_annotation(
                text=self.eqn,
                xref="paper",yref="paper",
                x= 0, y=1.1,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Black"
                    ),
                showarrow=False
                )
        

   def get_apt_linear_equation_string(self,apt,c,year_min):
    c00 = c[0] + year_min*c[1]
    c11 = c[1]
    

    a00 = "{:.1f}".format(c00)
    a11 = "{:.1f}".format(c11)
    
    apt_str = " [" +apt +": Ops = "
    if c11 < 0:
        sign11 = ' - '
        a11="{:.4f}".format(-c11)
       # eqn_str = eqn_str + ' + '+ c11 + ' * t ]  '
    else:
        sign11 = ' + '
      
    #eqn_str = eqn_str + ' - '+ a1_0 +' * t ]  '
    apt_str = apt_str + a00 + sign11 +a11 + ' * t ] '   
    return apt_str
    


   def get_apt_quadratic_equation_string(self,apt,c,year_min):
        apt_str = " [" +apt +": Ops = "
        t0 = year_min
        c00 = c[0] + c[1]*t0 + c[2]*t0*t0
        c11 = c[1] + 2*c[2]*t0
        c22 = c[2]
        
        a00="{:.1f}".format(c00) 
        a11="{:.1f}".format(c11)
        a22="{:.1f}".format(c22)
        
        if c11 < 0:
            sign11 = ' - '
            a11="{:.1f}".format(-c11)
        else: 
            sign11 = ' + '
        
        if c22 < 0:
            sign22 = ' - '
            a22="{:.1f}".format(-c22)
        else:
            sign22 = ' + '
        
        
        apt_str = apt_str + a00 + sign11 +a11 + ' * t ' + sign22 + a22 + ' * t * t ] '
        return apt_str

   def get_scales(self,apt,y0,y1,active_variable):
        window=9
        self.df_fac['s09'] = self.df_fac[active_variable].rolling(window).mean()
        self.df_fac['s09'] = self.df_fac['s09'].shift(-window//2)
        window=31
        self.df_fac['s31'] = self.df_fac[active_variable].rolling(window).mean()
        self.df_fac['s31'] = self.df_fac['s31'].shift(-window//2)
        
        stdv09 = (self.df_fac[active_variable] - self.df_fac['s09']).std()
        stdv31 = (self.df_fac['s31']).std()
        str09 = "{:.1f}".format(stdv09)
        str31 = "{:.1f}".format(stdv31)
        stat_str = " [" +apt +": STDV09= " + str09 + '  STDV31= '  + str31 + ']'
        
        return stat_str
    
# =============================================================================
# Build the main scatter (time-series) chart                
# =============================================================================
   def update_mainchart(self,airport_list, yr_list, active_variable, smoothing,show_raw,show_poly,show_scales):
            
            var_str = self.var_dict.get(active_variable)
            eqn_str=""
            
            title_str0=':'.join(airport_list)
            title_str0 = title_str0 + ' ['+ var_str+']'+" Traffic by Year "
            
            year_min = float(min(yr_list))
            year_max = float(max(yr_list)+1.)

            self.fig_main = go.Figure()                      
            j = 0
            for i in airport_list: 
                    j = j+1
                    self.eqn=""
                    self.df_fac = self.df[self.df['facility'].isin({i})]
                                                
                    if show_raw == '1':
                        self.add_airport_trace(i,active_variable)                           
  
                    if smoothing != '0':                           
                        self.add_smooth_trace(i, smoothing,active_variable)
                                 
                    #
                    # Add polynomial fit for all available years
                    # Only for first 2 airports - to reduce clutter
                    #
                    if show_poly != '0' and j < 3:
                        self.df_vals = self.df_fac[self.df_fac['ydecimal'].between(year_min, year_max)]                                                

                        p = int(show_poly)                       
                        coefs = self.get_poly(i,p,year_min,year_max,active_variable)
                        
                        self.draw_poly(i,coefs)
                        
                        if p == 1:
                            eqn_str = eqn_str + self.get_apt_linear_equation_string(i,coefs,year_min)
                                                    
                        if p == 2:
                            eqn_str = eqn_str + self.get_apt_quadratic_equation_string(i,coefs,year_min)
                            
                        self.eqn = self.eqn + eqn_str
                        
                    if show_scales == '1':   
                        eqn_str = eqn_str + self.get_scales(i,year_min, year_max,active_variable)               
                        self.eqn = self.eqn + eqn_str
                        
            self.add_eqn_str()
                   
            self.add_watermark(self.fig_main,'[AVOPSinsight.com]')                
            self.fig_main.update(layout_xaxis_range = [year_min,year_max])
            self.add_titles(self.fig_main,title_str0,active_variable)
            self.add_black_border(self.fig_main)
            self.year_block_colors(year_min, year_max)   
            self.fig_main.update_layout(
                hovermode='x unified')        


   def update_mchart(self,airport_list, yr_list, active_variable):
        title_str0=':'.join(airport_list)
     
        self.fig_monthly = go.Figure()
      
        year_max = [max(yr_list)]
        year_str = str(year_max[0])+':'
        var_str = self.var_dict.get(active_variable)
        for i in airport_list:
                self.df_fac = self.df[self.df['facility'].isin({i})]           
                
                df_fac_yr = self.df_fac[self.df_fac['year'].isin(year_max)]
                self.fig_monthly.add_trace(go.Box(name=i+':'+str(year_max),
                        x=df_fac_yr['month'],
                        y=df_fac_yr[active_variable]))
              
        self.add_watermark(self.fig_monthly,'[AVOPSinsight.com]')
        self.add_black_border(self.fig_monthly)


        self.fig_monthly.update_layout(
            xaxis = dict(
            tickmode = 'array',
            tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ticktext = ['J','F', 'M', 'A', 'M', 'J','J','A','S','O','N','D']))
     
        self.fig_monthly.add_annotation(
            text=year_str+title_str0+" [Traffic by month]: " + var_str,
            xref="paper",yref="paper",
            x= 0, y=1.1,
            font=dict(
                family="sans serif",
                size=12,
                color="Black"
                ),
            showarrow=False)
          
        self.fig_monthly.update_layout(hovermode='x unified', boxmode='group') 
        
        
   def update_wchart(self,airport_list, yr_list, active_variable):
        title_str0=':'.join(airport_list)
        self.fig_weekly = go.Figure()
             
        year_max = [max(yr_list)]
        year_str = str(year_max[0])+':'
        var_str = self.var_dict.get(active_variable)
        for i in airport_list:
            self.df_fac = self.df[self.df['facility'].isin({i})]
            df_fac_yr = self.df_fac[self.df_fac['year'].isin(year_max)]
            
            window = 21
            df_fac = df_fac_yr[active_variable]
            df_fac_smth = df_fac.rolling(window).mean()
            df_fac_smth = df_fac_smth.shift(-window//2)
            df_diff = df_fac - df_fac_smth
            self.fig_weekly.add_trace(go.Box(name=i+':'+str(year_max),
                x=df_fac_yr['wdaynum'],
                y = df_diff
                ))


        self.fig_weekly.update_layout(
            xaxis = dict(
            tickmode = 'array',
            tickvals = [0, 1, 2, 3, 4, 5, 6],
            ticktext = ['M','Tu', 'W', 'Th', 'F', 'Sa','Su']))
        self.add_watermark(self.fig_weekly,'[AVOPSinsight.com]')

        self.fig_weekly.add_annotation(
            text=year_str+title_str0+" [Deviations by weekday]: "+var_str,
            xref="paper",yref="paper",
            x=0, y=1.1,
            font=dict(
                family="sans serif",
                size=12,
                color="Black"
                ),
            showarrow=False )
     
        self.fig_weekly.update_xaxes(nticks=7)
        self.add_black_border(self.fig_weekly)            
        self.fig_weekly.update_layout(hovermode='x unified',boxmode='group')
        


   def build_oshkosh_model(self,a1, a2):
        yf = [0]*364
        for i in range(175,182):
            yf[i] = a2
        
        yf = yf*5
        
        yb = [a1]*7
        yb = yb*52
        
        for i in range(0,364):
            yb[i] = yb[i]*math.sin(3.14*i/364)
            
        yb = yb*5
        
        y_osh = []
        for i in range(1820):
            y_osh.append(yf[i] + yb[i])
            
        return y_osh
    
                   
   def update_spectrum(self,airport_list, yr_list, active_variable):
        title_str0=':'.join(airport_list)
        self.fig_spectrum = go.Figure()
        var_str = self.var_dict.get(active_variable)
        for i in airport_list:
            
                y0 = self.df[self.df['facility'].isin({i})]
                y0 = y0[active_variable] - y0[active_variable].mean()
                y_vals = y0                             # set the input array for FFT
                y_vals = self.build_oshkosh_model(100,150)
                
                a_vals = np.abs(np.fft.fft(y_vals))     # get the FFT amplitude array a_vals[]
                
                N = len(y_vals)                         # set scaling parameters and arrays
                n = np.arange(N)
                T = N
                freq = n/T
                n_oneside = N//2
                
                fq_list = freq[:n_oneside]              # build list of frequencies
                a_vals = a_vals[:n_oneside]/n_oneside   # rescale amplitudes
                a_vals = a_vals /a_vals.max()           # Normalize to [0,1]
                
                fq_list[0] = 0.000001                   # avoid divide by zero     
                self.p_vals = np.reciprocal(fq_list)    # build array of periodicities

                self.fig_spectrum.add_trace(go.Scatter(name=i,
                    x=fq_list,
                    y=a_vals,
                    text=fq_list,
                    customdata = self.p_vals,
                      hovertemplate=
                      "Freq.: <b>%{text:0.3f}</b><br>" + 
                      "Period (days): <b>%{customdata:0.1f}</b>" +
                      "<extra></extra>"
                    ) )       
               
                self.add_watermark(self.fig_spectrum,'[AVOPSinsight.com]')
                
                self.add_black_border(self.fig_spectrum)
                self.fig_spectrum.update_layout(
                    title=title_str0+ ' '+ var_str+" Spectrum (Detected Usage Patterns)",
                    xaxis_title="Freq (1/day)",
                    yaxis_title=active_variable,
                    legend_title="Airport",
                    )
                
   def update_spectrum2(self,airport_list, yr_list, active_variable):
        title_str0=':'.join(airport_list)
        self.fig_spectrum = go.Figure()
        self.df3 = self.df
        var_str = self.var_dict.get(active_variable)

        for i in airport_list:
                df_fac4 = self.df3[self.df3['facility'].isin({i})]
                df_flat = df_fac4[active_variable] - df_fac4[active_variable].mean()
                
                yf = np.abs(np.fft.fft(df_flat))
                N = len(df_flat)
                n = np.arange(N)
                T = N
                freq = n/T
                n_oneside = N//2
                freq1 = freq[:n_oneside]
                yf1 =yf[:n_oneside]/n_oneside
                yf1 = yf1 /yf1.max()
                
                freq1[0] = 0.000001        #avoid divide by zero     
                self.p_vals = np.reciprocal(freq1)
                self.p_vals[0] = 1000000.
            
                self.fig_spectrum.add_trace(go.Scatter(name=i,
                    x=freq1,
                    y=yf1,
                    text=freq1,
                    customdata = self.p_vals,
                      hovertemplate=
                      "Freq.: <b>%{text:0.3f}</b><br>" + 
                      "Period (days): <b>%{customdata:0.1f}</b>" +
                      "<extra></extra>"
                    ) )       
               
                self.add_watermark(self.fig_spectrum,'[AVOPSinsight.com]')
                
                self.add_black_border(self.fig_spectrum)
                self.fig_spectrum.update_layout(
                    title=title_str0+ ' '+ var_str+" Spectrum (Detected Usage Patterns)",
                    xaxis_title="Freq (1/day)",
                    yaxis_title=active_variable,
                    legend_title="Airport",
                    )              