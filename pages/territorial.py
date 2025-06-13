import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, dash_table, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px


# Cargar el archivo CSV
df = pd.read_csv('empresas.csv', encoding='utf-8')

explicaciones = {
    'a': """
**Cantidad de empresas por sector en cada territorio**

Este análisis muestra cuántas empresas tienen su casa matriz en cada territorio y qué actividades económicas desarrollan. La distribución de empresas por territorio nos permite observar tanto la concentración empresarial como el tipo de actividades económicas que predominan en cada zona.

Al conocer cuántas y qué tipo de empresas operan en un lugar, podemos inferir en buena medida cómo se estructura la economía local y a qué se dedica la población. Una mayor cantidad de empresas y una mayor diversidad de actividades económicas son señales de una economía más compleja y dinámica, lo que suele estar asociado a mejores condiciones para el desarrollo.
""",
    'b': """
**Participación de ganancias por sector en cada territorio**

Este análisis muestra cómo se distribuyen las ganancias generadas por las empresas en cada territorio, indicando además qué actividades económicas están generando esos ingresos. Nos permite identificar los territorios que más contribuyen a la economía nacional y entender a qué se dedican los sectores más rentables.

Los territorios con mayor participación en las ganancias tienden a reflejar economías más dinámicas. Si además presentan diversidad de actividades, se trata de estructuras productivas más equilibradas y resilientes. Esta métrica también permite comprender de dónde provienen las principales fuentes de ingreso de cada zona, lo cual es útil para anticipar oportunidades o riesgos vinculados a la dependencia de ciertos sectores.
""",
    'c': """
**Participación de ganancias/empresas en cada territorio**

Este análisis muestra la participación en las ganancias generadas por las empresas en función de la participación que representa la cantidad de empresas en cada territorio. Se trata de una medida relativa que refleja la rentabilidad promedio de las empresas en un territorio, discriminando además por sector, división y actividad económica.

La métrica se construye dividiendo el porcentaje de participación en las ganancias por el porcentaje de participación en la cantidad de empresas. El resultado es un coeficiente que indica cuán rentable es, en promedio, la estructura empresarial de un territorio. Un coeficiente mayor a 1 implica que las empresas del territorio, en conjunto, generan más ganancias de las que cabría esperar según su peso en cantidad de empresas.

Este análisis es especialmente útil para identificar no solo los territorios más rentables, sino también los sectores y actividades económicas que generan mayores retornos. Además, permite explorar cómo se desempeñan las distintas actividades económicas en cada territorio, ayudando a comprender mejor la relación entre el lugar y el tipo de actividad en términos de rentabilidad relativa.
""",
    'd': """
**Cantidad de empresas/población en cada territorio**

Este análisis muestra la cantidad de empresas que existen en un territorio en relación con la cantidad de personas que lo habitan. La métrica se construye dividiendo el número total de empresas con matriz en ese territorio por su población, lo que permite observar cuántas empresas existen, en promedio, por cada habitante.

Si bien no mide directamente el bienestar ni la calidad del empleo, puede dar señales sobre la densidad empresarial y, en cierta medida, sobre el entorno económico en el que vive la población. También permite comparar territorios de distinto tamaño poblacional, ya que estandariza la cantidad de empresas en función de su población. Esto facilita identificar zonas donde la estructura empresarial es más densa y, por lo tanto, donde podrían existir mejores condiciones para el desarrollo económico local.
""",
    'e': """
**Participación de ganancias/población por sector en cada territorio**

Este análisis presenta la relación entre las ganancias generadas por las empresas de un territorio y la cantidad de personas que habitan en él, con el objetivo de ofrecer una medida más afinada para interpretar el nivel de productividad promedio. La participación absoluta en las ganancias suele ser mayor en zonas con mayor población, pero esto no implica necesariamente una situación de bienestar o eficiencia. Al ponderar las ganancias por la cantidad de habitantes, se obtiene una perspectiva más precisa de la productividad de un territorio.

La métrica utilizada surge de dividir el porcentaje de ganancias que representa un territorio respecto al total nacional, por el porcentaje de población que ese mismo territorio representa respecto a la población nacional. El resultado es un coeficiente que permite comparar territorios entre sí en términos relativos, más allá del tamaño de su población o su volumen total de ganancias. Mientras más alto el coeficiente, mayor la rentabilidad en el territorio.

Es importante aclarar que este indicador no representa ingresos individuales, pero sí brinda una primera aproximación sobre qué tan productivo es un territorio en relación con la cantidad de personas que lo habitan.
""",
    'f': """
**Cantidad de actividades por cada territorio**

Este análisis muestra cuántas actividades económicas distintas se desarrollan dentro de un territorio. A diferencia de otras métricas centradas en la cantidad de empresas o el volumen de ganancias, aquí el foco está en la diversidad de la estructura económica.

Los territorios con mayor cantidad de actividades presentan economías más diversificadas, lo que suele asociarse a una mayor capacidad de adaptación frente a cambios en el entorno, menor dependencia de un único sector y, en general, una estructura más sólida. Una mayor diversidad también puede reflejar un ecosistema económico más dinámico, capaz de generar oportunidades para distintos perfiles productivos y laborales.

Aunque no se evalúa el tamaño ni el peso de cada actividad, esta métrica ofrece una primera aproximación para identificar territorios con mayor variedad económica, lo que puede ser un factor relevante al analizar el potencial de desarrollo de una región.
"""
}
# Registrar la página en Dash multipágina
dash.register_page(__name__, path="/territorial")

