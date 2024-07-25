
import dash
from dash.dependencies import Input, Output
from atads_layout import  atads_layout
from atads_figures import atads_figures
from dash import html  

app = dash.Dash(__name__)
my_figs   = atads_figures()
my_layout = atads_layout()

def configure_settings():
    return html.Div(
        className="parameter_selections",
        children=
        [                                               
          my_layout.dropdown_airports(my_figs.df_airport_unique),    
          my_layout.dropdown_use_variable(my_figs.var_dict),
          html.Br(),
          my_layout.select_years(my_figs.df_years_unique),
          html.Label('Smoothing...'),                  
          my_layout.radio_smoothing(),     
          html.Br(),
          html.Label('Show Raw Plot...'),                
          my_layout.radio_show_raw(),
          html.Br(),
          html.Label('Polynomial'),                               
          my_layout.radio_show_poly(),
          html.Br(),
          html.Label('Show Weekly and Seasonal Scales'),                               
          my_layout.radio_show_scales()                  
      ])

app.layout = html.Div(              
            className="content",
            children=[  
            configure_settings(),
            my_layout.chart(),   
            my_layout.instructions(),
            my_layout.banner(),
            my_layout.mchart(),
            my_layout.wchart(),
            my_layout.spectrum_instructions(),
            my_layout.spectrum_chart()                                                          
            ])
                               
@app.callback(
    Output("mchart",        "figure"),
    Output("wchart",        "figure"),
    Output("scatter_plot",  "figure"),
    Output("spectrum",      "figure"),
    Input("airports",       "value"),
    Input("years",          "value"),
    Input("use_variable",   "value"),
    Input("smoothing",      "value"),
    Input("show_raw",       "value"),
    Input("show_poly",      "value"),
    Input("show_scales",      "value")
    )
def update_dashboard(airport_list, yr_list, active_variable, smoothing,show_raw,show_poly,show_scales):
    my_figs.get_airport_data(airport_list,yr_list)
    my_figs.update_wchart(airport_list, yr_list, active_variable)
    my_figs.update_mchart(airport_list, yr_list, active_variable)
    my_figs.update_mainchart(airport_list, yr_list, active_variable, smoothing,show_raw,show_poly,show_scales)  
    my_figs.update_spectrum(airport_list, yr_list, active_variable)
    return  my_figs.fig_monthly, my_figs.fig_weekly, my_figs.fig_main, my_figs.fig_spectrum
      
if __name__ == "__main__":
    app.run(host='0.0.0.0')
