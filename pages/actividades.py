import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output, dash_table, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

# Cargar el archivo CSV
df = pd.read_csv('actividades.csv')

descripciones = {
    'a': """
**Distribución de actividades por territorio según cantidad de empresas**

Este análisis muestra la cantidad de empresas que desarrollan la actividad económica seleccionada en cada departamento y distrito del país. Permite identificar en qué zonas del territorio nacional se concentra el desarrollo de dicha actividad, brindando una visión clara de su distribución geográfica.

Cuando se seleccionan varias actividades, el análisis también facilita la comparación entre ellas, tanto en términos de presencia como de alcance territorial.
""",
    'b': """
**Distribución de ganancias según actividad económica**

Este análisis muestra la participación de las diversas actividades económicas en las ganancias generadas en los distintos departamentos y distritos del país. Sirve para dimensionar la relevancia económica de cada sector, proporcionando una visión territorial del aporte que realizan a la generación de rentas empresariales.
""",
    'c': """
**Relación entre Ganancias y Empresas por Sector**

Este análisis muestra la relación existente entre las ganancias generadas por un sector o actividad económica y la cantidad de empresas que actúan en dicho sector, al dividir las ganancias totales del sector por el número de empresas. Además, se desglosa a nivel departamental y distrital, lo que permite identificar en qué zonas del país se concentran los sectores más rentables y productivos.

Esta medida resulta especialmente valiosa porque ofrece una visión del rendimiento económico promedio de las empresas en cada sector, facilitando la identificación de aquellos sectores que, a pesar de contar con un menor número de empresas, logran generar ganancias de forma más eficiente. Asimismo, ayuda a detectar áreas con alta saturación empresarial y relativamente baja rentabilidad, lo que puede sugerir la necesidad de intervenciones estratégicas o el ajuste en la asignación de recursos. En definitiva, esta proporción es una herramienta esencial para inversores, responsables de políticas públicas y empresarios, ya que resalta las oportunidades y fortalezas de cada sector en sentido de rentabilidad y productividad.
""",
    'd': """
**Cantidad de empresas según actividad económica**

Este análisis muestra la cantidad de empresas por sección, división y actividad económica. Sirve para dimensionar la cantidad de empresas en cada uno de estos niveles de agregación, brindando una mirada más detallada y profunda sobre la distribución empresarial según las actividades que desempeñan.
""",
    'e': """
**Ganancias por actividad económica**

Este análisis muestra la generación de ganancias por sección, división y actividad económica. El enfoque está puesto en la relevancia económica de cada sector en términos de rentabilidad.
Permite identificar qué actividades concentran mayores ingresos, ofreciendo una perspectiva clara sobre el aporte económico de cada rubro empresarial.
""",
    'f': """ 
**Cantidad de distritos por actividad económica**

Este análisis muestra la cantidad de distritos en los que se desarrolla cada actividad económica. Refleja el nivel de expansión territorial de una actividad, permitiendo evaluar qué tan extendida o concentrada está en el país.
Una actividad ampliamente distribuida sugiere una mayor adaptabilidad y popularidad, mientras que una distribución limitada puede indicar la necesidad de condiciones más específicas para su desarrollo.
""",

}

# Registrar la página en Dash multipágina
dash.register_page(__name__, path="/actividades")


# Inicializar la figura vacía para evitar errores
fig= go.Figure()
fig2= go.Figure()
# Layout de la página principal
layout = dbc.Container([

    # Título centrado
    dbc.Row([
        dbc.Col(
            html.H2("Análisis de características económicas del Paraguay", 
                    style={'textAlign': 'center', 'font-family': 'Avenir'}),
            width=12
        )
    ]),

    # Descripción
    dbc.Row([
        dbc.Col(
            html.P("Selecciona una opción en el menú para visualizar los datos (más opciones conlleva más tiempo de carga).", 
                   style={'textAlign': 'center', 'font-family': 'Cambria'}),
            width=8,
            className='mx-auto'
        )
    ]),

    html.Hr(),
    dbc.Row([
        dbc.Col(
            dcc.RadioItems(
                ['Seccion', 'Division', 'Actividad_principal'], 
                value='Seccion', 
                inline=True, 
                id='radioc',
                style={'font-family': 'Cambria'}
            ), 
            width=4,
            className='mx-auto'
        ),

    ]),

    html.Hr(),
    # Filtros y dropdowns
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='dropdown-optionsc',
                options=[],
                value=[],
                clearable=True,
                multi=True,
                placeholder='Selecciona una o varias opciones',
                style={'width': '100%', 'font-family': 'Cambria'}
            ),
            width=7,
            className='mx-auto'
        ),

        dbc.Col(
            dcc.Dropdown(
                id='infoc',
                options=[
                    {'label': 'Distribución de actividades por territorio s/ cantidad de empresas', 'value': 'a'},
                    {'label': 'Distribución de ganancias según actividad económica y territorio', 'value': 'b'},
                    {'label': 'Distribución de ganancias/empresas según actividad económica', 'value': 'c'},                    
                    {'label': 'Cantidad de empresas según por niveles actividad económica', 'value': 'd'},
                    {'label': 'Ganancias por niveles de actividad económica', 'value': 'e'},
                    {'label': 'Cantidad de distritos por actividad económica', 'value': 'f'},
                ],
                value='a',
                clearable=False,
                multi=False,
                placeholder='Selecciona una opción',
                style={'width': '100%', 'font-family': 'Cambria', 'maxHeight': '700px'},
            ),
            width=5,
            className='mx-auto'
        )
    ]),

   

    # Primer gráfico (centrado, ancho total)
    dbc.Row([
        dbc.Col(dcc.Graph(id='plot1c', figure=fig), width=12, md=12, sm=12, className='mx-auto'),
    ]),

    html.Hr(),

    dcc.Markdown(
        id='explicacion-containerb',
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


    # Segundo gráfico (centrado, ancho 8)
    dbc.Row([
        dbc.Col(dcc.Graph(id='plot2c', figure=fig2), width=10, className='mx-auto'),
    ]),

    html.Hr(),

    dbc.Tooltip(
        "Filtrá escribiendo en cada columna (El botón [Aa] desactiva la sensibilidad a mayúsculas.). Usá =, >, <, >=, <= para valores numéricos. Ejemplo: > 100 mostrará solo los valores mayores a 100.",
        target="tablec",
        placement="top",
    ),

    # Tabla
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='tablec',
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
                    'fontSize': '14px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'font-family': 'Cambria'
                },
                style_data={
                    'whiteSpace': 'normal',
                    'lineHeight': '15px'
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
    Output('dropdown-optionsc', 'options'),
    Output('dropdown-optionsc', 'value'),
    Input('radioc', 'value')
)
def dropdown(radio):
    if radio == 'Seccion':   
        valores = sorted(df['Seccion'].unique())
        options = [{"label": v, "value": v} for v in valores]
        value = ['ACTIVIDADES ADMINISTRATIVAS Y SERVICIOS DE APOYO']
    elif radio == 'Division':
        valores = sorted(df['Division'].unique())
        options = [{"label": v, "value": v} for v in valores]
        value = ['ACTIVIDADES ADMINISTRATIVAS DE OFICINAS Y OTRAS ACTIVIDADES AUXILIARES DE LAS EMPRESAS']
    elif radio == 'Actividad_principal':
        valores = sorted(df['Actividad_principal'].unique())
        options = [{"label": v, "value": v} for v in valores]
        value = ['01110 Cultivo de arroz']
    
    return options, value

@dash.callback(
    [Output('plot1c', 'figure'),
     Output('plot2c', 'figure'),
     Output('tablec', 'columns'),
     Output('tablec', 'data'),
     Output('explicacion-containerb', 'children')],  
    [State('radioc', 'value'),
     Input('dropdown-optionsc', 'value'),
     Input('infoc', 'value')]
)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def update_dashboard(radio, selected_options, selected_info):
    
