#!/usr/bin/env python
# -*- coding: latin-1 -*-

#################
# get  captures #
#################
import numpy
import Image

##############
# Parameters #
##############
Npc=15 # Set the number of Principal Components the EigenImages should be computed with
modelDir = 'model'

objectWidth  = 80
objectHeight = 60
Nobjects = 20

outputfilename = 'output'
ext = ".bmp" # extention of output file
##############

T = numpy.load(modelDir + '\\' + 'T.npy')
P = numpy.load(modelDir + '\\' + 'P.npy')
Xm = numpy.load(modelDir + '\\' + 'Xm.npy')

# Get EigenImage on the Npc first PCs
print "Sizes : T " + str(T.shape) + " - P " + str(P.shape)
principalComp=P[:Npc,...]


object = T[0,:Npc]
finalMatrix = numpy.dot(object,principalComp)
finalMatrix = finalMatrix + Xm
finalMatrix.shape = (objectHeight,objectWidth)

print numpy.shape(finalMatrix)
for i in range(1,Nobjects):
	object=T[i,:Npc]
	result = numpy.dot(object,principalComp)
	result = result + Xm
	result.shape = (objectHeight,objectWidth)
	finalMatrix = numpy.concatenate((finalMatrix, result), axis=1)

	print numpy.shape(finalMatrix)
	
max = numpy.max(finalMatrix)
min = numpy.min(finalMatrix)
print (max,min)
finalMatrix = numpy.floor((finalMatrix-min)*255/(max-min))
finalMatrix = finalMatrix.astype('uint8')

print object
print principalComp

resultIm = Image.fromarray(finalMatrix)
# resultIm.show()

resultIm.save(outputfilename + ext)

