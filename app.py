from datetime import datetime

import dash_ag_grid as dag
import dash_design_kit as ddk
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, callback, dcc, html, set_props

from data_jobs.mock_databricks import MockDatabricksJobs

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
                            "editable": False,
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


@callback(
    Output("scatter-plot", "figure"),
    Output("related-ag-grid", "rowData"),
    Output("non-related-ag-grid", "rowData"),
    Input("tails-ag-grid", "cellDoubleClicked"),
    allow_duplicate=True,
    prevent_initial_call=True,
)
def update_scatter_plot(tail_name: str):
    data, relevant_events, non_relevant_events = MockDatabricksJobs.fetch_plane_events()

    # Create figure based on query results
    fig = px.scatter(
        x=data.keys(),
        y=data.values(),
        labels={"x": "Date", "y": "Metric"},
        title=f"Full Flight Data for component on {tail_name['value']}",
    )

    # Populate AG Grids
    related_events_data = [
        {
            "Date": event.strftime("%Y-%m-%d"),
            "PN": tail_name["value"],
            "SN": "-",
            "Description": "-",
            "Notes": "-",
            "": "-",
        }
        for event in relevant_events
    ]

    non_related_events_data = [
        {
            "Date": event.strftime("%Y-%m-%d"),
            "PN": tail_name["value"],
            "SN": "-",
            "Description": "-",
            "Notes": "-",
            "": "-",
        }
        for event in non_relevant_events
    ]

    return fig, related_events_data, non_related_events_data


@callback(
    Input("related-ag-grid", "rowData"),
    State("scatter-plot", "figure"),
    prevent_initial_call=True,
)
def add_event_vertical_lines(row_data, figure):
    figure = go.Figure(figure)

    for event in row_data:
        date_obj = datetime.strptime(event["Date"], "%Y-%m-%d")

        figure.add_vline(
            x=date_obj,
            line=dict(dash="dash"),
        )

    # Set the figure prop of scatter plot
    set_props("scatter-plot", {"figure": figure})


if __name__ == "__main__":
    app.run(debug=True)
