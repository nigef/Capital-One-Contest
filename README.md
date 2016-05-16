# Capital-One-Contest, Summer 2015

[https://www.mindsumo.com/contests/credit-card-transactions](link)


# OOP Python Solution with O(n) and O(n^2) Public Methods and Including Bonus Questions


## Private Methods (_split_line, _process_year, _set_type, _process_line, _process)

We go through the data provided in the .csv file only once, upon initialization of the Clients class in a private method call to `Clients._process` from the constructor. As each line is read in the data, we build two dictionaries with: client subscription data, and yearly revenue (used in the bonus questions). We chose the dictionary data structure for its faster lookup time (hash table implementation). At this point, the worst case runtime is O(n). The client subscription data is stored by the private method `Clients._process_line` with the Subscription ID as the key, along with a list of the values: subscription type, duration, and the last date encountered during the line-by-lined data read. The date is used compared in `Clients._set_type` to determine the subscription type (one-off, daily, monthly, or yearly). 



## Public Methods (get_subscriber_category, get_revenue_numbers, get_revenue_extrema, predict_revenue)

The public method (`Clients.get_subscriber_category`) returns a list of strings of client subscription data in the form 'ID,type,duration' for example '1234,monthly,85 months'. To achieve this formatting, we loop through the instance variable dictionary once, which in addition to building it initially, results in O(n^2) runtime. If we could simply output the dictionary described above, then we could achieve an O(n) runtime.

The annual revenue numbers can be output with the public call `Clients.get_revenue_numbers`, which runs in O(n) because of looping through the data initially.

The years that had the highest revenue growth and loss is accessed with `Clients.get_revenue_extrema`. This output runs in O(n^2) including the initial building of the yearly revenue dictionary. With some further refactoring (not shown) we could boost the efficiency of this method to O(n) by calculating the yearly growth/loss during the initial building of the dictionary. 

Finally, the revenue prediction, with `Clients.predict_revenue` is based on a simplistic linear projection, based on the linearity of the data. Some limitations of this linear projection method include: logarithmic or exponential data, sharp changes in data trends, cyclical changes, and basically anything else that doesn't follow a macro-linear trend. The prediction method requires at least 3 different years of revenue data. This method runs in O(n) because its dominated by looping over the data initially.


## Sample Input and Calls

```python
>>> c = Clients('subscription_report.csv')

>>> c.get_subscriber_category()

>>> c.get_revenue_numbers()

>>> c.get_revenue_extrema()

>>> c.predict_revenue()
```


## Dependencies

We chose to import the `datetime` module (rather than create our own parser) to abstract calculating time intervals from dates in the form 'month/day/year'. This was used in the private method, Clients._set_type


## Error Types

`FileNotProcessedError`: raised when the dictionary has not been built (the client subscription data) and a call has been made to Clients.get_subscriber_category

`InvalidDateTypeError`: raised when we cannot discern a subscription type as either daily/monthly/yearly/(one-off). Raised from Clients._set_type

