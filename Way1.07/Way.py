import os
import sys
import json
import time
import shutil
import hashlib
import webbrowser
import multiprocessing

print('_____________________________________________________________________________')
print(' Way.py: founded by Jinwei Lin: an easy and fast front-end generator library.')
print('_____________________________________________________________________________')

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
way_router_path = config_f_read_json['way_router_path']

# Get auto restart
auto_restart = config_f_read_json['way_router_path']

# Get way_announce
way_announce = config_f_read_json['way_announce']
way_announce_str = "<script>console.log('\\\A/ Hi, Way! - An easy and fast front-end generator library.');</script>"

# Get welcome context
welcome_path = config_f_read_json['welcome_path']
welcome_context = config_f_read_json['welcome_context']

if welcome_context:
    with open(welcome_path, 'r',  encoding='UTF-8') as welcome_f:
        print(welcome_f.read())
    # print time
    print('______________________________________________________________________________')
    print('>> Way: Run Time:', time.strftime( "%a %b,%d %H:%M:%S %Y", time.localtime()), '\n')

# ============================================================================================================
# ============================================================================================================
# Auto-restart 
def auto_restart():
    if auto_restart:
        print('Way: Restarting...')
        sys.exit(0)
        os.system('python Way.py')


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
        auto_restart()
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
        print('IOError: read_files() error!')
        auto_restart()
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
    

# Get id context
def get_wr_context(tag):
    if 'wr=' in tag:
        # Get the index of 'wr= '
        wr_index = tag.index('wr="')
        # Get the text of other part
        other_context = tag[wr_index + 4:]
        # Get the wr of closed index
        closed_index = other_context.index('"')

        wr_context = tag[wr_index + 4:wr_index + 4 + closed_index]
        return wr_context

    else:
        return None


# Get way tags set
def get_way_tags_set(html_path):
    way_tags_set = []
    # with open(html_edit_path + '/' + html_path, 'r+', encoding='UTF-8') as fr:
    try:
        with open(html_path, 'r', encoding='UTF-8') as fr:
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
                            # test whether have a id
                            id_context = get_id_context(tag)
                            if id_context:
                                way_tags_set.append([id_context, start_index, end_index + 7, 'id'])
                                # print()

                            # if the way-tag is a wayrouter tag
                            else:
                                wr_context = get_wr_context(tag)
                                if wr_context:
                                    way_tags_set.append([wr_context, start_index, end_index + 7, 'wr'])
                                    # print('\nwr_context way_tags_set = ', wr_context)

                index += 1
            return way_tags_set

    except IOError:
        print('IOError: get_way_tags_set() error!')
        auto_restart()
        pass
    else:
        pass
        # print('Success!')


# get sparated set of text
def get_sparate_set(origin, start_sign, end_sign, item_index):
    start_sign_len = len(start_sign)
    end_sign_len = len(end_sign)

    # print('origin = ', origin)
    # print('start_sign = ', start_sign)
    # print('end_sign = ', end_sign)
    # print('item_index = ', item_index)

    start_index = 0
    result_set = []

    if origin != '':
        for char_i in origin:
            if char_i == start_sign[0]:
                s_sign = origin[start_index: start_index + 3]
                # print('start_sign = ', start_sign)

                if s_sign == start_sign:
                    rest_origin = origin[start_index+1:]
                    # print('rest_origin = ', rest_origin)

                    len_index = 0
                    for i_rest in rest_origin:
                        # print(i_rest)

                        if i_rest == end_sign:
                            # print(i_rest)

                            sparated = origin[start_index+1:start_index+len_index+1]
                            # print('sparated = ', sparated, '\n')

                            rest_origin = origin[start_index+len_index+2:]
                            # print('rest_origin = ', rest_origin, '\n')

                            item_index += 1
                            # print('item_index = ', item_index, '\n')
                            result_set.append([sparated, start_index+1, start_index+len_index+1, item_index-1]) 
                            get_sparate_set(rest_origin, start_sign, end_sign, item_index-1)
                            break

                        len_index += 1

            start_index += 1
        return result_set
    else:
        print("File Not Exist!")


