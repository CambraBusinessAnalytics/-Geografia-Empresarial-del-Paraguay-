import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Registrar página multipágina
dash.register_page(__name__, path="/metodologia")

texto_metodologia = '''

---

### ¿Quiénes somos?

**Cambra Business Analytics** es una consultoría especializada en el uso estratégico de datos para impulsar decisiones empresariales más efectivas.Aplicamos el enfoque de *Business Analytics*, que combina análisis estadísticos, modelos matemáticos y tecnología avanzada para transformar datos brutos en información valiosa.

Nuestro objetivo es ayudar a las empresas a identificar patrones, tendencias y relaciones en sus datos, lo que permite optimizar procesos, mejorar estrategias y aprovechar oportunidades.

En Cambra Business Analytics creemos que cada dato cuenta y, cuando se analiza de manera adecuada, puede ser el motor de crecimiento, rentabilidad y competitividad de cualquier organización.

---

### ¿Qué hicimos y por qué lo hicimos?

En este proyecto buscamos responder a una pregunta compleja pero fundamental: **¿cómo podemos entender la dimensión y la distribución de los sectores económicos en Paraguay?** Para ello, utilizamos como fuente principal los datos de las declaraciones del **Impuesto a la Renta Empresarial (IRE)**, un tributo que grava con un 10% las ganancias declaradas por las empresas.

A través de una solicitud de acceso a la información pública, obtuvimos de la Dirección Nacional de Ingresos Tributarios (DNIT) los datos correspondientes al periodo fiscal 2022. Estos datos fueron procesados, clasificados y agrupados para facilitar su análisis. Utilizamos como base la **Clasificación Nacional de Actividades Económicas del Paraguay**, que organiza las actividades en 87 divisiones económicas, a su vez agrupadas en 21 secciones. En este análisis trabajamos principalmente a nivel de sección económica.

Este trabajo fue realizado por **Cambra Business Analytics** durante los primeros meses del año 2025. Nuestra motivación principal fue **poner a disposición una herramienta valiosa para el estudio y la comprensión de la economía paraguaya**. Creemos firmemente en el poder de los datos, especialmente cuando estos se presentan de forma **visual, accesible e interactiva**. Aspiramos a que este trabajo sea útil para **estudiantes, investigadores, emprendedores, actores económicos, formuladores de políticas públicas y ciudadanos en general**.

Sabemos que esta es solo una parte de una realidad mucho más compleja. Paraguay cuenta con una gran cantidad de datos que aún no han sido transformados en información útil para la toma de decisiones. Este proyecto es, entonces, **un punto de partida**: una invitación a mirar con más detalle, a cuestionar, a complementar y a profundizar.

Finalmente, es importante señalar que este análisis fue realizado **con los mejores datos disponibles al momento**, reconociendo sus limitaciones. Tenemos la esperanza de poder **actualizar y enriquecer estos análisis en el futuro**, a medida que accedamos a información más completa y precisa.

---

### Consideraciones metodológicas y limitaciones del análisis

El presente análisis sobre la economía paraguaya se basa en los datos de las declaraciones de renta de las empresas ante el Ministerio de Hacienda (actual Dirección Nacional de Ingresos Tributarios) mediante una consulta en el Portal de Datos Abiertos. En Paraguay, las empresas tributan a través del Impuesto a la Renta Empresarial (IRE), que establece una tasa del 10% sobre las rentas declaradas. A partir de estos datos es posible estimar cuáles son los sectores económicos que más aportan y cuánto aporta cada uno al fisco, utilizando esta información como proxy para comprender la estructura y dinámica de la economía. No obstante, este enfoque presenta una serie de limitaciones importantes que deben ser tenidas en cuenta:

#### 1. Existencia de motores económicos ocultos

Existen sectores económicos que, a pesar de generar un movimiento económico significativo, no están gravados por el IRE y por ende no se reflejan en los datos disponibles. Un ejemplo claro son las universidades privadas, que están exentas del pago del impuesto a la renta pero tienen un fuerte impacto en varias ciudades del país. Otro caso relevante son las entidades binacionales como Itaipú y Yacyretá, que emplean a miles de personas y financian obras públicas de gran envergadura, pero cuyos aportes tampoco se ven reflejados en las estadísticas tributarias tradicionales. También debe considerarse el régimen de maquila, ampliamente extendido en el sector industrial, donde las empresas tributan bajo un esquema especial orientado a la exportación.

#### 2. Asignación territorial basada en la ubicación de la matriz

En el análisis territorial se asignan las ganancias generadas según el distrito donde se encuentra la **matriz** de la empresa. Esto implica una simplificación que puede inducir a errores, ya que muchas empresas cuentan con sucursales distribuidas en varias ciudades del país.

#### 3. Limitación en la asignación sectorial de las ganancias

Las empresas declaran una actividad económica principal y hasta cuatro secundarias. Sin embargo, es imposible discriminar que parte de la ganancia fue generada por una actividad u otra dentro de una empresa. Por lo tanto, los datos por sector económico reflejan la actividad declarada como principal (es principal justamente porque en teoria es la relevante), que quizas, no necesariamente sea la que más aporta en términos de rentabilidad o volumen de operaciones en realidad. En todo caso, es altamente probable que la actividad principal no sea la única fuente de rentabilidad a pesar de que en nuestro análisis se considere como tal.

#### 4. Conteo de empresas basado solo en la matriz

A la hora de contabilizar la cantidad de empresas por territorio, se tomó como referencia únicamente la **matriz** de cada empresa, sin incluir los demás establecimientos, debido a la falta de datos detallados sobre estos.

#### 5. Subdeclaración y economía sumergida

Existe la posibilidad de **subdeclaración**, es decir, que los contribuyentes reporten menos ingresos de los realmente generados. Este fenómeno se relaciona con la amplia economía informal en Paraguay. Diversos estudios, como los de la Fundación Pro Paraguay, estiman que aproximadamente el **43% de la economía paraguaya opera fuera del sistema formal**.

#### 6. Calidad y completitud de los datos

Se debe señalar que el análisis parte de la **presunción de integridad y validez de los datos provistos por el Ministerio de Hacienda**. Sin embargo, se observaron casos con información incompleta o inconsistente, lo cual puede afectar la calidad del análisis.

'''
layout = dbc.Container([
    html.H2("Consideraciones metodológicas y limitaciones del análisis", className="mt-4 mb-4", style={'textAlign': 'center', 'font-family': 'Avenir, sans-serif'}),

    dbc.Row([
        dbc.Col([
            dcc.Markdown(texto_metodologia, className="markdown", style={
                'textAlign': 'justify',
                'font-family': 'Cambria, serif',
                'text-indent': '2em',
                'fontSize': '16px',
            })
        ], width=8)
    ], justify="center"),
])
