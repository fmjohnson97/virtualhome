from simulation.environment.unity_environment import UnityEnvironment
import torch
import cv2
import json
from torch.utils.data import DataLoader
from scriptData import ScriptData
from matplotlib import pyplot as plt
from demo.utils_demo import *
from rl_utils import *
import random
from simulation.environment import utils as utils_environment
from hierarchical_IL_RL.agents import Manager, Worker
from hierarchical_IL_RL.buffers import ExpertBuffer

''' Set global script variables'''
scene_ids=[0,1,3,4,5,6] #ToDo: Env 2 might be broken!!!
epoch_length=100
total_epochs=20

''' Launch the simulator'''
env=UnityEnvironment(env_id=random.choice(scene_ids),
                    observation_types=[None, 'normal'], #one for each agent: partial, full, visible, image
                     recording_options={'recording': False,
                                        'output_folder': None,
                                        'file_name_prefix': None,
                                        'cameras': 'PERSON_FROM_BACK',
                                        'modality': 'normal'}
                     )
''' Other useful env variables:
    self.prev_reward
    self.actions_available
    self.comm
    self.agent_info
'''

#actions are ['turnleft', 'walkforward', 'turnright', 'no_action']
manager=Manager(in_chan=3,out_actions=4)#will probably need to change out actions here
# worker=Worker(in_chan=3, out_actions=4)

#make expert buffer
exBuff=ExpertBuffer(500)

''' Go through each epoch'''
for e in range(total_epochs):
    print('Epoch:',e)
    env.reset(environment_id=random.choice(scene_ids))
    s,graph=env.comm.environment_graph()
    destinations=get_destinations(graph['nodes'])
    location, loc_id = random.choice(destinations)
    destinations.pop(destinations.index((location,loc_id)))
    for step in range(epoch_length):
        # import pdb; pdb.set_trace()
        obs=env.get_observations()
        #obs[1] is the input for the 1st person POV image from the following agent
        action=torch.argmax(manager(torch.FloatTensor(obs[1]).T.unsqueeze(0)),-1)
        # x2=worker(torch.FloatTensor(obs[1]).T.unsqueeze(0),goal.detach())

        curr_graph = env.get_graph()
        agentids = [2]
        edges = [ed for ed in curr_graph['edges'] if ed['from_id'] in agentids and ed['relation_type']=='INSIDE']

        # print(location)
        action_name='walktowards'
        action_str = utils_environment.can_perform_action(action_name, loc_id, 0, curr_graph, {},
                                                          teleport=False)
        # import pdb; pdb.set_trace()
        s, graph = env.comm.environment_graph()
        for exp in getActionTranslation(agentids[0],loc_id,graph):
            exBuff.add(exp)

        #actions need to look like
        # '<char1> [walktowards]  <milk> (258)'
        # print(action_str)

        ''' RL AGENT ACTIONS GO HERE THEN ADD TO DICTIONARY IN STEP BELOW'''

        obs,reward, done, info = env.step({1:action_str})#{1:'walktowards '+location})

        if edges[0]['to_id']==loc_id or not info['success']:
            if len(destinations)==0:
                break
            location, loc_id = random.choice(destinations)
            destinations.pop(destinations.index((location, loc_id)))

        # import pdb; pdb.set_trace()
plt.show()