# get the segments of text by known sparated segments list
def sum_text_sparated (origin_text, sparated_list):
    text_sparated_set = []

    # print('\n', 'origin_text = ', origin_text)
    # print('sparated_list = ', sparated_list, '\n')

    if sparated_list != []:
        last_seg_index = 0 
        for i_seg in sparated_list:
            text_sparated_set.append(origin_text[last_seg_index:i_seg[1]])
            text_sparated_set.append(i_seg[0])
            last_seg_index = i_seg[2]

        text_sparated_set.append(origin_text[sparated_list[-1][2]:])
        # print('text_sparated_set = ', text_sparated_set)
        return text_sparated_set
    else:
        return origin_text


# get the level of a path:
def get_path_level(path):
    # print('path = ', path)
    level = 0

    for i_char in path:
        if i_char == '/':
            level += 1
    
    return level

 
# change the path to relative path automatically based on reference dir  
def auto_change_link(inside_path, change_path):

    inside_path_level = get_path_level(inside_path)
    change_path_level = get_path_level(change_path)

    # print('inside_path_level = ', inside_path_level)
    # print('change_path_level = ', change_path_level)

    if inside_path_level == 2:
        return change_path

    else:
         point = '../'
         font_point = ''
         for i in range(inside_path_level-2):
             font_point = font_point + point

         new_path = font_point + change_path[2:]
         return font_point + change_path[2:]


# chang and connect the wr text 
def change_connect(origin, embody, html_path):
    len_o = len(origin)
    len_e = len(embody)
    if len_o == 2*len_e + 1:
        for i in range(len_e):
            origin[2*i + 1] = auto_change_link(html_path, embody[i][0])

    return origin


# get changed wayrouter content
def get_wayrouted_content(way_path, html_path, way_router_path):

    # print('html_path = ',  html_path)
    # print('way_router_path = ',  way_router_path)
    
    wr_content_origin = read_files(way_path)
    # print('wr_content_origin = ',  wr_content_origin)
    
    new_cont_set = []
    sparated_set = get_sparate_set(wr_content_origin, '"./', '\"', 0)
    # print('sparated_set = ',  sparated_set, '\n')

    text_sparated_list = sum_text_sparated(wr_content_origin, sparated_set)
    # print('text_sparated_list = ', text_sparated_list,'\n')

    # print('len(sparated_set) = ', len(sparated_set))
    # print('len(text_sparated_list) = ', len(text_sparated_list),'\n')
    
    updated_sparated_set = change_connect(text_sparated_list, sparated_set, html_path)
    # print('get_list_str_in_all_wayrouter(updated_sparated_set) = ', get_list_str_in_all_wayrouter(updated_sparated_set))

    return get_list_str_in_all_wayrouter(updated_sparated_set)



# get the way segment content by way name
def get_way_content(way_name, way_class, html_path, html_way_path):
   
    # Handle the pure way 
    if way_class == 'id':
        all_way_path_item = get_all_items(html_way_path, [], [])
        way_path = html_way_path + '/' + way_name + '.html'

        # print('way_path = ', way_path, '\n')
        # print('all_way_path_item[1] = ', all_way_path_item[1], '\n')

        flag_true_return = False

        for i_way in all_way_path_item[1]:
            # print('i_way = ', i_way)
            if i_way == way_path:
                # print(' i_way == way_path = ', way_path)
                flag_true_return = True
                return read_files(way_path)

        if not flag_true_return:
            return None
    
    # Handle the way router
    elif way_class == 'wr':
        all_wayrouter_path = get_all_items(way_router_path, [], [])
        way_path = way_router_path + '/' + way_name + '.html'
        
        # print('html_path = ', html_path)
        # print('way_path = ', way_path, '\n')
        # print('all_wayrouter_path[1] = ', all_wayrouter_path[1], '\n')

        flag_true_return = False

        for i_wr in all_wayrouter_path[1]:
            # print('i_wr = ', i_wr)
            if i_wr == way_path:
                # print(' i_wr == way_path = ', way_path)
                flag_true_return = True

                # return read_files(way_path)
                return get_wayrouted_content(way_path, html_path, way_router_path)

        if not flag_true_return:
            return None


