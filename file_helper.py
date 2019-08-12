import os

class FileHelperBase(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def _get_leading_spaces(self, line):
        spaces = []
        for char in line:
            if char in ['\r', '\t', '\n', ' ']:
                spaces.append(char)
            else:
                break

        return spaces


    def can_be_accessed(self):
        result = True
        if not os.path.exists(self.file_path):
            print "%s does not exist!" % self.file_path
            result = False
        elif not os.path.isfile(self.file_path):
            print "%s is not a file!" % self.file_path
            result = False
        elif not os.access(self.file_path, os.W_OK):
            print "No permissions to edit file %s" % self.file_path
            result = False

        return result


class TextFileHelper(FileHelperBase):
    def __init__(self, file_path):
        super(TextFileHelper, self).__init__(file_path)


    def add_new_line_after(self, reference_line, new_line, keep_leading_spaces=True, add_if_already_existing=False):
        if self.can_be_accessed():
            new_line_index = -1
            reference_line_index = -1
            new_line_already_existing = False
            new_line_to_add = []
            file_lines = []

            with open(self.file_path, 'r') as the_file:
                file_lines = the_file.readlines()
                for i, line in enumerate(file_lines):
                    if reference_line in line:
                        new_line_index = i + 1
                        if keep_leading_spaces: # Keep the same indentation used by the reference line.
                            new_line_to_add.extend(self._get_leading_spaces(line))
                    elif new_line in line:
                        new_line_already_existing = True

            if new_line_index != -1 and not new_line_already_existing or add_if_already_existing:
                with open(self.file_path, 'w') as the_file:
                    new_line_to_add.extend(new_line)
                    file_lines.insert(new_line_index, ''.join(new_line_to_add) + '\n')
                    the_file.write(''.join(file_lines))


class ConfigFileHelper(FileHelperBase):
    def __init__(self, file_path):
        super(ConfigFileHelper, self).__init__(file_path)


    def add_key_value_pair(self, config_key, config_value):
        file_was_updated = False
        if self.can_be_accessed():
            key_was_updated = False
            key_value_pair = '%s="%s"\n' % (config_key, config_value)
            file_lines = []
            duplicated_keys = []

            with open(self.file_path, 'r') as conf_file:
                file_lines = conf_file.readlines()
                for i, line in enumerate(file_lines):
                    if line.strip().startswith(config_key):
                        if not key_was_updated:
                            file_lines.insert(i, key_value_pair) # Update current value.
                            key_was_updated = True
                        else:
                            duplicated_keys.append(i) # Keep track of any duplicated key to remove later on.

                if not key_was_updated:
                    file_lines.append(key_value_pair) # Create a new entry.

            with open(self.file_path, 'w') as conf_file:
                conf_file.write(''.join(line for i, line in enumerate(file_lines) if i not in duplicated_keys))

            file_was_updated = True

        return file_was_updated
