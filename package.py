#!/usr/bin/env python3
import os
import shutil
import subprocess
import argparse
import filecmp
from enum import Enum

"""
Static helpers
"""


def get_all_files(directory, rel=True):
    for path, subdirs, files in os.walk(directory):
        for name in sorted(files):
            if rel:
                rel_directory = os.path.relpath(path, directory)
                yield os.path.join(rel_directory, name)
            else:
                yield os.path.join(path, name)


def collect_files(fs):
    for f in fs:
        if os.path.isfile(f):
            yield f
        else:
            yield from get_all_files(f, rel=False)


def confirm(text):
    answer = input('%s [Y/n] ' % text)
    return (answer != 'n' and answer != 'N'
            and answer != 'No' and answer != 'no')


def find_broken_symlinks(file_or_directory):
    find = subprocess.Popen(['find', file_or_directory, '-type', 'l',
                             '-exec', 'test', '!', '-e', '{}', ';',
                             '-print'],
                            stdout=subprocess.PIPE)
    try:
        result = find.communicate()[0].decode('UTF-8')
        return result.split()
    except Exception:
        print("WARNING! Could not call find")
        return []


def split_path(path):
    head, tail = os.path.split(path)
    components = []
    while len(tail) > 0:
        components.insert(0, tail)
        head, tail = os.path.split(head)
    return components


def find_bottom(layer, all_layers):
    """
    Pick all candidates, s.t. layer starts with <candidate>-
    """
    candidates = [l for l in all_layers if layer.startswith(l + '-')]

    """
    Find the one highest up in the hierarchy
    """
    while True:
        next_candidates = []
        for c in candidates:
            if find_bottom(c, candidates) is not None:
                next_candidates += [c]

        if len(next_candidates) == 0:
            if len(candidates) > 1:
                raise Exception("Something went wrong")
            return candidates[0] if len(candidates) > 0 else None

        candidates = next_candidates


def find_top(layer, all_layers):
    """
    Pick all that start with <layer>-
    """
    candidates = [l for l in all_layers if l.startswith(layer + '-')]

    """
    Exclude the ones that have a bottom within candidates
    """
    return [l for l in candidates if find_bottom(l, candidates) is None]


"""
Classes
"""


