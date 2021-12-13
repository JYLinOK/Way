import os
import json
import time
import hashlib
import webbrowser
import multiprocessing

# Load the config
with open('./config.json', 'r',  encoding='UTF-8') as config_f:
    config_f_read = config_f.read()
    config_f_read_json = json.loads(config_f_read)


print()

# Set html ways path
html_ways_path = config_f_read_json['html_ways_path']

# Set html origin path
html_edit_path = config_f_read_json['html_edit_path']

# Set html html build path
html_build_path = config_f_read_json['html_build_path']

# Get the edit mode
auto_generate_seed = config_f_read_json['auto_generate_seed']
auto_scaner_seed = config_f_read_json['auto_scaner_seed']

# Get tag name list
home_index_html = os.getcwd() + '/' + config_f_read_json['home_index_html']
 
# Get tag name list
tag_name_list = os.listdir(html_ways_path)



# Get now lists
def get_now_lists():
    # Get files and paths lists
    all_html_list = os.listdir(html_edit_path)
    all_ways_list = os.listdir(html_ways_path)
    # print('all_html_list = ', all_html_list)
    # print('all_ways_list = ', all_ways_list)

    # initialize
    now_html_list = []
    now_way_list = []

    # Get the now_html_list
    for i in all_html_list:
        if i.endswith('.html'):
            now_html_list.append(i)

    # Get the now_way_list
    for i in all_ways_list:
        if i.endswith('.html'):
            now_way_list.append(i)

    # print('now_html_list = ', now_html_list)
    # print('now_way_list = ', now_way_list)

    return [now_html_list, now_way_list]



# Write file
def write_files(file_path, file_str):
    with open(file_path, 'w', encoding='UTF-8') as fw:
        fw.write(file_str)


# Read file
def read_files(file_path):
    with open(file_path, 'r', encoding='UTF-8') as fr:
        fr_read = fr.read()
        return fr_read


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
        # print("id = ", id_context)
        return id_context
    else:
        return None


# Get way tags set
def get_way_tags_set(html_name):
    way_tags_set = []
    with open(html_edit_path + '/' + html_name, 'r+', encoding='UTF-8') as fr:
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
                        # print('way tag = ', tag)
                        # print('way start_index = ', start_index)
                        # print('way end_index = ', end_index)

                        id_context = get_id_context(tag)
                        if id_context:
                            way_tags_set.append([id_context, start_index, end_index + 7])
                            # print()

            index += 1
    # print('____________________________________')   
    # print('way_tags_set = ', way_tags_set)
    return way_tags_set


def get_html_segments(html_name, way_tag_set):
    # Update to new html in html build
    f_read = read_files(html_edit_path + '/' + html_name)
    html_segments = []
    way_tag_end_index = 0
    sum_way_tag_index = 0
    way_tag_set_len = len(way_tag_set)

    # print('way_tag_set = ', way_tag_set)

    if way_tag_set_len > 0:
        for way_tag in way_tag_set:
            sum_way_tag_index += 1
            if way_tag_set_len - sum_way_tag_index >= 0:
                if way_tag[1] == 0:
                    seg_origin = ''
                elif way_tag[1] > 0:
                    seg_origin = f_read[way_tag_end_index:way_tag[1]]
                
                seg_way = read_files(html_ways_path + '/' + way_tag[0] + '.html')
                way_tag_end_index = way_tag[2]
                
                html_segments.append(seg_origin)
                html_segments.append(seg_way)
            

        html_segments.append(f_read[way_tag_end_index + 1:])

    # print('way_segments = \n', way_segments)
    # print('len(way_segments) = ', len(way_segments))
    # p = 0
    # for item in way_segments:
    #     print('\n-------------------------------------------------------------'
    #           '--------------------------------\n No. ', p, 'segment : \n', item)
    #     p += 1

    return html_segments


# Get the combination of all strings in a list
def get_list_str_in_all(list_name):
    all_str = ''
    for s in list_name:
        all_str += s
    return all_str


# Define way to handle html file
def way_html():
    now_html_list = get_now_lists()[0]
    for html_name in now_html_list:
        # print('-----------------------------------------')
        # print('edit html_name = ', html_name)
        way_tag_set = get_way_tags_set(html_name)
        # print('way_tag_set = ', way_tag_set)

        html_segments = get_html_segments(html_name, way_tag_set)
        # print('html_segments = ', html_segments)
        write_files(html_build_path + '/' + html_name, get_list_str_in_all(html_segments))


# Test:
# way_html()


# Way monitor for file individual update
def way_monitor_file_path(pipe):
    while True:
        html_way_list = get_now_lists()
        pipe.send(html_way_list)
        # print('A>> = ', html_way_list)
        # print()
        time.sleep(auto_scaner_seed)


# Way monitor for file content update
def way_monitor_file_way(pipe):
    # Use JSON to finish
    # print('instant_edit_mode')
    index_url = home_index_html
    webbrowser.open(index_url, new=0, autoraise=False)
    while True:
        way_html()
        # print('B>>...', pipe.recv(), '\n')
        time.sleep(auto_generate_seed)



# Main RUN WAY
if __name__ == "__main__":
    # Set pipe
    file_pipe = multiprocessing.Pipe()
    p_file_path = multiprocessing.Process(target=way_monitor_file_path, args=(file_pipe[0],))
    p_file_way = multiprocessing.Process(target=way_monitor_file_way, args=(file_pipe[1],))

    p_file_path.start()
    p_file_way.start()














