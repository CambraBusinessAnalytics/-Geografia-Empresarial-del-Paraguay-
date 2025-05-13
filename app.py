import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, page_container

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server
app.layout = html.Div([
    # Encabezado principal con fondo sutil
    html.Header(
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    dbc.Row([
                        dbc.Col(
                            html.Img(
                                src='/assets/CAMBRA.png',
                                style={'height': '80px', 'width': 'auto'}
                            ),
                            width="auto"
                        ),
                        dbc.Col(
                            html.H1(
                                "Geografía Económica y Productiva del Paraguay",
                                className="m-0",
                                style={
                                    'font-family': 'Avenir, sans-serif',
                                    'font-weight': '700',
                                    'font-size': '2rem',
                                    'text-align': 'center',
                                    'color': '#333'
                                }
                            ),
                            align="center"
                        )
                    ], align="center"),
                    width=10  # Este es el ancho central
                )
            ], justify="center", className="py-3")
        ]),
        style={'backgroundColor': 'white'},
    ),


    dbc.Nav(
        [
            dbc.NavLink("Inicio", href="/", active="exact", className="nav-link-custom"),
            dbc.NavLink("Análisis Territorial", href="/territorial", active="exact", className="nav-link-custom"),
            dbc.NavLink("Actividades", href="/actividades", active="exact", className="nav-link-custom"),
            dbc.NavLink("Metodología", href="/metodologia", active="exact", className="nav-link-custom"),
        ],
        pills=True,
        fill=True,
        style={
            'backgroundColor': 'white',
            'borderBottom': '1px solid #333'
        },
        className="mt-2 mb-4",
    ),

    # Contenedor de la página actual
    page_container
])



if __name__ == "__main__":
    app.run_server(debug=True)
