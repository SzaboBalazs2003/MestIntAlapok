import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Ellenőrzi, hogy az eredemény listában lévő indexek között van-e él a gráfban. Ha van akkor hamis értékkel tér vissza, mert akkor üti egymást a két királynő.
def is_consistent(graph, result):

    for i in range(len(result)):
        for j in range(i + 1, len(result)):
            if graph[result[i]][result[j]]:
                return False
    return True


# A visszalépéses algoritmus, rekurzívan bejárja a gráfot, és ha minden királynőt lerakott akkor megnézi hogy a kapott eredmény megoldás-e.
def backtracking_c(graph, result, nth_queen, number_of_queens, h=None):

    if nth_queen == number_of_queens:
        return h(graph,result)

    for i in range(len(graph)):
        if i not in result:
            result[nth_queen] = i
            if backtracking_c(graph, result, nth_queen+1, number_of_queens, h):
                return True
            result[nth_queen] = -1
    return False


# Az "n" adja meg hogy mennyi királynőt kell letenni egy mekkora táblán.
# Itt hozom létre a gráfot leíró mátrixot. A help tömb arra van hogy szimulálja a gráf megjelensét.
# A gráfban a node-ok azokkal a node-okkal vannak összekötve, ahova a királynő ütni tud az adott pozícióból.
n=6
size=n*n
help = np.arange(0,n*n).reshape(n,n)
graph=[]
for i in range(n):
    for j in range(n):
        tmp = np.zeros(n*n, dtype=int)
        tmp[i*n:i*n+n]=1
        tmp[j:size:n]=1
        tmp[np.diagonal(help,j-i)]=1
        tmp[np.fliplr(help).diagonal(((n-1)-j)-i)]=1
        graph.append(tmp.tolist())


# A gráf éleinek megadása
G = nx.Graph()
for i in range(len(graph)):
    for j in range(i+1, len(graph)):
        if graph[i][j]:
            G.add_edge(i+1, j+1)


# A result listában tárolom el a megoldások pozícióját.
result = [-1] * n
backtracking_c(graph, result, 0, n, is_consistent)

# Erre azért van szükség, mert a result lista indexeket tárol, a színezéshez, viszont a node key-ét a sorszámát használom.
for i in range(len(result)):
    result[i]+=1

# Meghatározzuk a node-ok színét az alapján, hogy a node benne van-e a result listában.
highlight_colors = []
for i in G.nodes:
    highlight_colors.append("red") if i in result else highlight_colors.append("lightblue")

# Legenerálja a node-ok pozícióját.
positions={}
for i in range(n):
    for j in range(j):
        key = i*n+j+1
        value = (j,n-i)
        positions.update({key:value})

pos=nx.spring_layout(G)
nx.draw(G, positions, node_color=highlight_colors)
nx.draw_networkx_labels(G, positions)
plt.show()

