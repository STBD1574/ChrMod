# -*- coding: utf-8 -*-
from ChrMod.Command.CommandManager import Command
import ChrMod.execute as execute
import _utility

class Execute(Command):
    def __init__(self):
        Command.__init__(self, "execute", "运行指定的文件或Python代码 (\\n为换行)。", ".execute <file> 或 .execute <pycode>", [])

    def Execute(self, label, args):
        _utility.switchAnimation(0)
        if len(args) > 0:
            if not execute.ExecuteFile(args[0]):
                cmdLine = ""
                for i in args:
                    cmdLine += i + " "
                execute.ExecutePython(cmdLine.replace("\\\\n", "//n").replace("\\n", "\n").replace("//n", "\\n"))
        else:
            execute.ExecuteFile("exec.py")
        return True