# Inicializar la figura vacía para evitar errores
fig= go.Figure()
fig2= go.Figure()
# Layout de la página principal
# Layout de la página principal
layout = dbc.Container([

    dbc.Row([
        dbc.Col(
            html.H2("Análisis de características económicas del Paraguay", 
                    style={'textAlign': 'center', 'font-family': 'Avenir'}),
            width=12
        )
    ]),

    dbc.Row([
        dbc.Col(
            html.P("Selecciona una opción en el menú para visualizar los datos (más opciones conlleva más tiempo de carga). ",
                   style={'textAlign': 'center', 'font-family': 'Cambria'}),
            width=8,
            className='mx-auto'
        )
    ]),

    html.Hr(),

    dbc.Row([
        dbc.Col(
            dcc.RadioItems(
                ['Departamentos', 'Distritos'], 
                value='Departamentos', 
                inline=True, 
                id='radiob'
            ), 
            xs=12, md=2,
            className='mb-3 mb-md-0 mx-auto'
        ),
    
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-optionsb',
                options=[],
                value=[],
                clearable=True,
                multi=True,
                placeholder='Selecciona una o varias opciones',
                style={'width': '100%', 'font-family': 'Cambria'}
            ),
            xs=12, md=4,
            className='mb-3 mb-md-0 mx-auto'
        ),
    
        dbc.Col(
            dcc.Dropdown(
                id='infob',
                options=[
                    {'label': 'Cantidad de empresas por sector en cada territorio', 'value': 'a'},
                    {'label': 'Participación de ganancias por sector en cada territorio', 'value': 'b'}, 
                    {'label': 'Participación de ganancias/empresas en cada territorio', 'value': 'c'},
                    {'label': 'Cantidad de empresas/población en cada territorio', 'value': 'd'},
                    {'label': 'Participación de ganancias/población en cada territorio', 'value': 'e'},
                    {'label': 'Cantidad de actividades por cada territorio', 'value': 'f'},
                ],
                value='a',
                clearable=False,
                multi=False,
                placeholder='Selecciona una opción',
                style={'width': '100%', 'font-family': 'Cambria', 'maxHeight': '800px'},
            ),
            xs=12, md=5,
            className='mx-auto'
        )
    ], justify='center', className='mb-4'),


    html.Hr(),

    # Primer gráfico (Treemap u otro), centrado en ancho 10
    dbc.Row([
        dbc.Col(dcc.Graph(id='plot1b', figure=fig), width=12,  md=12, sm=12, className='mx-auto'),
    ]),

    html.Hr(),

    dcc.Markdown(
        id='explicacion-container',
        style={
            'fontFamily': 'Cambria',
            'fontSize': '16px',
            'textAlign': 'justify',
            'lineHeight': '1.6',
            'width': '66%',
            'margin': '20px auto',
            'padding': '10px',
            'whiteSpace': 'pre-wrap'
        }
    ),

    # Segundo gráfico (barras u otro)
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='plot2b', figure=fig2, style={'width': '100%'}),
            xs=12, md=8,
            className='mx-auto mb-4'
        ),
    ]),


    html.Hr(),
    
    dbc.Tooltip(
        "Filtrá escribiendo en cada columna (El botón [Aa] desactiva la sensibilidad a mayúsculas.). Usá =, >, <, >=, <= para valores numéricos. Ejemplo: > 100 mostrará solo los valores mayores a 100.",
        target="tableb",
        placement="top",
    ),
    # Tabla
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='tableb',
                columns=[],
                style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold', 'font-family': 'Cambria'},
                style_table={
                    'maxWidth': '100%',
                    'overflowX': 'auto',
                    'overflowY': 'auto',  # Para que aparezca el scroll vertical
                    'maxHeight': '400px',  # Altura máxima de la tabla
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
                },
                data=[],
                filter_action='native',
                sort_action='native',
            ),
            width=8,
            className='mx-auto'
        )
    ]),

    html.Br(),

    # Footer
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

], fluid=True)

@dash.callback(
    Output('dropdown-optionsb', 'options'),
    Output('dropdown-optionsb', 'value'),
    Input('radiob', 'value')
)
def dropdown(radio):
    if radio == 'Departamentos':   
        valores = df['DEPARTAMENTO'].unique()  # Obtener valores únicos
        options = [{"label": departamento, "value": departamento} for departamento in valores]
        value = ['Alto Parana.', 'Asuncion.', 'Central.', 'Itapua.']
    elif radio == 'Distritos':
        valores = df['DISTRITO'].unique()  # Obtener valores únicos
        options = [{"label": distrito, "value": distrito} for distrito in valores]
        value = ['Ciudad Del Este', 'Presidente Franco', 'Hernandarias', 'Minga Guazu']
    return options, value

@dash.callback(
    [Output('plot1b', 'figure'),
     Output('plot2b', 'figure'),
     Output('tableb', 'columns'),
     Output('tableb', 'data'),
     Output('explicacion-container', 'children')],  
    [State('radiob', 'value'),
     Input('dropdown-optionsb', 'value'),
     Input('infob', 'value'),]
)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def update_dashboard(radio, selected_options, selected_info):
    
#----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

    if radio == 'Departamentos':
        
        seleccionados = selected_options
        dff = df.loc[df['DEPARTAMENTO'].isin(seleccionados)]
        dff2 = df.copy()
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------- 
#        
        if selected_info == 'a':
            children = explicaciones.get('a') 
            # Agrupación
            df_departamentos = dff.groupby(['DEPARTAMENTO', 'Seccion', 'Division', 'Actividad_principal'])['Cantidad_Empresas'].sum().reset_index()
            df_departamentos.fillna("Desconocido", inplace=True)
            
            # Crear IDs únicos para cada nivel
            df_departamentos['DEP_ID'] = df_departamentos['DEPARTAMENTO']
            df_departamentos['SEC_ID'] = df_departamentos['DEP_ID'] + ' - ' + df_departamentos['Seccion']
            df_departamentos['DIV_ID'] = df_departamentos['SEC_ID'] + ' - ' + df_departamentos['Division']
            df_departamentos['ACT_ID'] = df_departamentos['DIV_ID'] + ' - ' + df_departamentos['Actividad_principal']

            # Inicializar listas
            ids = []
            labels = []
            parents = []
            values = []

            # 1️⃣ Departamentos
            for _, row in df_departamentos[['DEP_ID', 'DEPARTAMENTO']].drop_duplicates().iterrows():
                ids.append(row['DEP_ID'])
                labels.append(row['DEPARTAMENTO'])  # solo nombre limpio
                parents.append('')
                values.append(df_departamentos[df_departamentos['DEP_ID'] == row['DEP_ID']]['Cantidad_Empresas'].sum())

            # 2️⃣ Secciones
            for _, row in df_departamentos[['SEC_ID', 'Seccion', 'DEP_ID']].drop_duplicates().iterrows():
                ids.append(row['SEC_ID'])
                labels.append(row['Seccion'])  # nombre simple
                parents.append(row['DEP_ID'])
                values.append(df_departamentos[df_departamentos['SEC_ID'] == row['SEC_ID']]['Cantidad_Empresas'].sum())

            # 3️⃣ Divisiones
            for _, row in df_departamentos[['DIV_ID', 'Division', 'SEC_ID']].drop_duplicates().iterrows():
                ids.append(row['DIV_ID'])
                labels.append(row['Division'])  # nombre simple
                parents.append(row['SEC_ID'])
                values.append(df_departamentos[df_departamentos['DIV_ID'] == row['DIV_ID']]['Cantidad_Empresas'].sum())

            # 4️⃣ Actividades
            for _, row in df_departamentos[['ACT_ID', 'Actividad_principal', 'DIV_ID']].drop_duplicates().iterrows():
                ids.append(row['ACT_ID'])
                labels.append(row['Actividad_principal'])  # solo nombre, no concatenado
                parents.append(row['DIV_ID'])
                values.append(df_departamentos[df_departamentos['ACT_ID'] == row['ACT_ID']]['Cantidad_Empresas'].sum())

            # Crear Treemap
            fig = go.Figure(go.Treemap(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",
                textinfo="label+value+percent entry",
            ))

            # Mostrar gráfico
            fig.update_layout(title=f'Cantidad de empresas por sector en {selected_options}')

            df_departamentos2 = dff2.groupby(['DEPARTAMENTO', 'Seccion', 'Division', 'Actividad_principal'])['Cantidad_Empresas'].sum().reset_index()
            df_departamentos2 = df_departamentos2.sort_values(by='Cantidad_Empresas', ascending=False)
            df_departamentos3 = df_departamentos2.groupby(['DEPARTAMENTO', 'Seccion'])['Cantidad_Empresas'].sum().reset_index()
            df_departamentos4 = df_departamentos2.groupby('DEPARTAMENTO')['Cantidad_Empresas'].sum().reset_index()
            datos = df_departamentos3.sort_values(by='Cantidad_Empresas', ascending=False)

            fig2 = px.bar(
                datos,
                x='DEPARTAMENTO',
                y='Cantidad_Empresas',
                color='Seccion',  # Se mantiene la categorización por 'Seccion'
                color_continuous_scale='Viridis',  # Aplica el mismo esquema de colores
                title='Cantidad de empresas por sector a nivel nacional')
            fig2.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-1,
                    xanchor="center",
                    x=0.5
                ),
                height=1000,
                xaxis_tickangle=-45,           # Rotar etiquetas 45 grados para evitar superposición
                xaxis_tickfont=dict(size=10),  # Reducir tamaño de fuente de etiquetas X
                margin=dict(t=50, b=100),      # Más espacio arriba y abajo para que no se corten
                xaxis=dict(automargin=True)    # Ajusta márgenes automáticamente para etiquetas largas
            )

           

            # Para la tabla se usan los datos filtrados
        
            data = df_departamentos4.to_dict('records')
            columns=[
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'CANTIDAD', 'id': 'Cantidad_Empresas'}
            ]



