'''
Created on Feb 28, 2015

@author: Ruby
'''
from collections import Counter

from categorization import nbhw_template as nb


def NB_from_data(target, data):
#     print('Target : ' + target)
    size = data.__len__() * 1.0
    target_map = {}
    for d in data:
        for key in d:
            if key == target:
                if d[key] in target_map.keys():
                    values = target_map[d[key]]
                    values.append(d)
                    target_map[d[key]] = values
                else:
                    values = []
                    values.append(d)
                    target_map[d[key]] = values

    nbFinalMap = {}
    nbTargetMap = {}
    for key, values in target_map.items():
#         print('Target choice : ' + key)
#         print('Target count : ' + str(values.__len__()))
        
        nbFinalMap[key] = (values.__len__() / size) + 0.0
        
        l = []
        for value in target_map[key]:
            vmap = {}
            vmap = value
            for vk in vmap.keys():
                m = {}
                m[vk] = vmap[vk]
                l.append(m)

        finalMap = {}
        for d in l:
            ((x, y),) = d.items()
            finalMap.setdefault(x, []).append(y)
        nbAttList = []
        for f, g in finalMap.items():  # {attribute:[outcomes]}
            if f != target:
                c = Counter(g)
                for k, value in c.items():
                    c[k] = value / (values.__len__() + 0.0)
                nbAtt = nb.Distribution(f, c)
                nbAttList.append(nbAtt)
                nbTargetMap[key] = nbAttList   
     
    targetObj = nb.Distribution(target, nbFinalMap)
    nbObj = nb.NB(targetObj, nbTargetMap)
#     print(str(nbObj))
    return nbObj