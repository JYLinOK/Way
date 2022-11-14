"""
author: Jinwei Lin
time: 2022/11/06
note: remote: import jtc, local: import jtc.jtc as jtc
"""

# import jtc
import jtc.jtc as jtc
import re


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
def get_rest_segs_list(segs_list:list, len_txt:int):
    """
    Get the rest segment coordinates tuple list from a segments coordinates tuple list orderly
    """
    rest_segs_list = []
    len_segs_list = len(segs_list)
    for i in range(len_segs_list):
        if i == 0 and segs_list[0][0] != 0:
            rest_segs_list.append((0, segs_list[0][0]))
        elif i == len_segs_list-1 and segs_list[-1][1] != len_txt:
            rest_segs_list.append((segs_list[-2][1], segs_list[-1][0]))
            rest_segs_list.append((segs_list[-1][1], len_txt))
        else:
            rest_segs_list.append((segs_list[i-1][1], segs_list[i][0]))

    return rest_segs_list



# ________________________________________________________________________________________________________
def insert_segs_in_file(segs_dict:dict, origin_f_path:str, new_f_path:str):
    """
    Insert segments list items in a file that has way-tag, rewrite the original file to make a new file
    """
    
    txt = jtc.read_file(origin_f_path)
    f_segs_list = segs_list(txt)
    segs_l = []
    for it in f_segs_list:
        segs_l.append(it[0])

    rest_segs_l = get_rest_segs_list(segs_l, len(txt))

    segs_l_class = []
    for it in segs_l:
        segs_l_class.append(['insert', it])

    rest_segs_l_class = []
    for it in rest_segs_l:
        rest_segs_l_class.append(['origin', it])

    all_segs_list = rest_segs_l_class + segs_l_class

    new_str = ''
    min_start = 0
    for i in range(len(all_segs_list)):
        for seg in all_segs_list:
            if seg[1][0] == min_start:
                if seg[0] == 'origin':
                    new_str += txt[seg[1][0]:seg[1][1]]
                elif seg[0] == 'insert':
                    for it in f_segs_list:
                        if it[0] == seg[1]:
                            insert_str = segs_dict[it[1][1]]
                    new_str += insert_str
                # print(f'\n{new_str = }')
                min_start = seg[1][1]
        
    jtc.write_file(new_f_path, new_str)



# ________________________________________________________________________________________________________
def batch_files_strs(segs_dict:dict, template_f_path:str, save_dir:str):
    """
    Generate batch files with special segs_dict one by one, inster str contents

    Example:

    save_dir = './gen_dir/'

    segs_dict = {
        'f1.extension':{
            'way_id_1': 'str_content_1',
            'way_id_2': 'str_content_2',
            ...
        },
        'f2.extension':{
            'way_id_1': 'str_content_3',
            'way_id_2': 'str_content_4',
            ...
        },
        ...
    }
    """
    jtc.if_path_not_exist_create(save_dir)

    for it in segs_dict:
        insert_segs_in_file(segs_dict[it], template_f_path, save_dir + '/' + it)



# ________________________________________________________________________________________________________
def batch_files(segs_dict:dict, template_f_path:str, save_dir:str):
    """
    Generate batch files with special segs_dict one by one, if file_path is file path, insert the content of the file, else insert str

    Example:

    save_dir = './gen_dir/'
    
    segs_dict = {
        'f1.extension':{
            'way_id_1': 'file_path_1 or str_content_1',
            'way_id_2': 'file_path_2 or str_content_2',
            ...
        },
        'f2.extension':{
            'way_id_1': 'file_path_3 or str_content_3',
            'way_id_2': 'file_path_4 or str_content_4',
            ...
        },
        ...
    }

    f1.extension, f2.extension ... are the names of the batch files that will be generated
    file_path_1 or str_content_1 ... are the name of the inserted files or strs that will be inserted
    """

    for it_exten in segs_dict:
        for tag_id in segs_dict[it_exten]:
            afile = segs_dict[it_exten][tag_id]
            if jtc.if_path_or_file_exist(afile):
                print(f'exist file: {afile = }')
                segs_dict[it_exten][tag_id] = jtc.read_file(afile)
            else:
                print('No exist file =============>> Str', )
                segs_dict[it_exten][tag_id] = afile

    # print(f'{segs_dict = }')
    batch_files_strs(segs_dict, template_f_path, save_dir)



