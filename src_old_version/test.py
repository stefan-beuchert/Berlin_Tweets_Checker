import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()


def load_data(path):
    df = pd.read_csv(path)
    return df


path = '../data/data_backup.csv'
data = load_data(path)
print(data.columns)

# visualize number of tweets per districts as bubbles

# visualize keywords (hasttags) for the tweets

tokens = []
lemma = []
pos = []
parsed_doc = []

for doc in nlp.pipe(data['text'].astype('unicode').values, batch_size=50):
    if doc.has_annotation("DEP"):
        parsed_doc.append(doc)
        # tokens.append([n.text for n in doc])
        # lemma.append([n.lemma_ for n in doc])
        # pos.append([n.pos_ for n in doc])
    else:
        print("parsing failed")
        # We want to make sure that the lists of parsed results have the
        # same number of entries of the original Dataframe, so add some blanks in case the parse fails
        # tokens.append(None)
        # lemma.append(None)
        # pos.append(None)

data['parsed_doc'] = parsed_doc
# data['comment_tokens'] = tokens
# data['comment_lemma'] = lemma
# data['pos_pos'] = pos

raw_G = nx.Graph()  # undirected
n = 0

for i in data['parsed_doc']:  # sure, it's inefficient, but it will do
    for j in data['parsed_doc']:
        if i != j:
            if not (raw_G.has_edge(j, i)):
                sim = i.similarity(j)
                raw_G.add_edge(i, j, weight=sim)
                n = n + 1

print(raw_G.number_of_nodes(), "nodes, and", raw_G.number_of_edges(), "edges created.")

edges_to_kill = []
min_wt = 0.9  # this is our cutoff value for a minimum edge-weight

for n, nbrs in raw_G.adj.items():
    # print("\nProcessing origin-node:", n, "... ")
    for nbr, eattr in nbrs.items():
        # remove edges below a certain weight
        data = eattr['weight']
        if data < min_wt:
            # print('(%.3f)' % (data))
            # print('(%d, %d, %.3f)' % (n, nbr, data))
            # print("\nNode: ", n, "\n <-", data, "-> ", "\nNeighbour: ", nbr)
            edges_to_kill.append((n, nbr))

print("\n", len(edges_to_kill) / 2, "edges to kill (of", raw_G.number_of_edges(), "), before de-duplicating")

for u, v in edges_to_kill:
    if raw_G.has_edge(u, v):  # catches (e.g.) those edges where we've removed them using reverse ... (v, u)
        raw_G.remove_edge(u, v)

strong_G = raw_G
print(strong_G.number_of_edges())

plt.rcParams['figure.figsize'] = [16, 9]  # a better aspect ratio for labelled nodes

nx.draw(strong_G, pos, font_size=3, node_size=50, edge_color='gray', with_labels=False)
for p in pos:  # raise positions of the labels, relative to the nodes
    pos[p][1] -= 0.03
nx.draw_networkx_labels(strong_G, pos, font_size=8, font_color='k')

plt.show()