#----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
    if radio == 'Seccion':
        seleccionados = selected_options
        dff = df.loc[df['Seccion'].isin(seleccionados)]
        dff2 = df.copy()
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------- 
#        
        if selected_info == 'a':
            
            children = descripciones.get('a') 

            # Agrupar y sumar las empresas por Sección, Departamento y Distrito
            df_secciones = dff.groupby(['Seccion', 'DEPARTAMENTO', 'DISTRITO'])['Cantidad_Empresas'].sum().reset_index()
            df_secciones2 = dff2.groupby(['Seccion', 'DEPARTAMENTO', 'DISTRITO'])['Cantidad_Empresas'].sum().reset_index()
            # Crear una columna de código único para Sección
            df_secciones['Codigo_Seccion'] = df_secciones['Seccion'].astype('category').cat.codes

            # Vincular el código de Sección a los Departamentos y Distritos
            df_secciones['DEPARTAMENTO_COD'] = df_secciones['Codigo_Seccion'].astype(str) + " - " + df_secciones['DEPARTAMENTO']
            df_secciones['DISTRITO_COD'] = df_secciones['DEPARTAMENTO_COD'] + " - " + df_secciones['DISTRITO']

            # Inicializar listas para el Treemap
            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar Secciones (Nivel Abuelo)
            for _, row in df_secciones[['Seccion', 'Codigo_Seccion']].drop_duplicates().iterrows():
                labels.append(row['Seccion'])
                parents.append('')  # No tiene padre, es la raíz
                values.append(df_secciones[df_secciones['Seccion'] == row['Seccion']]['Cantidad_Empresas'].sum())

            # 2️⃣ Agregar Departamentos (Nivel Padre)
            for _, row in df_secciones[['DEPARTAMENTO_COD', 'Seccion']].drop_duplicates().iterrows():
                labels.append(row['DEPARTAMENTO_COD'])
                parents.append(row['Seccion'])  # El padre de cada departamento es la sección
                values.append(df_secciones[df_secciones['DEPARTAMENTO_COD'] == row['DEPARTAMENTO_COD']]['Cantidad_Empresas'].sum())

            # 3️⃣ Agregar Distritos (Nivel Hijo)
            for _, row in df_secciones[['DISTRITO_COD', 'DEPARTAMENTO_COD']].drop_duplicates().iterrows():
                labels.append(row['DISTRITO_COD'])
                parents.append(row['DEPARTAMENTO_COD'])  # El padre de cada distrito es el departamento
                values.append(df_secciones[df_secciones['DISTRITO_COD'] == row['DISTRITO_COD']]['Cantidad_Empresas'].sum())

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",  # Información al pasar el mouse
                textinfo="label+value+percent entry",  # Mostrar etiqueta + valor + porcentaje
            ))

            # Mostrar gráfico
            fig.update_layout(title=f'Cantidad de empresas en cada territorio por secciones economicas')

            df_secciones2 = dff2.groupby(['Seccion', 'DEPARTAMENTO', 'DISTRITO'])['Cantidad_Empresas'].sum().reset_index()
            df_secciones2 = df_secciones2.sort_values(by='Cantidad_Empresas', ascending=False)
            df_secciones3 = df_secciones2.groupby(['Seccion', 'DEPARTAMENTO'])['Cantidad_Empresas'].sum().reset_index()
            df_secciones3 = df_secciones3.sort_values(by='Cantidad_Empresas', ascending=False)
            totales = df_secciones3.groupby('Seccion')['Cantidad_Empresas'].sum().reset_index()
            datos = df_secciones3
            fig2 = px.bar(
                            datos,
                            x='Seccion',
                            y='Cantidad_Empresas',
                            color='DEPARTAMENTO',  # Se mantiene la categorización por 'Seccion'
                            color_continuous_scale='Viridis',  # Aplica el mismo esquema de colores
                            title='Cantidad de empresas en cada territorio')
            # Ajustar la leyenda para que aparezca abajo
            for i, row in totales.iterrows():
                fig2.add_annotation(
                    x=row['Seccion'],
                    y=row['Cantidad_Empresas'],
                    text=f"{int(row['Cantidad_Empresas']):,}",  # Formato con separador de miles
                    showarrow=False,
                    yshift=22,
                    font=dict(color="black", size=12),
                    textangle=90
                )

            # Layout final
            fig2.update_layout(
                showlegend=True,
                height=1200
            )


            # Para la tabla se usan los datos filtrados
            from dash.dash_table.Format import Format, Group
            data = df_secciones2.to_dict('records')
            columns=[
                {'name': 'SECCION', 'id': 'Seccion'},
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'DISTRITO', 'id': 'DISTRITO'},
                {'name': 'CANTIDAD', 'id': 'Cantidad_Empresas', 'type': 'numeric', 'format': Format(
                        group=Group.yes,              # Activa el separador de miles
                        group_delimiter=',',          # Usa coma como separador
                        precision=0,                  # Sin decimales
                        scheme='f'                    # Notación fija (no científica)
                    )},       
            ]



#-------------------------------------------------------------------------------------------------------------------------------
#         
        elif selected_info == 'b':

            children = descripciones.get('b') 

            df_secciones = dff.groupby(['Seccion', 'DEPARTAMENTO', 'DISTRITO'])['PARTICIPACION'].sum().reset_index()
            df_secciones2 = dff2.groupby(['Seccion', 'DEPARTAMENTO', 'DISTRITO'])['PARTICIPACION'].sum().reset_index()
            # Crear una columna de código único para Sección
            df_secciones['Codigo_Seccion'] = df_secciones['Seccion'].astype('category').cat.codes

            # Vincular el código de Sección a los Departamentos y Distritos
            df_secciones['DEPARTAMENTO_COD'] = df_secciones['Codigo_Seccion'].astype(str) + " - " + df_secciones['DEPARTAMENTO']
            df_secciones['DISTRITO_COD'] = df_secciones['DEPARTAMENTO_COD'] + " - " + df_secciones['DISTRITO']

            # Inicializar listas para el Treemap
            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar Secciones (Nivel Abuelo)
            for _, row in df_secciones[['Seccion', 'Codigo_Seccion']].drop_duplicates().iterrows():
                labels.append(row['Seccion'])
                parents.append('')  # No tiene padre, es la raíz
                values.append(df_secciones[df_secciones['Seccion'] == row['Seccion']]['PARTICIPACION'].sum())

            # 2️⃣ Agregar Departamentos (Nivel Padre)
            for _, row in df_secciones[['DEPARTAMENTO_COD', 'Seccion']].drop_duplicates().iterrows():
                labels.append(row['DEPARTAMENTO_COD'])
                parents.append(row['Seccion'])  # El padre de cada departamento es la sección
                values.append(df_secciones[df_secciones['DEPARTAMENTO_COD'] == row['DEPARTAMENTO_COD']]['PARTICIPACION'].sum())

            # 3️⃣ Agregar Distritos (Nivel Hijo)
            for _, row in df_secciones[['DISTRITO_COD', 'DEPARTAMENTO_COD']].drop_duplicates().iterrows():
                labels.append(row['DISTRITO_COD'])
                parents.append(row['DEPARTAMENTO_COD'])  # El padre de cada distrito es el departamento
                values.append(df_secciones[df_secciones['DISTRITO_COD'] == row['DISTRITO_COD']]['PARTICIPACION'].sum())

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",  # Información al pasar el mouse
                textinfo="label+value+percent entry",  # Mostrar etiqueta + valor + porcentaje
            ))
            # Mostrar gráfico
            fig.update_layout(title=f'Distribucion de ganancias en cada territorio por secciones economicas')

            df_secciones2 = dff2.groupby(['Seccion', 'DEPARTAMENTO', 'DISTRITO'])['PARTICIPACION'].sum().reset_index()
            df_secciones2 = df_secciones2.sort_values(by='PARTICIPACION', ascending=False)
            df_secciones3 = df_secciones2.groupby(['Seccion', 'DEPARTAMENTO'])['PARTICIPACION'].sum().reset_index()
            df_secciones3 = df_secciones3.sort_values(by='PARTICIPACION', ascending=False)
            totales = df_secciones3.groupby('Seccion')['PARTICIPACION'].sum().reset_index()
            datos = df_secciones3
            fig2 = px.bar(
                            datos,
                            x='Seccion',
                            y='PARTICIPACION',
                            color='DEPARTAMENTO',  # Se mantiene la categorización por 'Seccion'
                            color_continuous_scale='Viridis',  # Aplica el mismo esquema de colores
                            title='Participacion de sectores en la ganancia nacional')
            # Ajustar la leyenda para que aparezca abajo
            # Ajustar la leyenda para que aparezca abajo
            for i, row in totales.iterrows():
                fig2.add_annotation(
                    x=row['Seccion'],
                    y=row['PARTICIPACION'],
                    text=f"{int(row['PARTICIPACION']):,}",  # Formato con separador de miles
                    showarrow=False,
                    yshift=22,
                    font=dict(color="black", size=12),
                    textangle=90
                )

            # Layout final
            fig2.update_layout(
                showlegend=True,
                height=1200
            )




            # Para la tabla se usan los datos filtrados
        
            data = df_secciones2.to_dict('records')
            
            from dash.dash_table.Format import Format, Scheme

            columns = [
                {'name': 'SECCION', 'id': 'Seccion'},
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'DISTRITO', 'id': 'DISTRITO'},
                {
                    'name': 'PARTICIPACION (%)',
                    'id': 'PARTICIPACION',
                    'type': 'numeric',
                    'format': Format(
                        scheme=Scheme.fixed,   # Notación fija
                        precision=2            # Dos decimales
                    )
                },
            ]
