def competitveAnalysis(start, end, topics, collection):
    user_obj = session.get('user', None)
    name = user_obj['hotel']
    place = user_obj['Place']
    group = user_obj['group']
    if group != []:
        group.insert(0, {"Name": name, "Place": place})
    else:
        if name != "Ammi's Biryani" and name != "RICE BAR":
            group.insert(0, {"Name": name, "Place": place})
        else:
            al = list(collection.aggregate([{"$group": {"_id": {"Name": "$Name", "Place": "$Place", "City": "$City"}}}]))
            for i in al:
                nname = i["_id"]["Name"]
                if nname == name:
                    nplace = i["_id"]["Place"]
                    group.insert(0, {"Name": nname, "Place": nplace})
    city_all = user_obj['City']
    city = user_obj['City_Name']
    final_data = []
    func_ranking = overallrank(collection,start,end)
    newlist = func_ranking[0]['newlist']
    rankset_overall = []
    s = set()
    for i in newlist:
        s.add(i['CSI'])
    rankset_overall = sorted(s, reverse=True)
    for x in topics:
        all_data = []
        func_topic_ranking = topicrank(collection,x,start,end)
        topic_newlist = func_topic_ranking[0]['newlist']
        rankset_topic = []
        s1 = set()
        for i in topic_newlist:
            s1.add(i['CSI'])
        rankset_topic = sorted(s1, reverse=True)
        if x == 'All':
            for hotel in group:
                hname = hotel["Name"]
                hplace = hotel["Place"]
                total_reviews_present_month = getReviewCount(hname, hplace, None, start, end, None)
                positive_reviews_present_month = getReviewCount(hname, hplace, 1, start, end, None)
                negative_reviews_present_month = getReviewCount(hname, hplace, 2, start, end, None)
                neutral_reviews_present_month = getReviewCount(hname, hplace, 0, start, end, None)
                if total_reviews_present_month == 0:
                    CSI_present_month = 0
                else:
                    CSI_present_month = (2 * total_reviews_present_month - (neutral_reviews_present_month * 0.5) - negative_reviews_present_month) * 100.0
                    CSI_present_month /= 2 * total_reviews_present_month
                total_reviews_last_month = getReviewCount(hname, hplace, None, (2 * start - end), start, None)
                positive_reviews_last_month = getReviewCount(hname, hplace, 1, (2 * start - end), start, None)
                negative_reviews_last_month = getReviewCount(hname, hplace, 2, (2 * start - end), start, None)
                neutral_reviews_last_month = getReviewCount(hname, hplace, 0, (2 * start - end), start, None)
                if total_reviews_last_month == 0:
                    CSI_last_month = 0
                else:
                    CSI_last_month = (2 * total_reviews_last_month - (neutral_reviews_last_month * 0.5) - negative_reviews_last_month) * 100.0
                    CSI_last_month /= 2 * total_reviews_last_month
                if CSI_last_month != 0.0:
                    change = (CSI_present_month - CSI_last_month) * 100.0
                    change /= CSI_last_month
                else:
                    change = 100.0
                if change < 0:
                    change = -(change)
                    csiUpDown = "fa-caret-down"
                    csiClass = "text-red"
                elif change == 0 or change > 0:
                    csiUpDown = "fa-caret-up"
                    csiClass = "text-green"
                count = 0
                for ele in newlist:
                    # if ele['Hotel'] == hname and ele['Place'] == hplace:
                    #     rank = count + 1
                    #     break
                    # else:
                    #     count = count + 1
                    if ele['Hotel'] == hname and ele['Place'] == hplace:

                        #rank = newlist.index(ele) + 1
                        for r in rankset_overall:
                            if r == ele['CSI']:
                                rank = rankset_overall.index(r) + 1
                                break
                            else:
                                count = count + 1
                all_data.append({'Topic': x, 'Name':hname, 'Place':hplace, 'CSI': round(CSI_present_month, 2), 'CSIchange': round(change, 2), 'csiUpDown': csiUpDown, 'csiClass':csiClass,
                             'total_reviews': total_reviews_present_month, 'Positive': positive_reviews_present_month, 'Negative': negative_reviews_present_month,
                             'Neutral': neutral_reviews_present_month, 'Rank': rank})
            final_data.append({'category':x, 'details':all_data})
        else:
            for hotel in group:
                hname = hotel["Name"]
                hplace = hotel["Place"]
                total_reviews_present_month = collection.find({'Name': hname, 'Place': hplace,
                                                           'Date': {'$gte': start, '$lt': end},
                                                           x: {'$ne': 3}}).count()
                positive_reviews_present_month = collection.find({'Name': hname, 'Place': hplace,
                                                           'Date': {'$gte': start, '$lt': end},
                                                           x: 1}).count()
                negative_reviews_present_month = collection.find({'Name': hname, 'Place': hplace,
                                                           'Date': {'$gte': start, '$lt': end},
                                                           x: 2}).count()
                neutral_reviews_present_month = collection.find({'Name': hname, 'Place': hplace,
                                                           'Date': {'$gte': start, '$lt': end},
                                                           x: 0}).count()
                if total_reviews_present_month == 0:
                    CSI_present_month = 0
                else:
                    CSI_present_month = (2 * total_reviews_present_month - (neutral_reviews_present_month * 0.5) - negative_reviews_present_month) * 100.0
                    CSI_present_month /= 2 * total_reviews_present_month
                total_reviews_last_month = collection.find({'Name': hname, 'Place': hplace,
                                                        'Date': {'$gte': 2 * start - end, '$lt': start},
                                                        x: {'$ne': 3}}).count()
                positive_reviews_last_month = collection.find({'Name': hname, 'Place': hplace,
                                                        'Date': {'$gte': 2 * start - end, '$lt': start},
                                                        x: 1}).count()
                negative_reviews_last_month = collection.find({'Name': hname, 'Place': hplace,
                                                        'Date': {'$gte': 2 * start - end, '$lt': start},
                                                        x: 2}).count()
                neutral_reviews_last_month = collection.find({'Name': hname, 'Place': hplace,
                                                        'Date': {'$gte': 2 * start - end, '$lt': start},
                                                        x: 0}).count()
                if total_reviews_last_month == 0:
                    CSI_last_month = 0
                else:
                    CSI_last_month = (2 * total_reviews_last_month - (neutral_reviews_last_month * 0.5) - negative_reviews_last_month) * 100.0
                    CSI_last_month /= 2 * total_reviews_last_month
                if CSI_last_month != 0.0:
                    change = (CSI_present_month - CSI_last_month) * 100.0
                    change /= CSI_last_month
                else:
                    change = 100.0
                if change < 0:
                    change = -(change)
                    csiUpDown = "fa-caret-down"
                    csiClass = "text-red"
                elif change == 0 or change > 0:
                    csiUpDown = "fa-caret-up"
                    csiClass = "text-green"
                count = 0
                for ele in topic_newlist:
                    # if ele['Hotel'] == hname and ele['Place'] == hplace:
                    #     rank = count + 1
                    #     break
                    # else:
                    #     count = count + 1
                    if ele['Hotel'] == hname and ele['Place'] == hplace:
                        #rank = topic_newlist.index(ele) + 1
                        for r in rankset_topic:
                            if r == ele['CSI']:
                                rank = rankset_topic.index(r) + 1
                                break
                            else:
                                count = count + 1
                all_data.append({'Topic': x, 'Name': hname, 'Place': hplace, 'CSI': round(CSI_present_month, 2),
                                 'CSIchange': round(change, 2), 'csiUpDown': csiUpDown, 'csiClass': csiClass,
                                 'total_reviews': total_reviews_present_month,
                                 'Positive': positive_reviews_present_month, 'Negative': negative_reviews_present_month,
                                 'Neutral': neutral_reviews_present_month, 'Rank': rank})
            final_data.append({'category':x, 'details':all_data})
    return final_data