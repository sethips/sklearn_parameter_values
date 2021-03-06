from __future__ import print_function
from sklearn.neighbors import KNeighborsClassifier as KNN
from time import time
import operator
#import numpy as np
#import matplotlib.pyplot as plt
#from class_vis import prettyPicture



# sample_size
# k
# weights
# algorithm
# n_jobs

#===============================================================================
#                                                                         MY_KNN
#===============================================================================
def my_knn(data_generator,
           sample_size=1000,
           k=8,
           weights="uniform",
           algorithm="auto",
           n_jobs=1):
    """
    Trains an adaboost classifier using a Decision Tree as its weak classifier.
    Trains on the data generated by the

    :param data_generator: (int)
        A function object that generates toy data to evaluate the classifier.
        The function must be able to accept the sample size as its one and only
        argument, and must return its data as a tuple or list of the following
        4 elements in this exact order:
            X_train, Y_train, X_test, Y_test
    :param sample_size: (int)
        Size of the data to generate.
    :param k:
    :param weights:
    :param algorithm:
    :param n_jobs:
    :return: (dict)
        Returns a dictionary with the following keys:

        model          = The trained model,
        in_sample_acc  = The accuracy calculated using the training set.
        out_sample_acc = The accuracy calculated using the validation set.
        train_time     = The time it took diring the training phase.
    """
    #===========================================================================
    X_train, Y_train, X_test, Y_test = data_generator(sample_size)

    model = model = KNN(n_neighbors=k,
                        weights=weights,
                        algorithm=algorithm,
                        n_jobs=n_jobs)

    # --------------------------------------------------------------------------
    #                                                   train boosted classifier
    # --------------------------------------------------------------------------
    t0 = time()
    model = model.fit(X_train, Y_train)
    train_time = time()- t0

    # --------------------------------------------------------------------------
    #                                                           Make predictions
    # --------------------------------------------------------------------------
    # t0 = time()
    # preds = model.predict(X_test)
    # pred_time = time()- t0

    # --------------------------------------------------------------------------
    #                                                                   Evaluate
    # --------------------------------------------------------------------------
    in_sample_accuracy = model.score(X_train, Y_train)
    out_of_sample_accuracy = model.score(X_test, Y_test)

    return {"model":model,
            "X_train":X_train,
            "Y_train":Y_train,
            "X_test":X_test,
            "Y_test":Y_test,
            "in_sample_acc":in_sample_accuracy,
            "out_sample_acc":out_of_sample_accuracy,
            "train_time":train_time}


# ==============================================================================
#                                                 LOOP_ADABOOST_WITH_SIMPLE_TREE
# ==============================================================================
def loop_knn(data_generator,
             sample_size=1000,
             k=8,
             weights="uniform",
             algorithm="auto",
             n_jobs=1):
    # ==========================================================================
    largs = {"sample_size": sample_size,    # Loopable arguments
            "k":k,
            "weights":weights,
            "algorithm":algorithm
            }

    looper_id = None
    #print("looking for looper")
    for key in largs.keys():            # Find out which argument will be looped
        if isinstance(largs[key], list):
            looper_id = key
            looper_values = largs[looper_id]
            #print("found looper!!!")
            break
    if looper_id is None:
        msg = "\n    One of the arguments MUST be a list of values"
        raise ValueError(msg)
    #print("Looper is ", looper_id)


    num_iterations = len(largs[looper_id])
    running_results = {"in_sample_acc":[None]*num_iterations,
                       "out_sample_acc": [None] * num_iterations,
                       "train_time": [None] * num_iterations,
                      }

    for i, val in enumerate(looper_values):#largs[looper_id]):
        largs[looper_id] = val

        temp_results = my_knn(data_generator,
                              sample_size=largs["sample_size"],
                              k=largs["k"],
                              weights=largs["weights"],
                              algorithm=largs["algorithm"],
                              n_jobs=n_jobs
                              )
        # Append the values for each metric being measured  for this iteration
        # of running resuts
        for key in running_results.keys():
            running_results[key][i] = temp_results[key]

    best_setting, best_setting_accuracy = max(
            zip(looper_values, running_results["out_sample_acc"]),
            key=operator.itemgetter(1))

    running_results["best_setting"] = best_setting
    running_results["best_setting_accuracy"] = best_setting_accuracy

    print("\n----------------------------------------",
          "\nBest Results",
          "\n----------------------------------------"
          "\n" + looper_id + ":", best_setting,
          "\nOut of sample accuracy:", best_setting_accuracy,
          "\n----------------------------------------")


    return running_results