class File:
    """
    Represents a configuration file living in $HOME.
    This is the active configuration.
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

    def is_invalid(self):
        for n in self.nodes:
            if n.state() == NodeState.INVALID:
                return True

        return False

    def get_hardlinks(self):
        for n in self.nodes:
            if n.state() == NodeState.HARDLINKED:
                yield n


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

    def get_abs(self, abs_path):
        abs_path = os.path.normpath(abs_path)
        if abs_path.startswith(self.configuration_root):
            abs_path = os.path.relpath(abs_path, self.configuration_root)

            """
            Remove first two components, i. e. layername/home
            from path to get a relative path
            """
            try:
                rel_path = os.path.join(split_path(abs_path)[2:])
            except Exception:
                return None
            return self.get(rel_path)

        elif abs_path.startswith(self.root):
            rel_path = os.path.relpath(abs_path, self.root)
            return self.get(rel_path)

        else:
            return None


class NodeState(Enum):
    """
    This file is only present in the configuration layer, not
    in the actual file system
    """
    UNMERGED = 'U'

    """
    This file is only present in the actual configuration,
    not in the layer. Intermediate state during ingest and release.
    """
    INGESTING = 'I'

    """
    The file is symlinked to this node
    """
    SYMLINKED = 'M'

    """
    The file is identical with this node
    """
    HARDLINKED = 'H'

    """
    The file is owned by another node (either SYMLINKED or HARDLINKED)
    """
    BLOCKED = 'x'

    """
    The file is owned by a layer on top
    """
    SHADOWED = '-'

    """
    Present, but not identical and not owned by another node.
    Implies all nodes associated to this file are INVALID

    Blocks all layer operations.
    """
    INVALID = '!'


class Node:
    """
    Represents one option for a configuration file.
    Implements the association between File and Layer.
    If file is given by ~/path/to/.conf, the node resides
    in dotfiles/layer/home/path/to/.conf

    Commands:
        unmerge:    UNMERGED, SYMLINKED             -> UNMERGED
        merge:      UNMERGED, SYMLINKED, HARDLINKED -> SYMLINKED
        ingest:     INGESTING                       -> SYMLINKED
        release:    SYMLINKED                       -> INGESTING
        force_out:  INVALID                         -> SYMLINKED
            overwriting changes in file
        force_out:  INVALID                         -> SYMLINKED
            overwriting changes in node
    """

    def __init__(self, file_, layer):
        self.file = file_
        self.layer = layer
        self.rel_path = file_.rel_path
        self.path = os.path.join(layer.node_root, file_.rel_path)

    def find_top(self):
        for layer in self.layer.top:
            for node in layer.nodes:
                if node.file == self.file:
                    yield node

    def find_bottom(self):
        if self.layer.bottom is not None:
            for node in self.layer.bottom.nodes:
                if node.file == self.file:
                    return node

        return None

    def print_detailed(self):
        print("\t[%s] %s" % (self.state().value, self.rel_path))

    def state(self):
        """
        Either file does not exist
        """
        if not os.path.isfile(self.file.path):
            return NodeState.UNMERGED

        if not os.path.isfile(self.path):
            return NodeState.INGESTING

        """
        We are symlinked
        """
        symlink = None
        try:
            symlink = os.readlink(self.file.path)
        except Exception:
            pass

        if (symlink is not None and
                os.path.normpath(symlink) ==
                os.path.normpath(self.path)):
            return NodeState.SYMLINKED

        """
        Layer on top claims ownership
        """
        for n in self.find_top():
            if n.state() in [NodeState.SHADOWED,
                             NodeState.SYMLINKED,
                             NodeState.HARDLINKED]:
                return NodeState.SHADOWED

        """
        File is identical => Claim ownership
        """
        if filecmp.cmp(self.path, self.file.path):
            return NodeState.HARDLINKED

        """
        File present and differs. If another node
        claims ownership, we acknowledge (BLOCKED),
        else move to INVALID
        """
        for n in self.file.nodes:
            if n != self and n.state() in [NodeState.SYMLINKED,
                                           NodeState.HARDLINKED]:
                return NodeState.BLOCKED

        return NodeState.INVALID

    def unmerge(self):
        state = self.state()

        """
        Safety checks
        """
        if state not in [NodeState.UNMERGED, NodeState.SYMLINKED]:
            raise Exception("Not allowed")

        if state == NodeState.UNMERGED:
            return

        print('Removing %s' % self.file.path)
        os.remove(self.file.path)

    def merge(self):
        state = self.state()

        """
        Safety checks
        """
        if state not in [NodeState.UNMERGED, NodeState.SYMLINKED,
                         NodeState.HARDLINKED]:
            raise Exception("Not allowed")

        if state == NodeState.SYMLINKED:
            return

        if state == NodeState.UNMERGED:
            os.makedirs(os.path.dirname(self.file.path), exist_ok=True)
        else:
            print('Removing %s' % self.file.path)
            os.remove(self.file.path)

        print('Symlinking %s -> %s' % (self.file.path, self.path))
        os.symlink(self.path, self.file.path)

    def ingest(self):
        """
        Safety checks
        """
        if self.state() != NodeState.INGESTING:
            raise Exception("Not allowed")

        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        shutil.copyfile(self.file.path, self.path)

        if self.state() != NodeState.HARDLINKED:
            raise Exception("Ingestion went wrong")

        self.merge()

    def release(self):
        """
        Safety checks
        """
        if self.state() != NodeState.SYMLINKED:
            raise Exception("Not allowed")

        os.remove(self.file.path)
        shutil.copyfile(self.path, self.file.path)

        if self.state() != NodeState.HARDLINKED:
            raise Exception("Release went wrong")

        os.remove(self.path)

        if self.state() != NodeState.INGESTING:
            raise Exception("Release went wrong")

    def force_out(self):
        """
        Safety checks
        """
        if self.state() != NodeState.INVALID:
            raise Exception("Not allowed")

        print('Warning! Overwriting changes in %s' % self.file.path)
        if(confirm('Proceed?')):
            os.remove(self.file.path)
            self.merge()

    def force_in(self):
        """
        Safety checks
        """
        if self.state() != NodeState.INVALID:
            raise Exception("Not allowed")

        print('Warning! Overwriting changes in %s' % self.path)
        if(confirm('Proceed?')):
            symlink = None
            try:
                symlink = os.path.readlink(self.file.path)
            except Exception:
                pass

            os.remove(self.path)
            if symlink is not None:
                shutil.copyfile(symlink, self.path)
            else:
                shutil.copyfile(self.file.path, self.path)


class LayerState(Enum):
    """
    All files are UNMERGED
    """
    UNMERGED = 'U'

    """
    All files are SYMLINKED
    """
    MERGED = 'M'

    """
    All files are either SYMLINKED or SHADOWED
    """
    SHADOWED = '-'

    """
    All other cases
    """
    INVALID = '!'


class Layer:
    """
    Represents a choice for a given subset of configuration files.
    Layers can be stacked on top of each other (i. e. nvim-dark is
    on top of nvim), meaning that nvim-dark requires nvim,
    but is allowed override parts of it.

    Commands:
        merge:  UNMERGED    -> MERGED
        unmerge: MERGED     -> UNMERGED
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
        self.top = []
        self.bottom = None

    def add_file(self, file_):
        self.nodes += [file_.create_node(self)]

    def link(self, all_layers):
        if self.bottom is not None:
            return

        top = find_top(self.name, [l.name for l in all_layers])
        self.top = [l for l in all_layers if l.name in top]

        bottom = find_bottom(self.name, [l.name for l in all_layers])
        self.bottom = [l for l in all_layers if l.name == bottom][0] \
            if bottom is not None else None

    def print_detailed(self):
        print("---------------------")
        print("[%s] %s" % (self.state().value, self.name))
        if self.bottom is not None:
            print("    -> %s" % self.bottom.name)
        for f in self.nodes:
            f.print_detailed()

    def state(self):
        states = {f.state() for f in self.nodes}

        if states == {NodeState.UNMERGED}:
            return LayerState.UNMERGED
        elif states == {NodeState.SYMLINKED}:
            return LayerState.MERGED
        elif states == {NodeState.SYMLINKED, NodeState.SHADOWED}:
            return LayerState.SHADOWED

        return LayerState.INVALID

    def merge(self):
        state = self.state()
        """
        Safety checks
        """
        if state not in [LayerState.UNMERGED, LayerState.MERGED]:
            raise Exception("Not allowed")

        if state == LayerState.MERGED:
            return

        if self.bottom is not None:
            self.bottom.merge()

        print("Merging %s..." % self.name)
        for f in self.nodes:
            f.merge()

        for f in self.merge_hooks:
            print("Executing hook %s..." % f)
            subprocess.call(f)

    def unmerge(self):
        state = self.state()

        """
        Safety checks
        """
        if state not in [LayerState.UNMERGED, LayerState.MERGED]:
            raise Exception("Not allowed")

        if state == LayerState.UNMERGED:
            return

        for layer in self.top:
            if layer.state() == LayerState.MERGED:
                layer.unmerge()

        print("Unmerging %s..." % self.name)
        for f in self.nodes:
            f.unmerge()


