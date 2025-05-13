import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import json
import os
# Inicialización de la app (si es standalone, si estás usando multipágina no la dupliques)
dash.register_page(__name__, path="/")

df = pd.read_csv('empresas.csv', encoding='utf-8')

df['Ganancias'] = df['Ganancias'] * 10
#df['Ganancias'] = df['Ganancias'].astype(float).round(0).astype(int)
#df['Ganancias'] = df['Ganancias'].fillna(0)


with open("assets/DEPARTAMENTOS_PY_CNPV2022.geojson", encoding='utf-8') as f:
    geojson_data = json.load(f)

# Layout
layout = html.Div([
    html.H2("Análisis de características económicas del Paraguay",    style={
        'font-family': 'Avenir, sans-serif',
        'text-align': 'center',
        'color': 'black',
        'margin-top': '20px'}),
    html.P("Selecciona una opción para visualizar los datos.", style={'text-align': 'center',}
           ),

    html.Hr(),

    dbc.Row([
        # Mapa + radio
        dbc.Col([
            dbc.RadioItems(
                id='radio',
                options=[
                    {'label': 'Cantidad de Empresas', 'value': 'Cantidad'},
                    {'label': 'Ganancia de Empresas', 'value': 'Ganancias'}
                ],
                value='Cantidad',
                inline=True
            ),
            dcc.Graph(id='plot-paraguay', style={'height': '800px', 'width': '100%'},  # O un valor fijo como 'width': '800px'
                      config={'scrollZoom': False})], width=7),

        # Gráficos de barra
        dbc.Col([
            dcc.Graph(id='bar1a',  style={'height': '50%'}),
            dcc.Graph(id='bar2a',  style={'height': '50%'})
        ], width=4)
    ], justify='center'),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dash_table.DataTable(
                        id='table1a',
                        style_table={
                            'maxWidth': '100%',
                            'overflowX': 'auto',
                            'margin': 'auto'
                        },
                        style_cell={'textAlign': 'center'},
                    ),
                    width=6
                ),
                dbc.Col(
                    dash_table.DataTable(
                        id='table2a',
                        style_table={
                            'maxWidth': '100%',
                            'overflowX': 'auto',
                            'margin': 'auto'
                        },
                        style_cell={
                            'textAlign': 'center',
                            'fontSize': '14px',  # Tamaño de letra más pequeño
                            'whiteSpace': 'normal',  # Permite que el texto haga salto de línea
                            'height': 'auto',        # Altura ajustable
                        },
                        style_data={
                            'whiteSpace': 'normal',  # Asegura que las celdas colapsen contenido
                            'lineHeight': '15px',    # Controla el espaciado de línea si querés que sea más compacto
                        }
                    )
                ),
            ])
        ], width=8)
    ], justify='center', style={'marginTop': '20px'}),

    html.Hr(),

   dbc.Row(
    dbc.Col(
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

            html.H3("Desigualdad en la Generación de Rentas",    style={
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
                html.H5("Distribución de Ganancias por Decil:",style={
        'font-family': 'Avenir, sans-serif',
        'text-align': 'center',
        'color': 'black',
        'margin-top': '20px'}),
                html.Div([
                    html.Table([
                        html.Thead(
                            html.Tr([
                                html.Th("D1", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Th("D2", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Th("D3", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Th("D4", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Th("D5", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Th("D6", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Th("D7", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Th("D8", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Th("D9", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Th("D10", style={'border': '1px solid black', 'padding': '8px'})
                            ])
                        ),
                        html.Tbody(
                            html.Tr([
                                html.Td("0,00%", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Td("0,01%", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Td("0,02%", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Td("0,03%", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Td("0,07%", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Td("0,14%", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Td("0,31%", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Td("0,73%", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Td("2,37%", style={'border': '1px solid black', 'padding': '8px'}),
                                html.Td("96,33%", style={'border': '1px solid black', 'padding': '8px'})
                            ])
                        )
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
            '''),
        ],
        style={
            'textAlign': 'justify',
            'font-family': 'Cambria, serif',
            'text-indent': '2em',  # <<< Sangría
            'fontSize': '16px',
        }),
        width=8,
        className="mx-auto"
    )
    ),

    # Luego de este bloque insertás tu mensaje final:
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
            #'border-radius': '10px',
            'line-height': '1.5',
            'font-size': '14px'
            }
        )
    ]),

])

@dash.callback(
    [Output('plot-paraguay', 'figure'),
     Output('bar1a', 'figure'),
     Output('bar2a', 'figure'),
     Output('table1a', 'data'),
     Output('table1a', 'columns'),
     Output('table2a', 'data'),
     Output('table2a', 'columns')],
    [Input('radio', 'value'),
     Input('plot-paraguay', 'clickData')]
)
def update_figures(radio, clickData):
    if radio == 'Cantidad':
        # Mapa
        df_agg = df.groupby('DPTO_DESC')['Cantidad_Empresas'].sum().reset_index()
        fig_map = px.choropleth_mapbox(
            df_agg,
            geojson=geojson_data,
            locations='DPTO_DESC',
            featureidkey="properties.DPTO_DESC",
            color='Cantidad_Empresas',
            mapbox_style="carto-positron",
            center={"lat": -23.4, "lon": -58.4},
            zoom= 5.5,
            opacity=0.9,
            color_continuous_scale='Blues',
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        # Filtro por click
        if clickData:
            departamento = clickData['points'][0]['location']
            df_filtered = df[df['DPTO_DESC'] == departamento]
        else:
            df_filtered = df.iloc[0:0]

        # Gráficos de barra
        distritos = df_filtered.groupby('DISTRITO')['Cantidad_Empresas'].sum().reset_index().sort_values(by='Cantidad_Empresas', ascending=False)
        secciones = df_filtered.groupby('Seccion')['Cantidad_Empresas'].sum().reset_index().sort_values(by='Cantidad_Empresas', ascending=False)

        bar1 = px.bar(distritos, x='DISTRITO', y='Cantidad_Empresas', title="Cantidad por Distrito")
        bar2 = px.bar(secciones, x='Seccion', y='Cantidad_Empresas', title="Cantidad por Sección")

        # Tablas
        table1_data = distritos.to_dict('records')
        table1_columns = [{"name": i, "id": i} for i in distritos.columns]
        table2_data = secciones.to_dict('records')
        table2_columns = [{"name": i, "id": i} for i in secciones.columns]

    elif radio == 'Ganancias':
        # Mapa
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

        # Filtro por click
        if clickData:
            departamento = clickData['points'][0]['location']
            df_filtered = df[df['DPTO_DESC'] == departamento]
        else:
            df_filtered = df.iloc[0:0]

        # Gráficos de barra
        # Agrupaciones y orden
        distritos = df_filtered.groupby('DISTRITO')['Ganancias'].sum().reset_index().sort_values(by='Ganancias', ascending=False)
        secciones = df_filtered.groupby('Seccion')['Ganancias'].sum().reset_index().sort_values(by='Ganancias', ascending=False)

        # Copias numéricas para el gráfico (mantienen los valores como numéricos)
        distritos_numeric = distritos.copy()
        secciones_numeric = secciones.copy()

        # Gráficos de barra con color rojo
        bar1 = px.bar(distritos_numeric, x='DISTRITO', y='Ganancias', title="Ganancias por Distrito", color_discrete_sequence=['red'])
        bar2 = px.bar(secciones_numeric, x='Seccion', y='Ganancias', title="Ganancias por Sección", color_discrete_sequence=['red'])


        if not distritos_numeric.empty and not secciones_numeric.empty:
            max_value1 = distritos_numeric['Ganancias'].max()
            max_value2 = secciones_numeric['Ganancias'].max()

            bar1.update_layout(
                yaxis=dict(
                    tickvals=[max_value1],
                    ticktext=[f"{max_value1:,.0f}".replace(",", ".")]
                )
            )
            bar2.update_layout(
                yaxis=dict(
                    tickvals=[max_value2],
                    ticktext=[f"{max_value2:,.0f}".replace(",", ".")]
                )
            )
        else:
            # Gráficos vacíos por defecto si no hay datos
            bar1 = px.bar(title="Ganancias por Distrito")
            bar2 = px.bar(title="Ganancias por Sección")

        # Formateo de columnas para las tablas (solo string con puntos como separador de miles)
        distritos['Ganancias'] = distritos['Ganancias'].apply(lambda x: f"{int(x):,}".replace(",", "."))
        secciones['Ganancias'] = secciones['Ganancias'].apply(lambda x: f"{int(x):,}".replace(",", "."))

        # Tablas
        table1_data = distritos.to_dict('records')
        table1_columns = [{"name": i, "id": i} for i in distritos.columns]

        table2_data = secciones.to_dict('records')
        table2_columns = [{"name": i, "id": i} for i in secciones.columns]


    return fig_map, bar1, bar2, table1_data, table1_columns, table2_data, table2_columns
