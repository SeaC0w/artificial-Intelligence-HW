There are 3 different files:

1)  Running decision.py will print out data on all the folds and averages of all folds and create lots of files.
    the decision-tree pdfs are visualizations of all the decision trees. The number in the file name indicates which
    fold it was created on. It will also output 3 html files that are the performance vs baseline graphs for recall,
    precision and F1.

2)  Running kmeans.py will output 14 html files. One is the graph for the elbow method of determining k, 3 are the
    clusterings for the entire dataset for each of the promising k-values output by the elbow method, and 11 are
    the result of running k-means clustering with k=4 for each of the 10 folds. The number in the file name
    indicates which k-value it was made with as well as fold it was created on.

3)  Running plots.py will output 2 htmls files. They plot all of the data just color coded in different ways: one
    by location and the other by osha class.