#-------------------------------------------------------------------------------------------------------------------------------
#         
        elif selected_info == 'b':
            children = explicaciones.get('b') 
            # Agrupación
            df_departamentos = dff.groupby(['DEPARTAMENTO', 'Seccion', 'Division', 'Actividad_principal'])['PARTICIPACION'].sum().reset_index()
            df_departamentos.fillna("Desconocido", inplace=True)

            # Crear IDs únicos para cada nivel
            df_departamentos['DEP_ID'] = df_departamentos['DEPARTAMENTO']
            df_departamentos['SEC_ID'] = df_departamentos['DEP_ID'] + ' - ' + df_departamentos['Seccion']
            df_departamentos['DIV_ID'] = df_departamentos['SEC_ID'] + ' - ' + df_departamentos['Division']
            df_departamentos['ACT_ID'] = df_departamentos['DIV_ID'] + ' - ' + df_departamentos['Actividad_principal']

            # Inicializar listas
            ids = []
            labels = []
            parents = []
            values = []

            # 1️⃣ Departamentos
            for _, row in df_departamentos[['DEP_ID', 'DEPARTAMENTO']].drop_duplicates().iterrows():
                ids.append(row['DEP_ID'])
                labels.append(row['DEPARTAMENTO'])
                parents.append('')
                values.append(df_departamentos[df_departamentos['DEP_ID'] == row['DEP_ID']]['PARTICIPACION'].sum())

            # 2️⃣ Secciones
            for _, row in df_departamentos[['SEC_ID', 'Seccion', 'DEP_ID']].drop_duplicates().iterrows():
                ids.append(row['SEC_ID'])
                labels.append(row['Seccion'])
                parents.append(row['DEP_ID'])
                values.append(df_departamentos[df_departamentos['SEC_ID'] == row['SEC_ID']]['PARTICIPACION'].sum())

            # 3️⃣ Divisiones
            for _, row in df_departamentos[['DIV_ID', 'Division', 'SEC_ID']].drop_duplicates().iterrows():
                ids.append(row['DIV_ID'])
                labels.append(row['Division'])
                parents.append(row['SEC_ID'])
                values.append(df_departamentos[df_departamentos['DIV_ID'] == row['DIV_ID']]['PARTICIPACION'].sum())

            # 4️⃣ Actividades
            for _, row in df_departamentos[['ACT_ID', 'Actividad_principal', 'DIV_ID']].drop_duplicates().iterrows():
                ids.append(row['ACT_ID'])
                labels.append(row['Actividad_principal'])
                parents.append(row['DIV_ID'])
                values.append(df_departamentos[df_departamentos['ACT_ID'] == row['ACT_ID']]['PARTICIPACION'].sum())

            # Crear Treemap
            fig = go.Figure(go.Treemap(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",
                textinfo="label+value+percent entry",
            ))

            # Mostrar gráfico
            fig.update_layout(title=f'Participación de ganancias por sector en {selected_options}')

            df_departamentos2 = dff2.groupby(['DEPARTAMENTO', 'Seccion', 'Division', 'Actividad_principal'])['PARTICIPACION'].sum().reset_index()
            df_departamentos2 = df_departamentos2.sort_values(by='PARTICIPACION', ascending=False)
            df_departamentos3 = df_departamentos2.groupby(['DEPARTAMENTO', 'Seccion'])['PARTICIPACION'].sum().reset_index()
            df_departamentos4 = df_departamentos2.groupby('DEPARTAMENTO')['PARTICIPACION'].sum().reset_index()
            datos = df_departamentos3.sort_values(by='PARTICIPACION', ascending=False)

            fig2 = px.bar(
                datos,
                x='DEPARTAMENTO',
                y='PARTICIPACION',
                color='Seccion',  # Se mantiene la categorización por 'Seccion'
                color_continuous_scale='Viridis',  # Aplica el mismo esquema de colores
                title='Participación de ganancias de cada departamento por sector a nivel nacional')
            fig2.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-1,
                    xanchor="center",
                    x=0.5
                ),
                height=1000,
                xaxis_tickangle=-45,           # Rotar etiquetas 45 grados para evitar superposición
                xaxis_tickfont=dict(size=10),  # Reducir tamaño de fuente de etiquetas X
                margin=dict(t=50, b=100),      # Más espacio arriba y abajo para que no se corten
                xaxis=dict(automargin=True)    # Ajusta márgenes automáticamente para etiquetas largas
            )

            # Para la tabla se usan los datos filtrados
            data = df_departamentos4.to_dict('records')
            columns=[
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'GANANCIAS (%)', 'id': 'PARTICIPACION'}
            ]


