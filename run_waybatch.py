"""
author: Jinwei Lin
time: 2022/11/06
usage: This is a simple example of using the WayBatch.

Note:
1. The default workspace of WayBatch is ./batchfiles.
2. The ./batchfiles/insertfiles saves the files that will be inserted.
3. The ./batchfiles/template saves the template files that is only one.
4. The ./batchfiles/output saves the ouput files that are generate automatically. 
5. If use the str values to insert, define them in the corresponding code.

"""
import WayBatch as wb



save_dir = './batchfiles/ouput/'

segs_dict = {
    'f1.html':{
        'way_id_1': 'str_content_1',
        'way_id_2': 'str_content_2',
    },
    'f2.html':{
        'way_id_1': 'str_content_3',
        'way_id_2': 'str_content_4',
    },
}
















