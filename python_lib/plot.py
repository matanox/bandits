import pandas as pd

def interval_binner(df, datetime_column, aggregation_interval_minutes):
    ''' bins the input dataframe data via a new dataframe column '''
    binned = df.groupby(pd.Grouper(
            key = datetime_column, 
            freq = str(aggregation_interval_minutes)+'Min', 
            label='left', 
            sort=True))

    interval_starts = []
    for bin_idx, bin_member_indices in binned.indices.items():
        for bin_member_index in bin_member_indices:
            interval_starts.append(bin_idx) 

    sorted_df = binned.apply(pd.DataFrame)            
    sorted_df['interval_start'] = interval_starts # using iloc directly is orders of magnitude slower
    
    return binned


def is_google_colaboratory_runtime():
    return get_ipython().__class__.__module__ == "google.colab._shell"

def colaboratory_enable_plotly():
  ''' for plotly working also in google colaboratory (source: https://stackoverflow.com/a/47230966/1509695) '''
  import IPython
  display(IPython.core.display.HTML('''
        <script src="/static/components/requirejs/require.js"></script>
        <script>
          requirejs.config({
            paths: {
              base: '/static/base',
              plotly: 'https://cdn.plot.ly/plotly-latest.min.js?noext',
            },
          });
        </script>
        '''))

def enable_for_google_colaboratory():
    if is_google_colaboratory_runtime():
        colaboratory_enable_plotly()


from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

def get_layout_dict(title='', x_axis_title='', y_axis_title=''):
    return dict(
        title='<b>'+title+'</b>',
        titlefont=dict(
                family='Courier New',
                size=22,
                color='#0077af'),
        xaxis=dict(
            title='<i>'+x_axis_title+'</i>',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'),
            showgrid=False,
            zeroline=False),
        yaxis=dict(
            title='<i>'+y_axis_title+'</i>',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'),
            showgrid=False,
            zeroline=False))



def plot_series(title, x_axis_title, y_axis_title, df, series, lines=False, fill=False, smoothing_fn=None, sliding_window_size=None, marker_size=5):
    ''' plot a set of series from a dataframe, in a jupyter notebook '''
    
    enable_for_google_colaboratory()
    
    layout_dict = get_layout_dict(title, x_axis_title, y_axis_title)
    
    init_notebook_mode(connected=True)
    
    normalized_series = []
    for serie in series:
        if not isinstance(serie, dict):
            normalized = dict(column=serie, display_name=serie)
        elif not 'display_name' in serie:
            normalized = dict(column=serie['column'],  display_name = serie['column'])
        else:
            normalized = serie
        normalized_series.append(normalized)
    
    series = normalized_series
    
    if lines or sliding_window_size:
        plot_mode = 'lines+markers'
    else:
        plot_mode = 'markers'
        
    if fill:
        fill='tozeroy'
    else:
        fill='none'
        
    if not sliding_window_size:
        
        plotly_series = [
            go.Scatter(
                x=df.index, 
                y=df[serie['column']], 
                name=serie['display_name'],
                mode = plot_mode,
                fill = fill,
                marker = dict(size = marker_size),
                hoverlabel = dict(namelength = -1)) for serie in series]
    
    else:

        sliding_window_index = df.index[sliding_window_size-1:]               
        plotly_series = [
            go.Scatter(
                x=sliding_window_index, 
                y=smoothing_fn(df[serie['column']], sliding_window_size), 
                name=serie['display_name'],
                mode = plot_mode,
                fill = fill,
                hoverlabel = dict(namelength = -1)) for serie in series]
     
    if layout_dict:
        iplot(dict(data=plotly_series, layout=go.Layout(**layout_dict)))
    else:
        iplot(plotly_series)


def plot_serie(title, x, y, serie_name, lines=False, marker_size=5):
    ''' plot a single serie in a jupyter notebook '''
    
    enable_for_google_colaboratory()
    
    layout_dict = get_layout_dict(title)
    
    if lines:
        plot_mode = 'lines+markers'
    else:
        plot_mode = 'markers'
    
    init_notebook_mode(connected=True)
    plotly_serie = go.Scatter(
        x=x,
        y=y,
        name=serie_name,
        mode = plot_mode,
        marker = dict(size = marker_size),
        hoverlabel = dict(namelength = -1))
        
    if layout_dict:
        iplot(dict(data=[plotly_serie], layout=go.Layout(**layout_dict)))
    else:
        iplot(plotly_series)

def to_sliding_window_series_end(series, window_size):
    '''sliding window taking window_size elements before each element, and the element itself'''
    display_range = range(window_size,len(series))
    return [series[idx - window_size : idx + 1].mean() 
           for idx in display_range]

assert list(to_sliding_window_series_end(pd.Series(range(10)), window_size=1)) == [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]
assert list(to_sliding_window_series_end(pd.Series(range(10)), window_size=4)) == [2.0, 3.0, 4.0, 5.0, 6.0, 7.0]


def to_sliding_window_series_middle(series, window_size):
    '''sliding window taking window_size elements before each element, the element itself, 
       and window_size elements folling the element'''
    display_range = range(window_size,len(series)-window_size)
    return [series[idx - window_size : idx + window_size+1].mean() 
           for idx in display_range]

to_sliding_window_series_middle(pd.Series(range(10)), window_size=1)
assert list(to_sliding_window_series_middle(pd.Series(range(10)), window_size=1)) == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
assert list(to_sliding_window_series_middle(pd.Series(range(10)), window_size=4)) == [4.0, 5.0]
