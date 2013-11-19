#!/usr/bin/env python
# -*- coding: latin-1 -*-

#################
# get  captures #
#################
import os
import numpy
import Image

imageDir = 'data\\20101024 80x60 grayscale Steph Baptiste'
modelDir = 'model'
Npc = 15 # Number of PCs to compute

path='C:\\Documents and Settings\Stéphanie\Bureau\Baptiste\CV'
images = os.listdir(path+ '\\' + imageDir)
#Nimg=len(images)
#a = numpy.asarray(Image.open(imageDir + '\\2010-10-22 140412.781000.ppm', 'r'))
#Nv = numpy.size(a)

#X = numpy.zeros((Nimg, Nv))

X = numpy.array

for filename in images:
	if filename != 'Thumbs.db':
		image= Image.open(imageDir + '\\' + filename, 'r')
		a = numpy.asarray(image)
		height = numpy.size(a,0)
		width = numpy.size(a,1)
		##print numpy.size(a,2) # exists only if not grayscale, i.e 3 channels
		Nv = numpy.size(a)
		a = numpy.reshape(a,(1,Nv))
		if numpy.size(X) == 1:
			X = a
		else:
			X = numpy.append(X, a, 0)
		print "Loaded image " + filename
		#print X.shape
		#image.show()
print 'Loaded a total of ' + str(numpy.size(X, 0)) + ' images containing each ' + str(width) + 'x' + str(height) + ' pixels.'

Xm= numpy.mean(X,axis=0)
X=X-Xm

print 'Now proceeding to PCA... '
from pca_module import *
#T, P, explained_var = PCA_svd(X, standardize=False)
#T, P, explained_var = PCA_nipals2(X, standardize=False, E_matrices=True) #yields T.shape = Nsample*10 ... wierd
T, P, explained_var = PCA_nipals2(X, standardize=False, PCs=Npc, threshold=0.0001, E_matrices=False)

print 'Explained var:' + str(numpy.sum(explained_var)) + ' , Explained var per PC : '
print explained_var

print "Sizes : T " + str(T.shape) + " - P " + str(P.shape)  + " - explained_var " + str(explained_var.shape)


numpy.save(modelDir + '\Xm.npy', Xm)
numpy.save(modelDir + '\T.npy', T)
numpy.save(modelDir + '\P.npy', P)
numpy.save(modelDir + '\explained_var.npy', explained_var)