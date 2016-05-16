'''Won the contest: https://www.mindsumo.com/contests/credit-card-transactions

Use transaction data to categorize clients

Online businesses of all sorts are increasingly reliant on credit card
transactions and the data they create. Information on where clients are, their
likely purchasing behaviors, and other bits of data can be used by business to
improve their practices. Taking the raw data and turning it into useful
information is no easy task though, which is why many engineers find
themselves processing and manipulating it on a regular basis.

Deliverables:

1) Outputs a list of subscription IDs, their subscription type (daily,
monthly, yearly, one-off), and the duration of their subscription.

2) Give annual revenue numbers for all years between 1966 and 2014.
Which years had the highest revenue growth, and highest revenue loss?

3) Predict annual revenue for year 2015 (based on historical retention and new
subscribers)
'''

import datetime


class InvalidDateTypeError(Exception):
    '''InvalidDateTypeError raised when we cannot discern a subscription type
    (day, month, year, one-off).'''


class FileNotProcessedError(Exception):
    '''FileNotProcessedError raised when file not yet processed.'''


class Clients(object):
    '''Use transaction data to categorize clients.
    Source: https://www.mindsumo.com/contests/credit-card-transactions
    '''

    def __init__(self, file_name):
        '''(Clients) -> NoneType
        Store the data in a dictionary for its faster lookup
        (in spite of its greater memory use).
        (Python dictionaries are implemented using hash tables.)

        >>> c = Clients('subscription_report.csv')
        '''

        self._file = file_name
        self._client_dict = {}

        # For Bonus Question:
        self._year_dict = {}
        # oldest, ..., recent
        self._last_three_years = [0, 0, 0]

        # Run the processing of the file
        self._process()

    def _split_line(self, line):
        '''(Clients, str) -> (int, int, int, str)
        A line is in the form: 525082,40662,5340,05/21/1986
        We extract and return each meaningful item: Subscription ID, Amount,
        Month, Day, and Year.
        '''

        # Remove trailing whitespace '\n', and separate by commas.
        L = line.strip().split(',')
        _id = int(L[1])
        _amount = int(L[2])
        _date = L[3]
        _year = int(L[3][6:])

        return _id, _amount, _year, _date

    def _process_year(self, year, amount):
        '''(Clients, int, int) -> NoneType
        Keep a running total of yearly revenue as we go through the data in
        O(n). Also, store the last three years, for later use with predicting
        revenue.
        '''

        # Build the dictionary of {year: amount}
        if year in self._year_dict:
            self._year_dict[year] += amount
        else:
            self._year_dict[year] = amount

        # Save the last (highest) 3 years for use with predict_revenue()
        if year not in self._last_three_years:
            if year > self._last_three_years[2]:
                self._last_three_years[0] = self._last_three_years[1]
                self._last_three_years[1] = self._last_three_years[2]
                self._last_three_years[2] = year
            elif year > self._last_three_years[1]:
                self._last_three_years[0] = self._last_three_years[1]
                self._last_three_years[1] = year
            elif year > self._last_three_years[0]:
                self._last_three_years[0] = year

    def _set_type(self, type_, prev_date, current_date):
        '''(Clients, list of int, list of int) -> str
        Set the subscription type, if not set yet.
        Note that a client can have a daily/monthly/yearly subscription and
        take some time off, so there could be a delta (time) that is greater
        than their (subscription) type. So, if we see a delta greater than the
        type, we won`t change the type. However if we see a delta lower than
        the type, we will always update the type to the lower unit.

        REQ: the subcription type of a client does not change.
        Raises: InvalidDateTypeError if met any unexpected type intervals.
        '''

        ret = ''

        # Subtract: current (greater) - previous (lower)
        delta = (datetime.datetime.strptime(current_date, "%m/%d/%Y") -
                 datetime.datetime.strptime(prev_date, "%m/%d/%Y")).days

        # Yearly subscription: don`t overwrite daily/monthly
        if delta > 31 and type_ != 'daily' and type_ != 'monthly':
            ret = 'yearly'
        # Monthly subscription: don`t overwrite daily
        elif (27 < delta < 32) and type_ != 'daily':
            ret = 'monthly'
        # Daily subscription
        elif 0 < delta < 28:
            ret = 'daily'
        else:  # error, negative
            raise InvalidDateTypeError

        return ret

    def _process_line(self, line):
        '''(Clients, str) -> NoneType
        Given a line from the data file, we update our dictionary with
        the new client data.
        The Subscription ID is the key, and we store the type and duration as
        str and int. We also use its type as the duration unit.
        While not required, we have chosen to track client subscription amount
        since that seems like the right thing to do.
        '''

        _id, _amount, _year, _date = self._split_line(line)

        # Update yearly revenue.
        self._process_year(_year, _amount)

        # If client is in our dictionary (as a key)
        # In the form: {subscription_id: [type, duration, 'month/day/year']}
        if _id in self._client_dict:
            # Get a pointer to the values
            _line_item = self._client_dict.get(_id)  # shallow copy
            # Increment the duration.
            _line_item[1] += 1
            # Set the subscripton type
            _line_item[0] = self._set_type(_line_item[0], _line_item[2], _date)
            # set recently visited date
            _line_item[2] = _date
        # make new entry
        else:
            # Default for first entry.
            self._client_dict[_id] = ['one-off', 1, _date]

    def _process(self):
        '''(Clients) -> NoneType
        Process the raw data file first. Go through the list once to
        acculumate subscriber data. This is in O(n)
        '''

        # open in read mode.
        # open 'with' to automatically destruct the file after done with it.
        with open(self._file, 'r') as input_file:

            # Skip first header description line; move ahead with readline()
            # "Id,Subscription ID,Amount (USD),Transaction Date"
            # line = input_file.readline()
            first_line = input_file.readline()
            if first_line[0:2] != 'Id':
                self._process_line(first_line)  # incase header is missing

            # Loop over the file object. This is relatively memory efficient,
            # fast, and simple.
            for line in input_file:
                self._process_line(line)

    def get_subscriber_category(self):
        '''(Client) -> list of str

        Returns a list of subscription IDs, their subscription type
        (daily, monthly, yearly, one-off), and the duration of their
        subscription. Goes through the list a second time to format it, which
        becomes O(n^2)

        Returns E.g.) ['1234,monthly,85 months', '1235,one-off,1 time', ...]
        Raises: FileNotProcessedError if file not processed

        >>> c = Clients('subscription_report.csv')
        >>> c.get_subscriber_category()
        {3159: ['monthly', 85, '07/08/1986'], 3160: ...}
        '''

        if self._client_dict == {}:
            raise FileNotProcessedError

        ret = []

        for key_, val_ in self._client_dict.items():
            type_ = val_[0]
            unit = 'time'  # default to one-off
            # Generate a unit
            if type_ is 'daily':
                unit = 'days'
            elif type_ is 'monthly':
                unit = 'months'
            elif type_ is 'yearly':
                unit = 'years'

            ret += [str(key_) + ',' + type_ + ',' + str(val_[1]) + ' ' + unit]

        return ret

    def get_revenue_numbers(self):
        '''(Clients) -> dict of {int: int}
        Give annual revenue numbers for all years between 1966 and 2014.
        This runs in O(n) because its dominated by looping over the data once.

        >>> c = Clients('subscription_report.csv')
        >>> c.get_revenue_numbers()
        {1966: 36431250, 1967: 55206230, 1968: 68890920, ...}
        '''

        return self._year_dict

    def get_revenue_extrema(self):
        '''(Clients) -> str
        The years that had the highest revenue growth, highest revenue loss.
        E.g.) 'Highest growth: 1967, 2110291. Highest loss: 2014, 1020112'
        Note that we could do this method recursively, if preferred.
        This runs in O(n^2), since the initial _process() was O(n).
        With further refactoring (not shown) this could be reduced to O(n)
        overall.

        >>> c = Clients('subscription_report.csv')
        >>> c.get_revenue_extrema()
        "Highest growth: (18774980, 1967). Highest loss: (-33216490, 1991)."
        '''

        growth_ = (0, 'N/A')
        loss_ = (0, 'N/A')

        for prev_year in self._year_dict:
            year_end = prev_year + 1
            if year_end in self._year_dict:
                diff = self._year_dict[year_end] - self._year_dict[prev_year]

                # Positive, growth
                if diff >= 0 and diff > growth_[0]:
                    growth_ = diff, year_end
                # Negative, loss
                elif diff < 0 and abs(diff) > abs(loss_[0]):
                    loss_ = diff, year_end

        return 'Highest growth: {}. Highest loss: {}.'.format(growth_, loss_)

    def predict_revenue(self):
        '''(Clients) -> int
        Given the linearity of the revenue plot, use the last three years of
        revenue data to predict the forward year. We consider this a simpler
        way, that is still technically based on historical retention and new
        subscribers. This method has been tailored to this particular data set.
        This runs in O(n) because its dominated by looping over the data
        initially (in one of the previous methods, _process).
        REQ: at least 3 years of revenue data.

        >>> c = Clients('subscription_report.csv')
        >>> c.predict_revenue()
        24680
        '''

        # Get the revenue for the last (highest) 3 years.
        # Lookup in list and dict in constant time, O(1).
        last_yr = self._last_three_years[2]
        thir_last_yr = self._last_three_years[0]
        last = self._year_dict[last_yr]
        sec_last = self._year_dict[self._last_three_years[1]]
        thir_last = self._year_dict[thir_last_yr]

        # Linear approximation, where, y = ((y2 - y1)/1)*(x) + b
        return (last - sec_last)*(last_yr - thir_last_yr + 1) + thir_last
