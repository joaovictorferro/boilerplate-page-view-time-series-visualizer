import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("/workspace/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv")

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) &  # Altura acima do percentil 2.5
        (df['value'] <= df['value'].quantile(0.975))   # Altura abaixo do percentil 97.5
        ]
df['date'] = pd.to_datetime(df['date'])

def draw_line_plot():
    # Draw line plot

  fig = plt.figure(figsize=(10, 6))

  plt.plot(df['date'], df['value'], color='red')

  plt.xlabel('Date')
  plt.ylabel('Page Views')
  plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig

def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = df.copy()

  # Adicionar colunas de ano e mês
  df_bar['year'] = df_bar['date'].dt.year
  df_bar['month'] = df_bar['date'].dt.month
  
  # Agrupar por ano e mês
  grouped = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()
  print(grouped)

  # Draw bar plot

  # Criar o gráfico de barras
  fig = plt.figure(figsize=(12, 6))

  # Usar seaborn para criar o gráfico de barras com a paleta "tab10"
  ax = sns.barplot(x='year', y='value', hue='month', data=grouped, palette="tab10")

  ax.grid(False)

  # Ajustar os rótulos e o título
  plt.xlabel(' Years', fontsize=12)
  plt.ylabel('Average Page Views', fontsize=12)

  # Adicionando os meses como rótulos
  month_labels = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
  ]
  handles, labels = ax.get_legend_handles_labels()

  # Atualizando os rótulos da legenda de acordo com os meses
  month_legend_labels = [month_labels[i-1] for i in range(1, len(labels)+1)]

  # Customizando a legenda
  plt.legend(handles, month_legend_labels, title='Months', loc='upper left')


  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

   # Criar o gráfico com subgráficos
    fig, axs = plt.subplots(ncols=2, figsize=(15, 5))

    # 1. Box Plot por Ano
    sns.boxplot(data=df_box, x='year', y='value', ax=axs[0], palette="tab10")
    axs[0].set(title='Year-wise Box Plot (Trend)', xlabel='Year', ylabel="Page Views")
    axs[0].legend([], [], frameon=False)  # Remover a legenda do gráfico de ano

    # 2. Box Plot por Mês (usando os números dos meses para ordenação)
    sns.boxplot(data=df_box, x='month', y='value', ax=axs[1], palette="tab10")
    axs[1].set(title='Month-wise Box Plot (Seasonality)', xlabel='Month', ylabel="Page Views")

    # Ajustar os rótulos dos meses
    axs[1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    # Remover qualquer legenda do gráfico de mês
    axs[1].legend([], [], frameon=False)


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
