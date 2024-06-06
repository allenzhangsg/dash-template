import time
import logging

from dash import register_page, html, callback, dcc, Output, Input, get_app
import _utils

register_page(__name__, path="/dashboard1")
app_logger: logging.Logger = get_app().logger

layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Option 1', 'value': '1'},
            {'label': 'Option 2', 'value': '2'},
            {'label': 'Option 3', 'value': '3'}
        ],
        value='1'  # Default value
    ),
    html.Div(id='my-output')
])


# Define the callback to update the output div
@callback(
    Output('my-output', 'children'),
    [Input('my-dropdown', 'value')]
)
@_utils.timing(logger=app_logger, filename=__name__)
def update_output(selected_value):
    time.sleep(4)
    return f'You have selected: {selected_value}'
