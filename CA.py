def summaryCA():
    collection = check_collection()
    user_obj = session.get('user', None)
    name = user_obj['hotel']
    place = user_obj['Place']
    group = user_obj['group']
    if group != []:
        group.insert(0, {"Name": name, "Place": place})
    else:
        if name != "Ammi's Biryani" and name != "RICE BAR" and name != "Sultan's Biryani":
            group.insert(0, {"Name": name, "Place": place})
        else:
            al = list(
                collection.aggregate([{"$group": {"_id": {"Name": "$Name", "Place": "$Place", "City": "$City"}}}]))
            for i in al:
                nname = i["_id"]["Name"]
                if nname == name:
                    nplace = i["_id"]["Place"]
                    group.insert(0, {"Name": nname, "Place": nplace})
    city_all = user_obj['City']
    city = user_obj['City_Name']
    func_ranking = ranking()
    newlist = func_ranking[0]['newlist']
    data = []
    rankset = []
    s = []
    if user_obj['propType'] == 'Hotel':
        TopicCategories = topicHotel

    rankset = sorted(s, reverse=True)
    count = 0
    for hotel in group:
        hname = hotel["Name"]
        hplace = hotel["Place"]
        for ele in newlist:
            if ele['Hotel'] == hname and ele['Place'] == hplace:
                for r in rankset:
                    rank = rankset.index(r) + 1
                if name != "Ammi's Biryani" and name != "RICE BAR" and name != "Sultan's Biryani":
                    data.append({"rank": rank, 'Hotel': ele['Hotel'], 'Place': ele['Place'], 'CSI': ele['CSI'], 'Logo':ele['Logo']})
                else:
                    if ele['Hotel'] == "Ammi's Biryani" or ele['Hotel'] == "RICE BAR" or ele['Hotel'] == "Sultan's Biryani":
                        data.append({"rank": rank, 'Hotel': ele['Hotel'], 'Place': ele['Place'], 'CSI': ele['CSI'], 'Logo': ele['Logo']})
                    else:
                        continue
    return data
