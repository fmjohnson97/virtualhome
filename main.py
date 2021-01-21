from simulation.environment.unity_environment import UnityEnvironment
# from watch_and_help.envs.python_environment import PythonEnvironment
import torch
import cv2
from torch.utils.data import DataLoader
from scriptData import ScriptData



''' Launch the simulator'''
env=UnityEnvironment(observation_types=None,
                     recording_options={'recording': False,
                                        'output_folder': None,
                                        'file_name_prefix': None,
                                        'cameras': 'PERSON_FROM_BACK',
                                        'modality': 'normal'}
                     )

''' Get the dataloader to give back all the script text'''
scene_id=env.env_id
scripts=ScriptData(scene_id)
dloader=DataLoader(scripts,batch_size=1, shuffle=True)
print('dloader made')

import pdb; pdb.set_trace()