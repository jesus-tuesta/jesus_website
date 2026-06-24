import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc
from flask import Flask

app = dash.Dash(
    __name__,
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"
    ],
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css"
    ],
    use_pages=True,
    title=" ",
)
server = app.server

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        {%title%}
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <script>hljs.highlightAll();</script>
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
"""


app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        # Top header built from HTML + Mantine components (dmc.Header isn't available in this env)
        html.Header(
            dmc.Container(
                dmc.Group(
                    align="center",
                    style={"height": "60px", "display": "flex", "alignItems": "center"},
                    children=[
                        dmc.Text("Jesus Personal Portfolio", size="xl"),
                        dmc.Group(
                            gap="md",
                            children=[
                                dcc.Link(
                                    page["name"],
                                    href=page["path"],
                                    style={"textDecoration": "none"},
                                )
                                for page in dash.page_registry.values()
                                if page["name"] == "Home"
                            ],
                        ),
                    ],
                ),
                fluid=True,
                style={"paddingTop": "6px", "paddingBottom": "6px"},
            ),
            style={"boxShadow": "0 1px 3px rgba(0,0,0,0.08)", "zIndex": 10},
        ),
        dcc.Location(id="url"),
        dash.page_container,
    ],
)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=False, port=8050, host="0.0.0.0")
