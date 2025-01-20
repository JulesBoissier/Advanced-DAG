import dash_ag_grid as dag
import dash_design_kit as ddk
from dash import Dash, Input, Output, callback, dcc, html

app = Dash(__name__)
server = app.server  # expose server variable for Procfile

app.layout = ddk.App(
    children=[
        ddk.Row(
            children=[
                ddk.Block(
                    width=50,
                    children=[
                        dcc.Input(
                            id="alerting-zone",
                            type="text",
                            placeholder="Alerting Zone",
                            style={"width": "25%"},
                        )
                    ],
                ),
                ddk.Block(
                    width=50,
                    children=[
                        dcc.Input(
                            id="threshold",
                            type="number",
                            placeholder="Threshold Value",
                            style={"width": "25%"},
                        )
                    ],
                ),
            ],
        ),
        ddk.Row(
            html.Button("RUN PERFORMANCE ANALYSIS", id="run-pa", n_clicks=0),
        ),
        ddk.Row(
            children=[
                ddk.Card(
                    dag.AgGrid(
                        id="tails-ag-grid",
                        rowData=[{"Tails": f"XX12{i}"} for i in range(25)],
                        columnDefs=[{"field": "Tails", "sortable": True}],
                        columnSize="sizeToFit",
                        dashGridOptions={"animateRows": False},
                        defaultColDef={
                            "filter": True,
                            "editable": True,
                            "cellDataType": False,
                        },
                    ),
                ),
                ddk.Card(
                    children=[
                        ddk.Row(
                            ddk.Graph(id="scatter-plot"),
                        ),
                        ddk.Row(
                            dag.AgGrid(
                                id="related-ag-grid",
                                rowData=[],
                                columnDefs=[
                                    {"field": "Date"},
                                    {"field": "PN"},
                                    {"field": "SN"},
                                    {"field": "Description", "sortable": False},
                                    {"field": "Notes", "sortable": False},
                                    {"field": "", "sortable": False},
                                ],
                                columnSize="sizeToFit",
                                dashGridOptions={"animateRows": False},
                                defaultColDef={
                                    "filter": True,
                                    "editable": True,
                                    "cellDataType": False,
                                },
                            ),
                        ),
                        ddk.Row(
                            dag.AgGrid(
                                id="non-related-ag-grid",
                                rowData=[],
                                columnDefs=[
                                    {"field": "Date"},
                                    {"field": "PN"},
                                    {"field": "SN"},
                                    {"field": "Description", "sortable": False},
                                    {"field": "Notes", "sortable": False},
                                    {"field": "", "sortable": False},
                                ],
                                columnSize="sizeToFit",
                                dashGridOptions={"animateRows": False},
                                defaultColDef={
                                    "filter": True,
                                    "editable": True,
                                    "cellDataType": False,
                                },
                            ),
                        ),
                    ]
                ),
            ]
        ),
    ]
)


if __name__ == "__main__":
    app.run(debug=True)
