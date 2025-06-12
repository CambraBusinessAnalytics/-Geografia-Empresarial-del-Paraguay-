import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import json

# Inicialización de la app (si es standalone, si estás usando multipágina no la dupliques)
dash.register_page(__name__, path="/")

df = pd.read_csv('empresas.csv', encoding='utf-8')

df['Ganancias'] = df['Ganancias'] * 10
#df['Ganancias'] = df['Ganancias'].astype(float).round(0).astype(int)
#df['Ganancias'] = df['Ganancias'].fillna(0)


with open("assets/DEPARTAMENTOS_PY_CNPV2022.geojson", encoding='utf-8') as f:
    geojson_data = json.load(f)

layout = html.Div([
    html.H2("Análisis de características económicas del Paraguay", style={
        'font-family': 'Avenir, sans-serif',
        'text-align': 'center',
        'color': 'black',
        'margin-top': '20px'}),
    
    html.P("Selecciona una opción para visualizar los datos.", style={'text-align': 'center'}),

    html.Hr(),

    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.RadioItems(
                    id='radio',
                    options=[
                        {'label': 'Cantidad de Empresas', 'value': 'Cantidad'},
                        {'label': 'Ganancia de Empresas', 'value': 'Ganancias'}],
                    value='Cantidad',
                    inline=True
                ),
                dcc.Graph(
                    id='plot-paraguay',
                    style={'height': '800px', 'width': '100%'},
                    config={'scrollZoom': False}),
            ], width=10)
        ], justify="center"),


        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='table1a',
                    style_table={
                        'maxWidth': '100%',
                        'overflowX': 'auto',
                        'margin': 'auto'
                    },
                    style_cell={'textAlign': 'center'},
                )
            ], xs=10, md=5),

            dbc.Col([
                dash_table.DataTable(
                    id='table2a',
                    style_table={
                        'maxWidth': '100%',
                        'overflowX': 'auto',
                        'margin': 'auto'
                    },
                    style_cell={
                        'textAlign': 'center',
                        'fontSize': '14px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                    style_data={
                        'whiteSpace': 'normal',
                        'lineHeight': '15px',
                    }
                )
            ], xs=10, md=5),
        ],justify="center", style={'marginTop': '20px'}),
    ], fluid=True),

    html.Hr(),

    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("Panorama Económico del Paraguay", style={
                        'font-family': 'Avenir, sans-serif',
                        'text-align': 'center',
                        'color': 'black',
                        'margin-top': '20px'}),
                    
                    html.P('''
Este análisis se basa en los registros disponibles de empresas que tributan el Impuesto a la Renta Empresarial (IRE), el cual grava las ganancias con una tasa del 10%. Según estos registros, se contabilizan un total de 188.900 empresas. Es importante destacar que esta cifra no representa la cantidad total de empresas existentes en el país, sino únicamente aquellas que se encuentran registradas como contribuyentes del IRE.
                    '''),
                    
                    html.P('''
A partir de esta base, se observa que el aporte total en concepto de IRE fue de 5.368.267.792.613 guaraníes, lo que implica que las empresas declararon, en conjunto, aproximadamente 53.682.677.926.130 guaraníes en ganancias durante el periodo considerado.     
                    '''),
                    html.P('''
En términos poblacionales, los distritos que figuran en los datos de Hacienda utilizados para este análisis suman un total de 6.019.352 habitantes, según los datos del Censo Nacional 2022. Esta cifra se aproxima bastante al total nacional reportado por el Instituto Nacional de Estadística (INE) para ese mismo año, que fue de 6.109.903 habitantes.
                    '''),

                    html.Hr(),

                    html.H3("Desigualdad en la Generación de Rentas", style={
                        'font-family': 'Avenir, sans-serif',
                        'text-align': 'center',
                        'color': 'black',
                        'margin-top': '20px'}),

                    html.P('Los datos analizados reflejan una fuerte concentración en la generación de rentas. Al segmentar a las empresas en deciles según su aporte, se observa que:'),
                    
                    html.Ul([
                        html.Li('El 10% superior concentra el 96,33% de las ganancias declaradas.'),
                        html.Li('El 1% superior de las empresas aporta el 72.15% del total.')
                    ]),

                    html.P('Esto evidencia una estructura económica profundamente desigual, donde una pequeña fracción de las empresas genera la casi totalidad de las utilidades.'),

                    html.Div([
                        html.H5("Distribución de Ganancias por Decil:", style={
                            'font-family': 'Avenir, sans-serif',
                            'text-align': 'center',
                            'color': 'black',
                            'margin-top': '20px'}),

                        html.Div([
                            html.Table([
                                html.Thead(html.Tr([html.Th(f"D{i+1}", style={'border': '1px solid black', 'padding': '8px'}) for i in range(10)])),
                                html.Tbody(html.Tr([
                                    html.Td(value, style={'border': '1px solid black', 'padding': '8px'}) for value in [
                                        "0,00%", "0,01%", "0,02%", "0,03%", "0,07%", "0,14%", "0,31%", "0,73%", "2,37%", "96,33%"
                                    ]
                                ]))
                            ], style={
                                'margin': 'auto',
                                'border-collapse': 'collapse',
                                'width': '90%',
                                'marginTop': '20px',
                                'marginBottom': '20px',
                                'overflowX': 'auto'
                            })
                        ], style={'overflowX': 'auto'})
                    ]),

                    html.P('''
Observemos la distribución de las ganancias según cada decil. Un decil representa el 10% de las empresas, lo que significa que este cuadro refleja cómo el 10% de las empresas más grandes concentra el 96% de las ganancias generadas, mientras que el resto de los deciles, que en conjunto suman el 90% restante, generan menos del 4% de las ganancias totales.

Con un total de 188.905 empresas en nuestro registro, cada decil representa a 18.891 empresas. Esto quiere decir que las 18.891 empresas más grandes son responsables de la casi totalidad de las ganancias.
                    ''')
                ], style={
                    'textAlign': 'justify',
                    'font-family': 'Cambria, serif',
                    'text-indent': '2em',
                    'fontSize': '16px',
                })
            ], width=12, lg=10, className="mx-auto")
        ])
    ], fluid=True),

    html.Div([
        html.P(
            "Importante: leer consideraciones metodológicas. // Realizado por Cambra Business Analytics. // Contacto: +595 0985 705586.",
            style={
                'font-family': 'Cambria, serif',
                'font-style': 'italic',
                'text-align': 'center',
                'color': 'white',
                'background-color': 'black',
                'margin-top': '20px',
                'width': '80%',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'padding': '10px',
                'line-height': '1.5',
                'font-size': '14px'
            }
        )
    ])
])


