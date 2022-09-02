import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, graph_name, aggregation, is_diff):
        self._graph_name = graph_name
        self._aggregation = aggregation
        self._is_diff = is_diff
        self._axes = self._create_figure()

    def _create_figure(self):
        """Create figure and axes with right sizes and settings for axis."""
        fig, axes = plt.subplots(figsize=(30, 15))
        if self._is_diff:
            axes.set_title(f'Времена ответов сервисов (агрегирование={self._aggregation}мин)', fontsize=30)
            axes.set_ylabel('Время ответа сервиса, с', fontsize=18, rotation=90)
        else:
            axes.set_title(f'Интенсивность ошибок (агрегирование={self._aggregation}мин)', fontsize=30)
            axes.set_ylabel('Количество за единицу времени, шт', fontsize=18, rotation=90)
        axes.set_xlabel('Время возникновения, чч:мм', fontsize=18)
        axes.grid(color='gray', linewidth=1, linestyle=':')
        axes.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(30))
        axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
        axes.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(30))
        axes.tick_params(axis='x', labelrotation=45, labelsize=18)
        axes.tick_params(axis='y', labelsize=18)
        fig.subplots_adjust(bottom=0.2)
        return axes

    def plot_graph(self, filename):
        """Add graph on created figure from table from filename."""
        row_df = pd.read_csv(
            filename,
            delimiter=";",
            parse_dates=[0, ],
            infer_datetime_format=True
        )
        row_df = row_df.set_index(row_df.columns[0])  # column with date set like an index

        if self._is_diff:
            row_df['response_time'] = row_df.index.asi8 // 10 ** 6  # datetime to timestamp in ms
            response_time_df = row_df.groupby(by=[row_df.columns[0]]).diff().dropna()  # find response times
            result_df = response_time_df.resample(f"{self._aggregation}T").mean()
            result_df['response_time'] = result_df['response_time'] / 1000  # from msec to sec
        else:
            result_df = row_df.resample(f"{self._aggregation}T").count()

        result_filename = filename.rsplit(".", 1)[0] + "_aggregated.csv"
        with open(result_filename, "w") as file:
            result_df.to_csv(file, index=True)
        self._axes.plot(result_df.index, result_df[result_df.columns[0]], linewidth=1)

    def set_legend(self, descriptions):
        """Set legend after all graphs was plotted."""
        self._axes.legend(descriptions, fontsize=16, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.25))

    def save_figure(self):
        """Save figure in filename"""
        plt.savefig(self._graph_name)
