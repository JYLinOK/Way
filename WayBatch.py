# import jtc
import jtc.jtc as jtc
import re




def segments_dict(file_path):
    file_txt = jtc.read_file(file_path)
    # # print(f'{file_txt = }')
    # segs_list = re.findall(r'{{\s*(way\S*)\s*:\s*(\S+)\s*}}', file_txt)
    # # print(f'{segs_list = }')
    # print(f'{segs_list = }')

    print(f'{file_txt[168:178] = }')

    pattern = re.compile(r'{{\s*(way\S*)\s*:\s*(\S+)\s*}}')
    mat = pattern.search(file_txt)
    print(f'{mat = }')
    print(f'{mat.span() = }')
    print(f'{mat.group() = }')
    print(f'{mat.groups() = }')





file_path = './index3.html'
segments_dict(file_path)