#---------------------------------------------------------------------------------------------------------------------------------------------------------
        elif selected_info == 'c':
            children = explicaciones.get('c') 

            # --- Paso preliminar: Cálculo global basado en dff2 (sin filtro) ---
            # Agrupar globalmente por DEPARTAMENTO (global: sin filtro)
            departamentos2 = dff2.groupby('DEPARTAMENTO').agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            ).reset_index()

            # Calcular el porcentaje global y la rentabilidad base para departamentos
            departamentos2['porcentaje_empresas'] = departamentos2['Cantidad_Empresas'] / departamentos2['Cantidad_Empresas'].sum() * 100
            departamentos2['rentabilidad_empresas'] = departamentos2['PARTICIPACION'] / departamentos2['porcentaje_empresas'] * 100

            # Extraer los totales globales (para usar en los cálculos con dff, datos filtrados)
            cantidad_empresas = departamentos2['Cantidad_Empresas'].sum()
            participacion_total = departamentos2['PARTICIPACION'].sum()

            # --- Paso 1: Crear el DataFrame de departamentos a partir de dff (Datos filtrados) ---
            df_departamentos = dff.groupby(['DEPARTAMENTO', 'Seccion', 'Division', 'Actividad_principal'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            # Usar los totales globales para calcular el porcentaje a este nivel
            df_departamentos['porcentaje_empresas'] = df_departamentos['Cantidad_Empresas'] / cantidad_empresas * 100
            df_departamentos = df_departamentos.fillna(0)

            # --- Paso 2: Nivel Departamentos ---
            # Agrupar los datos filtrados a nivel DEPARTAMENTO para calcular la rentabilidad a ese nivel
            df_departamentos_rentabilidad = df_departamentos.groupby('DEPARTAMENTO', as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            # Calcular el porcentaje usando el total global (cantidad_empresas)
            df_departamentos_rentabilidad['porcentaje_empresas'] = df_departamentos_rentabilidad['Cantidad_Empresas'] / cantidad_empresas * 100
            df_departamentos_rentabilidad['rentabilidad_empresas'] = df_departamentos_rentabilidad.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100) 
                            if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_departamentos_rentabilidad = df_departamentos_rentabilidad.fillna(0)

            # --- Paso 3: Nivel Secciones ---
            df_secciones = dff.groupby(['DEPARTAMENTO', 'Seccion'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            # Calcular porcentaje usando el total global
            df_secciones['porcentaje_empresas'] = df_secciones['Cantidad_Empresas'] / cantidad_empresas * 100
            df_secciones['rentabilidad_empresas'] = df_secciones.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                            if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_secciones = df_secciones.fillna(0)

            # --- Paso 4: Nivel Divisiones ---
            df_divisiones = dff.groupby(['DEPARTAMENTO', 'Seccion', 'Division'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_divisiones['porcentaje_empresas'] = df_divisiones['Cantidad_Empresas'] / cantidad_empresas * 100
            df_divisiones['rentabilidad_empresas'] = df_divisiones.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                            if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_divisiones = df_divisiones.fillna(0)

            # --- Paso 5: Nivel Actividades ---
            df_actividades = dff.groupby(['DEPARTAMENTO', 'Seccion', 'Division', 'Actividad_principal'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_actividades['porcentaje_empresas'] = df_actividades['Cantidad_Empresas'] / cantidad_empresas * 100
            df_actividades['rentabilidad_empresas'] = df_actividades.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                            if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_actividades = df_actividades.fillna(0)

            # --- Paso 6: Crear IDs únicos para cada nivel ---
            df_departamentos['DEP_ID'] = df_departamentos['DEPARTAMENTO']
            df_secciones['SEC_ID'] = df_secciones['DEPARTAMENTO'] + ' - ' + df_secciones['Seccion']
            df_divisiones['DIV_ID'] = df_divisiones['DEPARTAMENTO'] + ' - ' + df_divisiones['Seccion'] + ' - ' + df_divisiones['Division']
            df_actividades['ACT_ID'] = (
                df_actividades['DEPARTAMENTO'] + ' - ' +
                df_actividades['Seccion'] + ' - ' +
                df_actividades['Division'] + ' - ' +
                df_actividades['Actividad_principal']
            )

            # --- Paso 7: Inicializar las listas para el treemap ---
            ids = []
            labels = []
            parents = []
            values = []

            # Nivel Departamentos (usando df_departamentos_rentabilidad)
            for _, row in df_departamentos_rentabilidad.iterrows():
                ids.append(row['DEPARTAMENTO'])  # Cada departamento como identificador único
                labels.append(row['DEPARTAMENTO'])
                parents.append('')
                values.append(row['rentabilidad_empresas'])

            # Nivel Secciones
            for _, row in df_secciones.iterrows():
                sec_id = row['DEPARTAMENTO'] + ' - ' + row['Seccion']
                ids.append(sec_id)
                labels.append(row['Seccion'])
                parents.append(row['DEPARTAMENTO'])
                values.append(row['rentabilidad_empresas'])

            # Nivel Divisiones
            for _, row in df_divisiones.iterrows():
                div_id = row['DEPARTAMENTO'] + ' - ' + row['Seccion'] + ' - ' + row['Division']
                sec_id = row['DEPARTAMENTO'] + ' - ' + row['Seccion']
                ids.append(div_id)
                labels.append(row['Division'])
                parents.append(sec_id)
                values.append(row['rentabilidad_empresas'])

            # Nivel Actividades
            for _, row in df_actividades.iterrows():
                act_id = row['DEPARTAMENTO'] + ' - ' + row['Seccion'] + ' - ' + row['Division'] + ' - ' + row['Actividad_principal']
                div_id = row['DEPARTAMENTO'] + ' - ' + row['Seccion'] + ' - ' + row['Division']
                ids.append(act_id)
                labels.append(row['Actividad_principal'])
                parents.append(div_id)
                values.append(row['rentabilidad_empresas'])

            # --- Paso 8: Crear el treemap usando Plotly ---
            fig = go.Figure(go.Treemap(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",
                textinfo="label+value+percent entry",
                # marker=dict(colors=values, colorscale='RdBu', cmid=100)  # Opcional: ajustar la escala de colores
            ))

            # --- Paso 9: Actualizar el layout del gráfico ---
            fig.update_layout(title=f"Rentabilidad relativa por actividad y territorio en {selected_options}")

            # --- Opcional: Para la gráfica de barras y la tabla ---
            departamentos2 = departamentos2.sort_values(by='rentabilidad_empresas', ascending=False)
            departamentos2 = departamentos2.loc[departamentos2['DEPARTAMENTO'] != 'Sin Datos']
            departamentos3 = departamentos2.head(20)

            datos = departamentos3
            fig2 = px.bar(
                datos,
                x='DEPARTAMENTO',
                y='rentabilidad_empresas',
                title='Participación de ganancias por empresa en departamentos top 20'
            )

            data = departamentos2.to_dict('records')
            columns = [
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'EMPRESAS (%)', 'id': 'porcentaje_empresas'},
                {'name': 'GANANCIAS (%)', 'id': 'PARTICIPACION'},
                {'name': 'RELACION', 'id': 'rentabilidad_empresas'},
            ]

# Finalmente, en tu callback de Dash retornarías fig, fig2, columns y data (junto con la explicación, si se requiere)


 #----------------------------------------------------------------------------------------------------------------------------------------------------------       
        elif selected_info == 'd':
            children = explicaciones.get('d') 
# Cantidad de empresas por cada habitante 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # 1 Calcular el coeficiente distrital 

            departamentos = dff.groupby(['PAIS', 'DEPARTAMENTO', 'DISTRITO']).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                Poblacion=('Poblacion', 'max'),
                ).reset_index().reset_index()
            departamentos['empresas_habitantes'] = (
                departamentos['Cantidad_Empresas'] / departamentos['Poblacion']
            )

            # 2️⃣ Calcular el coeficiente departamental
            departamentos2 = dff.groupby(['PAIS', 'DEPARTAMENTO', 'DISTRITO']).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                Poblacion=('Poblacion', 'max'),
                ).reset_index().reset_index()
            departamentos2 = departamentos2.groupby(['PAIS', 'DEPARTAMENTO']).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                Poblacion=('Poblacion', 'sum'),
                ).reset_index()
            departamentos2['empresas_habitantes'] = (
                departamentos2['Cantidad_Empresas'] / departamentos2['Poblacion']
            )

            # 3️⃣ Agregar nivel PAÍS con coeficiente 

            departamentos3 = departamentos2.groupby(['PAIS']).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                Poblacion=('Poblacion', 'sum'))

            departamentos3['empresas_habitantes'] = (
                departamentos3['Cantidad_Empresas'] / departamentos3['Poblacion']
            )


            # 5️⃣ Inicializar listas para Treemap
            labels = []
            parents = []
            values = []

            # 🔹 Agregar país (nivel superior)
            labels.append("PARAGUAY")
            parents.append("")
            values.append(departamentos3['empresas_habitantes'])

            # 🔹 Agregar departamentos
            for _, row in departamentos2.iterrows():
                labels.append(row['DEPARTAMENTO'])
                parents.append("PARAGUAY")  # Conectar los departamentos al país
                values.append(row['empresas_habitantes'])

            # 🔹 Agregar distritos
            for _, row in departamentos.iterrows():
                labels.append(row['DISTRITO'])
                parents.append(row['DEPARTAMENTO'])  # Conectar distritos a departamentos
                values.append(row['empresas_habitantes'])

            # 6️⃣ Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value",
                textinfo="label+value",
            ))
            
            # Mostrar gráfico
            fig.update_layout(title=f'Cantidad de empresas por cada habitante en {selected_options}')


            departamentos5 = dff2.groupby(['DEPARTAMENTO', 'DISTRITO']).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                Poblacion=('Poblacion', 'max')
                ).reset_index()
            departamentos5 = departamentos5.groupby(['DEPARTAMENTO']).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                Poblacion=('Poblacion', 'sum'),
                ).reset_index()
            departamentos5['empresas_habitantes'] = (
                departamentos5['Cantidad_Empresas'] / departamentos5['Poblacion']
                        )
            datos = departamentos5.sort_values(by='empresas_habitantes', ascending=False)
            fig2 = px.bar(
                datos,
                x='DEPARTAMENTO',
                y='empresas_habitantes',
                #color='Seccion',  # Se mantiene la categorización por 'Seccion'
                #color_continuous_scale='Viridis',  # Aplica el mismo esquema de colores
                title='Cantidad de empresas por cada habitante a nivel nacional')
            
            data = datos.to_dict('records')
            columns=[
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'EMPRESAS', 'id': 'Cantidad_Empresas'},
                {'name': 'POBLACION', 'id': 'Poblacion'},
                {'name': 'RELACION', 'id': 'empresas_habitantes'},
            ]
 #----------------------------------------------------------------------------------------------------------------------------------------------------------       
        elif selected_info == 'e':
            children = explicaciones.get('e') 
