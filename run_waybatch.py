"""
author: Jinwei Lin
time: 2022/11/06
usage: This is a simple example of using the WayBatch.



"""
import WayBatch as wb



save_dir = './batchfiles/ouput/'
template_f_path = './batchfiles/template/template.html'

segs_dict = {
    'f1.html':{
        'way_id_1': 'str_content_1',
        'way_id_2': 'str_content_2',
    },
    'f2.html':{
        'way_id_1': 'str_content_3',
        'way_id_2': 'str_content_4',
    },
    'f3.html':{
        'way_id_1': 'str_content_4',
        'way_id_2': 'str_content_5',
    },
}


wb.batch_files(segs_dict, template_f_path, save_dir)













