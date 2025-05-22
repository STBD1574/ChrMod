# -*- coding: utf-8 -*-

from ..command import Command
from ..parameter import CommandParameter
from ..parameter import ParameterTypes
from ..command_argument import CommandArgument
import _utility # type: ignore
import fop      # type: ignore
import sys
import os

class ScriptsCommand(Command):
    def __init__(self):
        super(ScriptsCommand, self).__init__("scripts", "Run python script in minecraft game.", [ ])
        self.path = os.path.abspath(os.getcwd())

        self.add_parameter(CommandParameter("script", "The script file path.", True, ParameterTypes.STRING, []))
        self.add_parameter(CommandParameter("args", "The arguments for the script.", False, ParameterTypes.STRING, []))
        self.set_variable_args(True)

    def execute(self, args):
        # type: (CommandArgument) -> bool
        if len(args) < 1: 
            return False
        
        with open(args[0], "r") as f:
            code = compile("__args__ = %r\n" % (args[1:],) + f.read(), "<mc script>", "exec")

        fop.new_module("", code, sys.path)

        return True