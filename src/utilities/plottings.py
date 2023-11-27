from statsmodels.stats.outliers_influence import variance_inflation_factor
from matplotlib.cbook import boxplot_stats
from matplotlib import pyplot as plt
from scipy.stats import ks_2samp
import seaborn as sns
import pandas as pd
import numpy as np
import os

class plotter:
    
    # Idade
    # genero [barplot] str
    # estado str
    # operacao str
    # valor_principal int
    # quantidade_parcelas int 
    # quantidade_parcelas_pagas int
    # taxa_contrato int
    # valor_parcela int
    # valor_bruto int


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

        # Create a heatmap
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

