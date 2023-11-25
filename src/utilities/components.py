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
    def complex_fillna_per_id(col: str, data: pd.DataFrame) -> pd.DataFrame:
        """Preencher os nulos baseado numa regra
        de checar o id anterior e comparar com o id posterior
        utilizando as datas de operação.

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
    
    @staticmethod
    def complex_fillna_cep_complement(df: pd.DataFrame, col: str) -> None:
        """Função que preencha os dados adicionais do CEP como
        bairro, cidade e estado, evitando vazamento de informação.
        """
        ids_nulos = df[df[col].isna()]['id'].unique().tolist()

        for id_nulo in ids_nulos:
            print('Replicando para',id_nulo)

            df_a = df[df['id'] == id_nulo].sort_values(by='data_operacao').reset_index()
            index_todos = df_a[df_a[col].isna()].index.to_list()

            if df_a.shape[0] > 1:
                print('Index dos nulos', index_todos)

                for index_a in index_todos:
                    print('Replicando para o index_a', index_a)

                    cep_id_nulo = df_a.loc[index_a, 'cep']
                    print(cep_id_nulo)
                    dados_filtro = df_a[(df_a['cep'] == cep_id_nulo) & (df_a.index != index_a)][col].value_counts(dropna=False).reset_index()
                    print(dados_filtro)
                    if dados_filtro.empty:
                        print('Não encontrei nenhum CEP igual ao do index, portanto nan')
                        valor_receber = 'nan'
                    else:
                        if dados_filtro[(~dados_filtro['index'].isna())].empty:
                            print('As outras observações desse ID com esse CEP, só possuem nan')
                            valor_receber = 'nan'
                        else:
                            print('Filtrando pela observação que mais aparece')
                            valor_receber = str(dados_filtro[(~dados_filtro['index'].isna())][['index',col]].max()['index'])

                        # valor_receber = str(dados_filtro[(dados_filtro[col] == dados_filtro[col].max()) & (str(dados_filtro[col]) != 'nan')]['index'][0])

                    if valor_receber != 'nan':
                        df.loc[df_a.loc[index_a,'index'],col] = valor_receber
                    else:
                        df.loc[df_a.loc[index_a,'index'],col] = 'no_info'
            
            else:
                print('Apenas uma observação para esse id, no_info')
                df.loc[df_a.loc[index_todos[0],'index'],col] = 'no_info'



    
    @staticmethod
    def simple_fillna_per_id(df: pd.DataFrame, col: str) -> None:
        """Preenche os nulos de maneira simplificada
        utilizando ffill e bfill, se o DataFrame possui apenas 1 observação
        se utiliza então fillna('no_info')

        ffill: pega o valor anterior ao do id
        bfill: pega o valor posterior ao do id
        no_info: quando só existe uma observação para aquele ID.
        """
        df[col] = df.groupby(['id'])[col].transform(lambda x: x.fillna(method='ffill').fillna(method='bfill').fillna('no_info'))
    


