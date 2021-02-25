import numpy as np

def get_destinations(graph_list):
    #can go to Furniture, Appliances, Rooms,
    indices=[i for i,g in enumerate(graph_list) if g['category'] in ['Rooms']]
    features=[(g['class_name'],g['id']) for i,g in enumerate(graph_list) if i in indices]
    return features

def getActionTranslation(agent, destination,graph):
    # ToDo: this function translates what "walk towards" means in terms of the human agent's motion (not the follower)
    # gets approx diff in position between agent and destination and determines if its a walk towards, left, or right action
    # for position: Y is upright

    # import pdb; pdb.set_trace()
    print([x for x in graph['nodes'] if x['id']==agent])
    print([x for x in graph['nodes'] if x['id'] == destination])
    agentPos=[x['obj_transform']['position'] for x in graph['nodes'] if x['id']==agent]
    destPos = [x['obj_transform']['position'] for x in graph['nodes'] if x['id'] == destination]
    # print(agentPos)
    # print(destPos)
    actions=[]
    posDiff=np.array(agentPos) - np.array(destPos)
    posDiff=posDiff[0]
    print(np.arctan2(posDiff[-1],posDiff[0])*180/np.pi, agentPos, destPos)
    # import pdb; pdb.set_trace()
    return actions