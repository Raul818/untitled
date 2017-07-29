import date
def summaryChart(place, collection, year,method='average'):
    user_obj = session.get('user', None)
    name = user_obj['hotel']
    city = user_obj['City_Name']
    city_all = user_obj['City']
    data = []
    columns = ['year', 'month', 'sentiment']
    df = pd.DataFrame(columns=columns)
    m_all = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    if place == "-- All --" and city_all == "True":
        total_reviews = collection.find({'Name': name, 'City': city, 'Date': {'$gte': startdate, '$lt': enddate}})
    else:
        total_reviews = collection.find({'Name': name, 'Place': place, 'Date': {'$gte': startdate, '$lt': enddate}})
    for x in total_reviews:
        df.loc[len(df)] = [dtm.datetime.fromtimestamp(int(x['Date'])).strftime('%Y'),
                           dtm.datetime.fromtimestamp(int(x['Date'])).strftime('%m'),
                           str(x['Sentiment'])]
    df_sentiment = pd.get_dummies(df['sentiment'])
    df_new = pd.concat([df, df_sentiment], axis=1)
    df = df_new.groupby(['year', 'month']).sum().reset_index()
    end = int(dtm.datetime(year=int(year), month=, day=31).strftime("%s"))
    start = int(dtm.datetime(year=int(year), month=, day=1).strftime("%s"))
    months = [datetime.date(2000, m, 1).strftime('%B') for m in range(1, 13)]
    for month in months:
        enddate = int(dtm.datetime(year=int(year), month=12, day=31).strftime("%s"))
        startdate = int(dtm.datetime(year=int(year), month=1, day=1).strftime("%s"))
    if "2" not in list(df):
        df['2'] = 0.0
    if "1" not in list(df):
        df['1'] = 0.0
    if "0" not in list(df):
        df['0'] = 0.0
    if "3" not in list(df):
        df['3'] = 0.0
    data1 = []
    data_csi = []
    data_review = []
    month_list = []
    for index, row in df.iterrows():
        total = row['1'] + row['0'] + row['2']
        if total == 0:
            CSI = 0
        else:
            satisfaction = data#Call a function from here which should return a list of CSI's
            a = data1#Call a function which should return a list of respective reviews of above CSI's
            total_review = sum(data1)
            n = len(a)
            ivec = sorted(range(len(a)), key=a.__getitem__)
            svec = [a[rank] for rank in ivec]
            sumranks = 0
            dupcount = 0
            newarray = [0] * n
            for i in range(n):
                sumranks += i
                dupcount += 1
                if i == n - 1 or svec[i] != svec[i + 1]:
                    for j in range(i - dupcount + 1, i + 1):
                        if method == 'average':
                            averank = sumranks / float(dupcount) + 1
                            newarray[ivec[j]] = averank
                        elif method == 'max':
                            newarray[ivec[j]] = i + 1
                        elif method == 'min':
                            newarray[ivec[j]] = i + 1 - dupcount + 1
                        else:
                            raise NameError('Unsupported method')

                    sumranks = 0
                    dupcount = 0
            Avg = (sum(newarray) / 10)  # 10 is the number of departments
            weight = []
            for x in newarray:
                weight[:] = [x / Avg for x in newarray]
            preCSI = [weight[i] * satisfaction[i] for i in range(len(weight))]
            CSI = (sum(preCSI)) / 10
        reviewsNum = row['1'] + row['0'] + row['2'] + row['3']
        month = dtm.datetime.strptime(row['month'], '%m').strftime("%b")
        month_list.append(month)
        data_csi.append([month, round(CSI, 2)])
        data_review.append([month, int(reviewsNum)])
    for m in m_all:
        if m not in month_list:
            data_csi.append([m, 0])
            data_review.append([m, 0])
    data_csi_final = sorted(data_csi, key=lambda x: m_all.index(x[0]))
    data_review_final = sorted(data_review, key=lambda x: m_all.index(x[0]))
    data.append({"data_csi": data_csi_final, "data_review": data_review_final})
    return data

def csi_and_reviews(place, collection,method='average'):
    user_obj = session.get('user', None)
    name = user_obj['hotel']
    city = user_obj['City_Name']
    city_all = user_obj['City']
    sevendays = dtm.date.today() - dtm.timedelta(7)
    unix_time_month_first = int(sevendays.strftime("%s"))
    unix_time_today = int(dtm.date.today().strftime("%s"))
    if user_obj['propType'] == 'Hotel':
        TopicCategories = topicHotel
    elif user_obj['propType'] == 'Restaurant':
        TopicCategories = topicRestaurant
    if place == "-- All --":
        for x in TopicCategories:
            total_reviews = collection.find({'Name': name, 'City': city,
                                             'Date': {'$gte': unix_time_month_first,
                                                      '$lt': unix_time_today},
                                             x: {'$ne': 3}}).count()
            positive_reviews = collection.find({'Name': name, 'City': city,
                                                'Date': {'$gte': unix_time_month_first,
                                                         '$lt': unix_time_today},
                                                x: 1}).count()
            negative_reviews = collection.find({'Name': name, 'City': city,
                                                'Date': {'$gte': unix_time_month_first,
                                                         '$lt': unix_time_today},
                                                x: 2}).count()
            neutral_reviews = collection.find({'Name': name, 'City': city,
                                               'Date': {'$gte': unix_time_month_first,
                                                        '$lt': unix_time_today},
                                               x: 0}).count()

            if total_reviews == 0:
                CSI = 0
            else:
                CSI = total_reviews * 2 - (neutral_reviews * 0.5) - negative_reviews
                CSI /= total_reviews * 2
                CSI *= 100.0
            data.append(CSI)
            data1.append(total_reviews)
    else:
        for x in TopicCategories:
            total_reviews = collection.find({'Name': name, 'City': city,
                                             'Date': {'$gte': unix_time_month_first,
                                                      '$lt': unix_time_today},
                                             x: {'$ne': 3}}).count()
            positive_reviews = collection.find({'Name': name, 'City': city,
                                                'Date': {'$gte': unix_time_month_first,
                                                         '$lt': unix_time_today},
                                                x: 1}).count()
            negative_reviews = collection.find({'Name': name, 'City': city,
                                                'Date': {'$gte': unix_time_month_first,
                                                         '$lt': unix_time_today},
                                                x: 2}).count()
            neutral_reviews = collection.find({'Name': name, 'City': city,
                                               'Date': {'$gte': unix_time_month_first,
                                                        '$lt': unix_time_today},
                                               x: 0}).count()

            if total_reviews == 0:
                CSI = 0
            else:
                CSI = total_reviews * 2 - (neutral_reviews * 0.5) - negative_reviews
                CSI /= total_reviews * 2
                CSI *= 100.0
            data.append(CSI)
            data1.append(total_reviews)