"""
Functions
"""


def setup(excludes):
    files = Files()
    layers = []

    for f in next(os.walk(files.configuration_root))[1]:
        if f not in excludes:
            layers += [Layer(os.path.join(files.configuration_root, f), files)]

    for layer in layers:
        layer.link(layers)

    return files, layers


def doctor_broken_symlinks(files_or_directories):
    broken_symlinks = []
    for f in files_or_directories:
        broken_symlinks += find_broken_symlinks(f)

    if len(broken_symlinks) > 0:
        print("Found %d broken symlinks:" % len(broken_symlinks))

        for f in broken_symlinks:
            print("\t%s" % f)

        if confirm('Delete?'):
            for f in broken_symlinks:
                os.remove(f)


def doctor(files, layers):
    """
    Detect broken symlinks and delete them.
    We do not keep track of crated symlinks, so this will never work perfectly.
    """
    directories = {os.path.dirname(f.path) for f in files.files}
    if files.root in directories:
        directories.remove(files.root)

    doctor_broken_symlinks(directories)

    """
    Helper
    """
    def choose_layer(layers):
        for i, n in enumerate(layers):
            print("---------- %d -----------" % i)
            n.layer.print_detailed()
        while True:
            pick = input("Pick? ")
            try:
                idx = int(pick)
            except Exception:
                continue

            if idx >= len(f.nodes):
                continue

            return idx

    """
    Fix HARDLINKED files
    """
    for f in files.files:
        hardlinks = list(f.get_hardlinks())
        if len(hardlinks) > 0:
            print("Hardlinked file: %s" % f.rel_path)
            if len(hardlinks) == 1:
                hardlinks[0].merge()
            else:
                idx = choose_layer([n.layer for n in hardlinks])
                hardlinks[idx].merge()

    """
    Fix invalid files
    """
    for f in files.files:
        if f.is_invalid():
            print("Invalid file: %s" % f.rel_path)
            node = None
            if len(f.nodes) == 1:
                node = f.nodes[0]
            else:
                idx = choose_layer([n.layer for n in f.nodes])
                node = f.nodes[idx]

            print("")
            node.layer.print_detailed()

            force_in = None
            while True:
                force_in = input("[I]ngest or [R]elease? ")
                print("'%s'" % force_in)
                if force_in not in 'IiRr':
                    continue
                force_in = force_in in ['I', 'i']
                break

            if force_in:
                node.force_in()
            else:
                node.force_out()