#-----------------------------------------------------------------------------------------------------------------------------------
        elif selected_info == 'c':
            children = descripciones.get('c')

            # Agrupar globalmente por Sección (sector económico)
            secciones2 = dff2.groupby('Seccion').agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            ).reset_index()

            # Total global (para todos los sectores)
            global_empresas = dff2['Cantidad_Empresas'].sum()
            

            # Calcular el porcentaje global de empresas y la rentabilidad base para cada Sección
            secciones2['porcentaje_empresas'] = secciones2['Cantidad_Empresas'] / global_empresas * 100
            secciones2['rentabilidad_empresas'] = secciones2.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100) 
                    if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            secciones2 = secciones2.fillna(0)


            # Nivel 1: Sección (sector económico)
            df_seccion = dff.groupby('Seccion', as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_seccion['porcentaje_empresas'] = df_seccion['Cantidad_Empresas'] / global_empresas * 100
            df_seccion['rentabilidad_empresas'] = df_seccion.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                    if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_seccion = df_seccion.fillna(0)
            df_seccion['SEC_ID'] = df_seccion['Seccion']  # Identificador único para el nivel Sección

            # Nivel 2: Departamento, agrupando por Seccion y DEPARTAMENTO
            df_departamento = dff.groupby(['Seccion','DEPARTAMENTO'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_departamento['porcentaje_empresas'] = df_departamento['Cantidad_Empresas'] / global_empresas * 100
            df_departamento['rentabilidad_empresas'] = df_departamento.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                    if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_departamento = df_departamento.fillna(0)
            # Crear un ID combinando Seccion y Departamento
            df_departamento['DEP_ID'] = df_departamento['Seccion'] + ' - ' + df_departamento['DEPARTAMENTO']

            # Nivel 3: Distrito, agrupando por Seccion, DEPARTAMENTO y DISTRITO
            df_distrito = dff.groupby(['Seccion','DEPARTAMENTO','DISTRITO'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_distrito['porcentaje_empresas'] = df_distrito['Cantidad_Empresas'] / global_empresas * 100
            df_distrito['rentabilidad_empresas'] = df_distrito.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                    if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_distrito = df_distrito.fillna(0)
            # Crear un ID: Seccion - Departamento - Distrito
            df_distrito['DIST_ID'] = df_distrito['Seccion'] + ' - ' + df_distrito['DEPARTAMENTO'] + ' - ' + df_distrito['DISTRITO']


            ids = []
            labels = []
            parents = []
            values = []

            # Nivel 1: Sección
            for _, row in df_seccion.iterrows():
                ids.append(row['SEC_ID'])
                labels.append(row['Seccion'])
                parents.append('')  # Nivel superior
                values.append(row['rentabilidad_empresas'])

            # Nivel 2: Departamento
            for _, row in df_departamento.iterrows():
                ids.append(row['DEP_ID'])
                labels.append(row['DEPARTAMENTO'])
                parents.append(row['Seccion'])  # El padre es la Sección
                values.append(row['rentabilidad_empresas'])

            # Nivel 3: Distrito
            for _, row in df_distrito.iterrows():
                ids.append(row['DIST_ID'])
                labels.append(row['DISTRITO'])
                # El padre es el ID del departamento, que se compone de "Seccion - DEPARTAMENTO"
                padre = row['Seccion'] + ' - ' + row['DEPARTAMENTO']
                parents.append(padre)
                values.append(row['rentabilidad_empresas'])

            fig = go.Figure(go.Treemap(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",
                textinfo="label+value+percent entry"
            ))

            fig.update_layout(title=f"Rentabilidad por sector economico (treemap): Sección, Departamento y Distrito en {selected_options}")

            # Usamos los datos globales por Sección (secciones2) para el gráfico de barras.
            secciones2 = secciones2.sort_values(by='rentabilidad_empresas', ascending=False) 
  
            fig2 = px.bar(
                secciones2,
                x='Seccion',
                y='rentabilidad_empresas',
                title="Participación (Rentabilidad) por sector (Sección)"
            )



            data = secciones2.to_dict('records')
            columns = [
                {'name': 'SECCION', 'id': 'Seccion'},
                {'name': 'GANANCIAS (%)', 'id': 'PARTICIPACION'},
                {'name': 'EMPRESAS (%)', 'id': 'porcentaje_empresas'},
                {'name': 'RELACION', 'id': 'rentabilidad_empresas'}
            ]

#-----------------------------------------------------------------------------------------------------------------------------------

        elif selected_info == 'd':

            children = descripciones.get('d')

            # Agrupar y sumar las empresas por Sección, Division y actividad principal
            df_secciones = dff.groupby(['Seccion', 'Division', 'Actividad_principal'])['Cantidad_Empresas'].sum().reset_index()
            df_secciones2 = dff2.groupby(['Seccion', 'Division', 'Actividad_principal'])['Cantidad_Empresas'].sum().reset_index()
            # Crear una columna de código único para Sección
            df_secciones['Codigo_Seccion'] = df_secciones['Seccion'].astype('category').cat.codes
            df_secciones['Division_cod'] = df_secciones['Codigo_Seccion'].astype(str)+ " - " + df_secciones['Division']
            df_secciones['Actividad_principal_cod'] = df_secciones['Division_cod'] + " - " + df_secciones['Actividad_principal']


            # Inicializar listas para el Treemap
            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar Secciones (Nivel Abuelo)
            for _, row in df_secciones[['Seccion', 'Codigo_Seccion']].drop_duplicates().iterrows():
                labels.append(row['Seccion'])
                parents.append('')  # No tiene padre, es la raíz
                values.append(df_secciones[df_secciones['Seccion'] == row['Seccion']]['Cantidad_Empresas'].sum())

            # 2️⃣ Agregar Departamentos (Nivel Padre)
            for _, row in df_secciones[['Seccion', 'Division_cod']].drop_duplicates().iterrows():
                labels.append(row['Division_cod'])
                parents.append(row['Seccion'])  # El padre de cada division es la sección
                values.append(df_secciones[df_secciones['Division_cod'] == row['Division_cod']]['Cantidad_Empresas'].sum())

            # 3️⃣ Agregar Distritos (Nivel Hijo)
            for _, row in df_secciones[['Division_cod', 'Actividad_principal_cod']].drop_duplicates().iterrows():
                labels.append(row['Actividad_principal_cod'])
                parents.append(row['Division_cod'])  # El padre de cada actividad es la division
                values.append(df_secciones[df_secciones['Actividad_principal_cod'] == row['Actividad_principal_cod']]['Cantidad_Empresas'].sum())

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",  # Información al pasar el mouse
                textinfo="label+value+percent entry",  # Mostrar etiqueta + valor + porcentaje
            ))
            fig.update_layout(title='Cantidad de empresas segun secciones economicas seleccionadas')

            df_secciones2 = df_secciones2.sort_values(by='Cantidad_Empresas', ascending=False)
            df_secciones3 = df_secciones2.groupby(['Seccion', 'Division'])['Cantidad_Empresas'].sum().reset_index()
            df_secciones3 = df_secciones3.sort_values(by='Cantidad_Empresas', ascending=False)
            totales = df_secciones3.groupby('Seccion')['Cantidad_Empresas'].sum().reset_index()

            # Gráfico de barras apiladas
            fig2 = px.bar(
                df_secciones3,
                x='Seccion',
                y='Cantidad_Empresas',
                color='Division',
                title='Cantidad de empresas segun secciones economicas',
                color_discrete_sequence=px.colors.sequential.Viridis
            )

            # Agregar anotaciones con el total por Sección
            for i, row in totales.iterrows():
                fig2.add_annotation(
                    x=row['Seccion'],
                    y=row['Cantidad_Empresas'],
                    text=f"{int(row['Cantidad_Empresas']):,}",  # Formato con separador de miles
                    showarrow=False,
                    yshift=22,
                    font=dict(color="black", size=12),
                    textangle=90
                )

            # Layout final
            fig2.update_layout(
                showlegend=False,
                height=1200
            )


            # Para la tabla se usan los datos filtrados
            df_secciones4 = df_secciones2.groupby('Seccion')['Cantidad_Empresas'].sum().reset_index()
            data = df_secciones4.to_dict('records')
            from dash.dash_table.Format import Format, Scheme, Group
            columns=[
                {'name': 'SECCION', 'id': 'Seccion'},
                {'name': 'CANTIDAD', 'id': 'Cantidad_Empresas', 'type': 'numeric', 'format': Format(
                        group=Group.yes,              # Activa el separador de miles
                        group_delimiter=',',          # Usa coma como separador
                        precision=0,                  # Sin decimales
                        scheme='f'                    # Notación fija (no científica)
                    )},       
            ]

 #----------------------------------------------------------------------------------------------------------------------------------------------------------       
        elif selected_info == 'e':

            children = descripciones.get('e')

# Cantidad de empresas por cada habitante 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            pd.set_option('display.float_format', '{:,.0f}'.format)

            df_secciones = dff.groupby(['Seccion', 'Division', 'Actividad_principal'])['Aporte'].sum().reset_index()
            df_secciones2 = dff2.groupby(['Seccion', 'Division', 'Actividad_principal'])['Aporte'].sum().reset_index()
            df_secciones['GANANCIA'] = df_secciones['Aporte'] * 10
            df_secciones2['GANANCIA'] = df_secciones2['Aporte'] * 10
            df_secciones2['GANANCIA'] = df_secciones2['GANANCIA'].astype(float)

            # Crear una columna de código único para Sección
            df_secciones['Codigo_Seccion'] = df_secciones['Seccion'].astype('category').cat.codes
            df_secciones['Division_cod'] = df_secciones['Codigo_Seccion'].astype(str)+ " - " + df_secciones['Division']
            df_secciones['Actividad_principal_cod'] = df_secciones['Division_cod'] + " - " + df_secciones['Actividad_principal']


            # Rehacer listas con textos formateados
            labels = []
            parents = []
            values = []
            text = []
            hovertext = []

            # Secciones (abuelo)
            for _, row in df_secciones[['Seccion', 'Codigo_Seccion']].drop_duplicates().iterrows():
                total = int(df_secciones[df_secciones['Seccion'] == row['Seccion']]['GANANCIA'].sum())
                labels.append(row['Seccion'])
                parents.append('')
                values.append(total)
                text.append(f"{row['Seccion']}<br>{total:,.0f}")
                hovertext.append(f"Sección: {row['Seccion']}<br>Ganancia: {total:,.0f}")

            # Divisiones (padre)
            for _, row in df_secciones[['Seccion', 'Division_cod']].drop_duplicates().iterrows():
                total = int(df_secciones[df_secciones['Division_cod'] == row['Division_cod']]['GANANCIA'].sum())
                labels.append(row['Division_cod'])
                parents.append(row['Seccion'])
                values.append(total)
                text.append(f"{row['Division_cod']}<br>{total:,.0f}")
                hovertext.append(f"División: {row['Division_cod']}<br>Ganancia: {total:,.0f}")

            # Actividades (hijo)
            for _, row in df_secciones[['Division_cod', 'Actividad_principal_cod']].drop_duplicates().iterrows():
                total = int(df_secciones[df_secciones['Actividad_principal_cod'] == row['Actividad_principal_cod']]['GANANCIA'].sum())
                labels.append(row['Actividad_principal_cod'])
                parents.append(row['Division_cod'])
                values.append(total)
                text.append(f"{row['Actividad_principal_cod']}<br>{total:,.0f}")
                hovertext.append(f"Actividad: {row['Actividad_principal_cod']}<br>Ganancia: {total:,.0f}")

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                text=text,
                hovertext=hovertext,
                hoverinfo='text',
                textinfo='text'
            ))

            fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
            fig.update_layout(title='Ganancias por secciones economicas seleccionadas. Total Pais = G$ 53.682.677.926.130')

            df_secciones2 = df_secciones2.sort_values(by='GANANCIA', ascending=False)
            df_secciones3 = df_secciones2.groupby(['Seccion', 'Division'])['GANANCIA'].sum().reset_index()
            totales = df_secciones3.groupby('Seccion')['GANANCIA'].sum().reset_index()

            df_secciones2 = df_secciones2.sort_values(by='GANANCIA', ascending=False)
            df_secciones3 = df_secciones2.groupby(['Seccion', 'Division'])['GANANCIA'].sum().reset_index()
            df_secciones3 = df_secciones3.sort_values(by='GANANCIA', ascending=False)
            totales = df_secciones3.groupby('Seccion')['GANANCIA'].sum().reset_index()

            fig2 = px.bar(
                df_secciones3,
                x='Seccion',
                y='GANANCIA',
                color='Division',
                title='Ganancias por secciones económicas',
                color_discrete_sequence=px.colors.sequential.Viridis
            )

            # Agregar anotaciones con el total por Sección
            for i, row in totales.iterrows():
                fig2.add_annotation(
                    x=row['Seccion'],
                    y=row['GANANCIA'],
                    text=f"{int(row['GANANCIA']):,}".replace(",", "."),  # ✅ Separador de miles con punto
                    showarrow=False,
                    yshift=70,
                    font=dict(color="black", size=12),
                    textangle=90
                )

            # Formatear eje Y en miles de millones de guaraníes (eje nomás, sin cambiar datos)
            max_val = df_secciones3['GANANCIA'].max()
            tick_vals = np.arange(0, max_val + 1e12, 1e12)
            tick_texts = [f"{int(val / 1e9):,}".replace(",", ".") for val in tick_vals]

            fig2.update_layout(
                showlegend=False,
                height=1200,
                yaxis=dict(
                    title="Ganancia (miles de millones de Gs.)",
                    tickvals=tick_vals,
                    ticktext=tick_texts,
                )
            )




            # Para la tabla se usan los datos filtrados
            df_secciones4 = df_secciones2.groupby('Seccion')['GANANCIA'].sum().reset_index()

            # Pasar a la tabla
            data = df_secciones4.to_dict('records')

            # Columnas (GANANCIA se mantiene numérica, GANANCIA_FORMAT es solo visual)
            from dash.dash_table.Format import Format, Group

            columns = [
                {'name': 'SECCIONES', 'id': 'Seccion'},
                {
                    'name': 'GANANCIA (Gs)',
                    'id': 'GANANCIA',
                    'type': 'numeric',
                    'format': Format(
                        group=Group.yes,              # Activa el separador de miles
                        group_delimiter=',',          # Usa coma como separador
                        precision=0,                  # Sin decimales
                        scheme='f'                    # Notación fija (no científica)
                    )
                },
            ]

 #----------------------------------------------------------------------------------------------------------------------------------------


        elif selected_info == 'f':

            children = descripciones.get('f')

# Cantidad de distritos por seccion economica
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
          

            df_secciones = dff.groupby(['Seccion'])['DISTRITO'].nunique().reset_index()
            df_secciones2 = dff2.groupby(['Seccion'])['DISTRITO'].nunique().reset_index()

            # 2️⃣ Inicializar listas para Treemap
            labels = []
            parents = []
            values = []

            # 🔹 Agregar distritos como único nivel
            for _, row in df_secciones.iterrows():
                labels.append(row['Seccion'])
                parents.append("")  # Nivel raíz, ya que no hay departamentos ni país
                values.append(row['DISTRITO'])

            # 3️⃣ Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value",
                textinfo="label+value",
            ))


            fig.update_layout(title='Cantidad de distritos en las que se desarrollan las secciones seleccionadas. Total de distritos = 253')

            datos = df_secciones2.sort_values(by='DISTRITO', ascending=False)
            # Gráfico de barras apiladas
            fig2 = px.bar(
                datos,
                x='Seccion',
                y='DISTRITO',
                title='Cantidad de distritos en las que se desarrollan las secciones'
            )

            # Layout final
            fig2.update_layout(
                showlegend=False,
                height=800
            )


            # Para la tabla se usan los datos filtrados
            data = df_secciones2.to_dict('records')
            columns=[
                {'name': 'SECCION', 'id': 'Seccion'},
                {'name': 'DISTRITOS', 'id': 'DISTRITO'},
            ]


