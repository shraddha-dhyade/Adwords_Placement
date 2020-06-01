import sys
import csv
import pandas as pd
import numpy as np
import math
import random

def load_data():
	budget = {}
	bid_values = {}
	with open('queries.txt', 'r') as f:
		queries = list(map(lambda query: query.strip(), f))  

	bidder_df = pd.read_csv('bidder_dataset.csv')
	for i in range(0,bidder_df.shape[0]):
		if not (math.isnan(bidder_df.iloc[i]['Budget'])):
			budget[bidder_df.iloc[i]['Advertiser']] = bidder_df.iloc[i]['Budget']
		if not bidder_df.iloc[i]['Keyword'] in bid_values:
			bid_values[(bidder_df.iloc[i]['Keyword'])] = {}	
		if not bidder_df.iloc[i]['Advertiser'] in bid_values[bidder_df.iloc[i]['Keyword']]:
			bid_values[bidder_df.iloc[i]['Keyword']][bidder_df.iloc[i]['Advertiser']] = bidder_df.iloc[i]['Bid Value']
	return queries, budget, bid_values

def calc_budget(bids, budgets):
	keywords = bids.keys()
	for keyword in keywords:
		if(budgets[keyword]>=bids[keyword]):	
			return 0
	return -1

def bidder_greedy(bids, budgets):
	keywords = list(bids.keys())
	bid_winner = keywords[0]
	winner_bid_val = 0
	c = calc_budget(bids, budgets)
	if(c==-1):
		return -1
	for keyword in keywords: 
		if(budgets[keyword] >= bids[keyword]):
			if(winner_bid_val < bids[keyword]):
				winner_bid_val = bids[keyword]
				bid_winner = keyword
			elif(winner_bid_val == bids[keyword]):
				if(bid_winner>keyword):
					bid_winner = keyword
					winner_bid_val = bids[keyword]
	return bid_winner
	
def revenue_greedy(queries, budget, bid_values, reps):
	tot_revenue = 0
	for i in range(0,reps):
		revenue = 0
		budgets= dict(budget)
		random.shuffle(queries)
		for q in queries:
			bids = bid_values[q]
			bidder = bidder_greedy(bids, budgets)
			if(bidder!=-1):
				revenue+=bids[bidder]
				budgets[bidder]-=bids[bidder]
		tot_revenue=tot_revenue+revenue	
	return tot_revenue/reps

def msvv_bid(bid, rem_budget, budget):
	val = (budget-rem_budget)/budget
	return bid*(1 - np.exp(val-1))

def bidder_msvv(bids, rem_budgets, budgets):
	keywords = list(bids.keys())
	bid_winner = keywords[0]
	c = calc_budget(bids, budgets)
	if(c==-1):
		return -1
	for keyword in keywords: 
		if(budgets[keyword] >= bids[keyword]):
			bidder1 = msvv_bid(bids[bid_winner], rem_budgets[bid_winner], budgets[bid_winner])
			bidder2 = msvv_bid(bids[keyword], rem_budgets[keyword], budgets[keyword])
			if(bidder1 < bidder2):
				bid_winner = keyword
			elif(bidder1 == bidder2):
				if(bid_winner>keyword):
					bid_winner = keyword
	return bid_winner

def revenue_msvv(queries, budget, bid_values, reps):	
	tot_revenue = 0
	for i in range(reps):
		revenue = 0
		budgets= dict(budget)
		rem_budgets = dict(budget)
		random.shuffle(queries)
		for q in queries:
			bids = bid_values[q]
			bidder = bidder_msvv(bids, rem_budgets, budgets)
			if(bidder!=-1):
				revenue+=bids[bidder]
				rem_budgets[bidder]-=bids[bidder]
		tot_revenue=tot_revenue+revenue	
	return tot_revenue/reps

def bidder_balance(bids, budgets):
	keywords = list(bids.keys())
	bid_winner = keywords[0]
	c = calc_budget(bids, budgets)
	if(c==-1):
		return -1
	for keyword in keywords: 
		if(budgets[keyword] >= bids[keyword]):
			if(budgets[bid_winner] < bids[keyword]):
				bid_winner = keyword
			elif(budgets[bid_winner] == bids[keyword]):
				if(bid_winner>keyword):
					bid_winner = keyword
	return bid_winner

def revenue_balance(queries, budget, bid_values, reps):
	tot_revenue = 0
	for i in range(0,reps):
		revenue = 0
		budgets= dict(budget)
		random.shuffle(queries)
		for q in queries:
			bids = bid_values[q]
			bidder = bidder_balance(bids, budgets)
			if(bidder!=-1):
				revenue+=bids[bidder]
				budgets[bidder]-=bids[bidder]
		tot_revenue=tot_revenue+revenue	
	return tot_revenue/reps

def main(choice=0):
	queries, budgets, bid_values = load_data()
	reps = 100
	random.seed(0)
	revenue = 0
	if(choice == 1):
		revenue = revenue_greedy(queries, budgets, bid_values, reps)
	elif(choice == 2):
		revenue = revenue_msvv(queries, budgets, bid_values, reps)
	elif(choice == 3):
		revenue = revenue_balance(queries, budgets, bid_values, reps) 
	print(round(revenue,2))
	print(round(revenue/sum(budgets.values()),2))
	
if __name__ == '__main__':
	if(len(sys.argv)!=2):
		print('Usage: python adwords.py degree/msvv/balance')
	else:
		if(sys.argv[1] == 'greedy'):
			main(1)
		elif(sys.argv[1] == 'msvv'):
			main(2)
		elif(sys.argv[1] == 'balance'):
			main(3)
		else:
			print('Invalid choice of argument!')
