import dash_design_kit as ddk
from dash import Dash

app = Dash(__name__)
server = app.server  # expose server variable for Procfile

app.layout = ddk.App()

if __name__ == "__main__":
    app.run(debug=True)
