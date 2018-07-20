import dash
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
app.scripts.config.serve_locally = True

today_tasks = 15

specific_day = {
	'Tasks' : [None] * today_tasks,
	'Time Estimated (hrs)' : [None] * today_tasks,
	'Time Taken (hrs)' : [None] * today_tasks 
}

specific_day = pd.DataFrame(specific_day)
specific_day = specific_day[['Tasks', 'Time Estimated (hrs)', 'Time Taken (hrs)']]

app.layout = html.Div([
	html.Div([
		html.Div([
			html.H4('Daily Progress Tracker', style={'textAlign' : 'center'}),
			dcc.Location(id='location', refresh=False),
			html.Div(id='output'),
			dt.DataTable(
				id='daily-table',
				rows=specific_day.to_dict('records'),
				columns=specific_day.columns,
				editable=True
			)
		], className='five columns', style={'textAlign' : 'center'}),
		html.Div([
			html.H4('Progress Graph', style={'textAlign' : 'center'}),
			dcc.Graph(id='daily-progress'),
		], className='seven columns')
	], className='row'),
	html.Div([
		dcc.Textarea(
			placeholder='Remarks',
			value='',
			rows=50,
			style={'width' : '60%'},
			wrap=True,
			lang='en'
		)
	], style={'textAlign' : 'center'})
])

@app.callback(
	Output('daily-progress', 'figure'),
	[Input('daily-table', 'rows')]
)
def track_progress(rows):
	ddf = pd.DataFrame(rows)
	return {
		'data' : [
			{'x' : ddf['Tasks'], 'y' : ddf['Time Estimated (hrs)'], 'name' : 'Estimated'},
			{'x' : ddf['Tasks'], 'y' : ddf['Time Taken (hrs)'], 'name' : 'Taken'}
		]
	}

app.css.append_css({
	'external_url' : 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
	app.run_server(debug=True)