#-----------------------------------------------------------------------------------------------------------------------------------------------------------       
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    elif radio == 'Division':
        seleccionados = selected_options
        dff = df.loc[df['Division'].isin(seleccionados)]  
        dff2 = df.copy()    

    #------------------------------------------------------------------------------------------------------------------------------------------------------------- 
    #        
        if selected_info == 'a':

            children = descripciones.get('a')

            # Agrupar y sumar las empresas por Division, Departamento y Distrito
            df_divisiones = dff.groupby(['Division', 'DEPARTAMENTO', 'DISTRITO'])['Cantidad_Empresas'].sum().reset_index()
            df_divisiones2 = dff2.groupby(['Division', 'DEPARTAMENTO', 'DISTRITO'])['Cantidad_Empresas'].sum().reset_index()
            # Crear una columna de código único para Division
            df_divisiones['Codigo_Division'] = df_divisiones['Division'].astype('category').cat.codes

            # Vincular el código de Division a los Departamentos y Distritos
            df_divisiones['DEPARTAMENTO_COD'] = df_divisiones['Codigo_Division'].astype(str) + " - " + df_divisiones['DEPARTAMENTO']
            df_divisiones['DISTRITO_COD'] = df_divisiones['DEPARTAMENTO_COD'] + " - " + df_divisiones['DISTRITO']

            # Inicializar listas para el Treemap
            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar Division (Nivel Abuelo)
            for _, row in df_divisiones[['Division', 'Codigo_Division']].drop_duplicates().iterrows():
                labels.append(row['Division'])
                parents.append('')  # No tiene padre, es la raíz
                values.append(df_divisiones[df_divisiones['Division'] == row['Division']]['Cantidad_Empresas'].sum())

            # 2️⃣ Agregar Departamentos (Nivel Padre)
            for _, row in df_divisiones[['DEPARTAMENTO_COD', 'Division']].drop_duplicates().iterrows():
                labels.append(row['DEPARTAMENTO_COD'])
                parents.append(row['Division'])  # El padre de cada departamento es la Division
                values.append(df_divisiones[df_divisiones['DEPARTAMENTO_COD'] == row['DEPARTAMENTO_COD']]['Cantidad_Empresas'].sum())

            # 3️⃣ Agregar Distritos (Nivel Hijo)
            for _, row in df_divisiones[['DISTRITO_COD', 'DEPARTAMENTO_COD']].drop_duplicates().iterrows():
                labels.append(row['DISTRITO_COD'])
                parents.append(row['DEPARTAMENTO_COD'])  # El padre de cada distrito es el departamento
                values.append(df_divisiones[df_divisiones['DISTRITO_COD'] == row['DISTRITO_COD']]['Cantidad_Empresas'].sum())

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",  # Información al pasar el mouse
                textinfo="label+value+percent entry",  # Mostrar etiqueta + valor + porcentaje
            ))

            # Mostrar gráfico
            fig.update_layout(title=f'Cantidad de empresas en cada territorio por secciones economicas')

            df_divisiones3 = dff2.groupby('Division')['Cantidad_Empresas'].sum().reset_index()
            df_divisiones3 = df_divisiones3.sort_values(by='Cantidad_Empresas', ascending=False)
            df_divisiones3 = df_divisiones3.head(20)
            datos = df_divisiones3
            fig2 = px.bar(
                            datos,
                            x='Division',
                            y='Cantidad_Empresas',
                            title='Cantidad de empresas de las 20 divisiones principales. Total en datos disponibles = 188.905 empresas')
            # Ajustar la leyenda para que aparezca abajo
            fig2.update_layout(
                height=1000  # Ajustar la altura si es necesario
            )



            # Para la tabla se usan los datos filtrados
            from dash.dash_table.Format import Format, Group
            data = df_divisiones2.to_dict('records')
            columns=[
                {'name': 'DIVISION', 'id': 'Division'},
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'DISTRITO', 'id': 'DISTRITO'},
                {'name': 'CANTIDAD', 'id': 'Cantidad_Empresas', 'type': 'numeric', 'format': Format(
                        group=Group.yes,              # Activa el separador de miles
                        group_delimiter=',',          # Usa coma como separador
                        precision=0,                  # Sin decimales
                        scheme='f'                    # Notación fija (no científica)
                    )},       
            ]



    #-------------------------------------------------------------------------------------------------------------------------------
    #         
        elif selected_info == 'b':

            children = descripciones.get('b')   

            df_divisiones = dff.groupby(['Division', 'DEPARTAMENTO', 'DISTRITO'])['PARTICIPACION'].sum().reset_index()
            # Crear una columna de código único para Division
            df_divisiones['Codigo_Division'] = df_divisiones['Division'].astype('category').cat.codes

            # Vincular el código de Division a los Departamentos y Distritos
            df_divisiones['DEPARTAMENTO_COD'] = df_divisiones['Codigo_Division'].astype(str) + " - " + df_divisiones['DEPARTAMENTO']
            df_divisiones['DISTRITO_COD'] = df_divisiones['DEPARTAMENTO_COD'] + " - " + df_divisiones['DISTRITO']

            # Inicializar listas para el Treemap
            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar Division (Nivel Abuelo)
            for _, row in df_divisiones[['Division', 'Codigo_Division']].drop_duplicates().iterrows():
                labels.append(row['Division'])
                parents.append('')  # No tiene padre, es la raíz
                values.append(df_divisiones[df_divisiones['Division'] == row['Division']]['PARTICIPACION'].sum())

            # 2️⃣ Agregar Departamentos (Nivel Padre)
            for _, row in df_divisiones[['DEPARTAMENTO_COD', 'Division']].drop_duplicates().iterrows():
                labels.append(row['DEPARTAMENTO_COD'])
                parents.append(row['Division'])  # El padre de cada departamento es la sección
                values.append(df_divisiones[df_divisiones['DEPARTAMENTO_COD'] == row['DEPARTAMENTO_COD']]['PARTICIPACION'].sum())

            # 3️⃣ Agregar Distritos (Nivel Hijo)
            for _, row in df_divisiones[['DISTRITO_COD', 'DEPARTAMENTO_COD']].drop_duplicates().iterrows():
                labels.append(row['DISTRITO_COD'])
                parents.append(row['DEPARTAMENTO_COD'])  # El padre de cada distrito es el departamento
                values.append(df_divisiones[df_divisiones['DISTRITO_COD'] == row['DISTRITO_COD']]['PARTICIPACION'].sum())

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",  # Información al pasar el mouse
                textinfo="label+value+percent entry",  # Mostrar etiqueta + valor + porcentaje
            ))
            # Mostrar gráfico
            fig.update_layout(title=f'Distribucion de ganancias en cada territorio por divisiones economicas')

            df_divisiones2 = dff2.groupby(['Division', 'DEPARTAMENTO', 'DISTRITO'])['PARTICIPACION'].sum().reset_index()
            df_divisiones3 = df_divisiones2.groupby('Division')['PARTICIPACION'].sum().reset_index()
            df_divisiones3 = df_divisiones3.sort_values(by='PARTICIPACION', ascending=False)
            df_divisiones3 = df_divisiones3.head(20)
            df_divisiones3 = df_divisiones3.sort_values(by='PARTICIPACION', ascending=False)
            datos = df_divisiones3
            fig2 = px.bar(
                            datos,
                            x='Division',
                            y='PARTICIPACION',
                            title='Participacion porcentual de sectores en la ganancia nacional')
            # Ajustar la leyenda para que aparezca abajo
            fig2.update_layout(
                height=1200  # Ajustar la altura si es necesario
                        )

            # Para la tabla se usan los datos filtrados
        
            data = df_divisiones2.to_dict('records')
            from dash.dash_table.Format import Format, Scheme

            columns = [
                {'name': 'DIVISIONES', 'id': 'Division'},
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'DISTRITO', 'id': 'DISTRITO'},
                {
                    'name': 'PARTICIPACION (%)',
                    'id': 'PARTICIPACION',
                    'type': 'numeric',
                    'format': Format(
                        scheme=Scheme.fixed,   # Notación fija
                        precision=4            # 4 decimales
                    )
                },
            ]
