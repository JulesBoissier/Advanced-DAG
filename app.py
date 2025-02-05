from datetime import datetime, timedelta

import dash_ag_grid as dag
import dash_design_kit as ddk
import plotly.express as px
import plotly.graph_objects as go
from dash import (
    ClientsideFunction,
    Dash,
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    dcc,
    html,
    set_props,
)

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
                    #TODO: Nest events ag-grid with https://dash.plotly.com/dash-ag-grid/enterprise-master-detail
                    dag.AgGrid(
                        id="tails-ag-grid",
                        rowData=[{"Tails": f"XX12{i}", 
                                "cities" : [
                                    {"city": "Shanghai", "population_city": 24870895, "population_metro": "NA"},
                                    {"city": "Beijing", "population_city": 21893095, "population_metro": "NA"}
                                    ]
                                } for i in range(25)],
                        columnDefs=[{"field": "Tails", "sortable": True, "cellRenderer": "agGroupCellRenderer"}],
                        columnSize="sizeToFit",
                        dashGridOptions={"animateRows": False, "detailRowAutoHeight": True},
                        defaultColDef={
                            "filter": True,
                            "editable": False,
                            "cellDataType": False,
                        },
                        enableEnterpriseModules=True,
                        licenseKey=None, #os.environ["AGGRID_ENTERPRISE"],
                        masterDetail=True,
                        detailCellRendererParams={
                            "detailGridOptions": {
                                "columnDefs": [
                                    {"headerName": "City", "field": "city"},
                                    {"headerName": "Pop. (City proper)", "field": "population_city"},
                                    {"headerName": "Pop. (Metro area)", "field": "population_metro"},
                                ]
                            },
                            "detailColName": "cities",
                            "suppressCallback": True,
                        },
                    ),
                ),
                ddk.Card(
                    children=[
                        ddk.Row(
                            ddk.Graph(id="scatter-plot"),
                        ),
                        ddk.Row(
                            dcc.RadioItems(
                                id='test-button',
                                options={
                                    'move': 'Move',
                                    'deselect': 'Copy and Deselect',
                                    'none': 'Copy and Keep Selected'
                                },
                                value='move', inline=True, style={'margin': 10}
                            ),
                        ),
                        ddk.Row(
                            dag.AgGrid(
                                id="related-ag-grid",
                                rowData=[],
                                columnDefs=[
                                    {"field": "", "checkboxSelection": True},
                                    {"field": "Date"},
                                    {"field": "PN"},
                                    {"field": "SN"},
                                    {"field": "Description", "sortable": False},
                                    {"field": "Notes", "sortable": False},
                                    {"field": "", "sortable": False},
                                ],
                                columnSize="sizeToFit",
                                dashGridOptions={
                                    "rowSelection": "multiple",
                                    "suppressRowClickSelection": True,
                                    "animateRows": False,
                                    "rowDragManaged": True,
                                    "rowDragEntireRow": True,
                                    "rowDragMultiRow": True,
                                    "rowSelection": "multiple",
                                    "suppressMoveWhenRowDragging": True,
                                },
                                defaultColDef={
                                    "filter": True,
                                    "editable": False,
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
                                dashGridOptions={
                                    "animateRows": False,
                                    "rowDragManaged": True,
                                    "rowDragEntireRow": True,
                                    "rowDragMultiRow": True,
                                    "rowSelection": "multiple",
                                    "suppressMoveWhenRowDragging": True,
                                },
                                defaultColDef={
                                    "filter": True,
                                    "editable": False,
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


#* Copied from https://dash.plotly.com/dash-ag-grid/row-dragging-external-dropzone
clientside_callback(
    ClientsideFunction("addDropZone", "dropZoneGrid2GridComplex"),
    Output("non-related-ag-grid", "id"),
    Input("test-button", "value"),
    State("related-ag-grid", "id"),
    State("non-related-ag-grid", "id")
)


@callback(
    Output("scatter-plot", "figure"),
    Output("related-ag-grid", "rowData"),
    Output("related-ag-grid", "selectedRows"),
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

    return fig, related_events_data, related_events_data, non_related_events_data


@callback(
    Input("related-ag-grid", "selectedRows"),
    State("scatter-plot", "figure"),
    prevent_initial_call=True,
)
def add_event_vertical_lines(row_data, figure):
    min_date = datetime.strptime("2050-12-31", "%Y-%m-%d")
    max_date = datetime.strptime("1000-01-01", "%Y-%m-%d")

    figure = go.Figure(figure)

    # Remove all existing vlines on every callback run
    figure["layout"]["shapes"] = []

    for event in row_data:
        date_obj = datetime.strptime(event["Date"], "%Y-%m-%d")

        figure.add_vline(
            x=date_obj,
            line=dict(dash="dash"),
        )

        min_date = min(min_date, date_obj)
        max_date = max(max_date, date_obj)

    # Set the x-axis range
    figure.update_layout(
        xaxis=dict(range=[min_date - timedelta(weeks=4), max_date + timedelta(weeks=4)])
    )

    # Set the figure prop of scatter plot
    set_props("scatter-plot", {"figure": figure})


if __name__ == "__main__":
    app.run(debug=True)
