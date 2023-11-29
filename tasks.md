 - Desafio Técnico Paraná Banco -

 Descrição da Task:

Nesta avaliação encaminhamos em anexo um arquivo compactado com dados em csv. 
A base de dados apresenta informações fictícias sobre operações de clientes de uma instituição bancária. 
O tempo previsto para execução desta atividade é de até 2h. 
Utilizando Python e Jupyter Notebook, faça as seguintes tarefas: 

1.	[DONE] Faça uma análise inicial dos dados: você encontrou algum problema? Como você trataria estes problemas?

* Nulos NOK [DONE]
    * Utilizar a func da classe para
        * cep 
        * telefone
        * cartao
        * ocupacao
        * empregador
        * bairro [checar]
        * cidade [checar]
        * estado [checar]
    sns.pairplot(data=penguins, hue="species")
* Tipagem de dados [Chnage DateTime]
* Duplicatas [Não tem duplicatas]
* Alterar textos
* Checagem de colunas desnecessárias
* Utilizar CSS e HTML markdown


2.	Faça uma análise exploratória dos dados: distribuições de variáveis, outliers, correlações, etc.

* Distribuições
    * Variaveis padrão [DONE]
    * Variaveis em um scatterplot e dists [DONE]
    * Variaveis nested e teste kolmogorov smirnov [DONE]
* Outliers [Cooks distance, boxplot] [DONE]
    Estudo dos outliers [DONE]
* Correlações [Spearman, VIF] [DONE]
* Gráficos free [Ridge line] [DONE]
* Gráficos de séries temporais [Média {Operação}, Soma] [DONE]
* Gráfico de temporais utilizando bins [mensal, trimestral] [DONE]
* Calcular o PSI [DONE]

* Teste de hipótese

3.	Faça uma projeção do crescimento da carteira para os próximos 2 anos em termos de volume de operações e da carteira utilizando os métodos de ciência de dados que julgar mais adequados para essa tarefa.
* Fazer uma classe que cria todas as variáveis passadas [DONE]
* Entender a fundo o problema [DONE]
* Avaliar os residuos das correlações para entender a presença de sazonalidade e ruído branco com reg linear [DONE]
* Utilizando ARIMA fazer uma predição ao longo de 2 anos da quantidade de Empréstimo da Carteira [DONE]
* Utilizando ARIMA fazer uma predição ao longo de 2 anos da quantidade de contratos [DONE]


* Organizar o código. [DONE]
* Fazer os gráficos para ANO. [WORKING]