# get the combined string of original html ans way segments
def get_html_add_segments(html_path, way_tag_set):
    # Update to new html in html build
    f_read = read_files(html_path)
    html_add_segments = []
    way_tag_end_index = 0
    sum_way_tag_index = 0
    way_tag_set_len = len(way_tag_set)
    seg_origin = ''

    # print('>> get_html_add_segments()')
    # print('html_path = ', html_path, '\n')
    # print('way_tag_set = ', way_tag_set, '\n')

    if way_tag_set_len > 0:
        for way_tag in way_tag_set:
            sum_way_tag_index += 1
            if way_tag_set_len - sum_way_tag_index >= 0:
                if way_tag[1] == 0:
                    seg_origin = ''
                elif way_tag[1] > 0:
                    seg_origin = f_read[way_tag_end_index:way_tag[1]]
                
                seg_way_content = get_way_content(way_tag[0], way_tag[3], html_path, html_way_path)
                # print('seg_way_content = ', seg_way_content, '\n')

                way_tag_end_index = way_tag[2]

                html_add_segments.append(seg_origin)
                html_add_segments.append(seg_way_content)

        html_add_segments.append(f_read[way_tag_end_index + 1:])
    return html_add_segments



# Get the combination of all strings in a list
def get_list_str_in_all(list_name):
    
    # print('>> get_list_str_in_all')
    # print('list_name = ', list_name)
    if way_announce:
        all_str = ''
        for s in list_name:
            if s != None:
                if '</html>' in s:
                    all_str = all_str + way_announce_str + s 
                else: all_str += s
        return all_str 
    



# et the combination of all strings in a wayrouter list
def get_list_str_in_all_wayrouter(list_name):
    all_str = ''
    for s in list_name:
        if s != None:
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
                print('IOError: in delete_extra_files()!')
                auto_restart()
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
                auto_restart()
                print('IOError: in delete_extra_files()!')
                pass
            else:
                pass
                # print('Success!')

    # print()

            
# Define way to handle html file
def way_html():
    now_html_list = get_now_lists()[0]
    edit_path_len = len(html_edit_path)

    # print('now_html_list = ', now_html_list)

    for html_path in now_html_list:

        html_path_to_build = html_build_path + html_path[edit_path_len:]

        way_tag_set = get_way_tags_set(html_path)
        # print('way_tag_set = ', way_tag_set)

        html_add_way_segments = get_html_add_segments(html_path, way_tag_set)
        # print('html_add_way_segments = ', html_add_way_segments)
        # print('get_list_str_in_all(html_add_way_segments) = ', get_list_str_in_all(html_add_way_segments))

        write_files(html_path_to_build, get_list_str_in_all(html_add_way_segments))



# =============================================================================
# Static Test :

# way_html()

# now_update_scander(html_edit_path, html_edit_path)

# delete_extra_files()

# a = get_way_content('home/wr1', 'wr', './index.html', html_way_path)
# print('a = \n', a)


# way_path = './wayrouter/home/wr1.html'
# html_path = './htmledit/a/ydook.html'
# a = get_wayrouted_content(way_path, html_path, way_router_path)
# print('a = \n', a)


# a = [1, 3, 5, 7, 9, 11, 13, 15]
# b = [2, 4, 6, 8]
# print(change_connect(a, b))


# wr = './wayrouter/home/wr1.html'
# text = read_files(wr)
# a = get_sparate_set(text, '"./', '\"', 0)
# print('a = \n', a)


# inside_path = './a/a/a/ydook.html'
# change_path = './about.html'
# a = auto_change_link(inside_path, change_path)
# print('a = \n', a)

# auto_restart()

# =============================================================================
# =============================================================================


# Way monitor for file individual update
def way_monitor_file_path(pipe):
    while True:
        try:
            now_update_scander(html_edit_path, html_edit_path)
            delete_extra_files()
            time.sleep(auto_scaner_seed)
        except IOError:
            print('IOError: way_monitor_file_path error!')
            auto_restart()
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
        auto_restart()
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

    pass
    


# ======================================================================================
# ======================================================================================

















