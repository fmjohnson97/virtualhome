from simulation.unity_simulator.comm_unity import UnityCommunication
from demo.utils_demo import *
from matplotlib import pyplot as plt

scene_id = 5 # Scenes go from 0 - 6; 1 or 5 seem like they're the most open plan
comm = UnityCommunication()
comm.reset(scene_id)
s, graph = comm.environment_graph()

#add characters to the scene
comm.add_character('chars/Female4', initial_room='kitchen')
s, g = comm.environment_graph()

s, nc = comm.camera_count()
print("There are",nc,"cameras in this scene")
s, im = comm.camera_image([nc-5]) #overhead seems to be at the end and the rest are 1stPOV; humans get their own?
# last 6 cameras belong to the human just added
# -6 is top view; -5 is 1st POV; -4 is right 90; -3 is left 90; -2 is backwards from head; -1 is facing the human front on
plt.imshow(im[0][:,:,::-1])
plt.show()

sofa = find_nodes(graph, class_name='sofa')[-2]
program = [' <char0> [Walk] <sofa> ({})'.format(sofa['id']), '<char0> [Sit] <sofa> ({})'.format(sofa['id'])]
success, message = comm.render_script(script=program,
                                      processing_time_limit=60,
                                      find_solution=False,
                                      image_width=320,
                                      image_height=240,
                                      skip_animation=False,
                                      recording=True,
                                      file_name_prefix='test2',
                                      camera_mode=['FIRST_PERSON'])

print(success,message)