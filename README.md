# AdWords Placement Problem via Online Bipartite Graph Matching

## Objective

We are given a set of advertisers each of whom has a daily budget B<sub>i</sub> . When a user performs a query, an ad request is placed online and a group of advertisers can then bid for that advertisement slot. The bid of advertiser i for an ad request q is denoted as b<sub>iq</sub> . We assume that the bids are small with respect to the daily budgets of the advertisers (i.e., for each i and q, b<sub>iq</sub> ≪ B<sub>i</sub>) . Moreover, each advertisement slot can be allocated to at most one advertiser and the advertiser is charged his bid from his/her budget. The objective is to maximize the amount of money received from the advertisers.

We implement the Greedy, MSVV, and Balance algorithms. The code also calculates the revenue for the given keywords list (in that order) as well as calculate an estimation of a competitive ratio. The competitive ratio is defined as the minimum of ALG/OPT, where ALT is the mean revenue of your algorithm over all possible input sequences and OPT is the optimal matching. To estimate the value of ALG, simply compute the revenue over 100 random permutations of the input sequence and calculate the mean value.

## Dataset

The data set is the csv file [bidder_dataset.csv](./bidder_dataset.csv). This dataset contains information about the advertisers. There are four columns: advertiser ID, query that they bid on, bid value for that query, and their total budget (for all the keywords). The total budget is only listed once at the beginning of each advertiser’s list.

In addition, the file queries.txt contains the sequence of arrivals of the keywords that the
advertisers will bid on. These queries will arrive online and a fresh auctioning would be made for
each keyword in this list.

## algorithms

### Greedy

1. For each query q
  - If all neighbors (bidding advertisers for q) have spent their full budgets
    * continue
  - Else, match q to the neighbor with the highest bid.

### MSVV

Let x<sub>u</sub> be the fraction of advertiser's budget that has been spent up and ψ(x<sub>u</sub>) = 1 − e<sup>(x<sub>u</sub> −1)</sup> .
1. For each query q
 - If all neighbors have spent their full budgets
    * continue
 - Else, match q to the neighbor i that has the largest b<sub>iq</sub> ∗ ψ(x<sub>u</sub>) value.

### Balance

1. For each query q
  - If all neighbors have spent their full budgets
    * continue
  - Else, match q to the neighbor with the highest unspent budget.


## Run

To run the algorithms mentioned above simply use the following commands.

1. Greedy :  `python adwords.py greedy`
2. MSVV :    `python adwords.py msvv`
3. Balance : `python adwords.py balance`

## Output

Algorithm | Revenue | Competitive ratio
----|----|----
greedy | 16743.47 | 0.94
msvv | 17664.83 | 0.99
balance | 13070.27 | 0.73
