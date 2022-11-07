import os
import time
import shutil
import webbrowser
from pathlib import Path
from multiprocessing import Process, Queue


from wayconfig import wayconfig



# ============================================================================================================
# ============================================================================================================
# Load the config
home_index_html = os.getcwd() + '/' + wayconfig['home_index_html']

# Get tag name list
tag_name_list = os.listdir(wayconfig['html_way_path'])




# ============================================================================================================
# ============================================================================================================
# Set welcome
def welcome_show():
    if not wayconfig['welcome_got']:
        if wayconfig['welcome_context']:
            print('_____________________________________________________________________________')
            print(' Way.py: founded by Jinwei Lin: an easy and fast front-end generator library.')
            print('_____________________________________________________________________________')

            with open(wayconfig['welcome_path'], 'r',  encoding='UTF-8') as welcome_f:
                print(welcome_f.read())
            # print time
            print('______________________________________________________________________________')
            print('>> Way: Run Time:', time.strftime( "%a %b,%d %H:%M:%S %Y", time.localtime()), '\n')
            wayconfig['welcome_got'] = True

# Auto-restart 
def auto_restart():
    if wayconfig['auto_restart']:
        time.sleep(wayconfig['auto_restart_seed'])
        os.system('python Way.py')
        print('>> Way: Restarted')


# Get above father dir
def get_father_dir(son_dir):
    separator_index = son_dir[::-1].index('/')
    return son_dir[:len(son_dir)-separator_index-1]


# Get all items in a dir
def get_all_items(now_dir, dir_set, file_set):

    if os.path.exists(now_dir):
        now_item_list = os.listdir(now_dir)
        # print('now_item_list = ', now_item_list)

        if now_item_list != []:
            for item_name in now_item_list:
                # print('item_name = ', item_name)
                now_dir_file = now_dir + '/' + item_name
                item_is_file = if_is_file(now_dir_file)[0]

                if item_is_file:
                    # print('is file', '\n')
                    file_set.append(now_dir_file)

                elif not item_is_file:
                    # print('is dir', '\n')
                    dir_set.append(now_dir_file)
                    get_all_items(now_dir_file, dir_set, file_set)

        return [dir_set, file_set]
    


# Get now lists
def get_now_lists():
    # Get files and paths lists between editing and building
    all_edit_path_item = get_all_items(wayconfig['html_edit_path'], [], [])
    all_way_path_item = get_all_items(wayconfig['html_way_path'], [], [])

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
def if_is_file(item_name):
    f_extension = os.path.splitext(item_name)[1] 
    if Path(item_name).is_file():
        return [True, f_extension]
    else:
        return [False, None]


# Copy file
def copy_file(copy_path, paste_path):
    with open(copy_path, 'rb') as fr:
        with open(paste_path, 'wb') as fw:
            fw.write(fr.read())



# ________________________________________________________________________________________________________
def if_end_with_extend_list(file_name:str, extend_list:list):
    """
    Judge if a file name is end with the items in a extend_list or not
    """
    end_with = False
    for extend in extend_list:
        if file_name.endswith(extend):
            end_with = True
            break
    return end_with
    



# Get now lists
def now_update_scander(a_dir, edit_path):
    # Get files or directories list
    # print('\na_dir = ', a_dir)

    now_dir_scanning = a_dir
    files_list = os.listdir(now_dir_scanning)
    # print('files_list = ', files_list)

    # Scaner the files or directories
    if files_list != []:
        for item_name in files_list:
            # if not item_name:
                # print('item_name = ', item_name)
                now_dir_scanning = a_dir + '/' + item_name

                # print('now_dir_scanning = ', now_dir_scanning)
                # print('if_is_file(now_dir_scanning)[0] = ', if_is_file(now_dir_scanning)[0], '\n')

                # if item_name is a dir name
                extend_list = ['.html']
                if not if_is_file(now_dir_scanning)[0]:
                    build_dir_path = wayconfig['html_build_path'] + now_dir_scanning[len(edit_path):]
                    # print('not file: build_dir_path = ', build_dir_path,'\n')

                    if not os.path.exists(build_dir_path):
                        os.makedirs(build_dir_path)

                    # update iteration
                    now_update_scander(now_dir_scanning, edit_path)

                # if item_name is a file name
                elif not if_end_with_extend_list(item_name, extend_list):
                    build_file_path = wayconfig['html_build_path'] + now_dir_scanning[len(edit_path):]
                    # print('is file: build_dir_path = ', build_file_path,'\n')

                    # rewrite and create other formats but html files  
                    copy_file(now_dir_scanning, build_file_path)


