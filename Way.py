import os
import json
import time
import shutil
import hashlib
import webbrowser
import multiprocessing

print('____________________________________________________________________________')
print(' Way.py: founded by Jinwei Lin: a easy and fast front-end generator library.')
print('____________________________________________________________________________')

# Load the config
with open('./config.json', 'r',  encoding='UTF-8') as config_f:
    config_f_read = config_f.read()
    config_f_read_json = json.loads(config_f_read)

# Set html way path
html_way_path = config_f_read_json['html_way_path']

# Set html origin path
html_edit_path = config_f_read_json['html_edit_path']

# Set html html build path
html_build_path = config_f_read_json['html_build_path']

# Get the edit mode
auto_generate_seed = config_f_read_json['auto_generate_seed']
auto_scaner_seed = config_f_read_json['auto_scaner_seed']

# Get the browser path
browser_exe_path = config_f_read_json['browser_exe_path']

# Get tag name list
home_index_html = os.getcwd() + '/' + config_f_read_json['home_index_html']

# Get tag name list
tag_name_list = os.listdir(html_way_path)

# Get welcome context
welcome_path = config_f_read_json['welcome_path']
welcome_context = config_f_read_json['welcome_context']

if welcome_context:
    with open(welcome_path, 'r',  encoding='UTF-8') as welcome_f:
        print(welcome_f.read())
    # print time
    print('______________________________________________________________________________\n')
    print('>> Run Time:', time.strftime( "%a %b,%d %H:%M:%S %Y", time.localtime()))


# Get above father dir
def get_father_dir(son_dir):
    separator_index = son_dir[::-1].index('/')
    return son_dir[:len(son_dir)-separator_index-1]


# Get all items in a dir
def get_all_items(now_dir, dir_set, file_set):
    now_item_list = os.listdir(now_dir)

    if now_item_list != []:
        for item_name in now_item_list:
            if if_files(item_name)[0]:
                file_set.append(now_dir + '/' + item_name)

            elif not if_files(item_name)[0]:
                new_dir = now_dir + '/' + item_name
                dir_set.append(new_dir)
                get_all_items(new_dir, dir_set, file_set)

    return [dir_set, file_set]
    


# Get now lists
def get_now_lists():
    # Get files and paths lists between editing and building
    all_edit_path_item = get_all_items(html_edit_path, [], [])
    all_way_path_item = get_all_items(html_way_path, [], [])

    # initialize lists
    now_html_list = []
    now_way_list = []

    # Get the now_html_list
    for i in all_edit_path_item[1]:
        if i.endswith('.html'):
            now_html_list.append(i)

    # Get the now_way_list
    for i in all_way_path_item[1]:
        if i.endswith('.html'):
            now_way_list.append(i)

    return [now_html_list, now_way_list]


#  judge if item is file
def if_files(item_name):
    if '.' in item_name:
        point_index = item_name.index('.')
        f_extension = item_name[point_index+1:]

        if f_extension != '':
            return [True, f_extension]
    else:
        return [False, None]


# Copy file
def copy_file(copy_path, paste_path):
    with open(copy_path, 'rb') as fr:
        with open(paste_path, 'wb') as fw:
            fw.write(fr.read())


# Get now lists
def now_update_scander(a_dir, edit_path):
    # Get files or directories list
    now_dir_scanning = a_dir
    files_list = os.listdir(now_dir_scanning)

    # Scaner the files or directories
    if files_list != []:
        for item_name in files_list:
            now_dir_scanning = a_dir + '/' + item_name
            # print('now_dir_scanning = ', now_dir_scanning)

            if not if_files(item_name)[0]:
                build_dir_path = html_build_path + now_dir_scanning[len(edit_path):]

                if not os.path.exists(build_dir_path):
                    os.makedirs(build_dir_path)
                
                # update iteration
                now_update_scander(now_dir_scanning, edit_path)


            # if item_name is a file name
            elif not item_name.endswith('.html'):
                build_file_path = html_build_path + now_dir_scanning[len(edit_path):]

                if not os.path.exists(build_file_path):
                    copy_file(now_dir_scanning, build_file_path)


# Write file
def write_files(file_path, file_str):
    try:
        with open(file_path, 'w', encoding='UTF-8') as fw:
            fw.write(file_str)
    except IOError:
        print('IOError: write_files error!')
        pass
    else:
        pass
        # print('Success!')

# Read file
def read_files(file_path):
    try:
        with open(file_path, 'r', encoding='UTF-8') as fr:
            fr_read = fr.read()
            return fr_read
    except IOError:
        print('IOError: read_files error!')
        pass
    else:
        pass
        # print('Success!')

# Get id context
def get_id_context(tag):
    if 'id=' in tag:
        # Get the index of 'id= '
        id_index = tag.index('id="')
        # Get the text of other part
        other_context = tag[id_index + 4:]
        # Get the id of closed index
        closed_index = other_context.index('"')

        id_context = tag[id_index + 4:id_index + 4 + closed_index]
        return id_context

    else:
        return None