if __name__ == '__main__':
    excludes = ['.git',  'ignore']

    """
    Load data and ensure it is in a useful state
    """
    files, layers = setup(excludes)
    doctor(files, layers)

    """
    Setup parser
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    """
    Print summary of installed and available layers
    """
    def handle_status(args):
        for l in layers:
            l.print_detailed()

    status_parser = subparsers.add_parser('status')
    status_parser.set_defaults(func=handle_status)

    """
    Merge layer into actual configuration
    """
    def handle_merge(args):
        layer = None
        for l in layers:
            if l.name == args.layer:
                layer = l
                break

        if layer is None:
            print("Layer not found: %s" % args.layer)
            return

        additional_merges = []
        tmp = layer.bottom
        while tmp is not None:
            if tmp.state() != LayerState.MERGED:
                additional_merges += [tmp]

            tmp = tmp.bottom

        if len(additional_merges) > 0:
            print("This step requires merging of")
            for i, l in enumerate(additional_merges):
                for j in range(2 * i):
                    print(" ", end='')
                print("-> %s" % l.name)

            if not confirm("Confirm?"):
                return

        layer.merge()

    merge_parser = subparsers.add_parser('merge')
    merge_parser.set_defaults(func=handle_merge)
    merge_parser.add_argument('layer')

    """
    Remove layer from actual configuration
    """
    def handle_unmerge(args):
        layer = None
        for l in layers:
            if l.name == args.layer:
                layer = l
                break

        if layer is None:
            print("Layer not found: %s" % args.layer)
            return

        def collect(layer, additional_unmerges):
            for l in layer.top:
                if l.state() == LayerState.MERGED:
                    additional_unmerges += [l]
                    collect(l, additional_unmerges)
        additional_unmerges = []
        collect(layer, additional_unmerges)

        if len(additional_unmerges) > 0:
            print("This step requires unmerging of")
            for i, l in enumerate(additional_unmerges):
                for j in range(2 * i):
                    print(" ", end='')
                print("<- %s" % l.name)

            if not confirm("Confirm?"):
                return

        layer.unmerge()

    unmerge_parser = subparsers.add_parser('unmerge')
    unmerge_parser.set_defaults(func=handle_unmerge)
    unmerge_parser.add_argument('layer')

    """
    Check for broken symlinks in specific files/folders
    """
    def handle_doctor(args):
        doctor_broken_symlinks(args.files)

    doctor_parser = subparsers.add_parser('doctor')
    doctor_parser.set_defaults(func=handle_doctor)
    doctor_parser.add_argument('files', nargs='+')

    """
    Move actual configuration into existing/new layer
    """
    def handle_ingest(args):
        layer = None
        for l in layers:
            if l.name == args.layer:
                layer = l
                break

        new_layer = False
        if layer is None:
            layer = Layer(os.path.join(
                files.configuration_root, args.layer), [])
            new_layer = True

        new_nodes = []
        for f in collect_files(args.files):
            f = files.get_abs(f)
            if f is None:
                continue
            if len(f.nodes) > 0:
                continue

            layer.add_file(f)
            new_nodes += [layer.nodes[-1]]

        if len(new_nodes) == 0:
            print("Could not find any matching files.")
            return

        print("Ingesting...")
        for n in new_nodes:
            print("\t%s" % n.rel_path)
        print("...%d files into %slayer %s" %
              (len(new_nodes), "new " if new_layer else "", layer.name))

        if confirm("Confirm?"):
            for n in new_nodes:
                if n.state() != NodeState.INGESTING:
                    print("WARNING! Could not ingest %s" % n.rel_path)
                else:
                    n.ingest()

    ingest_parser = subparsers.add_parser('ingest')
    ingest_parser.set_defaults(func=handle_ingest)
    ingest_parser.add_argument('layer')
    ingest_parser.add_argument('files', nargs='+')

    """
    Move configuration form layer to outside no longer handling it
    """
    def handle_release(args):
        layer = None
        for l in layers:
            if l.name == args.layer:
                layer = l
                break

        if layer is None:
            print("Layer not found: %s" % args.layer)
            return

        nodes = []
        for f in collect_files(args.files):
            f = files.get_abs(f)
            if f is None:
                continue

            for n in f.nodes:
                if n.layer == layer:
                    nodes += [n]
                    break

        if len(nodes) == 0:
            print("Could not find any matching files.")
            return

        print("Releasing...")
        for n in nodes:
            print("\t%s" % n.rel_path)
        print("...%d files from layer %s" % (len(nodes), layer.name))

        if confirm("Confirm?"):
            for n in nodes:
                if n.state() != NodeState.SYMLINKED:
                    print("WARNING! Could not ingest %s" % n.rel_path)
                else:
                    n.release()

    release_parser = subparsers.add_parser('release')
    release_parser.set_defaults(func=handle_release)
    release_parser.add_argument('layer')
    release_parser.add_argument('files', nargs='+')

    """
    Main
    """
    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

















