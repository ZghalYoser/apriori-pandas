'''Van 20170627'''
'''
	helper script to process apriori from a panda dataset
	get support value and confidence
'''

#import area
from itertools import combinations
import collections
import pandas as pd
import numpy as np

#brute force get support
def get_support(df):
	pp = []
	print('Running apriori')
	for cnum in range(1, len(df.columns)+1):
		for cols in combinations(df, cnum):
			s = df[list(cols)].all(axis=1).sum()
			pp.append([",".join(cols), s])
	sdf = pd.DataFrame(pp, columns=["Pattern", "Support"])
	return sdf

#get apriori support
def apriori(trans, support=0.01, minlen=1, maxlen = -1):
	print("running apriori")
	#ts=pd.get_dummies(trans.unstack().dropna()).groupby(level=1).sum()
	ts=trans #test first

	rowlen, collen =ts.shape

	#skip combinations lower than support
	skipComb = []

	if(maxlen == -1):
		maxlen = collen

	maxlen+=1

	pattern = []
	for cnum in range(minlen, maxlen):
		for cols in combinations(ts, cnum):

			# skip the combination if already exists
			if(checkCombinations(cols,skipComb)):
				continue

			sup = ts[list(cols)].all(axis=1).sum()
			sup=float(sup)/rowlen

			#so that it doesn't throw an exception
			cols = [str(i) for i in cols]

			print("Combination:" + ",".join(cols) + "   Support:" + str(sup))

			#store combinations that are not reasonable
			if(sup < support):
				if(cols not in skipComb):
					skipComb.append(cols)
			else:
				cols = [str(i) for i in cols]
				pattern.append([','.join(cols), sup])

	sdf = pd.DataFrame(pattern, columns=["Pattern", "Support"])
	results=sdf[sdf.Support >= support]

	return results

#helper to check tuple subset
def checkCombinations(a,listCombs):
	current = set(list(a))
	for i in listCombs:
		if(set(list(i)).issubset(current)):
			return True
	return False


#helper to get confidence a=>b
def getConfidence(a,b, suppList):
	target=[]
	source=[]

	targetSupp = -1
	sourceSupp = -1
	if(type(a) is list):
		for i in a:
			target.append(i)
	else:
		target.append(a)

	source = target.copy()

	if(type(b) is list):
		for i in b:
			target.append(i)
	else:
		target.append(b)

	#get the support value
	targetSupp = getSupportValue(target,suppList)
	sourceSupp = getSupportValue(source,suppList)

	#avoid math error
	if(sourceSupp == 0):
		return 0
	return (targetSupp/sourceSupp)

#helper function to get support value
def getSupportValue(a,supp):
	for row in supp.itertuples():
		key = row[1].split(',')
		if(all(x in key for x in a)):
			return row[2]
	return 0