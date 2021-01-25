

def get_destinations(graph_list):
    #can go to Furniture, Appliances, Rooms,
    indices=[i for i,g in enumerate(graph_list) if g['category'] in ['Rooms']]
    features=[(g['class_name'],g['id']) for i,g in enumerate(graph_list) if i in indices]
    return features