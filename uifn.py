import base64
import io

from dash import dash_table
from dash import dcc,callback_context
from dash import html
import dash_daq as daq
from collections import OrderedDict

import re


def UI_orderedList(itm_list):
    div=html.Div([
            html.Ol(children=[html.Li(i) for i in itm_list])
        ])
    return div


#PDF to data table
def UI_PDFtoTable(data_df,height='300px'):
    div=dash_table.DataTable(
        data=data_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in data_df.columns],
        style_cell={'textAlign': 'left','height':'auto','whiteSpace': 'normal'},
        style_header={
        'backgroundColor': '#8febb5',
        'fontWeight': 'bold'
        },
        #page_size=2,
        style_table={'height': height, 'overflowY': 'auto'},#enable scroll
        # style_table={'height': '300px'},#enable scroll
        # style_table={
        #     'minHeight': '600px', 'height': '600px', 'maxHeight': '600px',
        #     'minWidth': '900px', 'width': '900px', 'maxWidth': '900px'
        # },
        # fixed_rows={'headers': True}
        )
    return div

def UI_PDFtoTableSelectable(data_df,table_id,height='300px'):
    div=dash_table.DataTable(
        id=table_id,
        data=data_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in data_df.columns],
        style_cell={'textAlign': 'left','height':'auto','whiteSpace': 'normal'},
        style_header={
        'backgroundColor': '#8febb5',
        'fontWeight': 'bold'
        },
        #page_size=2,
        style_table={'height': height, 'overflowY': 'auto'},#enable scroll
        row_selectable='single',
        selected_rows=[],
                # style_table={'height': '300px'},#enable scroll
        # style_table={
        #     'minHeight': '600px', 'height': '600px', 'maxHeight': '600px',
        #     'minWidth': '900px', 'width': '900px', 'maxWidth': '900px'
        # },
        # fixed_rows={'headers': True}
        )
    return div

def UI_dropdown(dropdown_id,option_list,styleDict={},defaultValue=None):
    div=dcc.Dropdown(
        id=dropdown_id,
        options=[
            {'label': i, 'value': i} for i in option_list
        ],
        value=defaultValue,
        style=styleDict)

    return div

def UI_multidropdown(dropdown_id,option_list,styleDict={}):
    div=dcc.Dropdown(
        id=dropdown_id,
        options=[
            {'label': i, 'value': i} for i in option_list
        ],
        style=styleDict,
        multi=True,
        value=option_list,
        )

    return div

def UI_multidropdown_empty(dropdown_id,option_list,styleDict={}):
    div=dcc.Dropdown(
        id=dropdown_id,
        options=[
            {'label': i, 'value': i} for i in option_list
        ],
        style=styleDict,
        multi=True,
        # value=option_list,
        )

    return div


#template download
# html.Div([
#     html.A('Download template',id='btn-template1',style={'font-style':'italic','textAlign': 'center'}),
#     dcc.Download(id='download-template1')
# ]),

def UI_fileUpload(upload_id):
    #upload file
    div=html.Div([
    html.P('Please upload csv file below to start',style={'font-style':'italic'}),
    dcc.Upload(
        id=upload_id,
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File')
        ]),
        style={
            'width': '98%',
            'height': '80px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    ])
    return div

#pdf to CSV
def UI_fileDownload(button_id,download_id,user_msg):
    div=html.Div([
    html.A(user_msg,id=button_id,style={'font-style':'italic','textAlign': 'left'}),
    dcc.Download(id=download_id)
    ])
    return div
# @app.callback(
#     Output("download-dataframe-csv", "data"),
#     Input("btn_csv", "n_clicks"),
#     prevent_initial_call=True,
# )
# def func(n_clicks):
#     return dcc.send_data_frame(df.to_csv, "mydf.csv")

#DF.to_json()
#pd.read_json(DF)

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        df=pd.DataFrame()

    return df

#DataTable with Per-Row Dropdowns
# def UI_table_dropdown(table_id,data):
def UI_table_dropdown(table_id,data):
    # table_id='test'
    # data={'Cname1':['1','2','3'],'Cname2':['11','22','33']}
    column_name_list=data.keys()

    L=[]
    for name in data:
        option_list=data[name]
        dict={'if': {'column_id': 'Value','filter_query': '{Column_name} eq '+name},'options': [{'label': str(i), 'value': str(i)}for i in option_list]}
        L.append(dict)


    df_per_row_dropdown = pd.DataFrame(OrderedDict([
        ('Column_name', column_name_list),
        # ('Value', ['213', '3213', '1232']),
    ]))

    div=html.Div([

    dash_table.DataTable(
        id=table_id,
        data=df_per_row_dropdown.to_dict('records'),
        columns=[
            {'id': 'Column_name', 'name': 'Column name'},
            {'id': 'Value', 'name': 'Value', 'presentation': 'dropdown'},
        ],
        editable=True,
        dropdown_conditional=L
    ),
])


    return div
