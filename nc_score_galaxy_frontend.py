#!/usr/bin/env python

"""
Author: George Weingart
Description: Wrapper program for nc_score
"""

#####################################################################################
#Copyright (C) <2012>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in the
#Software without restriction, including without limitation the rights to use, copy,
#modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#and to permit persons to whom the Software is furnished to do so, subject to
#the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies
#or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#####################################################################################

__author__ = "George Weingart"
__copyright__ = "Copyright 2014"
__credits__ = ["George Weingart"]
__license__ = "MIT"
__maintainer__ = "George Weingart"
__email__ = "george.weingart@gmail.com"
__status__ = "Development"

from cStringIO import StringIO
import sys,string
import os
import tempfile 
from pprint import pprint
import argparse


import rpy2.robjects as robjects
from rpy2.robjects.packages import *
import sys, os
from pprint import *




######################################################################################
#  Parse input parms                                                                 #
######################################################################################
def read_params(x):
	CommonArea = dict()	
	parser = argparse.ArgumentParser(description='ccrepe_Galaxy_Frontend_Argparser')
	parser.add_argument('--x', action="store", dest='x',nargs='?')

	CommonArea['y_Passed'] = 0
	try:
		parser.add_argument('--y', action="store", dest='y',nargs='?')
		CommonArea['y_Passed'] = 1
	except: 
		pass
		
	parser.add_argument('--bins', action="store", type=int,default=5,dest='bins',nargs='?')
	parser.add_argument('--min_abundance', action="store", type=float, dest='min_abundance',nargs='?', default='0.0001')
	parser.add_argument('--min_samples', action="store", type=float, dest='min_samples',nargs='?', default='0.1')

	parser.add_argument('--o_nc_score_results', action="store", dest='o_nc_score_results',nargs='?',  default='o_nc_score_results')

	CommonArea['parser'] = parser

	return  CommonArea








######################################################################################
#   Main  Program                                                                    #
######################################################################################
r = robjects.r

			
CommonArea = read_params( sys.argv )  # Parse command line in
parser = CommonArea['parser'] 
results = parser.parse_args()

infotheo =   importr('infotheo')
ccrepe =   importr('ccrepe')
strx = results.x
robjects.globalenv["x"] = strx
x1 = r("read.table(x, head = TRUE)")

bins = results.bins
robjects.globalenv["bins"] = bins

min_abundance = results.min_abundance
robjects.globalenv["min_abundance"] = min_abundance


min_samples = results.min_samples
robjects.globalenv["min_samples"] = min_samples



if results.y is  None:
	nc_score_results = ccrepe.nc_score(x=x1,bins=bins,min_abundance=min_abundance,min_samples=min_samples)

if results.y is not None:
	stry = results.y
	robjects.globalenv["y"] = stry
	y1 = r("read.table(y, head = TRUE)")
	nc_score_results = ccrepe.nc_score(x=x1,y=y1,bins=bins,min_abundance=min_abundance,min_samples=min_samples)

	

robjects.globalenv["nc_score_results"] = nc_score_results
robjects.globalenv["o_nc_score_results"] = results.o_nc_score_results
r('write.table(nc_score_results, file = o_nc_score_results , sep = "\t" )')





exit(0)