@dash.callback(
    [Output('plot-paraguay', 'figure'),
     Output('table1a', 'data'),
     Output('table1a', 'columns'),
     Output('table2a', 'data'),
     Output('table2a', 'columns')],
    [Input('radio', 'value'),
     Input('plot-paraguay', 'clickData')]
)
def update_figures(radio, clickData):
    import plotly.graph_objects as go

    if radio == 'Cantidad':
        df_agg = df.groupby('DPTO_DESC')['Cantidad_Empresas'].sum().reset_index()
        fig_map = px.choropleth_mapbox(
            df_agg,
            geojson=geojson_data,
            locations='DPTO_DESC',
            featureidkey="properties.DPTO_DESC",
            color='Cantidad_Empresas',
            mapbox_style="carto-positron",
            center={"lat": -23.4, "lon": -58.4},
            zoom=5.5,
            opacity=0.9,
            color_continuous_scale='Blues',
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        departamento = None
        if clickData and 'points' in clickData and len(clickData['points']) > 0:
            departamento = clickData['points'][0].get('location')

        if departamento:
            df_filtered = df[df['DPTO_DESC'] == departamento]
        else:
            df_filtered = df.iloc[0:0]

        distritos = df_filtered.groupby('DISTRITO')['Cantidad_Empresas'].sum().reset_index().sort_values(by='Cantidad_Empresas', ascending=False)
        secciones = df_filtered.groupby('Seccion')['Cantidad_Empresas'].sum().reset_index().sort_values(by='Cantidad_Empresas', ascending=False)

        bar1 = px.bar(distritos, x='DISTRITO', y='Cantidad_Empresas', title="Cantidad por Distrito")
        bar2 = px.bar(secciones, x='Seccion', y='Cantidad_Empresas', title="Cantidad por Sección")

        table1_data = distritos.to_dict('records')
        table1_columns = [{"name": i, "id": i} for i in distritos.columns]
        table2_data = secciones.to_dict('records')
        table2_columns = [{"name": i, "id": i} for i in secciones.columns]

    elif radio == 'Ganancias':
        df_agg = df.groupby('DPTO_DESC')['Ganancias'].sum().reset_index()
        fig_map = px.choropleth_mapbox(
            df_agg,
            geojson=geojson_data,
            locations='DPTO_DESC',
            featureidkey="properties.DPTO_DESC",
            color='Ganancias',
            mapbox_style="carto-positron",
            center={"lat": -23.4, "lon": -58.4},
            zoom=5.5,
            opacity=0.9,
            color_continuous_scale='OrRd',
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        departamento = None
        if clickData and 'points' in clickData and len(clickData['points']) > 0:
            departamento = clickData['points'][0].get('location')

        if departamento:
            df_filtered = df[df['DPTO_DESC'] == departamento]
        else:
            df_filtered = df.iloc[0:0]

        distritos = df_filtered.groupby('DISTRITO')['Ganancias'].sum().reset_index().sort_values(by='Ganancias', ascending=False)
        secciones = df_filtered.groupby('Seccion')['Ganancias'].sum().reset_index().sort_values(by='Ganancias', ascending=False)

        distritos_numeric = distritos.copy()
        secciones_numeric = secciones.copy()

        distritos['Ganancias'] = distritos['Ganancias'].apply(lambda x: f"{int(x):,}".replace(",", "."))
        secciones['Ganancias'] = secciones['Ganancias'].apply(lambda x: f"{int(x):,}".replace(",", "."))

        table1_data = distritos.to_dict('records')
        table1_columns = [{"name": i, "id": i} for i in distritos.columns]
        table2_data = secciones.to_dict('records')
        table2_columns = [{"name": i, "id": i} for i in secciones.columns]

    else:
        fig_map = go.Figure()
        table1_data = []
        table1_columns = []
        table2_data = []
        table2_columns = []

    return fig_map, table1_data, table1_columns, table2_data, table2_columns
