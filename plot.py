#!/usr/bin/python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import sys, getopt

import mod_csv

def main():
    input_file = "RESULT.csv"
    output_file = "RESULT_mod.csv"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input_file=", "output_file="])
    except getopt.GetoptError:
        print ('Invalid option')
        print ('USAGE : plot.py -i <input file> -o <output file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print ('plot.py -i <input file> -o <output file>')
            sys.exit()
        elif opt in ("-o", "--output_file"):
            output_file = arg
        elif opt in ("-i", "--input_file"):
            input_file = arg

    mod_csv.main(input_file, output_file)

    flights_raw = pd.read_csv(output_file)
    flight_matrix = flights_raw.pivot_table(values="Time", index="B", columns="A", dropna=False)

    ind = range(1, 81)
    col = range(1, 81)

    df = pd.DataFrame(index=ind, columns=col)
    df.index.name = 'B'
    df.columns.name = 'A'

    df.update(flight_matrix)

    df.fillna(value=0, inplace=True)

    yticks = df.index
    keptticks = yticks[::int(len(yticks)/40)]
    yticks = ['' for y in yticks]
    yticks[::int(len(yticks)/40)] = keptticks

    xticks = df.columns
    keptticks = xticks[::int(len(xticks)/40)]
    xticks = ['' for x in xticks]
    xticks[::int(len(xticks)/40)] = keptticks

    # fig = plt.figure(figsize=(10,10))

    colors = ["#66ff66","#00ff00", "#00b300", "#008000", "#004d00", "#ff6666", "#ff0000", "#b30000", "#800000"]
    cmap = sns.blend_palette(colors, 100)
    # cmap = sns.color_palette(colors, 100)

    cmap1 = mpl.colors.ListedColormap(['w'])
    cmap2 = mpl.colors.ListedColormap(['#0000ff'])
    cmap3 = mpl.colors.ListedColormap(["Black"])

    ticks = list(range(0,3601,100))
    ticks.append(1)

    cbar_kws = {"ticks":ticks}
    r = sns.heatmap(df, linewidths=.5, cbar_kws=cbar_kws, cmap=cmap, yticklabels=yticks, xticklabels=xticks, vmin=1, vmax=3600, center=2500)
    sns.heatmap(df, mask=(df != 0), cbar=False, linewidths=.5, cmap=cmap1, yticklabels=yticks, xticklabels=xticks, robust=True)
    sns.heatmap(df, mask=(df != -1), linewidths=.5, cbar=False, cmap=cmap2, yticklabels=yticks, xticklabels=xticks, robust=True)
    sns.heatmap(df, mask=(df != -2), linewidths=.5, cbar=False, cmap=cmap3, yticklabels=yticks, xticklabels=xticks, robust=True)
    r.set_title("Max 10 DSP heatmap")

    plt.yticks(rotation=0)
    plt.xticks(rotation=0)
    plt.show()

if __name__ == "__main__":
    main()
