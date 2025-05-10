# -*- coding: utf-8 -*-

import _gui # type: ignore
from ..command import Command
from ..argument import CommandArgument
from ..registry import CommandRegistry
from ..parameter import CommandParameter
from ..parameter_type import ParameterType, ParameterTypes
from ...text.chat_color import ColorCode

class HelpCommand(Command):
    def __init__(self):
        super(HelpCommand, self).__init__("help", "Displays help information for commands", ["?"])

        self.add_parameter(CommandParameter("command_name", "The name of the command to display help for", False, ParameterType.STRING, None))
        
    def execute(self, args):
        # type: (CommandArgument) -> None
        if not args.has_argument(1):
            self.print_help()
            return
        
        command = CommandRegistry().get_command_by_name(args.get_argument(1, ParameterTypes.STRING))
        if command is None:
            ModGameInfo().display_client_message(ColorCode.RED + "Command not found: " + args.get_argument(1, ParameterTypes.STRING))

        self.print_command(command)
        
    @staticmethod
    def print_help():
        # type: () -> None
        ModGameInfo().display_client_message("Available commands:")

        for command in CommandRegistry().get_commands():
            ModGameInfo().display_client_message(ColorCode.GRAY + command.name + " - " + command.description)

    @staticmethod
    def print_parameter(command, parameter, parent_parameter):
        # type: (Command, CommandParameter, list[CommandParameter]) -> None
        if parameter.sub_parameters is not None:
            parent_parameter.append(parameter)

            for sub_parameter in parameter.sub_parameters:
                HelpCommand.print_parameter(sub_parameter, command, parent_parameter)
        else:
            ModGameInfo().display_client_message(ColorCode.GRAY + command.name + " "  + " ".join(parent_parameter))

    @staticmethod
    def print_command(command):
        # type: (Command) -> None
        _gui.set_left_corner_notify_msg("The usage of " + command.name + " command is:")

        for parameter in command.parameters:
            HelpCommand.print_parameter(parameter, [])

_command = HelpCommand()