#-----------------------------------------------------------------------------------------------------------------------------------
        elif selected_info == 'c':
            children = descripciones.get('c')

            # Agrupar globalmente por DIVISION
            divisiones2 = dff2.groupby('Division').agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            ).reset_index()

            # Calcular los totales globales (para usar en el cálculo de porcentajes en el DataFrame filtrado)
            global_empresas = dff2['Cantidad_Empresas'].sum()


            # Calcular el porcentaje global de empresas y la rentabilidad base para cada División
            divisiones2['porcentaje_empresas'] = divisiones2['Cantidad_Empresas'] / global_empresas * 100
            divisiones2['rentabilidad_empresas'] = divisiones2.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                    if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            divisiones2 = divisiones2.fillna(0)

            # Nivel 1: División (agrupación a nivel Division)
            df_division = dff.groupby('Division', as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_division['porcentaje_empresas'] = df_division['Cantidad_Empresas'] / global_empresas * 100
            df_division['rentabilidad_empresas'] = df_division.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                    if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_division = df_division.fillna(0)
            df_division['DIV_ID'] = df_division['Division']  # Identificador único para el nivel división

            # Nivel 2: Departamento, agrupando por Division y DEPARTAMENTO
            df_departamento = dff.groupby(['Division', 'DEPARTAMENTO'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_departamento['porcentaje_empresas'] = df_departamento['Cantidad_Empresas'] / global_empresas * 100
            df_departamento['rentabilidad_empresas'] = df_departamento.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                    if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_departamento = df_departamento.fillna(0)
            df_departamento['DEP_ID'] = df_departamento['Division'] + ' - ' + df_departamento['DEPARTAMENTO']

            # Nivel 3: Distrito, agrupando por Division, DEPARTAMENTO y DISTRITO
            df_distrito = dff.groupby(['Division', 'DEPARTAMENTO', 'DISTRITO'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_distrito['porcentaje_empresas'] = df_distrito['Cantidad_Empresas'] / global_empresas * 100
            df_distrito['rentabilidad_empresas'] = df_distrito.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                    if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0) else 0,
                axis=1
            )
            df_distrito = df_distrito.fillna(0)
            df_distrito['DIST_ID'] = df_distrito['Division'] + ' - ' + df_distrito['DEPARTAMENTO'] + ' - ' + df_distrito['DISTRITO']


            ids = []
            labels = []
            parents = []
            values = []

            # Nivel 1: División
            for _, row in df_division.iterrows():
                ids.append(row['DIV_ID'])
                labels.append(row['Division'])
                parents.append('')  # Sin padre (nivel superior)
                values.append(row['rentabilidad_empresas'])

            # Nivel 2: Departamento
            for _, row in df_departamento.iterrows():
                ids.append(row['DEP_ID'])
                labels.append(row['DEPARTAMENTO'])
                # El padre es el valor de 'Division' (ID del nivel 1)
                parents.append(row['Division'])
                values.append(row['rentabilidad_empresas'])

            # Nivel 3: Distrito
            for _, row in df_distrito.iterrows():
                ids.append(row['DIST_ID'])
                labels.append(row['DISTRITO'])
                # El padre es la combinación: Division - DEPARTAMENTO
                padre = row['Division'] + ' - ' + row['DEPARTAMENTO']
                parents.append(padre)
                values.append(row['rentabilidad_empresas'])

            fig = go.Figure(go.Treemap(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",
                textinfo="label+value+percent entry"
            ))
            fig.update_layout(title=f"Rentabilidad por sector economico (treemap): División, Departamento y Distrito en {selected_options}")

            divisiones2 = divisiones2.sort_values(by='rentabilidad_empresas', ascending=False)
            divisiones3 = divisiones2.head(20)
            # Para el gráfico de barras usamos los datos globales por División (divisiones2)
            fig2 = px.bar(
                divisiones3,
                x='Division',
                y='rentabilidad_empresas',
                title="Participación (Rentabilidad) por sector (Division)"
            )

   
            data = divisiones2.to_dict('records')
            columns = [
                {'name': 'DIVISION', 'id': 'Division'},
                {'name': 'GANANCIAS (%)', 'id': 'PARTICIPACION'},
                {'name': 'EMPRESAS (%)', 'id': 'porcentaje_empresas'},
                {'name': 'RELACION', 'id': 'rentabilidad_empresas'}
            ]

#-----------------------------------------------------------------------------------------------------------------------------------

        elif selected_info == 'd':

            children = descripciones.get('d') 



            # Agrupar y sumar las empresas por División y Actividad Principal
            df_divisiones = dff.groupby(['Division', 'Actividad_principal'])['Cantidad_Empresas'].sum().reset_index()
            df_divisiones2 = dff2.groupby(['Division', 'Actividad_principal'])['Cantidad_Empresas'].sum().reset_index()
            df_divisiones = df_divisiones.loc[df_divisiones['Division'] != 'Desconocido']
            df_divisiones2 = df_divisiones2.loc[df_divisiones2['Division'] != 'Desconocido']
            # Crear una columna de código único para División
            df_divisiones['Codigo_Division'] = df_divisiones['Division'].astype('category').cat.codes.astype(str)
            df_divisiones['Actividad_principal_cod'] = df_divisiones['Codigo_Division'] + " - " + df_divisiones['Actividad_principal']

            # Inicializar listas para el Treemap
            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar División (Nivel raíz)
            for division in df_divisiones['Division'].unique():
                total_empresas = df_divisiones[df_divisiones['Division'] == division]['Cantidad_Empresas'].sum()
                labels.append(division)
                parents.append("")  # Nivel raíz
                values.append(total_empresas)

            # 2️⃣ Agregar Actividades principales (Nivel hijo)
            for _, row in df_divisiones.iterrows():
                labels.append(row['Actividad_principal_cod'])
                parents.append(row['Division'])  # El padre es la División
                values.append(row['Cantidad_Empresas'])

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent parent",
                textinfo="label+value+percent parent"
            ))

            fig.update_layout(title='Cantidad de empresas según divisiones económicas seleccionadas')

            df_divisiones3 = df_divisiones2.groupby(['Division'])['Cantidad_Empresas'].sum().reset_index()
            df_divisiones3 = df_divisiones3.sort_values(by='Cantidad_Empresas', ascending=False)
            df_divisiones3 = df_divisiones3.head(20)
            df_divisiones3 = df_divisiones3.sort_values(by='Cantidad_Empresas', ascending=False)


            # Gráfico de barras apiladas
            fig2 = px.bar(
                df_divisiones3,
                x='Division',
                y='Cantidad_Empresas',
                title='Cantidad de empresas segun divisiones economicas',
            )

            # Layout final
            fig2.update_layout(
                showlegend=False,
                height=1000
            )

            # Para la tabla se usan los datos filtrados
            df_divisiones4 = df_divisiones2.groupby('Division')['Cantidad_Empresas'].sum().reset_index()
            data = df_divisiones4.to_dict('records')
            from dash.dash_table.Format import Format, Scheme, Group
            columns=[
                {'name': 'DIVISION', 'id': 'Division'},
                {'name': 'CANTIDAD', 'id': 'Cantidad_Empresas', 'type': 'numeric', 'format': Format(
                        group=Group.yes,              # Activa el separador de miles
                        group_delimiter=',',          # Usa coma como separador
                        precision=0,                  # Sin decimales
                        scheme='f'                    # Notación fija (no científica)
                    )},       
            ]

    #----------------------------------------------------------------------------------------------------------------------------------------------------------       
        elif selected_info == 'e':

            children = descripciones.get('e')

            pd.set_option('display.float_format', '{:,.0f}'.format)

                        # Agrupar y calcular ganancia por División y Actividad Principal
            df_divisiones = dff.groupby(['Division', 'Actividad_principal'])['Aporte'].sum().reset_index()
            df_divisiones2 = dff2.groupby(['Division', 'Actividad_principal'])['Aporte'].sum().reset_index()
            df_divisiones = df_divisiones.loc[df_divisiones['Division'] != 'Desconocido']
            df_divisiones2 = df_divisiones2.loc[df_divisiones2['Division'] != 'Desconocido']
            # Calcular ganancia
            df_divisiones['GANANCIA'] = df_divisiones['Aporte'] * 10
            df_divisiones2['GANANCIA'] = df_divisiones2['Aporte'] * 10
            df_divisiones2['GANANCIA'] = df_divisiones2['GANANCIA'].astype(float)

            # Crear códigos únicos
            df_divisiones['Codigo_Division'] = df_divisiones['Division'].astype('category').cat.codes
            df_divisiones['Actividad_principal_cod'] = df_divisiones['Codigo_Division'].astype(str) + " - " + df_divisiones['Actividad_principal']

            # Inicializar listas
            labels = []
            parents = []
            values = []
            text = []
            hovertext = []

            # División (padre)
            for _, row in df_divisiones[['Division', 'Codigo_Division']].drop_duplicates().iterrows():
                total = int(df_divisiones[df_divisiones['Division'] == row['Division']]['GANANCIA'].sum())
                labels.append(row['Division'])
                parents.append('')
                values.append(total)
                text.append(f"{row['Division']}<br>{total:,.0f}")
                hovertext.append(f"División: {row['Division']}<br>Ganancia: {total:,.0f}")

            # Actividades (hijo)
            for _, row in df_divisiones[['Division', 'Actividad_principal_cod']].drop_duplicates().iterrows():
                total = int(df_divisiones[df_divisiones['Actividad_principal_cod'] == row['Actividad_principal_cod']]['GANANCIA'].sum())
                labels.append(row['Actividad_principal_cod'])
                parents.append(row['Division'])
                values.append(total)
                text.append(f"{row['Actividad_principal_cod']}<br>{total:,.0f}")
                hovertext.append(f"Actividad: {row['Actividad_principal_cod']}<br>Ganancia: {total:,.0f}")

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                text=text,
                hovertext=hovertext,
                hoverinfo='text',
                textinfo='text'
            ))

            fig.update_layout(
                title='Ganancias por divisiones económicas seleccionadas. Total País = G$ 53.682.677.926.130',
                margin=dict(t=50, l=25, r=25, b=25)
            )


            # Datos para gráfico de barras
            df_divisiones3 = df_divisiones2.groupby(['Division'])['GANANCIA'].sum().reset_index()
            df_divisiones3 = df_divisiones3.sort_values(by='GANANCIA', ascending=False)
            df_divisiones3 = df_divisiones3.head(20)
            df_divisiones3 = df_divisiones3.sort_values(by='GANANCIA', ascending=False)
            totales = df_divisiones3.groupby('Division')['GANANCIA'].sum().reset_index()

            import numpy as np

            fig2 = px.bar(
                df_divisiones3,
                x='Division',
                y='GANANCIA',
                #color='Division',
                title='Ganancias por divisiones económicas',
                color_discrete_sequence=px.colors.sequential.Viridis
            )

            # Agregar anotaciones con el total por Sección
            for i, row in totales.iterrows():
                fig2.add_annotation(
                    x=row['Division'],
                    y=row['GANANCIA'],
                    text=f"{int(row['GANANCIA']):,}".replace(",", "."),  # ✅ Separador de miles con punto
                    showarrow=False,
                    yshift=70,
                    font=dict(color="black", size=12),
                    textangle=90
                )

            # Formatear eje Y en miles de millones de guaraníes (eje nomás, sin cambiar datos)
            max_val = df_divisiones3['GANANCIA'].max()
            tick_vals = np.arange(0, max_val + 1e12, 1e12)
            tick_texts = [f"{int(val / 1e9):,}".replace(",", ".") for val in tick_vals]

            fig2.update_layout(
                showlegend=False,
                height=1500,
                yaxis=dict(
                    title="Ganancia (miles de millones de Gs.)",
                    tickvals=tick_vals,
                    ticktext=tick_texts,
                )
            )


            # Tabla de resumen por División
            df_divisiones4 = df_divisiones2.groupby('Division')['GANANCIA'].sum().reset_index()

            # Pasar a la tabla
            data = df_divisiones4.to_dict('records')

            from dash.dash_table.Format import Format, Group

            columns = [
                {'name': 'DIVISIONES', 'id': 'Division'},
                {
                    'name': 'GANANCIA (Gs)',
                    'id': 'GANANCIA',
                    'type': 'numeric',
                    'format': Format(
                        group=Group.yes,              # Activa el separador de miles
                        group_delimiter=',',          # Usa coma como separador
                        precision=0,                  # Sin decimales
                        scheme='f'                    # Notación fija (no científica)
                    )
                },
            ]
    #----------------------------------------------------------------------------------------------------------------------------------------


        elif selected_info == 'f':

            children = descripciones.get('f')   
         
                # Cantidad de distritos por división económica
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            df_divisiones = dff.groupby(['Division'])['DISTRITO'].nunique().reset_index()
            df_divisiones2 = dff2.groupby(['Division'])['DISTRITO'].nunique().reset_index()
            df_divisiones = df_divisiones.loc[df_divisiones['Division'] != 'Desconocido']
            df_divisiones2 = df_divisiones2.loc[df_divisiones2['Division'] != 'Desconocido']
            # Inicializar listas para Treemap
            labels = []
            parents = []
            values = []

            # 🔹 Agregar divisiones como único nivel
            for _, row in df_divisiones.iterrows():
                labels.append(row['Division'])
                parents.append("")  # Nivel raíz
                values.append(row['DISTRITO'])

            # Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value",
                textinfo="label+value",
            ))

            fig.update_layout(title='Cantidad de distritos en las que se desarrollan las divisiones seleccionadas. Total de distritos = 253')  

                # Gráfico de barras apiladas
            df_divisiones2 = df_divisiones2.sort_values(by='DISTRITO', ascending=False)
            datos = df_divisiones2.head(20)
            fig2 = px.bar(
                datos,
                x='Division',
                y='DISTRITO',
                title='Cantidad de distritos en las que se desarrollan las divisiones. Total de distritos = 253'
            )

            fig2.update_layout(
                showlegend=False,
                height=800
            )


            # Tabla con datos filtrados
            data = df_divisiones2.to_dict('records')
            columns = [
                {'name': 'DIVISION', 'id': 'Division'},
                {'name': 'DISTRITOS', 'id': 'DISTRITO'},
            ]
            
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    elif radio == 'Actividad_principal':
        seleccionados = selected_options
        dff = df.loc[df['Actividad_principal'].isin(seleccionados)]  
        dff2 = df.copy()    

    #------------------------------------------------------------------------------------------------------------------------------------------------------------- 
    #        
        if selected_info == 'a':

            children = descripciones.get('a')

            # Agrupar y sumar las empresas por Actividad_principal, Departamento y Distrito
            df_actividades = dff.groupby(['Actividad_principal', 'DEPARTAMENTO', 'DISTRITO'])['Cantidad_Empresas'].sum().reset_index()
            df_actividades2 = dff2.groupby(['Actividad_principal', 'DEPARTAMENTO', 'DISTRITO'])['Cantidad_Empresas'].sum().reset_index()
            # Crear una columna de código único para Actividad_principal
            df_actividades['Codigo_Actividad'] = df_actividades['Actividad_principal'].astype('category').cat.codes

            # Vincular el código de Actividad_principal a los Departamentos y Distritos
            df_actividades['DEPARTAMENTO_COD'] = df_actividades['Codigo_Actividad'].astype(str) + " - " + df_actividades['DEPARTAMENTO']
            df_actividades['DISTRITO_COD'] = df_actividades['DEPARTAMENTO_COD'] + " - " + df_actividades['DISTRITO']

            # Inicializar listas para el Treemap
            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar Actividad_principal (Nivel Abuelo)
            for _, row in df_actividades[['Actividad_principal', 'Codigo_Actividad']].drop_duplicates().iterrows():
                labels.append(row['Actividad_principal'])
                parents.append('')  # No tiene padre, es la raíz
                values.append(df_actividades[df_actividades['Actividad_principal'] == row['Actividad_principal']]['Cantidad_Empresas'].sum())

            # 2️⃣ Agregar Departamentos (Nivel Padre)
            for _, row in df_actividades[['DEPARTAMENTO_COD', 'Actividad_principal']].drop_duplicates().iterrows():
                labels.append(row['DEPARTAMENTO_COD'])
                parents.append(row['Actividad_principal'])  # El padre de cada departamento es la Actividad_principal
                values.append(df_actividades[df_actividades['DEPARTAMENTO_COD'] == row['DEPARTAMENTO_COD']]['Cantidad_Empresas'].sum())

            # 3️⃣ Agregar Distritos (Nivel Hijo)
            for _, row in df_actividades[['DISTRITO_COD', 'DEPARTAMENTO_COD']].drop_duplicates().iterrows():
                labels.append(row['DISTRITO_COD'])
                parents.append(row['DEPARTAMENTO_COD'])  # El padre de cada distrito es el departamento
                values.append(df_actividades[df_actividades['DISTRITO_COD'] == row['DISTRITO_COD']]['Cantidad_Empresas'].sum())

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",  # Información al pasar el mouse
                textinfo="label+value+percent entry",  # Mostrar etiqueta + valor + porcentaje
            ))

            # Mostrar gráfico
            fig.update_layout(title=f'Cantidad de empresas en cada territorio por actividad economicas')

            df_actividades3 = dff2.groupby('Actividad_principal')['Cantidad_Empresas'].sum().reset_index()
            df_actividades3 = df_actividades3.sort_values(by='Cantidad_Empresas', ascending=False)
            df_actividades3 = df_actividades3.head(20)
            datos = df_actividades3
            fig2 = px.bar(
                            datos,
                            x='Actividad_principal',
                            y='Cantidad_Empresas',
                            title='Cantidad de empresas de las 20 actividades principales. Total en datos disponibles = 188.905 empresas')
            # Ajustar la leyenda para que aparezca abajo
            fig2.update_layout(
                height=1000  # Ajustar la altura si es necesario
            )




            # Para la tabla se usan los datos filtrados
            from dash.dash_table.Format import Format, Group
            data = df_actividades2.to_dict('records')
            columns=[
                {'name': 'ACTIVIDAD', 'id': 'Actividad_principal'},
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'DISTRITO', 'id': 'DISTRITO'},
                {'name': 'CANTIDAD', 'id': 'Cantidad_Empresas', 'type': 'numeric', 'format': Format(
                        group=Group.yes,              # Activa el separador de miles
                        group_delimiter=',',          # Usa coma como separador
                        precision=0,                  # Sin decimales
                        scheme='f'                    # Notación fija (no científica)
                    )},       
            ]



    #-------------------------------------------------------------------------------------------------------------------------------
    #         
        elif selected_info == 'b':

            children = descripciones.get('b')

            df_actividades = dff.groupby(['Actividad_principal', 'DEPARTAMENTO', 'DISTRITO'])['PARTICIPACION'].sum().reset_index()
            df_actividades2 = dff2.groupby(['Actividad_principal', 'DEPARTAMENTO', 'DISTRITO'])['PARTICIPACION'].sum().reset_index()

            # Crear una columna de código único para Actividad_principal
            df_actividades['Codigo_Actividad'] = df_actividades['Actividad_principal'].astype('category').cat.codes

            # Vincular el código de Actividad_principal a los Departamentos y Distritos
            df_actividades['DEPARTAMENTO_COD'] = df_actividades['Codigo_Actividad'].astype(str) + " - " + df_actividades['DEPARTAMENTO']
            df_actividades['DISTRITO_COD'] = df_actividades['DEPARTAMENTO_COD'] + " - " + df_actividades['DISTRITO']

            # Inicializar listas para el Treemap
            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar Actividad_principal (Nivel Abuelo)
            for _, row in df_actividades[['Actividad_principal', 'Codigo_Actividad']].drop_duplicates().iterrows():
                labels.append(row['Actividad_principal'])
                parents.append('')  # No tiene padre, es la raíz
                values.append(df_actividades[df_actividades['Actividad_principal'] == row['Actividad_principal']]['PARTICIPACION'].sum())

            # 2️⃣ Agregar Departamentos (Nivel Padre)
            for _, row in df_actividades[['DEPARTAMENTO_COD', 'Actividad_principal']].drop_duplicates().iterrows():
                labels.append(row['DEPARTAMENTO_COD'])
                parents.append(row['Actividad_principal'])  # El padre de cada departamento es la actividad
                values.append(df_actividades[df_actividades['DEPARTAMENTO_COD'] == row['DEPARTAMENTO_COD']]['PARTICIPACION'].sum())

            # 3️⃣ Agregar Distritos (Nivel Hijo)
            for _, row in df_actividades[['DISTRITO_COD', 'DEPARTAMENTO_COD']].drop_duplicates().iterrows():
                labels.append(row['DISTRITO_COD'])
                parents.append(row['DEPARTAMENTO_COD'])  # El padre de cada distrito es el departamento
                values.append(df_actividades[df_actividades['DISTRITO_COD'] == row['DISTRITO_COD']]['PARTICIPACION'].sum())

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",  # Información al pasar el mouse
                textinfo="label+value+percent entry",  # Mostrar etiqueta + valor + porcentaje
            ))
            fig.update_layout(title='Distribución de ganancias en cada territorio por actividades económicas')

            # Barras horizontales: principales actividades
            df_actividades3 = df_actividades2.groupby('Actividad_principal')['PARTICIPACION'].sum().reset_index()
            df_actividades3 = df_actividades3.sort_values(by='PARTICIPACION', ascending=False).head(20)
            df_actividades3 = df_actividades3.sort_values(by='PARTICIPACION', ascending=False)
            fig2 = px.bar(
                df_actividades3,
                x='Actividad_principal',
                y='PARTICIPACION',
                title='Participación porcentual de sectores en la ganancia nacional'
            )
            fig2.update_layout(height=1000)

            # Tabla
            data = df_actividades2.to_dict('records')
            from dash.dash_table.Format import Format, Scheme

            columns = [
                {'name': 'ACTIVIDADES PRINCIPALES', 'id': 'Actividad_principal'},
                {'name': 'DEPARTAMENTO', 'id': 'DEPARTAMENTO'},
                {'name': 'DISTRITO', 'id': 'DISTRITO'},
                {
                    'name': 'PARTICIPACION (%)',
                    'id': 'PARTICIPACION',
                    'type': 'numeric',
                    'format': Format(
                        scheme=Scheme.fixed,   # Notación fija
                        precision=5            # 5 decimales
                    )
                },
            ]
