#!/usr/bin/env python3
import os
import shutil
import subprocess
import argparse

"""
Static helpers
"""


def get_all_files(directory):
    for path, subdirs, files in os.walk(directory):
        for name in sorted(files):
            rel_directory = os.path.relpath(path, directory)
            yield os.path.join(rel_directory, name)


def git_diff(file1, file2):
    """
    Returns True if the files are identical
    """

    diff = subprocess.Popen(['git', 'diff', '--no-index', file1, file2],
                            stdout=subprocess.PIPE)

    try:
        result = diff.communicate()[0].decode('UTF-8')
        return result.strip() == ""
    except Exception:
        print("WARNING! Could not call git diff")
        return False


def confirm(text):
    answer = input('%s [Y/n]' % text)
    return (answer != 'n' and answer != 'N'
            and answer != 'No' and answer != 'no')


"""
Classes
"""


class File:
    """
    Represents one file of the active configuration, e. g. ~/.vimrc.
    This may be associated to many different nodes (i. e. alternatives)
    """
    def __init__(self, rel_path, path):
        self.rel_path = rel_path
        self.path = path
        self.nodes = []

    def create_node(self, layer):
        for p in self.nodes:
            if p.layer == layer:
                return p

        p = Node(self, layer)
        self.nodes += [p]
        return p


class Files:
    """
    Container for all Files
    """
    def __init__(self):
        self.files = []
        self.configuration_root = os.path.dirname(os.path.realpath(__file__))
        self.root = os.environ['HOME']

    def get(self, rel_path):
        rel_path = os.path.normpath(rel_path)
        for f in self.files:
            if f.rel_path == rel_path:
                return f

        f = File(rel_path, os.path.join(self.root, rel_path))
        self.files += [f]
        return f

    def detect_broken_symlinks(self):
        def test_dir(directory):
            find = subprocess.Popen(['find', directory, '-type', 'l',
                                     '-exec', 'test', '!', '-e', '{}', ';',
                                     '-print'],
                                    stdout=subprocess.PIPE)
            try:
                result = find.communicate()[0].decode('UTF-8')
                return result.split()
            except Exception:
                print("WARNING! Could not call find")
                return []

        directories = {os.path.dirname(f.path) for f in self.files}

        """
        Exclude $HOME
        """
        if self.root in directories:
            directories.remove(self.root)

        for d in directories:
            for f in test_dir(d):
                yield f


class Node:
    """
    The association between a File and a Layer

    Status:
        N => Target file is not present
        O => Target file is owned by another layer
        S => Correctly symlinked
        C => Present and identical
        ! => Present and differs (can only happen for all Nodes
                linked to one File)

    Commands:
        merge:      SCN -> S
        unmerge:    SCN -> N
        force_out:  !   -> S        overwriting changes in target
        force_in:   !   -> S        overwriting changes in node

    Notice that the state 'O' needs to be resolved in the owning layer.
    All methods will raise an Exception when called on 'O'
    """

    def __init__(self, file_, layer):
        self.file = file_
        self.layer = layer
        self.rel_path = file_.rel_path
        self.path = os.path.join(layer.node_root, file_.rel_path)

    def get_status(self):
        """
        First case: File does not exist
        """
        if not os.path.isfile(self.file.path):
            return 'N'

        """
        Second case: We are symlinked
        """
        symlink = None
        try:
            symlink = os.readlink(self.file.path)
        except Exception:
            pass

        if (symlink is not None and
                os.path.normpath(symlink) ==
                os.path.normpath(self.path)):
            return 'S'

        """
        Third case: File is identical => Claim ownership
        """
        if git_diff(self.path, self.file.path):
            return 'C'

        """
        Fourth case: File present and differs. If another node
        claims ownership, we acknowledge (O), else move to !
        """
        for n in self.file.nodes:
            if n != self and n.get_status() in ['C', 'S']:
                return 'O'

        return '!'

    def unmerge(self):
        status = self.get_status()

        """
        Safety checks
        """
        if status not in ['C', 'S', 'N']:
            raise Exception("Not supported")

        if status == 'N':
            return

        print('Removing %s' % self.file.path)
        os.remove(self.file.path)

    def merge(self):
        status = self.get_status()

        """
        Safety checks
        """
        if status not in ['C', 'S', 'N']:
            raise Exception("Not supported")

        if status == 'S':
            return

        self.unmerge()

        if status == 'N':
            os.makedirs(os.path.dirname(self.file.path), exist_ok=True)

        print('Symlinking %s -> %s' % (self.file.path, self.path))
        os.symlink(self.path, self.file.path)

    def force_out(self):
        status = self.get_status()

        """
        Safety checks
        """
        if status != '!':
            raise Exception("Not supported")

        print('Warning! Overwriting changes in %s' % self.file.path)
        if(confirm('Proceed?')):
            os.remove(self.file.path)
            self.merge()

    def force_in(self):
        status = self.get_status()

        """
        Safety checks
        """
        if status != '!':
            raise Exception("Not supported")

        print('Warning! Overwriting changes in %s' % self.path)
        if(confirm('Proceed?')):
            symlink = None
            try:
                symlink = os.path.readlink(self.file.path)
            except Exception:
                pass

            os.remove(self.package)
            if symlink is not None:
                shutil.copyfile(symlink, self.path)
            else:
                shutil.copyfile(self.file.path, self.path)

    def print_detailed(self):
        print("\t[%s] %s" % (self.get_status(), self.rel_path))


