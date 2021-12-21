import numpy as np
import matplotlib.pyplot as plt

def trca(X, t1, Nexp):
    '''

    :param X: data matrix (N channels * T time points)
    :param t1: task onsets (vector)
    :param Nexp: task duration (sampling unit)
    :return:
   
    '''

    nb_channel = X.shape[1]     #read the channels (rows) (64/9/7)
    nb_trial = t1.shape[0]      #read different blocks (6)

    S = np.zeros((nb_channel, nb_channel))      #64*64 

    # computation of correlation matrices:
    for i in range(nb_channel):
        for j in range(nb_channel):
            for k in range(nb_trial):
                for l in range(nb_trial):
                    if k != l:
                        tk =t1[k] # onset of k-th block
                        tl =t1[l] # onset of l-th block
                        xi = X[tk:tk+Nexp,i].reshape(1,Nexp)
                        xj = X[tl:tl+Nexp,j].reshape(1,Nexp)
                        #Matrix S: Cov(xk(i),xl(j))
                        S[i,j] += np.dot((xi-np.mean(xi, axis=1)),(xj-np.mean(xj,axis=1)).T)  
#   # Centralization of data matrix 
    X_aver = X - np.tile(np.mean(X, axis=0).reshape(nb_channel),(X.shape[0],1)) 
    # Matri Q: Cov(x(i),x(j))
    Q = np.dot(X_aver, X_aver.T)
    # D is eigenvalue, V is eigenvector
    D, V = np.linalg.eig(np.dot(np.linalg.inv(Q), S))
    W = V[0,:]  #weighted coefficient
    Y = np.dot(V.T, X_aver)     #task-related components for all channel
    C = Y[0,:]      #the component of different channel
    plt.figure()
    plt.plot(C)
    plt.title('reconstruacted signal',fontsize=9,color='blue')
    plt.show()

    return C, W