#-----------------------------------------------------------------------------------------------------------------------------------
        elif selected_info == 'c':
            children = descripciones.get('c')

            # Agrupar globalmente por Actividad_principal
            act2 = dff2.groupby('Actividad_principal').agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            ).reset_index()

            # Total global de empresas (usado para el cálculo de porcentajes)
            global_empresas = dff2['Cantidad_Empresas'].sum()

            # Calcular el porcentaje global de empresas para cada Actividad_principal
            act2['porcentaje_empresas'] = act2['Cantidad_Empresas'] / global_empresas * 100
            act2['rentabilidad_empresas'] = act2.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                            if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0)
                            else 0,
                axis=1
            )
            act2 = act2.fillna(0)

         

            # Nivel 1: Actividad_principal (agrupación a nivel top)
            df_actividad = dff.groupby('Actividad_principal', as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_actividad['porcentaje_empresas'] = df_actividad['Cantidad_Empresas'] / global_empresas * 100
            df_actividad['rentabilidad_empresas'] = df_actividad.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                            if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0)
                            else 0,
                axis=1
            )
            df_actividad = df_actividad.fillna(0)
            # Usamos el propio campo como ID en este nivel
            df_actividad['ACT_ID'] = df_actividad['Actividad_principal']

            # Nivel 2: Departamento, agrupando por Actividad_principal y DEPARTAMENTO
            df_dep = dff.groupby(['Actividad_principal','DEPARTAMENTO'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_dep['porcentaje_empresas'] = df_dep['Cantidad_Empresas'] / global_empresas * 100
            df_dep['rentabilidad_empresas'] = df_dep.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                            if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0)
                            else 0,
                axis=1
            )
            df_dep = df_dep.fillna(0)
            # Crear ID: concatenamos Actividad_principal y DEPARTAMENTO
            df_dep['DEP_ID'] = df_dep['Actividad_principal'] + ' - ' + df_dep['DEPARTAMENTO']

            # Nivel 3: Distrito, agrupando por Actividad_principal, DEPARTAMENTO y DISTRITO
            df_dist = dff.groupby(['Actividad_principal','DEPARTAMENTO','DISTRITO'], as_index=False).agg(
                Cantidad_Empresas=('Cantidad_Empresas', 'sum'),
                PARTICIPACION=('PARTICIPACION', 'sum')
            )
            df_dist['porcentaje_empresas'] = df_dist['Cantidad_Empresas'] / global_empresas * 100
            df_dist['rentabilidad_empresas'] = df_dist.apply(
                lambda row: (row['PARTICIPACION'] / row['porcentaje_empresas'] * 100)
                            if (row['porcentaje_empresas'] > 0 and row['PARTICIPACION'] > 0)
                            else 0,
                axis=1
            )
            df_dist = df_dist.fillna(0)
            # Crear ID: Concatenar Actividad_principal, DEPARTAMENTO y DISTRITO
            df_dist['DIST_ID'] = df_dist['Actividad_principal'] + ' - ' + df_dist['DEPARTAMENTO'] + ' - ' + df_dist['DISTRITO']


            ids = []
            labels = []
            parents = []
            values = []

            # Nivel 1: Actividad_principal
            for _, row in df_actividad.iterrows():
                ids.append(row['ACT_ID'])
                labels.append(row['Actividad_principal'])
                parents.append('')  # Nivel superior
                values.append(row['rentabilidad_empresas'])

            # Nivel 2: Departamento
            for _, row in df_dep.iterrows():
                ids.append(row['DEP_ID'])
                labels.append(row['DEPARTAMENTO'])
                # El padre es el valor de Actividad_principal (tal como aparece en row['Actividad_principal'])
                parents.append(row['Actividad_principal'])
                values.append(row['rentabilidad_empresas'])

            # Nivel 3: Distrito
            for _, row in df_dist.iterrows():
                ids.append(row['DIST_ID'])
                labels.append(row['DISTRITO'])
                # El padre es la concatenación: Actividad_principal - DEPARTAMENTO (igual al DEP_ID)
                padre = row['Actividad_principal'] + ' - ' + row['DEPARTAMENTO']
                parents.append(padre)
                values.append(row['rentabilidad_empresas'])

            fig = go.Figure(go.Treemap(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",
                textinfo="label+value+percent entry"
            ))
            fig.update_layout(title=f"Rentabilidad por sector economico (treemap): Actividad, Departamento y Distrito en {selected_options}")

            act2 = act2.sort_values(by='rentabilidad_empresas', ascending=False)
            act3 = act2.head(20)
            fig2 = px.bar(
                act3,
                x='Actividad_principal',
                y='rentabilidad_empresas',
                title="Participación (Rentabilidad) por sector (Actividad principal)"
            )

            data = act2.to_dict('records')
            columns = [
                {'name': 'Actividad_principal', 'id': 'Actividad_principal'},
                {'name': 'GANANCIAS (%)', 'id': 'PARTICIPACION'},
                {'name': 'EMPRESAS (%)', 'id': 'porcentaje_empresas'},
                {'name': 'RELACION', 'id': 'rentabilidad_empresas'}
            ]

    #-----------------------------------------------------------------------------------------------------------------------------------

        elif selected_info == 'd':

            children = descripciones.get('d')

        # Cantidad de empresas por actividad economica

           # Agrupar y sumar las empresas por Actividad Principal
            df_actividades = dff.groupby(['Actividad_principal'])['Cantidad_Empresas'].sum().reset_index()
            df_actividades2 = dff2.groupby(['Actividad_principal'])['Cantidad_Empresas'].sum().reset_index()
            df_actividades = df_actividades.loc[df_actividades['Actividad_principal'] != 'Desconocido']
            df_actividades2 = df_actividades2.loc[df_actividades2['Actividad_principal'] != 'Desconocido']
            # Crear una columna de código (si se quiere mantener para etiquetas únicas)
            df_actividades['Codigo_Actividad'] = df_actividades['Actividad_principal'].astype('category').cat.codes.astype(str)

            # Inicializar listas para el Treemap
            labels = []
            parents = []
            values = []

            # 1️⃣ Agregar Actividades principales (único nivel, raíz)
            for _, row in df_actividades.iterrows():
                labels.append(row['Actividad_principal'])
                parents.append("")  # No hay jerarquía, todos están al mismo nivel
                values.append(row['Cantidad_Empresas'])

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value+percent entry",
                textinfo="label+value+percent entry"
            ))

            fig.update_layout(title='Cantidad de empresas según actividades económicas principales')

            # Gráfico de barras: top 20 actividades
            df_actividades3 = df_actividades2.sort_values(by='Cantidad_Empresas', ascending=False).head(20)
            df_actividades3 = df_actividades3.sort_values(by='Cantidad_Empresas', ascending=False)

            fig2 = px.bar(
                df_actividades3,
                x='Actividad_principal',
                y='Cantidad_Empresas',
                title='Cantidad de empresas según actividades económicas principales',
            )

            fig2.update_layout(
                showlegend=False,
                height=1000
            )

            # Tabla con los datos
            data = df_actividades2.to_dict('records')
            from dash.dash_table.Format import Format, Scheme, Group
            columns = [
                {'name': 'ACTIVIDAD PRINCIPAL', 'id': 'Actividad_principal'},
                 {'name': 'CANTIDAD', 'id': 'Cantidad_Empresas', 'type': 'numeric', 'format': Format(
                        group=Group.yes,              # Activa el separador de miles
                        group_delimiter=',',          # Usa coma como separador
                        precision=0,                  # Sin decimales
                        scheme='f'                    # Notación fija (no científica)
                    )},       
            ]


    #----------------------------------------------------------------------------------------------------------------------------------------------------------       
        elif selected_info == 'e':

            children = descripciones.get('e')


            pd.set_option('display.float_format', '{:,.0f}'.format)

            # Agrupar y calcular ganancia por Actividad Principal
            df_actividades = dff.groupby(['Actividad_principal'])['Aporte'].sum().reset_index()
            df_actividades2 = dff2.groupby(['Actividad_principal'])['Aporte'].sum().reset_index()
            df_actividades = df_actividades.loc[df_actividades['Actividad_principal'] != 'Desconocido']
            df_actividades2 = df_actividades2.loc[df_actividades2['Actividad_principal'] != 'Desconocido']
            # Calcular ganancia
            df_actividades['GANANCIA'] = df_actividades['Aporte'] * 10
            df_actividades2['GANANCIA'] = df_actividades2['Aporte'] * 10
            df_actividades2['GANANCIA'] = df_actividades2['GANANCIA'].astype(float)

            # Inicializar listas
            labels = []
            parents = []
            values = []
            text = []
            hovertext = []

            # Actividades (único nivel raíz)
            for _, row in df_actividades.iterrows():
                total = int(row['GANANCIA'])
                labels.append(row['Actividad_principal'])
                parents.append('')
                values.append(total)
                text.append(f"{row['Actividad_principal']}<br>{total:,.0f}")
                hovertext.append(f"Actividad: {row['Actividad_principal']}<br>Ganancia: {total:,.0f}")

            # Crear el gráfico Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                text=text,
                hovertext=hovertext,
                hoverinfo='text',
                textinfo='text'
            ))

            fig.update_layout(
                title='Ganancias por actividades económicas principales. Total País = G$ 53.682.677.926.130',
                margin=dict(t=50, l=25, r=25, b=25)
            )

            # Datos para gráfico de barras: top 20 actividades
            df_actividades3 = df_actividades2.sort_values(by='GANANCIA', ascending=False).head(20)
            df_actividades3 = df_actividades3.sort_values(by='GANANCIA', ascending=False)
            totales = df_actividades3.groupby('Actividad_principal')['GANANCIA'].sum().reset_index()

            import numpy as np

            fig2 = px.bar(
                df_actividades3,
                x='Actividad_principal',
                y='GANANCIA',
                #color='Division',
                title='Ganancias por secciones económicas',
                color_discrete_sequence=px.colors.sequential.Viridis
            )

            # Agregar anotaciones con el total por Sección
            for i, row in totales.iterrows():
                fig2.add_annotation(
                    x=row['Actividad_principal'],
                    y=row['GANANCIA'],
                    text=f"{int(row['GANANCIA']):,}".replace(",", "."),  # ✅ Separador de miles con punto
                    showarrow=False,
                    yshift=70,
                    font=dict(color="black", size=12),
                    textangle=90
                )

            # Formatear eje Y en miles de millones de guaraníes (eje nomás, sin cambiar datos)
            max_val = df_actividades3['GANANCIA'].max()
            tick_vals = np.arange(0, max_val + 1e12, 1e12)
            tick_texts = [f"{int(val / 1e9):,}".replace(",", ".") for val in tick_vals]

            fig2.update_layout(
                showlegend=False,
                height=1200,
                yaxis=dict(
                    title="Ganancia (miles de millones de Gs.)",
                    tickvals=tick_vals,
                    ticktext=tick_texts,
                )
            )
            # Tabla de resumen por Actividad
            df_actividades4 = df_actividades2.groupby('Actividad_principal')['GANANCIA'].sum().reset_index()
            

            # Convertir a lista de diccionarios para la DataTable
            data = df_actividades4.to_dict('records')

            from dash.dash_table.Format import Format, Group

            columns = [
                {'name': 'ACTIVIDADES PRINCIPALES', 'id': 'Actividad_principal'},
                {
                    'name': 'GANANCIA (Gs)',
                    'id': 'GANANCIA',
                    'type': 'numeric',
                    'format': Format(
                        group=Group.yes,              # Activa el separador de miles
                        group_delimiter=',',          # Usa coma como separador
                        precision=0,                  # Sin decimales
                        scheme='f'                    # Notación fija (no científica)
                    )
                },
            ]


    #----------------------------------------------------------------------------------------------------------------------------------------


        elif selected_info == 'f':

            children = descripciones.get('f')

            df_actividades = dff.groupby(['Actividad_principal'])['DISTRITO'].nunique().reset_index()
            df_actividades2 = dff2.groupby(['Actividad_principal'])['DISTRITO'].nunique().reset_index()
            df_actividades = df_actividades.loc[df_actividades['Actividad_principal'] != 'Desconocido']
            df_actividades2 = df_actividades2.loc[df_actividades2['Actividad_principal'] != 'Desconocido']

            # Inicializar listas para Treemap
            labels = []
            parents = []
            values = []

            # 🔹 Agregar actividades como único nivel
            for _, row in df_actividades.iterrows():
                labels.append(row['Actividad_principal'])
                parents.append("")  # Nivel raíz
                values.append(row['DISTRITO'])

            # Crear Treemap
            fig = go.Figure(go.Treemap(
                labels=labels,
                parents=parents,
                values=values,
                hoverinfo="label+value",
                textinfo="label+value",
            ))

            fig.update_layout(title='Cantidad de distritos en los que se desarrollan las actividades económicas principales. Total de distritos = 253')

            # Gráfico de barras
            df_actividades2 = df_actividades2.sort_values(by='DISTRITO', ascending=False)
            datos = df_actividades2.head(20)
            fig2 = px.bar(
                datos,
                x='Actividad_principal',
                y='DISTRITO',
                title='Cantidad de distritos en los que se desarrollan las actividades económicas principales. Total de distritos = 253'
            )

            fig2.update_layout(
                showlegend=False,
                height=800
            )

            # Tabla con datos filtrados
            data = df_actividades2.to_dict('records')
            columns = [
                {'name': 'ACTIVIDAD PRINCIPAL', 'id': 'Actividad_principal'},
                {'name': 'DISTRITOS', 'id': 'DISTRITO'},
            ]
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

    return fig, fig2, columns, data, children
