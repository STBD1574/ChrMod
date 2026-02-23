# -*- coding: utf-8 -*-

from ...pyimport import Module, builtins
from ..registry import Command
from ...api.client import DisplayClientMessage

os       = Module('os')
fop      = Module('fop')
_utility = Module('_utility')
compile_ = builtins()['compile']

# ['__doc__', '__name__', '__package__', 'find_file', 'get_file', 'get_new_modules', 'new_module', 'pyerr_print', 'record_new_modules']

class Scripts(Command):
    def __init__(self):
        Command.__init__(self, 'scripts', '执行Python脚本， 在chrmod/scripts目录下。', '.scripts <script>', set())

        self.path = os.path.abspath(os.getcwd())

    def Execute(self, args): # type: (list[str]) -> bool
        if len(args) < 1:
            return False
        
        try:
            _utility.switchAnimation(0)
            with open('./chrmod/scripts/{}'.format(args[0]), 'r') as file:
                fop.new_module('', compile_(file.read(), '<script>', 'exec'), [self.path])
                DisplayClientMessage('§cC§eh§ar§bMod §7>§r 加载脚本: {}'.format(args[0]))
                
        except IOError:
            DisplayClientMessage('§cC§eh§ar§bMod §7>§r 文件 {} 不存在!'.format(args[0]))