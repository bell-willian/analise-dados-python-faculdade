#Neste momento inicial do codigo eu importo as lib que usarei durante o codigo que são sqlite3, pandas,matplotlib e seaborn
import sqlite3 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#Agora nos fazemos a conexão com banco de dados via sqlite3.connect('dados_vendas.db')
conexao = sqlite3.connect('dados_vendas.db')
#Agora criamos o cursor que serve como um ponteiro no codigo atraves do codigo conexao.cursor()
cursor = conexao.cursor()
#Agora uso um comando cursor.execute() para criar o banco de dados caso ele não exista caso ele exista não ira acontecer nada
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas1(
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    data_venda DATE,
    produto TEXT,
    categoria TEXT,
    valor_venda REAL
)
''')
#Agora uso o mesmo comando para inserir dados ao banco de dados usando INSERT INTO vendas1 
cursor.execute('''
INSERT INTO vendas1(data_venda,produto,categoria,valor_venda)VALUES
    ('2023-01-01', 'Produto A', 'Eletrônicos', 1500.00),
    ('2023-01-05', 'Produto B', 'Roupas', 350.00),
    ('2023-02-10', 'Produto C', 'Eletrônicos', 1200.00),
    ('2023-03-15', 'Produto D', 'Livros', 200.00),
    ('2023-03-20', 'Produto E', 'Eletrônicos', 800.00),
    ('2023-04-02', 'Produto F', 'Roupas', 400.00),
    ('2023-05-05', 'Produto G', 'Livros', 150.00),
    ('2023-06-10', 'Produto H', 'Eletrônicos', 1000.00),
    ('2023-07-20', 'Produto I', 'Roupas', 600.00),
    ('2023-08-25', 'Produto J', 'Eletrônicos', 700.00),
    ('2023-09-30', 'Produto K', 'Livros', 300.00),
    ('2023-10-05', 'Produto L', 'Roupas', 450.00),
    ('2023-11-15', 'Produto M', 'Eletrônicos', 900.00),
    ('2023-12-20', 'Produto N', 'Livros', 250.00);
''')
#Aqui eu faço os commit no banco de dados para que tudo seja feito
conexao.commit()
#agora nessa parte eu carrego os datos em um DataFrame usando a variavel vendas para selecionar todos os dados da tabela vendas1
vendas = 'SELECT * FROM vendas1'
#e agora uso df_vendas para carregar tudo no DataFrame
df_vendas = pd.read_sql_query(vendas, conexao)
#Agora começo a parte de analise dos dados em meu codigo
#Nesse primeiro momento eu analiso a quantidade de vendas por categoria na variavel contagem_caregoria uso ela para somar quantas vezes cada categoria apareceu na tabela assim sabendo quantas vendas teve por categoria
print('---QUANTIDADE DE VENDAS POR CATEGORIA---')
serie_categoria = pd.Series(df_vendas['categoria'])
contagem_categoria = serie_categoria.value_counts()
print(contagem_categoria)
#Agora eu analise o valor total de vendas por categoria  com a variavel total_categoria eu uso a função groupby que agrupa as linhas que tem algo em comum e no final uso a função .sum() para somar os valores de cada categoria
total_categoria = df_vendas.groupby('categoria')['valor_venda'].sum()
print('\n---VALOR TOTAL POR CATEGORIA---')
print(total_categoria)
#Agora eu analise a media de vendas por categoria  é basicamente a mesma coisa do caso passado porem no lugar de somar usando .sum() eu uso o .mean() para pegar a media
media_categoria = df_vendas.groupby('categoria')['valor_venda'].mean()
print('\nVALOR MEDIO POR CATEGORIA')
print(media_categoria)
#Agora eu analiso a venda mensal é bem parecido com os casos anteriores porem agora uso a td_datetime para pegar os meses e no final uso a groupby novamente para somar os valores dentro dos meses
df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])
df_vendas['mes'] = df_vendas['data_venda'].dt.to_period('M')
vendas_mensais = df_vendas.groupby('mes')['valor_venda'].sum()
print('\nVALOR VENDAS MENSAL')
print(vendas_mensais)
#Agora analiso qual foi o produto mais caro e o mais barato usando .loc para isso e tbm uso o .idxmax() que serve para ver o maior valor e  o idxmin() para achar o menor valor
produto_mais_caro = df_vendas.loc[df_vendas['valor_venda'].idxmax()]
produto_mais_barato = df_vendas.loc[df_vendas['valor_venda'].idxmin()]
print('\nPRODUTO MAIS CARO')
print(produto_mais_caro)
print('\nPRODUTO MAIS BARATO')
print(produto_mais_barato)
#Agora faço um grafico em barras para mostrar o total de vendas por categoria usando matplotlib e seaborn(sns.barplot)
total_por_categoria = df_vendas.groupby('categoria')['valor_venda'].sum().sort_values()

plt.figure(figsize=(8, 6))
sns.barplot(x=total_por_categoria.values, y=total_por_categoria.index)
plt.title('Total de Vendas por Categoria')
plt.xlabel('Valor Total (R$)')
plt.ylabel('Categoria')
plt.tight_layout()
plt.show()
#Agora eu faço um grafico em barras que mostra o total de vendas por mês  usando novamente o matplotlib e seaborn como o caso anterior porem agora as barras estão ao contrario do caso anterior
df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])
df_vendas['mes'] = df_vendas['data_venda'].dt.to_period('M').astype(str)

vendas_mensais = df_vendas.groupby('mes')['valor_venda'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=vendas_mensais, x='mes', y='valor_venda', color='skyblue')
plt.title('Total de Vendas por Mês')
plt.xlabel('Mês')
plt.ylabel('Valor Total (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#Aqui agora faço um grafico em pizza usando apenas o matplotlib podemos fazer o grafico de pizza usando plt.pie
total_categoria = df_vendas.groupby('categoria')['valor_venda'].sum()

plt.figure(figsize=(6, 6))
plt.pie(total_categoria, labels=total_categoria.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('Participação das Categorias no Total de Vendas')
plt.axis('equal')
plt.show()