# Cantidad de empresas por cada habitante 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # 1 Calcular el coeficiente distrital 

            departamentos = dff.groupby(['PAIS', 'DEPARTAMENTO', 'DISTRITO']).agg(
                PARTICIPACION =('PARTICIPACION', 'sum'),
                Poblacion=('Poblacion', 'max'),
                ).reset_index().reset_index()
            departamentos['ganancias_habitantes'] = (
                departamentos['PARTICIPACION'] / departamentos['Poblacion']
            )

            # 2️⃣ Calcular el coeficiente departamental
            departamentos2 = dff.groupby(['PAIS', 'DEPARTAMENTO', 'DISTRITO']).agg(
                PARTICIPACION=('PARTICIPACION', 'sum'),
                Poblacion=('Poblacion', 'max'),
                ).reset_index().reset_index()
            departamentos2 = departamentos2.groupby(['PAIS', 'DEPARTAMENTO']).agg(
                PARTICIPACION=('PARTICIPACION', 'sum'),
                Poblacion=('Poblacion', 'sum'),
                ).reset_index()
            departamentos2['ganancias_habitantes'] = (
                departamentos2['PARTICIPACION'] / departamentos2['Poblacion']
            )

            # 3️⃣ Agregar nivel PAÍS con coeficiente 

            departamentos3 = departamentos2.groupby(['PAIS']).agg(
                PARTICIPACION=('PARTICIPACION', 'sum'),
                Poblacion=('Poblacion', 'sum'))

            departamentos3['ganancias_habitantes'] = (
                departamentos3['PARTICIPACION'] / departamentos3['Poblacion']
            )


            # 5️⃣ Inicializar listas para Treemap
            labels = []
            parents = []
            values = []

            # 🔹 Agregar país (nivel superior)
            labels.append("PARAGUAY")
            parents.append("")
            values.append(departamentos3['ganancias_habitantes'])

            # 🔹 Agregar departamentos
            for _, row in departamentos2.iterrows():
                labels.append(row['DEPARTAMENTO'])
                parents.append("PARAGUAY")  # Conectar los departamentos al país
                values.append(row['ganancias_habitantes'])

            # 🔹 Agregar distritos
            for _, row in departamentos.iterrows():
                labels.append(row['DISTRITO'])
                parents.append(row['DEPARTAMENTO'])  # Conectar distritos a departamentos
                values.append(row['ganancias_habitantes'])

            # 6️⃣ Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value",
                textinfo="label+value",
            ))
            
            # Mostrar gráfico
            fig.update_layout(title=f'Cantidad de empresas por cada habitante en {selected_options}')


            departamentos5 = dff2.groupby(['DEPARTAMENTO', 'DISTRITO']).agg(
                PARTICIPACION=('PARTICIPACION', 'sum'),
                Poblacion=('Poblacion', 'max')
                ).reset_index()
            departamentos5 = departamentos5.groupby(['DEPARTAMENTO']).agg(
                PARTICIPACION=('PARTICIPACION', 'sum'),
                Poblacion=('Poblacion', 'sum'),
                ).reset_index()
            departamentos5['ganancias_habitantes'] = (
                departamentos5['PARTICIPACION'] / departamentos5['Poblacion']
                        )
            datos = departamentos5.sort_values(by='ganancias_habitantes', ascending=False)
            fig2 = px.bar(
                datos,
                x='DEPARTAMENTO',
                y='ganancias_habitantes',
                #color='Seccion',  # Se mantiene la categorización por 'Seccion'
                #color_continuous_scale='Viridis',  # Aplica el mismo esquema de colores
                title='Cantidad de empresas por cada habitante a nivel nacional')
            
            data = datos.to_dict('records')
            columns=[
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'GANANCIAS (%)', 'id': 'PARTICIPACION'},
                {'name': 'POBLACION', 'id': 'Poblacion'},
                {'name': 'RELACION', 'id': 'ganancias_habitantes'},]
 #----------------------------------------------------------------------------------------------------------------------------------------


        elif selected_info == 'f':
            children = explicaciones.get('f') 
# Cantidad de actividades por cada territorio
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # 1 Calcular el coeficiente distrital 

            departamentos = dff.groupby('PAIS')['Actividad_principal'].nunique().reset_index()
            departamentos2 = dff.groupby(['PAIS', 'DEPARTAMENTO'])['Actividad_principal'].nunique().reset_index()
            departamentos3 = dff.groupby(['PAIS', 'DEPARTAMENTO', 'DISTRITO'])['Actividad_principal'].nunique().reset_index()

            # 5️⃣ Inicializar listas para Treemap
            labels = []
            parents = []
            values = []

            # 🔹 Agregar país (nivel superior)
            labels.append("PARAGUAY")
            parents.append("")
            values.append(departamentos['Actividad_principal'])

            # 🔹 Agregar departamentos
            for _, row in departamentos2.iterrows():
                labels.append(row['DEPARTAMENTO'])
                parents.append("PARAGUAY")  # Conectar los departamentos al país
                values.append(row['Actividad_principal'])

            # 🔹 Agregar distritos
            for _, row in departamentos3.iterrows():
                labels.append(row['DISTRITO'])
                parents.append(row['DEPARTAMENTO'])  # Conectar distritos a departamentos
                values.append(row['Actividad_principal'])

            # 6️⃣ Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value",
                textinfo="label+value",
            ))

            # Mostrar gráfico
            fig.update_layout(title=f'Cantidad de actividades economicas desarrolladas en {selected_options}')

            departamentos5 = dff2.groupby(['DEPARTAMENTO'])['Actividad_principal'].nunique().reset_index()
            datos = departamentos5.sort_values(by='Actividad_principal', ascending=False)

            fig2 = px.bar(
                datos,
                x='DEPARTAMENTO',
                y='Actividad_principal',
                #color='Seccion',  # Se mantiene la categorización por 'Seccion'
                #color_continuous_scale='Viridis',  # Aplica el mismo esquema de colores
                title='Cantidad de actividades economicas desarrolladas en cada Departamento')
          
            
            data = datos.to_dict('records')
            columns=[
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'CANTIDAD DE ACTIVIDADES', 'id': 'Actividad_principal'}
            ]


