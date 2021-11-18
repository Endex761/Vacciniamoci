import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from settings import IMG_INPUT_DATA, IMG_FILE 


class ImageGenerator():

    def __init__(self) -> None:
        self.img_file = IMG_FILE
        self.source = IMG_INPUT_DATA

    def generate(self) -> None:

        # read the full data from remote
        df_csv = pd.read_csv(self.source)

        # clean the dataframe
        df_csv = df_csv[['data_somministrazione','totale','prima_dose','seconda_dose']]
        
        # sum data by day
        aggregated_df = df_csv.groupby(by='data_somministrazione').sum()

        # code to generate the chart
        cumsum_df = aggregated_df.cumsum()

        labels = ['seconda dose','prima dose']
        colors = ['#258EA6', '#549F93']

        sns.set_style('whitegrid')

        fig, ax = plt.subplots()

        sns.lineplot(data=cumsum_df, x=cumsum_df.index, y='prima_dose', color=colors[0], ax=ax, label="prima dose")
        sns.lineplot(data=cumsum_df, x=cumsum_df.index, y='seconda_dose', color=colors[1], ax=ax, label="seconda dose")
        ax.set_xticks(ax.get_xticks()[::60]) 

        ax.fill_between(cumsum_df.index, cumsum_df['prima_dose'],cumsum_df['seconda_dose'], color=colors[0], alpha=.5)
        ax.fill_between(cumsum_df.index, cumsum_df['seconda_dose'],[0 for _ in range(len(cumsum_df))], color=colors[1], alpha=.5)
        ax.tick_params(axis='x', rotation=0)
        ax.legend(loc='upper left')

        ax.ticklabel_format(axis='y', style='sci', scilimits=(6,6))
        plt.title('Vaccinazioni fino al ' + cumsum_df.index[-1])
        plt.xlabel('Data')
        plt.ylabel('Vaccinati [mln]')

        # save the image
        fig.savefig(IMG_FILE)
        