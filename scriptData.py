from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from glob import glob
import pandas as pd
from tqdm import tqdm
class ScriptData(Dataset):
    def __init__(self, scene_id,makeList=False):
        ''' initFile is broken in the unity sim'''
        self.makeList=makeList
        self.exeFiles=glob('dataset/programs_processed_precond_nograb_morepreconds/executable_programs/TrimmedTestScene'+str(scene_id)+'_graph/results_intentions_march-13-18/*.txt', recursive=True)
        # self.exeFiles=pd.read_csv('walkProgs_'+str(scene_id)+'.csv',index_col=0, header=0)['0'].tolist()
        # self.initFinGraph=glob('dataset/programs_processed_precond_nograb_morepreconds/init_and_final_graphs/TrimmedTestScene'+str(scene_id)+'_graph/results_intentions_march-13-18/*.json', recursive=True)
        self.files=[]
        self.scene_id=scene_id

    def __len__(self):
        return len(self.exeFiles)

    def __getitem__(self, item):
        # import pdb; pdb.set_trace()
        commands=[]
        with open(self.exeFiles[item],'r') as f:
            # import pdb; pdb.set_trace()
            for i,lines in enumerate(f):
                if i==1:
                    temp=lines
                # if i==4 and lines[:6].lower() not in ['[walk]','[stand','[wakeu']:
                #     import pdb; pdb.set_trace()

                if lines[0]=='[':
                    commands.append('<char0> '+lines.strip().split('(')[0])
        # import pdb; pdb.set_trace()
        if self.makeList and sum(['WALK' in c for c in commands])>0 and sum(['CAT' in c for c in commands])==0:
            self.files.append(self.exeFiles[item])
        # tag=self.exeFiles[item].split('executable_programs/')[-1].split('.')[0]
        # ind=[i for i, s in enumerate(self.initFinGraph) if tag in s]
        # initFile=self.initFinGraph[ind[0]]

        return commands#,self.exeFiles[item]#, initFile


# x=ScriptData(5,True)
# d=DataLoader(x)
# for a,b in tqdm(d):
#     print(b)
#     print(a)
#     import pdb; pdb.set_trace()
# temp=pd.DataFrame(x.files)
# temp.to_csv('walkProgs_'+str(x.scene_id)+'.csv')
# print(len(temp), 'used')
# print(len(d)-len(temp), 'not used')
# for i in range(100):
#     y,z=x.__getitem__(i)
#     print(z)
#     print(y)