# Write file
def write_files(file_path, file_str):
    try:
        with open(file_path, 'w', encoding='UTF-8') as fw:
            fw.write(file_str)
    except IOError:
        print('IOError: write_files error!')
        try:
            write_files(file_path, file_str)
        except IOError:
            wayconfig['auto_restart']()


# Read file
def read_files(file_path):
    if Path(file_path).is_file():  
        try:
            with open(file_path, 'r', encoding='UTF-8') as fr:
                fr_read = fr.read()
                return fr_read
        except IOError:
            print('IOError: read_files() error!')
            try:
                read_files(file_path)
            except IOError:
                wayconfig['auto_restart']()


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
    if Path(html_path).is_file():    
        way_tags_set = []
        # with open(wayconfig['html_edit_path'] + '/' + html_path, 'r+', encoding='UTF-8') as fr:
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
            try:
                get_way_tags_set(html_path)
            except IOError:
                wayconfig['auto_restart']()


# get sparated set of text
# sparated_set = get_sparate_set(wr_content_origin, '"./', '\"', 0)
def get_sparate_set(origin, start_sign, end_sign, item_index):
    if origin != '':
        start_sign_len = len(start_sign)
        end_sign_len = len(end_sign)

        # print('origin = ', origin)
        # print('start_sign = ', start_sign)
        # print('end_sign = ', end_sign)
        # print('item_index = ', item_index)

        start_index = 0
        result_set = []

        try:
            for char_i in origin:
                if char_i == start_sign[0] or char_i == "\'":
                    s_sign = origin[start_index: start_index + 3]
                    # print('start_sign = ', start_sign)

                    if s_sign == start_sign or s_sign == "'./":
                        rest_origin = origin[start_index+1:]
                        # print('rest_origin = ', rest_origin)

                        len_index = 0
                        for i_rest in rest_origin:
                            # print(i_rest)

                            if i_rest == end_sign or i_rest == "\'":
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

        except IOError:
            print('IOError: get_sparate_set() error!')
            try:
                get_sparate_set(origin, start_sign, end_sign, item_index)
            except IOError:
                wayconfig['auto_restart']()


# get the segments of text by known sparated segments list
def sum_text_sparated (origin_text, sparated_list):
    text_sparated_set = []

    # print('\n', 'origin_text = ', origin_text)
    # print('sparated_list = ', sparated_list, '\n')

    if sparated_list:
        last_seg_index = 0 
        for i_seg in sparated_list:
            if i_seg:
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
    if origin and embody:
        len_o = len(origin)
        len_e = len(embody)
        if len_o == 2*len_e + 1:
            for i in range(len_e):
                origin[2*i + 1] = auto_change_link(html_path, embody[i][0])

    return origin


# get changed wayrouter content
def get_wayrouted_content(way_path, html_path, wayconfig):

    # print('html_path = ',  html_path)
    # print('wayconfig['way_router_path'] = ',  wayconfig['way_router_path'])
    
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
def get_way_content(way_name, way_class, html_path, wayconfig):
   
    # Handle the pure way 
    if way_class == 'id':
        all_way_path_item = get_all_items(wayconfig['html_way_path'], [], [])
        way_path = wayconfig['html_way_path'] + '/' + way_name + '.html'

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
        all_wayrouter_path = get_all_items(wayconfig['way_router_path'], [], [])
        way_path = wayconfig['way_router_path'] + '/' + way_name + '.html'
        
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
                return get_wayrouted_content(way_path, html_path, wayconfig)

        if not flag_true_return:
            return None


