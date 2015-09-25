# Copyright 2015, The Lvn Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import json
import os
import sys
import subprocess


class Branch(object):
    def __init__(self, name, json_object=None):
        self.name = name
        if json_object is None:
            self.patch_file = None
            return
        self.patch_file = json_object.get('patch_file')

    def ToJson(self):
        result = {}
        if self.patch_file is not None:
            result['patch_file'] = self.patch_file
        return result

    def Rename(self, patch_dir, name):
        self.name = name
        if self.patch_file is not None:
            new_patch_file = name + '.patch'
            os.rename(os.path.join(patch_dir, self.patch_file),
                      os.path.join(patch_dir, new_patch_file))
            self.patch_file = new_patch_file


class Lvn(object):
    def __init__(self, lvn_file=None):
        if lvn_file is None:
            self.current_branch = 'master-1'
            self.branches = {}
            self.branches[self.current_branch] = Branch(self.current_branch)
            return
        self.lvn_dir, _ = os.path.split(lvn_file)
        self.top_dir = os.path.abspath(os.path.join(self.lvn_dir, '..', '..'))
        with open(lvn_file, 'r') as lvn_json_file:
            json_obj = json.loads(lvn_json_file.read())
            self.current_branch = json_obj['current_branch']
            self.branches = {}
            for key, value in json_obj['branches'].iteritems():
                self.branches[key] = Branch(key, value)

    def Save(self, lvn_file=None):
        if lvn_file is None:
            lvn_file = os.path.join(self.lvn_dir, 'lvn.json')
        json_obj = {}
        json_obj['current_branch'] = self.current_branch
        branches = {}
        for key, branch in self.branches.iteritems():
            branches[key] = branch.ToJson()
        json_obj['branches'] = branches
        with open(lvn_file, 'w') as lvn_json_file:
            json.dump(json_obj, lvn_json_file)

    def RenameBranch(self, old_name, new_name):
        branch = self.branches[old_name]
        del self.branches[old_name]
        branch.Rename(self.lvn_dir, new_name)
        self.branches[new_name] = branch
        if self.current_branch == old_name:
            self.current_branch = new_name

    def SaveCurrentBranch(self):
        branch = self.branches[self.current_branch]
        if branch.patch_file is None:
            branch.patch_file = branch.name + '.patch'
        with open(os.path.join(self.lvn_dir, branch.patch_file), 'w') as patch_file:
            ret = subprocess.call(['svn', 'diff', self.top_dir], cwd=self.top_dir, stdout=patch_file)
        if ret != 0:
            raise Exception('svn diff failed')

    def Revert(self):
        p = subprocess.Popen(['svn', 'status'], cwd=self.top_dir, stdout=subprocess.PIPE)
        added = []
        for line in p.stdout:
            if line.startswith('A'):
                added.append(line[8:].strip())
        if p.wait() != 0:
            raise Exception('svn status failed')

        ret = subprocess.call(['svn', 'revert', '-R', self.top_dir], cwd=self.top_dir)
        if ret != 0:
            raise Exception('svn revert failed')

        for p in reversed(added):
            p = os.path.join(self.top_dir, p)
            try:
                if os.path.isdir(p):
                    sys.stderr.write('Removing dir %r\n' % p)
                    os.rmdir(p)
                else:
                    sys.stderr.write('Removing file %r\n' % p)
                    os.unlink(p)
            except OSError, e:
                sys.stderr.write(str(e) + '\n')

    def RestoreBranch(self):
        branch = self.branches[self.current_branch]
        if branch.patch_file is None:
            return
        patch_file_name = os.path.join(self.lvn_dir, branch.patch_file)
        ret = subprocess.call(['svn', 'patch', patch_file_name], cwd=self.top_dir)
        if ret != 0:
            raise Exception('svn apply failed')

    def Delete(self, branch_name):
        branch = self.branches[branch_name]
        del self.branches[branch_name]
        if branch.patch_file is not None:
            os.remove(os.path.join(self.lvn_dir, branch.patch_file))


def GetSvnDir(working_dir):
    while working_dir != ' ' and working_dir != '/':
        svn_dir = os.path.join(working_dir, '.svn')
        if os.path.isdir(svn_dir):
            return svn_dir
        working_dir, _ = os.path.split(working_dir)
    return None


def GetLvnDir(working_dir):
    svn_dir = GetSvnDir(working_dir)
    if svn_dir is not None:
        lvn_dir = os.path.join(svn_dir, 'lvn')
        if os.path.isdir(lvn_dir):
            return lvn_dir
    return None


def GetLvn(working_dir):
    svn_dir = GetSvnDir(working_dir)
    if svn_dir is None:
        print 'svn repository not found'
        return None
    lvn_dir = os.path.join(svn_dir, 'lvn')
    if not os.path.isdir(lvn_dir):
        print 'lvn is not initialized, run lvn init'
        return None
    lvn_file = os.path.join(lvn_dir, 'lvn.json')
    if not os.path.exists(lvn_file):
        print 'lvn is not initialized, run lvn init'
        return None
    return Lvn(lvn_file)
