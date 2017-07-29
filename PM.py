#Present_Month_CSI
def presentMonth(place,collection,method='average'):
    dt = dtm.datetime(year=int(time.strftime("%Y")),month=int(time.strftime("%m")), day=1)
    unix_time_month_first = int(time.mktime(dt.timetuple()))
    unix_time_today = int(dtm.date.today().strftime("%s"))
    st=dtm.date.today()
    user_obj = session.get('user', None)
    name = user_obj['hotel']
    city = user_obj['City_Name']
    city_all = user_obj['City']
    data = []
    data1 = []
    data2 = []
    if user_obj['propType'] == 'Hotel':
        TopicCategories = topicHotel
    elif user_obj['propType'] == 'Restaurant':
        TopicCategories = topicRestaurant
    if city_all == "True" and place == "-- All --":
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
            # data2.append({"total_reviews":total_reviews,"positive_reviews": positive_reviews, "negative_reviews": negative_reviews,"neutral_reviews": neutral_reviews})
    satisfaction = data
    a = data1
    total_review=sum(data1)
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
    data2.append({"CSI": CSI, "total_review": total_review})
    return data2