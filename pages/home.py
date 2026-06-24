import dash
from dash import html, dcc
import dash_mantine_components as dmc

dash.register_page(__name__, path="/", name="Home")

# Example project data - replace or extend with real projects
PROJECTS = [
    {
        "title": "Multitreading on C++",
        "summary": "A C++ application that demonstrates the use of multithreading and their sintaxis. I leverage use my real-time bar engine to show how multitreading and showing several concepts",
        "tags": ["multithreading", "asynchronous programming", "lock free programming"],
        "link": "/projects/multithreading",
    },
    {
        "title": "Bar Generation through Boost::Beast",
        "summary": "A high‑performance C++ application designed for real‑time bar construction from tick data. It uses Boost.Beast to maintain a secure WebSocket connection, ensuring fast and reliable data ingestion. The system also leverages the Parquet library to store output in the Parquet format, enabling efficient processing, compact storage, and easy retrieval for later analysis.",
        "tags": ["networking", "bar construction", "tick data"],
        "link": "/projects/bar-generation",
    },
    {
        "title": "Order Book Contruction",
        "summary": "Recreate the logic of a matching engine and build a full order book from raw market data using market standard C++ techniques.",
        "tags": ["C++", "order books", "execution", "low-latency"],
        "link": "/projects/order-book",
    },
    {
        "title": "Webscrapping & Sentiment Analysis",
        "summary": "Modified a standard webscrapping structure using beutifulsoup4 and requests to collect and analyse sentiment from crypto-magazines.",
        "tags": ["python", "webscrapping", "sentiment analysis"],
        "link": "/projects/webscrapping-crypto",
    },
]


def project_card(p):
    return dmc.Card(
        children=[
            dmc.Group(
                [
                    dmc.Text(p["title"], size="lg"),
                    dmc.Badge(
                        ", ".join(p["tags"]),
                        variant="light",
                        color="blue",
                        style={"marginLeft": "auto"},
                    ),
                ],
                style={"justifyContent": "space-between"},
            ),
            dmc.Space(h=8),
            dmc.Text(p["summary"], style={"color": "#555"}, size="sm"),
            dmc.Space(h=12),
            dmc.Group(
                [
                    dcc.Link(
                        dmc.Button("Open", variant="outline", size="sm"), href=p["link"]
                    ),
                    dcc.Link(dmc.Button("Details", size="sm"), href=p["link"]),
                ],
                style={"gap": "0.5rem"},
            ),
        ],
        shadow="sm",
        radius="md",
        style={"minWidth": 300, "padding": "1.5rem"},
    )


layout = dmc.Container(
    size="xl",
    style={"padding": "0 1rem"},
    children=[
        dmc.Space(h=20),
        # Hero
        dmc.SimpleGrid(
            [
                dmc.Stack(
                    [
                        dmc.Title("Quant Portfolio - Research & Engineering", order=1),
                        dmc.Text(
                            "A few projects that showcase my skills in quantitative research, data engineering, and software development within execution trading and data science.",
                            style={"color": "#555"},
                        ),
                        dmc.Space(h=10),
                        dmc.Group(
                            children=[
                                dcc.Link(
                                    dmc.Button(
                                        "Projects",
                                        variant="gradient",
                                        gradient={"from": "indigo", "to": "cyan"},
                                    ),
                                    href="/projects",
                                ),
                                dmc.Anchor(
                                    dmc.Button("Resume / CV", variant="outline"),
                                    href="/assets/Jesus_Anderson_Tuesta_Soto.pdf",
                                    target="_blank",
                                ),
                            ]
                        ),
                    ]
                ),
                dmc.Card(
                    children=[
                        dmc.Image(
                            src="assets/linkedInProfilePic.png",
                            alt="finance",
                            h=200,
                            fit="contain",
                        ),
                        dmc.Text(
                            "Quantitative analysis • Execution • Data engineering",
                            ta="center",
                            size="sm",
                            style={"color": "#555"},
                        ),
                    ],
                    shadow="sm",
                ),
            ],
            cols=2,
        ),
        dmc.Space(h=30),
        # Projects section
        dmc.Title("Projects", order=2),
        dmc.Text(
            "Selected work and internal projects from my quant research and engineering efforts.",
            size="sm",
            style={"color": "#555"},
        ),
        dmc.Space(h=12),
        dmc.SimpleGrid(
            [project_card(p) for p in PROJECTS],
            cols=3,
        ),
        dmc.Space(h=80),
        # Resume section
        dmc.Group(
            [
                dmc.Stack(
                    [
                        dmc.Title("Resume", order=2),
                        dmc.Text(
                            "A short summary of professional experience and a downloadable CV."
                        ),
                        dmc.Container(
                            dmc.Card(
                                [
                                    dmc.Text(
                                        "- 2 years at systematic hedge funds\n- Python, C++, SQL, KDB+ \n- Exeution & Data engineering",
                                    ),
                                ],
                                shadow="xs",
                                style={
                                    "width": "1000px",
                                    "padding": "1rem",
                                    "alignItems": "center",
                                },
                            ),
                        ),
                        dmc.List(
                            [
                                dmc.ListItem(
                                    "Systematic Strategy Design & Optimization – implemented rolling-window frameworks to adapt to shifting market regimes"
                                ),
                                dmc.ListItem(
                                    "Execution & Transaction Cost Analysis – automated TCA processes to monitor slippage, optimize routing, and reduce trading costs across listed and OTC markets"
                                ),
                                dmc.ListItem(
                                    "Data Engineering & Infrastructure – built scalable analytics platforms and real-time dashboards in Python, KDB+, and C++; integrated low-latency pipelines to support execution logic, and research scalability"
                                ),
                            ]
                        ),
                        dmc.Space(h=8),
                        dmc.Group(
                            children=[
                                dmc.Anchor(
                                    dmc.Button("Download CV", variant="outline"),
                                    href="/assets/Jesus_Anderson_Tuesta_Soto.pdf",
                                    target="_blank",
                                ),
                                dcc.Link(
                                    dmc.Button("LinkedIn"),
                                    href="https://www.linkedin.com/in/jesus-tuesta/",
                                    target="_blank",
                                ),
                            ]
                        ),
                    ],
                    gap="xs",
                    align="center",
                ),
            ],
        ),
        dmc.Space(h=40),
        html.Footer(
            dmc.Text("© Jesus Tuesta — Built with Dash & Mantine", size="sm"),
        ),
    ],
)
