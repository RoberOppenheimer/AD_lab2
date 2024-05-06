import numpy as np
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from scipy.signal import iirfilter, filtfilt

app = dash.Dash(__name__)

t = np.linspace(0, 60, 1000)

def generate_harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise=True, filter_noise=False,
                                 nyquist=0.5 * 1000, cutoff_freq=0.1):

    harmonic = amplitude * np.sin(frequency * t + phase)
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
    signal_with_noise = harmonic + noise

    if filter_noise:
        b, a = iirfilter(4, cutoff_freq/nyquist, btype='highpass', ftype='butter')
        filtered_signal = filtfilt(b, a, signal_with_noise)
    else:
        filtered_signal = signal_with_noise

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=filtered_signal, mode='lines', name='Гармоніка'))

    if show_noise:
        fig.add_trace(go.Scatter(x=t, y=noise, mode='lines', name='Шум'))

    fig.update_layout(
        title='Гармоніка з шумом',
        xaxis_title='Час',
        yaxis_title='Амплітуда',
        showlegend=True,
        template='plotly_white'
    )

    return fig

default_amplitude = 1
default_frequency = 1
default_phase = 0
default_noise_mean = 0
default_noise_covariance = 0
default_show_noise = False
default_filter_noise = False



app.layout = html.Div([
    html.H1("Гармоніка з шумом"),
    dcc.Graph(id='graph'),
    dcc.Checklist(
        id='show-noise',
        options=[{'label': 'Показати шум', 'value': 'show'}],
        value=[]
    ),
    html.Label('Амплітуда гармоніки'),
    dcc.Slider(
        id='amplitude-slider',
        min=0,
        max=2,
        step=0.1,
        value=default_amplitude,
        marks={0: '0', 1: '1', 2: '2'}
    ),
    html.Label('Частота гармоніки'),
    dcc.Slider(
        id='frequency-slider',
        min=0,
        max=10,
        step=0.1,
        value=default_frequency,
        marks={0: '0', 5: '5', 10: '10'}
    ),
    html.Label('Амплітуда шуму'),
    dcc.Slider(
        id='noise-amplitude-slider',
        min=-0.5,
        max=0.5,
        step=0.1,
        value=default_noise_mean,
        marks={-0.5: '-0.5', 0: '0', 0.5: '0.5'}
    ),
    html.Label('Дисперсія шуму'),
    dcc.Slider(
        id='noise-covariance-slider',
        min=0,
        max=1,
        step=0.001,
        value=default_noise_covariance,
        marks={0: '0', 0.5: '0.05', 1: '1'}
    ),
    dcc.Checklist(
        id='filter-noise',
        options=[{'label': 'Фільтрувати шум', 'value': 'filter'}],
        value=[]
    ),
    dcc.Graph(id='filtered-graph'),
    html.Label('Частота Найквіста'),
    dcc.Slider(
        id='nyquist-slider',
        min=0.01,
        max=1000,
        step=0.01,
        value=0.01,
        marks={0.01: '0.01', 500: '500', 1000: '1000'}
    ),
    html.Label('Частота зрізу'),
    dcc.Slider(
        id='cutoff-freq-slider',
        min=0.001,
        max=0.2,
        step=0.001,
        value=0.001,
        marks={0.001: '0.001', 0.1: '0.1', 0.2: '0.2'}
    ),
    html.Button('Скинути', id='reset-button', n_clicks=0)
])



@app.callback(
    Output('graph', 'figure'),
    [Input('amplitude-slider', 'value'),
     Input('frequency-slider', 'value'),
     Input('noise-amplitude-slider', 'value'),
     Input('noise-covariance-slider', 'value'),
     Input('show-noise', 'value')]
)
def update_graph_on_change(amplitude, frequency, noise_amplitude, noise_covariance, show_noise):
    if 'show' in show_noise:
        show_noise_flag = True
    else:
        show_noise_flag = False

    fig = generate_harmonic_with_noise(amplitude, frequency, default_phase, noise_amplitude,
                                       noise_covariance, show_noise_flag)
    return fig


@app.callback(
    Output('filtered-graph', 'figure'),
    [Input('amplitude-slider', 'value'),
     Input('frequency-slider', 'value'),
     Input('noise-amplitude-slider', 'value'),
     Input('noise-covariance-slider', 'value'),
     Input('show-noise', 'value'),
     Input('filter-noise', 'value'),
     Input('nyquist-slider', 'value'),
     Input('cutoff-freq-slider', 'value')]
)
def update_filtered_graph(amplitude, frequency, noise_amplitude, noise_covariance, show_noise, filter_noise, nyquist, cutoff_freq):
    if 'filter' in filter_noise:
        filter_noise_flag = True
    else:
        filter_noise_flag = False

    fig = generate_harmonic_with_noise(amplitude, frequency, default_phase, noise_amplitude,
                                       noise_covariance, show_noise, filter_noise_flag, nyquist, cutoff_freq)
    return fig


@app.callback(
    Output('amplitude-slider', 'value'),
    Output('frequency-slider', 'value'),
    Output('noise-amplitude-slider', 'value'),
    Output('noise-covariance-slider', 'value'),
    Output('show-noise', 'value'),
    Output('filter-noise', 'value'),
    Output('nyquist-slider', 'value'),
    Output('cutoff-freq-slider', 'value'),
    [Input('reset-button', 'n_clicks')]
)
def reset_parameters_on_click(n_clicks):
    if n_clicks > 0:
        return default_amplitude, default_frequency, default_noise_mean, default_noise_covariance, [], [], 5, 0.1
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)
