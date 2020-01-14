from ProcessObj.textprocess import *


class FilterObj:
    def __init__(self, data_section_file, text_section_file, tags_file):
        self.__final_text_out = "/tmp/FinalTextOut"
        self.__future_tags_file = tags_file
        self.__text_process_obj = TextProcessObj(
            data_section_file=data_section_file, text_section_file=text_section_file)
        # {'name' : [dir_level1, 'dir_level2', ...]}
        self.tag_dict = {}
        # {'dir_level1' : 'name'}
        self.dir_dict = {}
        self.init_tag_dict()
        self.start()

    # filter functions to the directory it belongs to
    def final_trip(self):
        for e in self.tag_dict:
            if self.tag_dict[e][-1] == 'xxxhit':
                up_level_dir = self.tag_dict[e][0]
                g = self.dir_dict.get(up_level_dir)
                if g is None:
                    self.dir_dict[up_level_dir] = [e]
                else:
                    # get the first function in the directory
                    self.dir_dict[up_level_dir].append(e)

    def init_tag_dict(self):
        tags_file = open(self.__future_tags_file, 'r')
        tag_lines = tags_file.readlines()
        for single_line in tag_lines:
            if not re.findall(r'^!', single_line):
                tag_list = single_line.split()
                dir_list = tag_list[1].split('/')
                self.tag_dict[tag_list[0]] = dir_list
        tags_file.close()

        # debug_tag_list = open('/tmp/debugTagList', 'w')
        # for e in self.tag_dict:
        #     debug_tag_list.write('%s: %s\n' % (e, self.tag_dict[e]))
        # debug_tag_list.close()

    def start(self):
        self.__text_process_obj.start_strip()
        self.__text_process_obj.rough_count()
        unused = self.__text_process_obj.unused
        for e in unused:
            g = self.tag_dict.get(unused[e][0])
            if g is not None:
                # mark the function which hit in the directories
                self.tag_dict[unused[e][0]].append('xxxhit')
        self.final_trip()
        final_text_out = open(self.__final_text_out, 'w')
        for e in self.dir_dict:
            final_text_out.write('%s:\n' % e)
            for i in self.dir_dict[e]:
                final_text_out.write('\t%s\n' % i)
            final_text_out.write('\n\n')

        final_text_out.close()
