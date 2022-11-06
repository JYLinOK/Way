# import jtc
import jtc.jtc as jtc
import re




def segments_list(file_path):
    file_txt = jtc.read_file(file_path)
    find_list = []
    pattern = re.compile(r'{{\s*(way\S*)\s*:\s*(\S+)\s*}}')
    finish = False
    ind = 0
    while not finish:
        mat = pattern.search(file_txt)
        if mat != None:
            if ind == 0:
                find_list.append([mat.span(), mat.groups()])
            else:
                print(f'{find_list = }')
                last_span = (mat.span()[0]+find_list[ind-1][0][1], mat.span()[1]+find_list[ind-1][0][1])
                find_list.append([last_span, mat.groups()])

            file_txt = file_txt[mat.span()[1]:]
            ind += 1
        else:
            finish = True



file_path = './index3.html'
segments_list(file_path)