# Get way tags set
def get_way_tags_set(html_name):
    way_tags_set = []
    # with open(html_edit_path + '/' + html_name, 'r+', encoding='UTF-8') as fr:
    try:
        with open(html_name, 'r', encoding='UTF-8') as fr:
            # Get the file content
            f_read = fr.read()
            # Define the index
            index = 0
            start_index = 0
            new_tag = False

            for char_i in f_read:
                if not new_tag:
                    if char_i == '<':
                        new_tag = True
                        start_index = index
                if new_tag:
                    if char_i == '>':
                        new_tag = False
                        end_index = index
                        # get tage segment
                        tag = f_read[start_index: end_index + 1]
                        # print('tag = ', tag)

                        # Handel the way tags
                        if tag[0:5] == '<way ':
                            id_context = get_id_context(tag)
                            if id_context:
                                way_tags_set.append([id_context, start_index, end_index + 7])
                                # print()
                index += 1
            return way_tags_set

    except IOError:
        print('IOError: get_way_tags_set error!')
        pass
    else:
        pass
        # print('Success!')


def get_html_segments(html_name, way_tag_set):
    # Update to new html in html build
    f_read = read_files(html_name)
    html_segments = []
    way_tag_end_index = 0
    sum_way_tag_index = 0
    way_tag_set_len = len(way_tag_set)


    if way_tag_set_len > 0:
        for way_tag in way_tag_set:
            sum_way_tag_index += 1
            if way_tag_set_len - sum_way_tag_index >= 0:
                if way_tag[1] == 0:
                    seg_origin = ''
                elif way_tag[1] > 0:
                    seg_origin = f_read[way_tag_end_index:way_tag[1]]

                seg_way = read_files(html_way_path + '/' + way_tag[0] + '.html')
                way_tag_end_index = way_tag[2]

                html_segments.append(seg_origin)
                html_segments.append(seg_way)

        html_segments.append(f_read[way_tag_end_index + 1:])
    return html_segments


# Get the combination of all strings in a list
def get_list_str_in_all(list_name):
    all_str = ''
    for s in list_name:
        all_str += s
    return all_str


# Delete the extra files in building folder
def delete_extra_files():
    # Get files and paths lists between editing and building
    all_edit_path_item = get_all_items(html_edit_path, [], [])
    all_build_path_item = get_all_items(html_build_path, [], [])

    # print('all_edit_path_item = ', all_edit_path_item)
    # print()
    # print('all_build_path_item = ', all_build_path_item)
    # print()

    len_build = len(html_build_path)

    # delete excess files
    for f_built_file in all_build_path_item[1]:
        f_built_2_edit = html_edit_path + f_built_file[len_build:]

        if f_built_2_edit not in all_edit_path_item[1]:
            # print('file ========>', f_built_2_edit, ' not in all_edit_path_item\n')
            try:
                os.remove(f_built_file)
            except IOError:
                # print('IOError: in delete_extra_files()!')
                pass
            else:
                pass
                # print('Success!')
        

    # delete excess dirs
    for f_built_dir in all_build_path_item[0]:
        f_built_2_edit = html_edit_path + f_built_dir[len_build:]
        # print('f_built_2_edit = ', f_built_2_edit)

        if f_built_2_edit not in all_edit_path_item[0]:
            # print('dir ========>', f_built_2_edit, ' not in all_edit_path_item\n')

            try:
                shutil.rmtree(f_built_dir)
            except IOError:
                # print('IOError: in delete_extra_files()!')
                pass
            else:
                pass
                # print('Success!')

    # print()

            
# Define way to handle html file
def way_html():
    now_html_list = get_now_lists()[0]
    edit_path_len = len(html_edit_path)

    for html_name in now_html_list:

        html_name_to_build = html_build_path + html_name[edit_path_len:]

        way_tag_set = get_way_tags_set(html_name)

        html_segments = get_html_segments(html_name, way_tag_set)

        write_files(html_name_to_build, get_list_str_in_all(html_segments))


# Static Test :

# way_html()
# now_update_scander(html_edit_path, html_edit_path)

# delete_extra_files()



# Way monitor for file individual update
def way_monitor_file_path(pipe):
    while True:
        try:
            now_update_scander(html_edit_path, html_edit_path)
            delete_extra_files()
            time.sleep(auto_scaner_seed)
        except IOError:
            print('IOError: way_monitor_file_path error!')
            pass
        else:
            pass
            # print('Success!')
       

# Way monitor for file content update
def way_monitor_file_way(pipe):
    # Use JSON to finish
    index_url = home_index_html
    browser_path = browser_exe_path

    try:
        if os.path.exists(browser_path):
            webbrowser.register('browser', None, webbrowser.BackgroundBrowser(browser_path))
            browser = webbrowser.get('browser')
            browser.open(index_url, new=0, autoraise=True)
        else:
            webbrowser.open(index_url, new=0, autoraise=True)

        while True:
            way_html()
            time.sleep(auto_generate_seed)
    except IOError:
        print('IOError: way_monitor_file_way error!')
        pass
    else:
        pass
        # print('Success!')

   


# Main RUN WAY
if __name__ == "__main__":
    # Set pipe
    file_pipe = multiprocessing.Pipe()
    # Set Processes
    p_file_path = multiprocessing.Process(target=way_monitor_file_path, args=(file_pipe[0],))
    p_file_way = multiprocessing.Process(target=way_monitor_file_way, args=(file_pipe[1],))

    p_file_path.start()
    p_file_way.start()


    




