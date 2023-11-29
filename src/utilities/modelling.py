from utilities.components import data_processing
from matplotlib.ticker import FuncFormatter
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os


class modeller(data_processing):
    def __init__(self,df: pd.DataFrame)->pd.DataFrame:
        super().__init__(df=df)
        self.df = self._create_variables(df=df)

    
    def _create_variables(self,df: pd.DataFrame) -> pd.DataFrame:
        """Função que cria todas as variáveis formadas nas etapas anteriores]
        Utiliza do simple_fillna_per_id para a construção do DataFrame
        """
        # Transforma Null para np.nan

        print('FILL NA: Pode levar em torno de 36s')

        df = self.check_na()
        df.sort_values(by='data_operacao',inplace=True)

        # Variáveis criadas para a etapa 1
        df['idade'] = df.apply(lambda x: int(round(((x['data_operacao'] - x['nascimento']).days/365),0)) if str(x['idade']) == 'nan' else x['idade'],axis=1)
        self.simple_fillna_per_id(df=df,col='genero')
        self.simple_fillna_per_id(df=df,col='bairro')
        self.simple_fillna_per_id(df=df,col='cidade')
        self.simple_fillna_per_id(df=df,col='estado')
        self.simple_fillna_per_id(df=df,col='cep')
        self.simple_fillna_per_id(df=df,col='telefone')
        self.simple_fillna_per_id(df=df,col='cartao')
        self.simple_fillna_per_id(df=df,col='email')
        self.simple_fillna_per_id(df=df,col='ocupacao')
        self.simple_fillna_per_id(df=df,col='empregador')

        print('Conclui o FILLNA, criando as variáveis com apply')

        df['bairro'] = df.apply(lambda x: x['bairro'].strip(), axis=1)
        df['cidade'] = df.apply(lambda x: x['cidade'].strip(), axis=1)
        df['estado'] = df.apply(lambda x: x['estado'].strip(), axis=1)

        self.split_email(df=df)
        df.drop(['parcelas','parcelas_pagas'],axis=1,inplace=True)

        # Variáveis criadas para maiores visualizações na etapa 2
        df['idade'] = df['idade'].astype('int')
        df['idade_class'] = pd.cut(df['idade'], bins=[0,30,40,70], labels=['jovem','adulto','adulto_idoso'])
        df['valor_parcela_class'] = pd.cut(df['valor_parcela'], bins=[0,720,1500,7000], labels=['abaixo','acima','muito_acima'])
        df['valor_bruto_class'] = pd.cut(df['valor_bruto'], bins=[float('-inf'),50000,500000], labels=['abaixo','acima'])
        df['valor_bruto_class'].astype('object').fillna('abaixo',inplace=True)
        df['parcelas_pagas_class'] = pd.cut(df['quantidade_parcelas_pagas'], bins=[0,20,60,1000], labels=['abaixo','acima','muito_acima'],include_lowest=True)
        df['parcelas_pagas_class'].astype('object').fillna('normal',inplace=True)
        df['qtde_parcelas_class'] = pd.cut(df['quantidade_parcelas'], bins=[0,60,100,3000], labels=['normal','acima','muito_acima'])
        df['mes_ano'] = df.apply(lambda x: str(x['data_operacao'].month) + '_' + str(x['data_operacao'].year),axis=1)
        df['ano'] = df.apply(lambda x: str(x['data_operacao'].year),axis=1)
        df['month'] = df.apply(lambda x: int(x['data_operacao'].month),axis=1)
        df['month_class'] = pd.cut(df['month'], bins=[1,3,6,9,12], labels=['inicio','inicio_meio','meio_fim','fim'],include_lowest=True)

        print('Conclui as de APPLY, criando as variáveis da Plotter')

        # Variaveis criadas nos plots
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
        df['mes_ano_formatted'] = pd.to_datetime(df['mes_ano'], format='%m_%Y')
        df['mes_ano_formatted'] = df['mes_ano_formatted'].apply(lambda x: x.strftime('%Y-%m-%d'))
        df['mes_ano_formatted'] = pd.to_datetime(df['mes_ano_formatted'])
        df['quarter_mes_ano'] = df['mes_ano_formatted'].dt.to_period('Q').astype(str)

        print(df.shape)
        print('Conclui todas as etapas!')

        return df.reset_index(drop=True)
    
    @staticmethod
    def plotar_soma_linha_temporal(df: pd.DataFrame)->None:
        """Plota o somatório temporal dos dados sem filtros
        """
        plt.subplots(figsize=(12,8))
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
    def desempenho_modelo(resultados: pd.DataFrame, df_arima: pd.DataFrame)->None:
        """Plota o desempenho do modelo e seus resultados.
        """
        plt.subplots(figsize=(12,8))
        plt.plot(resultados.apply(lambda x: np.quantile(x,0.5),axis=1),color='#2EC647',label='mediana')
        plt.plot(resultados.apply(lambda x: np.quantile(x,0.95),axis=1),color='#29A4E1',label='intervalo superior')
        plt.plot(resultados.apply(lambda x: np.quantile(x,0.05),axis=1),color='#1E6F49',label='intervalo inferior')
        plt.plot(df_arima)
        plt.title('Analisando o desempenho do Arima',fontsize='20',pad=10)
        plt.legend(title='Curvas')
        plt.show()
