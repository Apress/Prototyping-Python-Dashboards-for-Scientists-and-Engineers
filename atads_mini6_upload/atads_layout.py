# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 20:37:55 2021

@author: pjhmx
"""


from dash import dcc
from dash import html
    
class atads_layout:
    """ A class to support adding plotly dash html elements"""
    
    def __init__(self):
        #self.app = ap
        self.overlap = 0

            
            
    def logo(self):
        return html.Div(
                    className='logo',
                    children=[
                    html.H2("AVOPSinsight.com"),
                    ])
    
    def banner(self):
        return      html.Div(
                    className="banner",
                    children=[     
                    html.H1("Airport Operations Display Module "),
                    html.P("This module can be used to explore airport \
                           activity as reported by the FAA's ATADS database."),
                     ])
                           
    def instructions(self):
        return         html.Div(
            className="instructions",
            children=[
                html.P("Use the Airport drop-down menu to find the airport(s) of interest."),
                html.P("Use the Variable menu to select the parameter of interest. "),
                html.P("Explore trends and reduce clutter using the polynomial \
                            smoothing options"),
                html.P("Use the mouse and scroll button to explore the charts \
                       with the Zoom, Pan, and Download buttons etc. "),
                html.P("The Weekly and Seasonal scales are the standard deviations of\
                       short period and long period fluctuations called\
                           stdv09 and stdv31, since they are based on 9-day\
                               and 31-day smoothing filters.")
                
                ])
      
    def spectrum_instructions(self):
        return         html.Div(
            className="spectrum_instructions",
            children=[
                html.P("The spectrum of a time series can show cyclical usage patterns."),
                html.P("A weekly pattern would have a frequency of f = 1/7 = 0.14 per day"),
                html.P("and a period P = 7 days"),
                html.P("Annual airshows (e.g. OSH) show strong signals near P = 360 days"),
                html.P("Use the mouse to explore the chart."),
                html.P("The plots have been scaled to lie in [0,1]."),
                html.Br(),                
                ])
    
    
    def mchart(self):
        return             html.Div( 
                className="monthly_chart",
                children=[                            
                dcc.Graph(id="mchart"),
            ]) 
    
    def wchart(self):
        return             html.Div( 
                className="weekly_chart",
                children=[                            
                dcc.Graph(id="wchart"),
            ]) 
    
        
    def chart(self):
        return  html.Div( 
                className="chart",
                children=[                            
                dcc.Graph(id="scatter_plot"),
            ])

    def spectrum_chart(self):
        return  html.Div( 
                className="spectrum_chart",
                children=[                            
                dcc.Graph(id="spectrum"),
            ])    
   


    def dropdown_airports(self,df_airport_unique):
        return dcc.Dropdown(id='airports', options=[
                    {'label': i, 'value': i} for i in df_airport_unique
                  ], multi=True, value=["PHX"],placeholder='Filter by airport...')
    
    def dropdown_use_variable(self,var_dict):
        return    dcc.Dropdown(id='use_variable', 
                        options=[
                        {'label':var_dict[i], 'value':i} for i in var_dict

                 ], multi=False, value="i_carrier",placeholder='Filter by variable...')
    

 
    
    def year_range(self):
        return dcc.RangeSlider(
                    id='year_range',
                    min=1990, max=2023,  step=1,
                    marks={
                        1990: '1990',
                        2000: '2000',
                        2010: '2010',
                        2015: '2015',
                        2020: '2020'                 
                        },
                    #vertical=True,
                    value=[2006, 2023] )                 # end user_selections
    
    def select_years(self,df_years_unique):
        return dcc.Checklist(id='years', options=[
                    {'label': i, 'value': i} for i in df_years_unique
                     
                  ],inline=True, value=[2023])       


    def radio_smoothing(self):
         return   dcc.RadioItems(id='smoothing',
                        options=[
                            {'label': 'None', 'value': '0'},
                            {'label': '7 day', 'value': '7'},
                            {'label': '10 day', 'value': '10'},
                            {'label': '30 day', 'value': '30'}
                        ],
                        value='0',
                        labelStyle={'display': 'inline-block'}
                    )
     
        
    def radio_overlap(self):
          return   dcc.RadioItems(id='overlap',
                        options=[
                            {'label': 'Yes', 'value': 1},
                            {'label': 'No', 'value': 0}                          
                        ],
                        value=0,
                        labelStyle={'display': 'inline-block'}
                    ) 
     
        
        
    def radio_show_raw(self):
            return  dcc.RadioItems(id='show_raw',
                    options=[
                        {'label': 'Yes', 'value': '1'},
                        {'label': 'No', 'value': '0'},
    
                    ],
                    value='1',
                    labelStyle={'display': 'inline-block'}
                )
        
        
    def radio_show_poly(self):
        return      dcc.RadioItems(id='show_poly',
                    options=[
                        {'label': 'None', 'value': '0'},
                        {'label': 'Linear', 'value': '1'},
                        {'label': 'Quadratic', 'value': '2'}
                     
                    ],
                    value='0',
                    labelStyle={'display': 'inline-block'}
                )
    

    def radio_show_scales(self):
          return      dcc.RadioItems(id='show_scales',
                      options=[
                          {'label': 'No', 'value': '0'},
                          {'label': 'Yes', 'value': '1'}
                       
                      ],
                      value='0',
                      labelStyle={'display': 'inline-block'}
                  )      

                               
                           
