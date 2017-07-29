def lastMonth(place,collection,start,end,method='average'):
    dt = dtm.datetime(year=int(time.strftime("%Y")), month=int(time.strftime("%m")), day=1)
    enddate= int(time.mktime(dt.timetuple()))
    dt = dtm.datetime(year=int(time.strftime("%Y")), month=int(time.strftime("%m")), day=1) - dtm.timedelta(31)
    startdate = int(time.mktime(dt.timetuple()))
    data = []
    total_reviews=collection.find()
    if total_reviews=0:
        CSI=0
    else:
        CSI=total_reviews*2 - neutral_reviews*0.5 - negative reviews
        CSI/=total_reviews*2
        CSI*=100
    user_obj = session.get('user', None)
    name = user_obj['hotel']
    city = user_obj['City_Name']
    if place == "-- All --":
        #positive_reviews = collection.find({'Name':name,'City':city,'Sentiment':2,'Date':{'$gte': unix_time_last_month_first,'$lt':unix_time_month_first}}).count()
        total_reviews = collection.find(
                    {'Name': name, 'City': city, 'Sentiment': {'$ne': 3}, 'Date': {'$gte': unix_time_last_month_first, '$lt': unix_time_month_first}}).count()
        postive_reviews = collection.find({'Name': name, 'City': city, 'Sentiment':1,'Date': {'$gte': unix_time_last_month_first, '$lt': unix_time_month_first}}).count()
        negative_reviews = collection.find({'Name': name, 'City': city, 'Sentiment':2,'Date': {'$gte': unix_time_last_month_first, '$lt': unix_time_month_first}}).count()
        neutral_reviews = collection.find({'Name': name, 'City': city, 'Sentiment':0,'Date': {'$gte': unix_time_last_month_first, '$lt': unix_time_month_first}}).count()
    else:
        total_reviews = collection.find(
            {'Name': name, 'Place': place,'City': city, 'Sentiment': {'$ne': 3},
             'Date': {'$gte': unix_time_last_month_first, '$lt': unix_time_month_first}}).count()
        postive_reviews = collection.find({'Name': name,'Place': place, 'City': city, 'Sentiment': 1,
                                           'Date': {'$gte': unix_time_last_month_first, '$lt': unix_time_month_first}}).count()
        negative_reviews = collection.find({'Name': name, 'Place': place,'City': city, 'Sentiment': 2,
                                            'Date': {'$gte': unix_time_last_month_first, '$lt': unix_time_month_first}}).count()
        neutral_reviews = collection.find({'Name': name, 'Place': place, 'City': city, 'Sentiment': 0,
                                           'Date': {'$gte': unix_time_last_month_first, '$lt': unix_time_month_first}}).count()
    if total_reviews == 0:
        CSI = 0
    else:
        CSI = total_reviews * 2 - (neutral_reviews * 0.5) - negative_reviews
        CSI /= total_reviews * 2
        CSI *= 100.0
        data.append({"CSI": round(CSI, 2), "total_reviews": total_reviews, "positive_reviews": postive_reviews,
                 "negative_reviews": negative_reviews})
    return data
