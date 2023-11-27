import pandas as pd
import numpy as np
import os
from utilities.components import data_processing


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
