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
            rest_segs_list.append((segs_list[i-1][1]+1, segs_list[i][0]+1))

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

    a = 0
    print(f'\n{txt[f_segs_list[a][0][0]:f_segs_list[a][0][1]] = }')
    
    segs_l = []
    for it in f_segs_list:
        segs_l.append(it[0])

    rest_segs_l = get_rest_segs_list(segs_l, len(txt))
    print(f'{rest_segs_l = }')

    a = 2
    print(f'\n{txt[rest_segs_l[a][0]:rest_segs_l[a][1]] = }')

    segs_l_class = []
    for it in segs_l:
        segs_l_class.append(['insert', it])
    print(f'\n{segs_l_class = }')

    rest_segs_l_class = []
    for it in rest_segs_l:
        rest_segs_l_class.append(['origin', it])
    print(f'{rest_segs_l_class = }')

    all_segs_list = rest_segs_l_class + segs_l_class
    print(f'{all_segs_list = }')

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

                print(f'\n{new_str = }')

                min_start = seg[1][1]
        
    




            
    jtc.write_file('./index_new.html', new_str)


  










file_path = './index3.html'
segs_dict = {
    'a': 'aa',
    'abc123': 'abc123',
}



find_list = insert_segs_in_file(segs_dict, file_path)


