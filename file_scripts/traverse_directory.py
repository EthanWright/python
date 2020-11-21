class TraverseDirectory(object):

    def handle_dir(self, dir_name, directory, full_path):
        return True

    def handle_file(self, file_name, directory, full_path):
        return True

    def iterate_files_recursively(self, directory, lazy=False):
        if lazy:
            recursive_function = self.iterate_files_recursively_lazy
        else:
            recursive_function = self.iterate_files_recursively_normal

        # Check root dir and kick off recursive search
        if self.handle_dir('', directory, directory):
            recursive_function(directory)

    def iterate_files_recursively_normal(self, directory):

        for file_name in os.listdir(directory):
            full_path = os.path.join(directory, file_name)

            if os.path.isfile(full_path):
                self.handle_file(file_name, directory, full_path)

            elif os.path.isdir(full_path):
                if self.handle_dir(file_name, directory, full_path):
                    self.iterate_files_recursively_normal(full_path)

    def iterate_files_recursively_lazy(self, directory):
        found_dirs = []
        for file_name in os.listdir(directory):
            full_path = os.path.join(directory, file_name)

            if os.path.isfile(full_path):
                self.handle_file(file_name, directory, full_path)

            elif os.path.isdir(full_path):
                found_dirs.append(file_name)

        for dir_name in found_dirs:
            full_path = os.path.join(directory, dir_name)
            if self.handle_dir(dir_name, directory, full_path):
                self.iterate_files_recursively_lazy(full_path)

