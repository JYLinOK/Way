# import jtc
import jtc.jtc as jtc
import re
import numpy


# ________________________________________________________________________________________________________
def segs_list(txt:str):
    """
    Get the way segments list of a specific file 
    """
    find_list = []
    pattern = re.compile(r'{{\s*(way\S*)\s*:\s*(\S+)\s*}}')
    finish = False
    ind = 0
    while not finish:
        mat = pattern.search(txt)
        if mat != None:
            if ind == 0:
                find_list.append([mat.span(), mat.groups()])
            else:
                # print(f'{find_list = }')
                last_span = (mat.span()[0]+find_list[ind-1][0][1], mat.span()[1]+find_list[ind-1][0][1])
                find_list.append([last_span, mat.groups()])

            txt = txt[mat.span()[1]:]
            ind += 1
        else:
            finish = True
    return find_list



# ________________________________________________________________________________________________________
def get_rest_segs_list(segs_list:list):
    """
    Get the rest segment coordinates tuple list from a segments coordinates tuple list orderly
    """
    rest_segs_list = []
    len_segs_list = len(segs_list)
    for i in range(len_segs_list):
        if i == 0 and segs_list[0][0] != 0:
            rest_segs_list.append((0, segs_list[0][0]-1))
        elif i == len_segs_list-1 and segs_list[-1][1] != len_segs_list:
            rest_segs_list.append((segs_list[-2][1]+1, segs_list[-1][0]-1))
            rest_segs_list.append((segs_list[-1][1]+1, len(txt)))
        else:
            rest_segs_list.append((segs_list[i-1][1]+1, segs_list[i][0]-1))

    return rest_segs_list



# ________________________________________________________________________________________________________
def insert_segs_in_file(segs_dict:dict, file_path:str):
    """
    Insert segments list items in a file that has way-tag 
    """
    
    txt = jtc.read_file(file_path)
    f_segs_list = segs_list(txt)

    print(f'{segs_dict = }')
    print(f'{f_segs_list = }')
    print(f'{len(txt) = }')
    
    new_str = ''
    segs_list = []
    for it in f_segs_list:
        segs_list.append(it[0])

    print(f'{segs_list = }')

  










file_path = './index3.html'
segs_dict = {
    'a': 'this is segment a',
    'abc123': 'this is segment abc123',
}



find_list = insert_segs_in_file(segs_dict, file_path)