class Layer:
    """
    Configuration Unit: A bunch of files grouped together

    Status:
        N => Not merged, maybe same files but different content.
        O => Contains files owned by other layers. Can't be merged.
        C => Merged, but not all files are symlinked.
        S => Merged, all files are symlinked.

    Commands:
        merge:      SCN -> S
        unmerge:    SCN -> N

    O needs to be resolved in the conflicting layer
    """
    def __init__(self, path, files):
        self.path = path
        self.node_root = os.path.join(self.path, 'home')
        self.name = os.path.basename(os.path.normpath(path))

        self.nodes = [files.get(f).create_node(self) for f in
                      get_all_files(self.node_root)]

        self.merge_hooks = [os.path.join(self.path, 'merge', f) for f in
                            get_all_files(
                                os.path.join(self.path, 'merge'))]
        self.unmerge_hooks = [os.path.join(self.path, 'unmerge', f) for f in
                              get_all_files(
                                  os.path.join(self.path, 'unmerge'))]

    def get_status(self):
        status = 'S'
        for f in self.nodes:
            s = f.get_status()
            if s == 'N':
                return 'N'

            elif s == '!':
                return 'N'

            elif s == 'O':
                return 'O'

            elif s == 'S':
                continue

            elif s == 'C':
                status = 'C'
                continue

            else:
                raise Exception("Unexpected status")

        return status

    def merge(self):
        status = self.get_status()

        """
        Safety checks
        """
        if status not in ['C', 'S', 'N']:
            raise Exception("Not supported")

        if status == 'S':
            return

        print("Merging %s..." % self.name)
        for f in self.nodes:
            f.merge()

        for f in self.merge_hooks:
            print("Executing hook %s..." % f)
            subprocess.call(f)

    def unmerge(self):
        status = self.get_status()

        """
        Safety checks
        """
        if status not in ['C', 'S', 'N']:
            raise Exception("Not supported")

        if status == 'N':
            return

        print("Unmerging %s..." % self.name)
        for f in self.nodes:
            f.unmerge()

    def print_detailed(self):
        print("---------------------")
        print("[%s] %s" % (self.get_status(), self.name))
        for f in self.nodes:
            f.print_detailed()


if __name__ == '__main__':
    excludes = ['.git']

    """
    Load data
    """
    files = Files()
    layers = []

    for f in next(os.walk(files.configuration_root))[1]:
        if f not in excludes:
            layers += [Layer(os.path.join(files.configuration_root, f), files)]

    def handle_status(args):
        for l in layers:
            l.print_detailed()

    def handle_doctor(args):
        for l in layers:
            if l.get_status() == 'C':
                l.convert_to_symlink()

        broken_symlinks = list(files.detect_broken_symlinks())
        if len(broken_symlinks) > 0:
            print("Found %d broken symlinks:" % len(broken_symlinks))

            for f in broken_symlinks:
                print("\t%s" % f)

            if confirm('Delete?'):
                for f in broken_symlinks:
                    os.remove(f)




    def handle_merge(args):
        layer = None
        for l in layers:
            if l.name == args.layer:
                layer = l
                break

        if layer is None:
            print("Layer not found: %s" % args.layer)
        else:
            layer.merge()

    def handle_unmerge(args):
        layer = None
        for l in layers:
            if l.name == args.layer:
                layer = l
                break

        if layer is None:
            print("Layer not found: %s" % args.layer)
        else:
            layer.unmerge()

    """
    Parse command line
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    status_parser = subparsers.add_parser('status')
    doctor_parser = subparsers.add_parser('doctor')
    merge_parser = subparsers.add_parser('merge')
    unmerge_parser = subparsers.add_parser('unmerge')

    status_parser.set_defaults(func=handle_status)
    doctor_parser.set_defaults(func=handle_doctor)
    merge_parser.set_defaults(func=handle_merge)
    unmerge_parser.set_defaults(func=handle_unmerge)

    merge_parser.add_argument('layer')
    unmerge_parser.add_argument('layer')

    """
    Main
    """
    args = parser.parse_args()
    # try:
    args.func(args)
    # except Exception:
    #     parser.print_help()

















