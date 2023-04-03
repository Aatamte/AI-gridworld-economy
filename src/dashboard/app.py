from dash import Dash
from dash import html
from dash import dcc
import plotly.graph_objs as go

from dash import Dash, dcc, html
import plotly.express as px

fig = px.line(x=[1, 2, 3, 4], y=[1, 4, 9, 16], title=r'$\alpha_{1c} = 352 \pm 11 \text{ km s}^{-1}$')
fig.update_layout(
    xaxis_title=r'$\sqrt{(n_\text{c}(t|{T_\text{early}}))}$',
    yaxis_title=r'$d, r \text{ (solar radius)}$'
)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(mathjax=True, figure=fig)]
)

if __name__ == '__main__':
    app.run_server(debug=True)