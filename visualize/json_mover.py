import shutil
import os

dist = './non_interactive_wordcloud/json_file/'

category_list = ['english', 'journal', 'korean']

for category in category_list:
    category_path = './' + category + '_visualize/'
    platform_list = os.listdir(category_path)
    for platform in platform_list:
        platform_path = category_path + platform + '/'
        if category == 'korean':
            platform_file_list = os.listdir(platform_path)
            for screen in platform_file_list:
                screen_path = platform_path + screen + '/'
                screen_file_list = os.listdir(screen_path)
                json_file_list = [file for file in screen_file_list if file.endswith('.json')]
                for json_file in json_file_list:
                    json_path = screen_path + json_file
                    new_file_name = category + '_' + platform + '_' + screen + '_' + json_file
                    shutil.copy(json_path, dist + new_file_name)
        else:
            platform_file_list = os.listdir(platform_path)
            json_file_list = [file for file in platform_file_list if file.endswith('.json')]
            for json_file in json_file_list:
                json_path = platform_path + json_file
                new_file_name = category + '_' + platform + '_' + json_file
                shutil.copy(json_path, dist + new_file_name)

