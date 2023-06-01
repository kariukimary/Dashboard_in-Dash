#in dash we have important categories such as dash core components which includes radio buttons,sliders,checkbox etc
#the other one is plotly where you can plot various types of graphs
#lastly  is the callback which connects the dash core components and the plots inorder to create an interactive capability

#import libraries
import pandas as pd
from dash import Dash,html,dcc,callback,Input,Output
import plotly.express as px

#intialize the app
app=Dash(__name__)


#loading the data
df=pd.read_csv("insurance.csv")

#selecting and calculating the mean
df=df.groupby(["age","bmi","region","sex","smoker","children"])[["charges"]].mean()
df.reset_index(inplace=True)
print(df[:5])

#app layout
#the first div id=s for the input and the other div is for output
#both division are supossed to be inside the main div
#whatever goes inside the app layout is the dash core components like dropdowns,html title and the graphs
app.layout=html.Div([html.H1("Web Application Dashboard With Dash",style={'text-align':'center'}),
                     html.Label('Dropdown'),
                     dcc.Dropdown(['0','1','2'],
                                  id='select_number_children',
                                  multi=False,
                                  value=1),
        
                
            #html.Div(id="output_container",children=[]),
            html.Br(),
            #we put a break so as to have the space between the graph and the divs above
            #the graph below is an empty graph 
            dcc.Graph(id="my_insurance_map", figure={})
                     ])
#connect the plotly graoh with the dash components using callbacks
@callback(
   # [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_insurance_map',component_property='figure'),
     Input(component_id='select_number_children',component_property='value'),
)
#the callback function where the arguments for the function refers to the component property of the input
#if we have one input we will only use one argument if there are two arguments we will use the two arguments inside the function
def update_graph(option_select):
    print(option_select)
    print(type(option_select))
    
    #container="the number of children selected was: {}" .format(option_select)
    
    
    dff=df.copy()
    filtered_df=dff[dff.children==option_select]
    #dff=dff[dff["children"]== option_select]
    #dff=dff[dff["region"]=='southeast']
    
    #plotly express
    #the scope and the locationmode are already defined, for scope it can be africa,europe amomg others and the locationmode can be usa,iso3 etc
    #fig=px.scatter(
        #data_frame=dff,
        #color='charges',
        #labels={'charges': '% of charges on medical'},
       # template='plotly_dark',
        #hover_data=['region','charges'],
        #color_continuous_scale=px.colors.sequential.YlOrRd,
        #scope='africa',
        #locations='bmi',
        #locationmode='USA-states'
    #)
    fig=px.scatter(filtered_df,x="bmi",y="age",size="bmi",color="charges",
                   hover_name="region",log_x=True,size_max=20)
    return fig

if __name__=="__main__":
    app.run_server(debug=True)