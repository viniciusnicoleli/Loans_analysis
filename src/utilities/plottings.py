from statsmodels.stats.outliers_influence import variance_inflation_factor
from matplotlib.ticker import FuncFormatter
from matplotlib.cbook import boxplot_stats
from matplotlib import pyplot as plt
from scipy.stats import ks_2samp
import seaborn as sns
import pandas as pd
import numpy as np
import joypy
import os

# Esse arquivo possui 14 plots diferetens para a task 2.


class plotter:
    @staticmethod
    def plotar_dist(df: pd.DataFrame) -> None:
        """Função que plota gráficos de distribuição
        em uma única célula
        """
        fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 10))
        axes = axes.flatten()

        for i, column in enumerate(df.columns):
            df[column].hist(ax=axes[i],
                            edgecolor='white',
                            color='#3366FF'
                        )
            
            axes[i].set_title(f'{column}') 
            axes[i].set_xlabel('') 
            axes[i].set_ylabel('Frequency') 
            
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plotar_dist_four(df: pd.DataFrame) -> None:
        """Função que plota gráficos de distribuição
        em uma única célula
        """
        fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(30, 10))
        axes = axes.flatten()

        for i, column in enumerate(df.columns):
            df[column].hist(ax=axes[i],
                            edgecolor='white',
                            color='#3366FF'
                        )
            
            axes[i].set_title(f'{column}') 
            axes[i].set_xlabel('') 
            axes[i].set_ylabel('Frequency') 
            
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plotar_nested_dist(df: pd.DataFrame, cols: list) -> None:
        """Função que plota gráfico de distribuição nested
        """
        fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 8))
        axes = axes.flatten()

        i = 0
        for col in cols:
            palette = sns.color_palette("Set2", n_colors=len(df[col].unique()))
            sns.histplot(x=df['valor_principal'], hue=df[col],
                          ax=axes[i], kde=False,element='poly',palette=palette)
            axes[i].set_title(f'valor_p cat por {col}') 
            i += 1

        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plotar_scatter(df: pd.DataFrame, col_x: str, col_y: str) -> None:
        """Plota um gráfico de joinplot do seaborn
        com a ideia de comparar duas variáveis
        """
        dot_color = "#3366FF"
        sns.set(style="white", rc={"axes.facecolor": (0.95, 0.95, 1.0)})
        sns.pairplot(df, diag_kind='kde', plot_kws={'alpha': 0.2,"s":3},
                     scatter_kws={'color': dot_color})
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def ks_statistic(df: pd.DataFrame, col: str, value_1: str, value_2: str) -> None:
        """Teste de Kolmogorov Smirnov para checar se as distribuições
        são parecidas
        """
        print(f'Testando para a coluna {col}, para os valores {value_1} e {value_2}')
        grupo_1 = df[df[col] == value_1]['valor_principal']
        grupo_2 = df[df[col] == value_2]['valor_principal']
        ks_statistic, p_value = ks_2samp(grupo_1, grupo_2)
        print('####################################################################')
        if p_value < 0.05:
            print("Rejeitamos a hipótese nula: as distribuições são diferentes")
        else:
            print("Não rejeitamos a hipótese nula: as distribuições não são diferentes")
        print('####################################################################')
    
    @staticmethod
    def corrplot(df: pd.DataFrame) -> None:
        """Plota a correlação de Spearman das variáveis de um DataFrame
        """
        correlation_matrix = df.corr(method='spearman')

        plt.figure(figsize=(8, 6))
        # Criei uns filtros adicionais para embelezar
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
        plt.title('Correlação de Spearman')
        plt.show()

    @staticmethod
    def vif(df: pd.DataFrame)->pd.DataFrame:
        """VIF avalia a correlação Multilinear de variáveis
        numéricas, auxilia na deducação da correlação.
        """
        vif = pd.DataFrame()
        vif['features'] = df.columns
        vif['VIF_Value'] = [variance_inflation_factor(df.values, i) 
                            for i in range(df.shape[1])]
        
        return(vif)
    
    @staticmethod
    def plotar_nested_boxplot(df: pd.DataFrame, cols: list) -> None:
        """Função que plota gráfico de boxplot além de devolver
        quais são os valores que se apresentaram como outliers
        permitindo vermos o tamanho, qtde e valores.
        """
        fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 8))
        axes = axes.flatten()

        i = 0
        outliers = pd.DataFrame()
        for col in cols:
            palette = sns.color_palette("Set2", n_colors=len(df[col].unique()))
            sns.boxplot(df[col], ax=axes[i], palette=palette)
            axes[i].set_title(f'{col} Boxplot') 

            # Coleta os outliers que foram apresentados no gráfico.
            stats = boxplot_stats(df[col])
            outliers[col] = [outlier for outlier in stats[0]['fliers']] + [None] * (len(df) - len(stats[0]['fliers']))

            i += 1

        plt.tight_layout()
        plt.show()

        return outliers
    
    @staticmethod
    def criar_ridge(df: pd.DataFrame)->None:
        """Criar um ridge para avaliar a evolução de cada variável.
        """
        dict_pro_mapping = {1: 'janeiro',
                            2: 'fevereiro',
                            3: 'março',
                            4: 'abril',
                            5: 'maio',
                            6: 'junho',
                            7: 'julho',
                            8: 'agosto',
                            9: 'setembro',
                            10: 'outubro',
                            11: 'novembro',
                            12: 'dezembro'}

        df['month_descrito'] = df['month'].map(dict_pro_mapping)
        df_ridge = df[['month','month_descrito','valor_principal']].sort_values(by='month')
        month_mean_serie = df_ridge.groupby('month_descrito')['valor_principal'].mean()
        df_ridge['mean_month'] = df_ridge['month_descrito'].map(month_mean_serie)

        palette = sns.color_palette("husl", n_colors=len(df_ridge['month'].unique()))
        fig, axes = joypy.joyplot(df_ridge, by='month', column='valor_principal',
                                grid=True, linewidth=1, legend=False, overlap=0.5,
                                labels=df_ridge['month_descrito'].unique(),
                                color=palette, linecolor='k', fade=True)

        for i, ax in enumerate(axes):
            for line in ax.lines:
                line.set_linestyle('--')
                line.set_alpha(0.7)

        for i, (ax, color) in enumerate(zip(axes, palette)):
            if i < len(df_ridge['month'].unique()):
                ax.text(-0.1, 0.15, df_ridge['month_descrito'].unique()[i], transform=ax.transAxes,
                        rotation=0, va='center', ha='right', fontsize=12, fontweight='bold',color=color)
                
        plt.title("Ridgeline para checagem mensal das distribuições", fontsize=12, fontweight='bold')
        plt.subplots_adjust(top=0.85)

        plt.show()
    
    @staticmethod
    def criar_ridge_grande(df: pd.DataFrame)->None:
        dict_pro_mapping = {1: 'janeiro',
                            2: 'fevereiro',
                            3: 'março',
                            4: 'abril',
                            5: 'maio',
                            6: 'junho',
                            7: 'julho',
                            8: 'agosto',
                            9: 'setembro',
                            10: 'outubro',
                            11: 'novembro',
                            12: 'dezembro'}

        df['month_descrito'] = df['month'].map(dict_pro_mapping)
        df_ridge = df[['month','month_descrito','valor_principal']].sort_values(by='month')
        month_mean_serie = df_ridge.groupby('month_descrito')['valor_principal'].mean()
        df_ridge['mean_month'] = df_ridge['month_descrito'].map(month_mean_serie)

        palette = sns.color_palette("husl", n_colors=len(df_ridge['month'].unique()))
        fig, ax = plt.subplots(figsize=(12, 8))

        joypy.joyplot(df_ridge, by='month', column='valor_principal',
                    grid=True, linewidth=1, legend=False, overlap=0.5,
                    labels=df_ridge['month_descrito'].unique(),
                    color=palette, linecolor='k', fade=True, ax=ax)

        for line in ax.lines:
            line.set_linestyle('--')
            line.set_alpha(0.7)

        for i, (month, color) in enumerate(zip(df_ridge['month'].unique(), palette)):
            ax.text(-0.1, (i + 1) / len(df_ridge['month'].unique()), month,
                    transform=ax.transAxes, va='center', ha='right', fontsize=12, fontweight='bold', color=color)

        plt.title("Ridgeline Plot of valor_principal by Month", fontsize=16, fontweight='bold', pad=20)
        plt.subplots_adjust(top=0.85)
        plt.show()

    @staticmethod
    def serie_acumulada_soma(df: pd.DataFrame) -> None:
        """Função que analise a serie temporal 
        com a soma acumulada da mesma.
        """

        df['mes_ano_formatted'] = pd.to_datetime(df['mes_ano'], format='%m_%Y')
        df_accumulated = df.groupby(['operacao','mes_ano_formatted'])['valor_principal'].sum()
        df_accumulated = df_accumulated.reset_index()
        colors = {'Refin': '#437CDF', 'Prod': '#2E4D50', 'Port + Refin': '#0651A8'}

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.lineplot(data=df_accumulated, x="mes_ano_formatted", y="valor_principal", hue="operacao", ax=ax,
                    linewidth=2.5, palette=colors)

        plt.title('Série Temporal: Visualização da soma do valor_principal', fontsize=16, fontweight='bold', pad=10)
        plt.ylabel('Soma valor_principal (Milhão)')
        plt.legend(title='Operação',title_fontsize='x-large',bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize='x-large', ncol=1)

        # Editando a maneira com que aparece a label do eixo Y, antes estava so como 4, 5.
        formatter = FuncFormatter(lambda x, _: f'{x / 1e6:.1f} MM')
        ax.yaxis.set_major_formatter(formatter)

        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def serie_acumulada_media(df: pd.DataFrame) -> None:
        """Função que analise a serie temporal 
        com a soma acumulada da mesma.
        """

        df['mes_ano_formatted'] = pd.to_datetime(df['mes_ano'], format='%m_%Y')
        df_accumulated = df.groupby(['operacao','mes_ano_formatted'])['valor_principal'].mean()
        df_accumulated = df_accumulated.reset_index()
        colors = {'Refin': '#437CDF', 'Prod': '#2E4D50', 'Port + Refin': '#0651A8'}

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.lineplot(data=df_accumulated, x="mes_ano_formatted", y="valor_principal", hue="operacao", ax=ax,
                    linewidth=2.5, palette=colors)

        plt.title('Série Temporal: Visualização da media do valor_principal', fontsize=16, fontweight='bold', pad=10)
        plt.ylabel('Media valor_principal')
        plt.legend(title='Operação',title_fontsize='x-large',bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize='x-large', ncol=1)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def serie_acumulada_soma_ano(df: pd.DataFrame) -> None:
        plt.subplots(figsize=(12,8))
        colors = {'2019': '#437CDF', '2020': '#2E4D50', '2021': '#0651A8', '2022': '#9E9844'}
        df['month'] = df['month'].astype('O')
        sns.lineplot(data=df, x="month", y="valor_principal", hue="ano", palette=colors,ci=None)
        plt.title('Série Temporal: Visualização por mes', fontsize=16, fontweight='bold', pad=10)
        plt.ylabel('Total do valor principal')
        plt.legend(title='Ano',title_fontsize='x-large',bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize='x-large', ncol=1)
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def checar_volumetria(df: pd.DataFrame)->None:
        """Checar a volumetria por mes de cada um dos decentis
        """
        deciles = df['valor_principal'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        df['decile'] = pd.cut(df['valor_principal'], bins=[0] + list(deciles) + [float('inf')], labels=[f'Decentil {label:.1f}' for label in deciles] + ['maior_que_ultimo'], include_lowest=True, right=False)
        df['mes_ano_formatted'] = pd.to_datetime(df['mes_ano'], format='%m_%Y')
        df['mes_ano_formatted'] = df['mes_ano_formatted'].apply(lambda x: x.strftime('%Y-%m-%d'))

        grouped_df = df.groupby(['mes_ano_formatted', 'decile']).size().unstack(fill_value=0)

        grouped_df.plot(kind='bar', stacked=True, figsize=(12, 8))
        plt.title('Distribuição do Decentil ao longo do tempo')
        plt.ylabel('Frequencia')
        plt.legend(title='Decile', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

    @staticmethod
    def checar_volumetria_trimestre(df: pd.DataFrame)->None:
        """Checar a volumetria por trimestre de cada um dos decentis
        """
        deciles = df['valor_principal'].quantile([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        df['decile'] = pd.cut(df['valor_principal'], bins=[0] + list(deciles) + [float('inf')], labels=[f'Decentil {label:.1f}' for label in deciles] + ['maior_que_ultimo'], include_lowest=True, right=False)
        df['mes_ano_formatted'] = pd.to_datetime(df['mes_ano'], format='%m_%Y')
        df['mes_ano_formatted'] = df['mes_ano_formatted'].apply(lambda x: x.strftime('%Y-%m-%d'))
        df['mes_ano_formatted'] = pd.to_datetime(df['mes_ano_formatted'])
        df['quarter_mes_ano'] = df['mes_ano_formatted'].dt.to_period('Q').astype(str)

        grouped_df = df.groupby(['quarter_mes_ano', 'decile']).size().unstack(fill_value=0)
        grouped_df.plot(kind='bar', stacked=True, figsize=(12, 8))
        plt.title('Distribuição do Decentil ao longo do tempo')
        plt.ylabel('Frequencia')
        plt.legend(title='Decile', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

    @staticmethod
    def plotar_soma_linha_temporal(df: pd.DataFrame)->None:
        """Plota o somatório temporal dos dados sem filtros
        """
        df['mes_ano_formatted'] = pd.to_datetime(df['mes_ano'], format='%m_%Y')
        df_accumulated = df.groupby(['mes_ano_formatted'])['valor_principal'].sum()
        df_accumulated = df_accumulated.reset_index()
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.lineplot(data=df_accumulated, x="mes_ano_formatted", y="valor_principal", ax=ax,
                    linewidth=2.5)

        plt.title('Série Temporal: Visualização da soma do valor_principal', fontsize=16, fontweight='bold', pad=10)
        plt.ylabel('valor')

        formatter = FuncFormatter(lambda x, _: f'{int(x/1e6)}MM')
        ax.yaxis.set_major_formatter(formatter)

        plt.show()
    
    @staticmethod
    def plotar_media_linha_temporal(df: pd.DataFrame)->None:
        """plota a média temporal dos dados sem filtros
        """
        df['mes_ano_formatted'] = pd.to_datetime(df['mes_ano'], format='%m_%Y')
        df_accumulated = df.groupby(['mes_ano_formatted'])['valor_principal'].mean()
        df_accumulated = df_accumulated.reset_index()
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.lineplot(data=df_accumulated, x="mes_ano_formatted", y="valor_principal", ax=ax,
                    linewidth=2.5)

        plt.title('Série Temporal: Visualização da media do valor_principal', fontsize=16, fontweight='bold', pad=10)
        plt.ylabel('valor')
        plt.show()
    
    def calculate_psi(self,baseline, current, variable):
        """Função que calcula o PSI
        """
        baseline_counts = baseline[variable].value_counts(normalize=True).sort_index()
        current_counts = current[variable].value_counts(normalize=True).sort_index()

        psi_values = (current_counts - baseline_counts) * np.log(current_counts / baseline_counts)
        psi = psi_values.sum()

        return psi
    
    def get_psi(self,df: pd.DataFrame, variable: str,df_input: pd.DataFrame)->pd.DataFrame:   
        """Função que executa o PSI para diversas variáveis
        """ 
        def custom_sort(value):
            """Função que realiza um sorting
            baseado no YYYYQ{numero_do_quarter}
            Tive que implementar porque não existia.
            """
            year, quarter = value[:-2], value[-2:]
            return int(year), int(quarter[1:])

        df_input['mes_ano_formatted'] = pd.to_datetime(df_input['mes_ano'], format='%m_%Y')
        df_input['mes_ano_formatted_quarterfy'] = df_input['mes_ano_formatted'].apply(lambda x: x.strftime('%Y-%m-%d'))
        df_input['mes_ano_formatted_quarterfy'] = pd.to_datetime(df_input['mes_ano_formatted_quarterfy'])
        df_input['quarter_mes_ano'] = df_input['mes_ano_formatted_quarterfy'].dt.to_period('Q').astype(str)

        i = 0
        psi_values = pd.DataFrame()
        psi = []
        quarter_cur = []
        quarter_bas = []
        var = []
        listing_quarters = df_input['quarter_mes_ano'].value_counts().reset_index().sort_values(by='index', key=lambda x: x.map(custom_sort)).reset_index()['index']
        for quarter in listing_quarters:
            if listing_quarters.index[i] != 0:
                current = df_input[df_input['quarter_mes_ano'] == quarter]
                baseline = df_input[df_input['quarter_mes_ano'] == listing_quarters[i-1]]
                psi.append(self.calculate_psi(baseline=baseline,current=current,variable=variable))
                quarter_cur.append(quarter)
                quarter_bas.append(listing_quarters[i-1])
                var.append(variable)
            i +=1

        psi_values['psi'] = psi
        psi_values['quarter_cur'] = quarter_cur
        psi_values['quarter_bas'] = quarter_bas
        psi_values['variable'] = var
        
        return psi_values