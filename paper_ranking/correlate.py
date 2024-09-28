import numpy as np 
import polars as pl
import json 
import matplotlib.pyplot as plt 
from collections import defaultdict
from scipy.stats import pearsonr

# import matplotlib 

# import stat
with open('descriptive_stat.json') as f:
    stats = json.load(f)

# import score
score_dist = defaultdict(int)
with open('grade_2.json') as f:
    scores = json.load(f)

for score in scores.values():
    score_dist[score] += 1

plt.bar(list(score_dist.keys()), list(score_dist.values()), width=.5, align='center', edgecolor='black')
plt.title("score distribution")
plt.savefig('fig/score_distribution.png')
plt.close()

# graph with various stat
n_paras_dict = defaultdict(int)
avg_sen_len_dict = defaultdict(float)
min_sen_len_dict = defaultdict(int)
max_sen_len_dict = defaultdict(int)
avg_n_sen_dict = defaultdict(float)

for intro, stat in stats.items():
    n_paras_dict[intro] = stat['n_params']
    avg_sen_len_dict[intro] = stat['avg_sen_len']
    min_sen_len_dict[intro] = stat['min_sen_len']
    max_sen_len_dict[intro] = stat['max_sen_len']
    avg_n_sen_dict[intro] = stat['avg_n_sen']



def plot_with_score(score, param, save_path, y_label, name):
    x = []
    y = []
    for intro_name in score.keys():
        plt.scatter(score[intro_name], param[intro_name], c = 'b', marker='x')
        x.append(score[intro_name])
        y.append(param[intro_name])
    corr = pearsonr(x, y)

    plt.xlabel('score')
    plt.ylabel(y_label)
    
    plt.title(f"{name}, correlation {round(corr.statistic, 2)}, p-value {round(corr.pvalue, 2)},")
    plt.savefig(save_path)
    plt.close()

plot_with_score(scores, n_paras_dict, 'fig/score_n_paras.png', '# paragraphs', 'score vs num paragraphs')
plot_with_score(scores, avg_sen_len_dict, 'fig/score_avg_sen_len.png', 'avg sentence length (# words)', 'score vs average sentence length')
plot_with_score(scores, min_sen_len_dict, 'fig/min_sen_len.png', 'min sentence length (# words)', 'score vs min sentence length')
plot_with_score(scores, max_sen_len_dict, 'fig/max_sen_len.png', 'max sentence length (# words)', 'score vs min sentence length')
plot_with_score(scores, avg_n_sen_dict, 'fig/avg_n_sen.png', 'avg # sentences', 'score vs avg paragraph length')
