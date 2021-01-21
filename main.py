from simulation.environment.unity_environment import UnityEnvironment
# from watch_and_help.envs.python_environment import PythonEnvironment
import torch
import cv2
from torch.utils.data import DataLoader
from scriptData import ScriptData



''' Launch the simulator'''
scene_id=5
env=UnityEnvironment(env_id=scene_id,
                    observation_types=['normal', 'normal'], #one for each agent: partial, full, visible, image
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

''' Get the dataloader to give back all the script text'''
env.reset(environment_id=5)
scripts=ScriptData(scene_id)
dloader=DataLoader(scripts,batch_size=1, shuffle=True)
# print('dloader made')

import pdb; pdb.set_trace()