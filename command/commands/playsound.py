# -*- coding: utf-8 -*-

from collections import defaultdict
from ...pyimport import Module
from ..registry import Command
from ...api import client, sound, entity
from ...lib import pynbs

os = Module('os')

class PlaySound(Command):
    def __init__(self):
        Command.__init__(self, 'playsound', '向全体玩家播放音效。', '.platform <soundfile>', set())

        self.tick = 0
        self.timer = None

    def Execute(self, args):
        if len(args) < 1:
            return client.DisplayClientMessage('§cC§eh§ar§bMod §7>§r 参数错误!') is None
        
        try:
            if self.timer:
                client.CancelTimer(self.timer)

            file = pynbs.read(unicode(args[0]))  # type: ignore
            file_notes = defaultdict(list)

            for tick, chord in file:
                file_notes[tick] += chord


            self.tick = 0
            self.timer = client.AddRepeatedTimer(1 / file.header.tempo, self.PlaySound, file, file_notes)

            client.DisplayClientMessage('§cC§eh§ar§bMod §7>§r 正在播放文件: {}'.format(os.path.basename(args[0])))
        except Exception as e:
            return client.DisplayClientMessage('§cC§eh§ar§bMod §7>§r 读取音效文件失败! {}'.format(e)) is None

        return True
    
    def PlaySound(self, file, file_notes): 
        # type: (pynbs.File, dict[int, pynbs.Note]) -> None
        try:
            self.tick += 1
            if self.tick > file.header.song_length:
                client.CancelTimer(self.timer)
                return

            for playerId in client.GetPlayerList():
                for note in file_notes[self.tick]:
                    position = entity.GetPosition(playerId)
                    if position is None:
                        continue

                    key = 81

                    instrument = {0: 23, 1: 4, 2: 6, 3: 2, 4: '??', 5: '??', 6: '??', 7: 5, 8: 7}.get(note.instrument, note.instrument)

                    if instrument == '??':
                        instrument = 23

                    sound.PlaySystemSound(key, position, (instrument << 8) | (note.key - 33), 319, False, True)
            
        except Exception as e:
            client.CancelTimer(self.timer)
            client.DisplayClientMessage('§cC§eh§ar§bMod §7>§r 音效播放失败! {}'.format(e))