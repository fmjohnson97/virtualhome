from simulation.unity_simulator.comm_unity import UnityCommunication
from simulation.environment.unity_environment import UnityEnvironment
from scriptData import ScriptData
from torch.utils.data import DataLoader
import json
# from matplotlib import pyplot as plt
import cv2


''' Make the scene '''
scene_id = 5 # Scenes go from 0 - 6; 1 or 5 seem like they're the most open plan
comm = UnityCommunication()
comm.reset(scene_id)
# env=UnityEnvironment()
print('env created')


''' Get the dataloader to give back all the script text'''
scripts=ScriptData(scene_id)
dloader=DataLoader(scripts,batch_size=1, shuffle=True)
print('dloader made')

count=0
''' Start the train loop'''
for actions,init, skip in dloader:
    if not skip:
        import pdb; pdb.set_trace()
        comm.reset(scene_id)
        with open(init[0], 'r') as f:
            graphs = json.load(f)
            first_graph = graphs['init_graph']
        print('graph loaded')
        # obs=env.reset(environment_graph=first_graph, environment_id=scene_id)
        s, message = comm.expand_scene(first_graph)
        if not s:
            print('cant expand scene')
            print(init)
            print(s,message)
            # continue
            import pdb; pdb.set_trace()

        ''' Add the 2 agents'''
        # the agent doing the actions
        comm.add_character('chars/Female1', initial_room='livingroom')
        # the agent following (never seen bc the camera is their 1st POV)
        comm.add_character('chars/Female4', initial_room='livingroom')
        if not s:
            print('cant load characters')
            import pdb; pdb.set_trace()

        s, cc = comm.camera_count()
        print('cameras counted')
        for script_instruction in actions:
            print(script_instruction)
            success, message = comm.render_script([script_instruction[0]], image_synthesis=[], processing_time_limit=80,
                                                  find_solution=False, recording=False)#, skip_animation=True
            print(success, message)
            # Here you can get an observation, for instance
            s, im = comm.camera_image([cc-6], image_width=300, image_height=300)
            # plt.imshow(im[0][:, :, ::-1])
            # plt.show()
            cv2.imshow('',im[0])
            cv2.waitKey(5)

            #ToDO: put agent RL stuff here!


        import pdb;pdb.set_trace()

