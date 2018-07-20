import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
app.scripts.config.serve_locally = True

app.layout = html.Div([
	html.H2('Daily Progress Tracker', style={'textAlign' : 'center'}),
	html.Div([
		html.Div([
			html.Div([
				html.H4('How many Tasks? '),
				dcc.Input(id='total-tasks', type='text', placeholder='Total Tasks: ', value=3),
			], style={'margin-bottom' : 35, 'textAlign' : 'center'}),
			html.Div(id='daily-table'),
			html.Div(dt.DataTable(id='table', rows=[{}]), style={'display' : 'none'}),
		], className='six columns'),
		html.Div([
			dcc.Graph(id='daily-progress')
		], className='six columns')
	], className='row')
])

@app.callback(
	Output('daily-table', 'children'),
	[Input('total-tasks', 'value')]
)
def decide_total_tasks(tasks):
	try:
		today_tasks = int(tasks)
		specific_day = {
			'Tasks' : [None] * today_tasks,
			'Time Estimated (hrs)' : [None] * today_tasks,
			'Time Taken (hrs)' : [None] * today_tasks 
		}
		specific_day = pd.DataFrame(specific_day)
		specific_day = specific_day[['Tasks', 'Time Estimated (hrs)', 'Time Taken (hrs)']]

		return html.Div([
			dt.DataTable(
				rows=specific_day.to_dict('records'),
				columns=specific_day.columns,
				editable=True
			)
		], style={'textAlign' : 'center'})
	except Exception as e:
		return html.Div([
			html.H2('Please provide a number')
		], style={'textAlign' : 'center'})


@app.callback(
	Output('daily-progress', 'figure'),
	[Input('table', 'rows')]
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
