#!/usr/bin/env python

"""
Author: George Weingart
Description: Wrapper program for maaslin
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
	parser.add_argument('--min_subj', action="store", type=int,default=20,dest='min_subj',nargs='?')
	parser.add_argument('--iterations', action="store", type=int,default=1000,dest='iterations',nargs='?')
	parser.add_argument('--errthresh', action="store", type=float, dest='errthresh',nargs='?', default='0.0001')

	parser.add_argument('--o_p_value', action="store", dest='o_p_value',nargs='?',  default='o_p_value')
	parser.add_argument('--o_q_value', action="store", dest='o_q_value',nargs='?',  default='o_q_value')
	parser.add_argument('--o_sim_score_results', action="store", dest='o_sim_score_results',nargs='?',  default='o_sim_score_results')
	parser.add_argument('--o_z_stat_results', action="store", dest='o_z_stat_results',nargs='?', default='o_z_stat_results')	
	CommonArea['parser'] = parser

	return  CommonArea








######################################################################################
#   Main  Program                                                                    #
######################################################################################
r = robjects.r

			
CommonArea = read_params( sys.argv )  # Parse command line in
parser = CommonArea['parser'] 
results = parser.parse_args()


ccrepe =   importr('ccrepe')
strx = results.x
robjects.globalenv["x"] = strx
x1 = r("read.table(x, head = TRUE)")

min_subj = results.min_subj
robjects.globalenv["min_subj"] = min_subj


iterations = results.iterations
robjects.globalenv["iterations"] = iterations

errthresh = results.errthresh
robjects.globalenv["errthresh"] = errthresh

if results.y is  None:
	ccrepe_results = ccrepe.ccrepe(x=x1,min_subj=min_subj,iterations=iterations, errthresh=errthresh)

if results.y is not None:
	stry = results.y
	robjects.globalenv["y"] = stry
	y1 = r("read.table(y, head = TRUE)")
	ccrepe_results = ccrepe.ccrepe(x=x1,y=y1,min_subj=min_subj,iterations=iterations, errthresh=errthresh)



p_value = ccrepe_results[0]
robjects.globalenv["p_value"] = p_value
robjects.globalenv["o_p_value"] = results.o_p_value
r('write.table(p_value, file = o_p_value , sep = "\t", col.names = colnames(p_value))')


q_value = ccrepe_results[1]
robjects.globalenv["q_value"] = q_value
robjects.globalenv["o_q_value"] = results.o_q_value
r('write.table(q_value, file = o_q_value, sep = "\t", col.names = colnames(q_value))')
 
sim_score_results = ccrepe_results[2]
robjects.globalenv["sim_score_results"] = sim_score_results
robjects.globalenv["o_sim_score_results"] = results.o_sim_score_results
r('write.table(sim_score_results, file = o_sim_score_results, sep = "\t", col.names = colnames(sim_score_results))')
x=8

z_stat_results = ccrepe_results[3]
robjects.globalenv["z_stat_results"] = z_stat_results
robjects.globalenv["o_z_stat_results"] = results.o_z_stat_results
r('write.table(z_stat_results, file = o_z_stat_results, sep = "\t", col.names = colnames(z_stat_results))')
x=8
exit(0)