# get the combined string of original html ans way segments
def get_html_add_segments(html_path, way_tag_set, wayconfig):
    # Update to new html in html build
    f_read = read_files(html_path)
    html_add_segments = []
    way_tag_end_index = 0
    sum_way_tag_index = 0
    seg_origin = ''

    # print('>> get_html_add_segments()')
    # print('html_path = ', html_path, '\n')
    # print('way_tag_set = ', way_tag_set, '\n')

    if way_tag_set:
        way_tag_set_len = len(way_tag_set)
        for way_tag in way_tag_set:
            sum_way_tag_index += 1
            if way_tag_set_len - sum_way_tag_index >= 0:
                if way_tag[1] == 0:
                    seg_origin = ''
                elif way_tag[1] > 0:
                    seg_origin = f_read[way_tag_end_index:way_tag[1]]
                
                seg_way_content = get_way_content(way_tag[0], way_tag[3], html_path, wayconfig)
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
    if wayconfig['way_announce']:
        all_str = ''
        for s in list_name:
            if s != None:
                if '</html>' in s:
                    all_str = all_str + wayconfig['way_announce_str'] + s 
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
    all_edit_path_item = get_all_items(wayconfig['html_edit_path'], [], [])
    all_build_path_item = get_all_items(wayconfig['html_build_path'], [], [])

    # print('all_edit_path_item = ', all_edit_path_item)
    # print()
    # print('all_build_path_item = ', all_build_path_item)
    # print()

    len_build = len(wayconfig['html_build_path'])

    # delete excess files
    for f_built_file in all_build_path_item[1]:
        f_built_2_edit = wayconfig['html_edit_path'] + f_built_file[len_build:]

        if f_built_2_edit not in all_edit_path_item[1]:
            # print('file ========>', f_built_2_edit, ' not in all_edit_path_item\n')
            if Path(f_built_file).is_file():
                try:
                    os.remove(f_built_file)
                except IOError:
                    print('IOError: in delete_extra_files()!')
                    try:
                        os.remove(f_built_file)
                    except IOError:
                        wayconfig['auto_restart']()
    
        
    # delete excess dirs
    for f_built_dir in all_build_path_item[0]:
        f_built_2_edit = wayconfig['html_edit_path'] + f_built_dir[len_build:]
        # print('f_built_2_edit = ', f_built_2_edit)

        if f_built_2_edit not in all_edit_path_item[0]:
            # print('dir ========>', f_built_2_edit, ' not in all_edit_path_item\n')
            if Path(f_built_dir).is_dir():
                try:
                    shutil.rmtree(f_built_dir)
                except IOError:
                    print('IOError: in delete_extra_files()!')
                    time.sleep(1)
                    shutil.rmtree(f_built_dir)
                    pass
                else:
                    pass
                    # print('Success!')

    # print()

            
# Define way to handle html file
def way_html(wayconfig):
    now_html_list = get_now_lists()[0]
    edit_path_len = len(wayconfig['html_edit_path'])

    # print('now_html_list = ', now_html_list)
    try:
        for html_path in now_html_list:
            html_path_to_build = wayconfig['html_build_path'] + html_path[edit_path_len:]

            way_tag_set = get_way_tags_set(html_path)
            # print('way_tag_set = ', way_tag_set)

            html_add_way_segments = get_html_add_segments(html_path, way_tag_set, wayconfig)
            # print('html_add_way_segments = ', html_add_way_segments)
            # print('get_list_str_in_all(html_add_way_segments) = ', get_list_str_in_all(html_add_way_segments))

            write_files(html_path_to_build, get_list_str_in_all(html_add_way_segments))
        
    except IOError:
        print('IOError: way_html error!')
        try:
            way_html(wayconfig)
        except IOError:
            wayconfig['auto_restart']()



# =============================================================================
# =============================================================================

# Run the web browser
def run_browser():
    # Get specified browser location 
    index_url = home_index_html
    browser_path = wayconfig['browser_exe_path']

    try:
        # Run specified browser
        if os.path.exists(browser_path):
            webbrowser.register('browser', None, webbrowser.BackgroundBrowser(browser_path))
            browser = webbrowser.get('browser')
            browser.open(index_url, new=0, autoraise=True)
        # Run normal browser
        else:
            webbrowser.open(index_url, new=0, autoraise=True)
    except IOError:
        print('IOError: run_browser error!')
        try:
            run_browser()
        except IOError:
            wayconfig['auto_restart']()


# Way monitor for file individual update
def way_update_structure(q):
    try:
        while True:
            now_update_scander(wayconfig['html_edit_path'], wayconfig['html_edit_path'])
            delete_extra_files()
            q.put('structure')
            time.sleep(wayconfig['auto_scaner_seed'])
          
    except IOError:
        print('IOError: way_update_structure error!')
        way_update_structure(q)
        pass
    else:
        pass
        # print('Success!')


# Way monitor for file content update
def way_update_keyfiles(q, wayconfig):
    # print('q.get() = ', q.get())

    try:
        run_browser()
        while True:
            if q.get() == 'structure':
                # print('q.get() = ', q.get())
                # print('q.empty() = ', q.empty(), '\n')
                way_html(wayconfig)
                time.sleep(wayconfig['auto_generate_seed'])
        
    except IOError:
        print('IOError: way_update_keyfiles error!')
        way_update_keyfiles(q)
        pass
    else:
        pass
        # print('Success!')



# ________________________________________________________________________________________________________
def simple_run(wayconfig):
    """
    Quickly run the Way
    """
    # Show welcom
    welcome_show()

    # Set Queue
    q = Queue()
    q_structure = Process(target=way_update_structure, args=(q,))
    q_keyfiles = Process(target=way_update_keyfiles, args=(q, wayconfig))

    # Start Process
    q_structure.start()
    q_keyfiles.start()

    # Join Process
    q_structure.join()
    q_keyfiles.join()


   


# ============================================================================================================
# ============================================================================================================
# Main RUN WAY
if __name__ == "__main__":
    simple_run(wayconfig)

    pass
    


# ======================================================================================
# ======================================================================================