#-----------------------------------------------------------------------------------------------------------------------------------------------------------       
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    elif radio == 'Distritos':
        seleccionados = selected_options
        dff = df.loc[df['DISTRITO'].isin(seleccionados)]      
        dff2 = df.copy()
    #------------------------------------------------------------------------------------------------------------------------------------------------------------- 
    #        
        if selected_info == 'a':
            children = explicaciones.get('a') 

            df_distritos = dff.groupby(['DISTRITO', 'Seccion', 'Division', 'Actividad_principal'])['Cantidad_Empresas'].sum().reset_index()
            df_distritos.fillna("Desconocido", inplace=True)
            df_distritos['Seccion'] = df_distritos['DISTRITO'] + " - " + df_distritos['Seccion']
            df_distritos['Division'] = df_distritos['Seccion'] + " - " + df_distritos['Division']
            df_distritos['Actividad_principal'] = df_distritos['Division'] + " - " + df_distritos['Actividad_principal']

            # Inicializar listas
            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar departamentos (Nivel Superior - Bisabuelo)
            for distrito in df_distritos['DISTRITO'].unique():
                labels.append(distrito)
                parents.append('')  
                values.append(df_distritos[df_distritos['DISTRITO'] == distrito]['Cantidad_Empresas'].sum())

            # 2️⃣ Agregar Secciones (Nivel Abuelo)
            for _, row in df_distritos[['DISTRITO', 'Seccion']].drop_duplicates().iterrows():
                labels.append(row['Seccion'])
                parents.append(row['DISTRITO'])  
                values.append(df_distritos[df_distritos['Seccion'] == row['Seccion']]['Cantidad_Empresas'].sum())

            # 3️⃣ Agregar Divisiones (Nivel Padre)
            for _, row in df_distritos[['Seccion', 'Division']].drop_duplicates().iterrows():
                labels.append(row['Division'])
                parents.append(row['Seccion'])  
                values.append(df_distritos[df_distritos['Division'] == row['Division']]['Cantidad_Empresas'].sum())

            # 4️⃣ Agregar Actividades Principales (Nivel Hijo)
            for _, row in df_distritos[['Division', 'Actividad_principal']].drop_duplicates().iterrows():
                labels.append(row['Actividad_principal'])
                parents.append(row['Division'])  
                values.append(df_distritos[df_distritos['Actividad_principal'] == row['Actividad_principal']]['Cantidad_Empresas'].sum())

            # Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",
                textinfo="label+value+percent entry",
            ))

            fig.update_layout(title=f'Cantidad de empresas por sector en {selected_options}')

            df_distritos2 = dff2.groupby('DISTRITO')['Cantidad_Empresas'].sum().reset_index()
            top2 = df_distritos2.sort_values(by='Cantidad_Empresas', ascending=False).head(20)
            dff3 = dff2.loc[dff2['DISTRITO'].isin(top2['DISTRITO'])]
            df_distritos3 = dff3.groupby(['DISTRITO', 'Seccion'])['Cantidad_Empresas'].sum().reset_index()
            df_distritos3 = df_distritos3.sort_values(by='Cantidad_Empresas', ascending=False).head(20)

            # Crear el gráfico con los datos corregidos
            fig2 = px.bar(
                df_distritos3,
                x='DISTRITO',
                y='Cantidad_Empresas',
                color='Seccion',
                title='Cantidad de empresas por sector en los 20 principales distritos',
                color_continuous_scale='Viridis',
            )

            # Ajustar la leyenda para que aparezca abajo
            fig2.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-1,
                    xanchor="center",
                    x=0.5
                ),
                height=1000,
                xaxis_tickangle=-45,           # Rotar etiquetas 45 grados para evitar superposición
                xaxis_tickfont=dict(size=10),  # Reducir tamaño de fuente de etiquetas X
                margin=dict(t=50, b=100),      # Más espacio arriba y abajo para que no se corten
                xaxis=dict(automargin=True)    # Ajusta márgenes automáticamente para etiquetas largas
            )

            # Para la tabla se usan los datos filtrados
            data = df_distritos2.to_dict('records')
            columns=[
                {'name': 'DISTRITOS', 'id': 'DISTRITO'},
                {'name': 'EMPRESAS', 'id': 'Cantidad_Empresas'}]


    #-------------------------------------------------------------------------------------------------------------------------------
    #         
        elif selected_info == 'b':
            children = explicaciones.get('b') 

            df_distritos = dff.groupby(['DISTRITO', 'Seccion', 'Division', 'Actividad_principal'])['PARTICIPACION'].sum().reset_index()
            df_distritos.fillna("Desconocido", inplace=True)
            df_distritos['Seccion'] = df_distritos['DISTRITO'] + " - " + df_distritos['Seccion']
            df_distritos['Division'] = df_distritos['Seccion'] + " - " + df_distritos['Division']
            df_distritos['Actividad_principal'] = df_distritos['Division'] + " - " + df_distritos['Actividad_principal']

            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar distritos (Nivel Superior - Bisabuelo)
            for distrito in df_distritos['DISTRITO'].unique():
                labels.append(distrito)
                parents.append('')
                values.append(df_distritos[df_distritos['DISTRITO'] == distrito]['PARTICIPACION'].sum())

            # 2️⃣ Agregar Secciones (Nivel Abuelo)
            for _, row in df_distritos[['DISTRITO', 'Seccion']].drop_duplicates().iterrows():
                labels.append(row['Seccion'])
                parents.append(row['DISTRITO'])
                values.append(df_distritos[df_distritos['Seccion'] == row['Seccion']]['PARTICIPACION'].sum())

            # 3️⃣ Agregar Divisiones (Nivel Padre)
            for _, row in df_distritos[['Seccion', 'Division']].drop_duplicates().iterrows():
                labels.append(row['Division'])
                parents.append(row['Seccion'])
                values.append(df_distritos[df_distritos['Division'] == row['Division']]['PARTICIPACION'].sum())

            # 4️⃣ Agregar Actividades Principales (Nivel Hijo)
            for _, row in df_distritos[['Division', 'Actividad_principal']].drop_duplicates().iterrows():
                labels.append(row['Actividad_principal'])
                parents.append(row['Division'])
                values.append(df_distritos[df_distritos['Actividad_principal'] == row['Actividad_principal']]['PARTICIPACION'].sum())

            # Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",
                textinfo="label+value+percent entry",
            ))

            fig.update_layout(title=f'Participación de ganancias por sector en {selected_options}')

            df_distritos2 = dff2.groupby('DISTRITO')['PARTICIPACION'].sum().reset_index()
            top2 = df_distritos2.sort_values(by='PARTICIPACION', ascending=False).head(20)
            dff3 = dff2.loc[dff2['DISTRITO'].isin(top2['DISTRITO'])]
            df_distritos3 = dff3.groupby(['DISTRITO', 'Seccion'])['PARTICIPACION'].sum().reset_index()
            df_distritos3 = df_distritos3.sort_values(by='PARTICIPACION', ascending=False).head(20)

            # Crear el gráfico con los datos corregidos
            fig2 = px.bar(
                df_distritos3,
                x='DISTRITO',
                y='PARTICIPACION',
                color='Seccion',
                title='Participacion de ganancias por sector en los 20 principales distritos',
                color_continuous_scale='Viridis',
            )

            # Ajustar la leyenda para que aparezca abajo
            fig2.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-1,
                    xanchor="center",
                    x=0.5
                ),
                height=1000,
                xaxis_tickangle=-45,           # Rotar etiquetas 45 grados para evitar superposición
                xaxis_tickfont=dict(size=10),  # Reducir tamaño de fuente de etiquetas X
                margin=dict(t=50, b=100),      # Más espacio arriba y abajo para que no se corten
                xaxis=dict(automargin=True)    # Ajusta márgenes automáticamente para etiquetas largas
            )
            data = df_distritos2.to_dict('records')
            columns=[
                {'name': 'DISTRITOS', 'id': 'DISTRITO'},
                {'name': 'GANANCIAS (%)', 'id': 'PARTICIPACION'}]

    #-----------------------------------------------------------------------------------------------------------------------------------
        elif selected_info == 'c':
            children = explicaciones.get('c') 

            # --- Paso preliminar: Cálculo global basado en dff2 (sin filtro) ---

            # Agrupar globalmente por DISTRITO
            distritos2 = dff2.groupby('DISTRITO').agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            ).reset_index()

            # Calcular el porcentaje global de empresas y la "rentabilidad" (cálculo base)
            distritos2['porcentaje_empresas'] = distritos2['Cantidad_Empresas'] / distritos2['Cantidad_Empresas'].sum() * 100
            distritos2['rentabilidad_empresas'] = distritos2['PARTICIPACION'] / distritos2['porcentaje_empresas'] * 100

            # Extraer los totales globales (estos se usarán para el cálculo de porcentajes a nivel filtrado)
            cantidad_empresas = distritos2['Cantidad_Empresas'].sum()
            participacion_total = distritos2['PARTICIPACION'].sum()
            

            # --- Paso 1: Crear el DataFrame de distritos a partir de dff (Datos filtrados) ---
            df_distritos = dff.groupby(['DISTRITO', 'Seccion', 'Division', 'Actividad_principal'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            # Usar los totales globales para el porcentaje
            df_distritos['porcentaje_empresas'] = df_distritos['Cantidad_Empresas'] / cantidad_empresas * 100
            df_distritos = df_distritos.fillna(0)

            # --- Paso 2: Nivel Distritos ---
            # Agrupar los datos filtrados a nivel distrito para calcular la rentabilidad
            df_distritos_rentabilidad = df_distritos.groupby('DISTRITO', as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            # Aquí usamos el total de empresas de este groupby para el cálculo del porcentaje en este nivel
            df_distritos_rentabilidad['porcentaje_empresas'] = df_distritos_rentabilidad['Cantidad_Empresas'] / cantidad_empresas * 100
            df_distritos_rentabilidad['rentabilidad_empresas'] = df_distritos_rentabilidad.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_distritos_rentabilidad = df_distritos_rentabilidad.fillna(0)

            # --- Paso 3: Nivel Secciones ---
            df_secciones = dff.groupby(['DISTRITO', 'Seccion'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            # Usar el total global (cantidad_empresas) para calcular este porcentaje
            df_secciones['porcentaje_empresas'] = df_secciones['Cantidad_Empresas'] / cantidad_empresas * 100
            df_secciones['rentabilidad_empresas'] = df_secciones.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_secciones = df_secciones.fillna(0)

            # --- Paso 4: Nivel Divisiones ---
            df_divisiones = dff.groupby(['DISTRITO', 'Seccion', 'Division'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_divisiones['porcentaje_empresas'] = df_divisiones['Cantidad_Empresas'] / cantidad_empresas * 100
            df_divisiones['rentabilidad_empresas'] = df_divisiones.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_divisiones = df_divisiones.fillna(0)

            # --- Paso 5: Nivel Actividades ---
            df_actividades = dff.groupby(['DISTRITO', 'Seccion', 'Division', 'Actividad_principal'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_actividades['porcentaje_empresas'] = df_actividades['Cantidad_Empresas'] / cantidad_empresas * 100
            df_actividades['rentabilidad_empresas'] = df_actividades.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_actividades = df_actividades.fillna(0)

            # --- Paso 6: Crear IDs únicos para cada nivel ---
            df_distritos['DIST_ID'] = df_distritos['DISTRITO']
            df_secciones['SEC_ID'] = df_secciones['DISTRITO'] + ' - ' + df_secciones['Seccion']
            df_divisiones['DIV_ID'] = df_divisiones['DISTRITO'] + ' - ' + df_divisiones['Seccion'] + ' - ' + df_divisiones['Division']
            df_actividades['ACT_ID'] = df_actividades['DISTRITO'] + ' - ' + df_actividades['Seccion'] + ' - ' + df_actividades['Division'] + ' - ' + df_actividades['Actividad_principal']

            # --- Paso 7: Inicializar las listas para el treemap ---
            ids = []
            labels = []
            parents = []
            values = []

            # Nivel Distritos (usando df_distritos_rentabilidad)
            for _, row in df_distritos_rentabilidad.iterrows():
                ids.append(row['DISTRITO'])       # Cada distrito como identificador único
                labels.append(row['DISTRITO'])
                parents.append('')
                values.append(row['rentabilidad_empresas'])

            # Nivel Secciones
            for _, row in df_secciones.iterrows():
                sec_id = row['DISTRITO'] + ' - ' + row['Seccion']
                ids.append(sec_id)
                labels.append(row['Seccion'])
                parents.append(row['DISTRITO'])
                values.append(row['rentabilidad_empresas'])

            # Nivel Divisiones
            for _, row in df_divisiones.iterrows():
                div_id = row['DISTRITO'] + ' - ' + row['Seccion'] + ' - ' + row['Division']
                sec_id = row['DISTRITO'] + ' - ' + row['Seccion']
                ids.append(div_id)
                labels.append(row['Division'])
                parents.append(sec_id)
                values.append(row['rentabilidad_empresas'])

            # Nivel Actividades
            for _, row in df_actividades.iterrows():
                act_id = row['DISTRITO'] + ' - ' + row['Seccion'] + ' - ' + row['Division'] + ' - ' + row['Actividad_principal']
                div_id = row['DISTRITO'] + ' - ' + row['Seccion'] + ' - ' + row['Division']
                ids.append(act_id)
                labels.append(row['Actividad_principal'])
                parents.append(div_id)
                values.append(row['rentabilidad_empresas'])

            # --- Paso 8: Crear el treemap usando Plotly ---
            fig = go.Figure(go.Treemap(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",
                textinfo="label+value+percent entry",
                # Puedes ajustar la escala de colores según tus necesidades:
                # marker=dict(colors=values, colorscale='RdBu', cmid=100)
            ))

            # --- Paso 9: Actualizar el layout del gráfico ---
            fig.update_layout(title=f"Rentabilidad relativa por actividad y territorio en {selected_options}")



            distritos2 = distritos2.sort_values(by='rentabilidad_empresas', ascending=False)
            distritos2 = distritos2.loc[distritos2['DISTRITO'] != 'Sin Datos']
            distritos3 = distritos2.head(20)

            datos = distritos3
            fig2 = px.bar(
                datos,
                x='DISTRITO',
                y='rentabilidad_empresas',
                title='Participación de ganancias por empresa en distritos top 20'
            )

            data = distritos2.to_dict('records')
            columns = [
                {'name': 'DISTRITO', 'id': 'DISTRITO'},
                {'name': 'EMPRESAS (%)', 'id': 'porcentaje_empresas'},
                {'name': 'GANANCIAS (%)', 'id': 'PARTICIPACION'},
                {'name': 'RELACION', 'id': 'rentabilidad_empresas'},
            ]


#---------------------------------------------------------------------------------------------------------------------------------------------------------

        elif selected_info == 'd':
            children = explicaciones.get('d') 
            # 1 Calcular el coeficiente distrital 

            # 1️⃣ Calcular el coeficiente distrital (Empresas por habitante)
            distritos = dff.groupby('DISTRITO').agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                Poblacion=('Poblacion', 'max'),
            ).reset_index()

            distritos['empresas_habitantes'] = distritos['Cantidad_Empresas'] / distritos['Poblacion']

            # 2️⃣ Inicializar listas para Treemap
            labels = []
            parents = []
            values = []

            # 🔹 Agregar distritos como único nivel
            for _, row in distritos.iterrows():
                labels.append(row['DISTRITO'])
                parents.append("")  # Nivel raíz, ya que no hay departamentos ni país
                values.append(row['empresas_habitantes'])

            # 3️⃣ Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value",
                textinfo="label+value",
            ))

            # 4️⃣ Mostrar gráfico
            fig.update_layout(title=f'Cantidad de empresas por cada habitante a nivel distrital en {selected_options}')
            
            distritos2 = dff2.groupby('DISTRITO').agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                Poblacion=('Poblacion', 'max'),
            ).reset_index()

            distritos2['Empresas_por_Habitantes'] = distritos2['Cantidad_Empresas'] / distritos2['Poblacion']
            distritos2 = distritos2.sort_values(by='Empresas_por_Habitantes', ascending=False)
            distritos2 = distritos2.loc[distritos2['DISTRITO'] != 'Sin Datos']  # Filtrar el distrito "Sin Datos"
            distritos3 = distritos2.head(20)

            datos = distritos3
            fig2 = px.bar(
                datos,
                x='DISTRITO',
                y='Empresas_por_Habitantes',
                #color='Seccion',  # Se mantiene la categorización por 'Seccion'
                #color_continuous_scale='Viridis',  # Aplica el mismo esquema de colores
                title='Cantidad de empresas por cada habitante en distritos top 20')


            data = distritos2.to_dict('records')
            columns=[
                {'name': 'DISTRITOS', 'id': 'DISTRITO'},
                {'name': 'EMPRESAS', 'id': 'Cantidad_Empresas'},
                {'name': 'POBLACION', 'id': 'Poblacion'},
                {'name': 'RELACION', 'id': 'Empresas_por_Habitantes'},
            ]



    #-------------------------------------------------------------------------------------------------------------------------------------

    
        elif selected_info == 'e':
            children = explicaciones.get('e') 

            distritos = dff.groupby('DISTRITO').agg(
                PARTICIPACION=('PARTICIPACION', 'sum'),
                Porcentaje_poblacion=('Porcentaje_poblacion', 'max')
            ).reset_index()

            # Calcular la relación de ganancias por población a nivel distrital
            distritos['ganancias_por_poblacion_distrital'] = distritos['PARTICIPACION'] / distritos['Porcentaje_poblacion']

            # Inicializar listas para el treemap
            labels = []
            parents = []
            values = []

            # Agregar distritos como únicos niveles
            for _, row in distritos.iterrows():
                labels.append(row['DISTRITO'])
                parents.append("")  # Nivel raíz, ya que no hay departamentos
                values.append(row['ganancias_por_poblacion_distrital'])

            # Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value",
                textinfo="label+value",
            ))

            fig.update_layout(title=f'Relación entre el porcentaje de ganancia y el porcentaje de población a nivel distrital en {selected_options}')

            
            distritos2 = dff2.groupby('DISTRITO').agg(
                PARTICIPACION=('PARTICIPACION', 'sum'),
                Porcentaje_poblacion=('Porcentaje_poblacion', 'max')
            ).reset_index()

            # Calcular la relación de ganancias por población a nivel distrital
            distritos2['Ganancias_por_Poblacion_Distrital'] = distritos2['PARTICIPACION'] / distritos2['Porcentaje_poblacion']
            distritos2 = distritos2.sort_values(by='Ganancias_por_Poblacion_Distrital', ascending=False)
            distritos2 = distritos2.loc[distritos2['DISTRITO'] != 'Sin Datos']  # Filtrar el distrito "Sin Datos"
            distritos3 = distritos2.head(20)

            datos = distritos3
            fig2 = px.bar(
                datos,
                x='DISTRITO',
                y='Ganancias_por_Poblacion_Distrital',
                #color='Seccion',  # Se mantiene la categorización por 'Seccion'
                #color_continuous_scale='Viridis',  # Aplica el mismo esquema de colores
                title='Relación entre el porcentaje de ganancia y el porcentaje de población')


            data = distritos2.to_dict('records')
            columns=[
                {'name': 'DISTRITOS', 'id': 'DISTRITO'},
                {'name': 'GANANCIAS (%)', 'id': 'PARTICIPACION'},
                {'name': 'POBLACION (%)', 'id': 'Porcentaje_poblacion'},
                {'name': 'RELACION', 'id': 'Ganancias_por_Poblacion_Distrital'},
            ]

#-----------------------------------------------------------------------------------------------------------------------------------

        elif selected_info == 'f':
            children = explicaciones.get('f') 
 
            distritos = dff.groupby(['DISTRITO'])['Actividad_principal'].nunique().reset_index()

            # 2️⃣ Inicializar listas para Treemap
            labels = []
            parents = []
            values = []

            # 🔹 Agregar distritos como único nivel
            for _, row in distritos.iterrows():
                labels.append(row['DISTRITO'])
                parents.append("")  # Nivel raíz, ya que no hay departamentos ni país
                values.append(row['Actividad_principal'])

            # 3️⃣ Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value",
                textinfo="label+value",
            ))

            
            # Mostrar gráfico
            fig.update_layout(title=f'Cantidad de actividades economicas desarrolladas en {selected_options}')
            
            distritos = dff2.groupby(['DISTRITO'])['Actividad_principal'].nunique().reset_index()
            distritos2 = distritos.sort_values(by='Actividad_principal', ascending=False)
            distritos3 = distritos2.head(20)
            distritos3 = distritos3.sort_values(by='Actividad_principal', ascending=False)

            datos = distritos3
            fig2 = px.bar(
                datos,
                x='DISTRITO',
                y='Actividad_principal',
                #color='Seccion',  # Se mantiene la categorización por 'Seccion'
                #color_continuous_scale='Viridis',  # Aplica el mismo esquema de colores
                title='Top 20 Distritos por cantidad de actividades economicas desarrolladas')


            data = distritos2.to_dict('records')
            columns=[
                {'name': 'DISTRITOS', 'id': 'DISTRITO'},
                {'name': 'Cantidad de Actividades', 'id': 'Actividad_principal'},
            ]




    return fig, fig2, columns, data, children
