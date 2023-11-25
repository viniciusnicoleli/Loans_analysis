import pandas as pd
import numpy as np
import os

class data_processing:
    def __init__(self,df: pd.DataFrame) -> None:
        self.df = df
        self.df['data_operacao'] = pd.to_datetime(self.df['data_operacao'], format='%Y-%m-%d') 
        self.df['nascimento'] = pd.to_datetime(self.df['nascimento'], format='%Y-%m-%d')
    
    def check_na(self) -> pd.DataFrame:
        """Checar por strings Null não reconhecidas
        pelo código isna()
        """
        for col in self.df.columns:
            data_list = self.df[col].value_counts().reset_index()['index'].to_list()

            if 'Null' in data_list:
                self.df[col].replace({'Null':np.nan},inplace=True)

        return self.df
    
    @staticmethod
    def fill_nulls_per_id(col: str, data: pd.DataFrame) -> pd.DataFrame:
        """Preencher os nulos baseado numa regra
        de checar o id anterior e comparar com o id posterior

        *Coleta os ID's nulos para aquela coluna
        *FOR para cada um dos ID's que possuem nulos
            *Criamos o DataFrame "DF_A" com o ID que o looping iterou organizando os valores da data em ordem
            *Coleto todos os ID's que possuem nulos

            *FOR para cada ID_nulo de todos os index_nulos

                Testagem
                    * IF o DF_A possue mais que um registro

                        * Se não, IF o index não é 0 da iteração e também não é o ultimo valor

                            * Calculo a diferença de dias do index superior e o index inferior
                            * IF a coluna a ser avaliada do index superior é igual a do inferior
                                * Então coloco o index inferior 
                            * ELIF se a diferença de dias do index superior é menor do que a do index inferior
                            * ELSE para coletar o contrário do ELIF acima.

                        * ELSE se Index é zero ou é o ultimo valor NA para aquele ID

                            * IF o index é o ultimo coletar a info do index anterior
                            * IF o index é o primeiro coletar a info do index posterior

                    * ELSE o DF_A possue apenas um registro
                        * Setar o valor do index como no_info
        
        Se o valor posterior ou anterior do index, for escolhido e é NaN, eu seto como no_info.
        """
        # Coletando todos os id's nulos para a col
        ids_nulos = data[data[col].isna()]['id'].unique().tolist()

        for id_nulo in ids_nulos:

            print('Atualizando para o cliente:',id_nulo)

            # Filtrando apenas um dos ID's para correção
            df_a = data[data['id'] == id_nulo].sort_values(by='data_operacao').reset_index()
            print(df_a.shape)
            print(df_a[col])
            index_todos = df_a[df_a[col].isna()].index.to_list()
            print(index_todos)

            for index_a in index_todos:

                print('Indexando por: ',index_a)
                print('Atualizando na base origial, index: ',df_a.loc[index_a,'index'])

                index_up = index_a + 1
                index_down = index_a -1

                if df_a.shape[0] > 1:
                    if index_a != 0 and index_a < len(df_a[col])-1:

                        days_diff_up = (df_a.iloc[index_up]['data_operacao'] - df_a.iloc[index_a]['data_operacao']).days
                        days_diff_down = (df_a.iloc[index_a]['data_operacao'] - df_a.iloc[index_down]['data_operacao']).days

                        if df_a.iloc[index_down][col] == df_a.iloc[index_up][col]:
                            print('São os mesmos cols, preenchendo com o index_down')
                            if str(df_a.iloc[index_down][col]) != 'nan':
                                data.loc[df_a.loc[index_a,'index'],col] = df_a.iloc[index_down][col]
                            else:
                                data.loc[df_a.loc[index_a,'index'],col] = 'no_info'
                        
                        elif days_diff_up < days_diff_down:
                            print('Eles não são iguais e a diferença de dias para cima é menor que para baixo, colocando-se com o index_up')
                            if str(df_a.iloc[index_up][col]) != 'nan':
                                data.loc[df_a.loc[index_a,'index'],col] = df_a.iloc[index_up][col]
                            else:
                                data.loc[df_a.loc[index_a,'index'],col] = 'no_info'

                        else:
                            print('Eles não são iguais e a diferença de dias para baixo é menor que para cima, colocando-se com o index_down')
                            if str(df_a.iloc[index_down][col]) != 'nan':
                                data.loc[df_a.loc[index_a,'index'],col] = df_a.iloc[index_down][col]
                            else:
                                data.loc[df_a.loc[index_a,'index'],col] = 'no_info'
                    
                    elif index_a == len(df_a[col])-1:
                        print('Último valor da lista, portanto indexando com o anterior')
                        if str(df_a.iloc[index_down][col]) != 'nan':
                            data.loc[df_a.loc[index_a,'index'],col] = df_a.iloc[index_down][col]
                        else:
                            data.loc[df_a.loc[index_a,'index'],col] = 'no_info'

                    else:
                        print('Index_a era zero e não o último valor, então substituindo por superior')
                        if str(df_a.iloc[index_up][col]) != 'nan':
                            data.loc[df_a.loc[index_a,'index'],col] = df_a.iloc[index_up][col]
                        else:
                            data.loc[df_a.loc[index_a,'index'],col] = 'no_info'
                else:
                    print('Df_a tem apenas uma observação, inserindo no_info')
                    data.loc[df_a.loc[index_a,'index'],col] = 'no_info'

        return data
