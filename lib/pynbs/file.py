__all__ = [
    "read",
    "new_file",
    "Parser",
    "Writer",
    "File",
    "Header",
    "Note",
    "Layer",
    "Instrument",
]

from struct import Struct

CURRENT_NBS_VERSION = 5

BYTE = Struct("<B")
SHORT = Struct("<H")
SSHORT = Struct("<h")
INT = Struct("<I")

class Instrument(object):
    def __init__(self, id, name, file, pitch=45, press_key=True):
        self.id = id                # type: int
        self.name = name            # type: str
        self.file = file            # type: str
        self.pitch = pitch          # type: int
        self.press_key = press_key  # type: bool


class Note(object):
    def __init__(self, tick, layer, instrument, key, velocity=100,
                 panning=0, pitch=0):
        self.tick = tick              # type: int
        self.layer = layer            # type: int
        self.instrument = instrument  # type: int
        self.key = key                # type: int
        self.velocity = velocity      # type: int
        self.panning = panning        # type: int
        self.pitch = pitch            # type: int


class Layer(object):
    def __init__(self, id, name="", lock=False, volume=100, panning=0):
        self.id = id            # type: int
        self.name = name        # type: str
        self.lock = lock        # type: bool
        self.volume = volume    # type: int
        self.panning = panning  # type: int
        


def read(filename):
    # type: (str) -> File
    with open(filename, "rb") as fileobj:
        return Parser(fileobj).read_file()


def new_file(**header):
    # type: (**dict) -> File
    return File(Header(**header), [], [Layer(0, "", False, 100, 0)], [])


class Header(object):
    def __init__(self, version=CURRENT_NBS_VERSION, default_instruments=16,
                 song_length=0, song_layers=0, song_name="", song_author="",
                 original_author="", description="", tempo=10.0,
                 auto_save=False, auto_save_duration=10, time_signature=4,
                 minutes_spent=0, left_clicks=0, right_clicks=0,
                 blocks_added=0, blocks_removed=0, song_origin="", loop=False,
                 max_loop_count=0, loop_start=0):
        self.version = version                          # type: int
        self.default_instruments = default_instruments  # type: int
        self.song_length = song_length                  # type: int
        self.song_layers = song_layers                  # type: int
        self.song_name = song_name                      # type: str
        self.song_author = song_author                  # type: str
        self.original_author = original_author          # type: str
        self.description = description                  # type: str
        self.tempo = tempo                              # type: float
        self.auto_save = auto_save                      # type: bool
        self.auto_save_duration = auto_save_duration    # type: int
        self.time_signature = time_signature            # type: int
        self.minutes_spent = minutes_spent              # type: int
        self.left_clicks = left_clicks                  # type: int
        self.right_clicks = right_clicks                # type: int
        self.blocks_added = blocks_added                # type: int
        self.blocks_removed = blocks_removed            # type: int
        self.song_origin = song_origin                  # type: str
        self.loop = loop                                # type: bool
        self.max_loop_count = max_loop_count            # type: int
        self.loop_start = loop_start                    # type: int


class File(object):
    def __init__(self, header, notes, layers, instruments):
        # type: (Header, list, list, list) -> None
        self.header = header            # type: Header
        self.notes = notes              # type: list[Note]
        self.layers = layers            # type: list[Layer]
        self.instruments = instruments  # type: list[Instrument]

    def update_header(self, version):
        self.header.version = version
        if self.notes:
            self.header.song_length = self.notes[-1].tick
        self.header.song_layers = len(self.layers)

    def save(self, filename, version=CURRENT_NBS_VERSION):
        self.update_header(version)  # type: None
        with open(filename, "wb") as fileobj:
            Writer(fileobj).encode_file(self, version)  # type: None

    def __iter__(self):
        # type: () -> iter
        if not self.notes:
            return
        chord = []
        current_tick = self.notes[0].tick  # type: int

        for note in sorted(self.notes, key=lambda n: n.tick):
            if note.tick == current_tick:
                chord.append(note)  # type: list
            else:
                chord.sort(key=lambda n: n.layer)  # type: list
                yield current_tick, chord  # type: None
                current_tick, chord = note.tick, [note]
        yield current_tick, chord  # type: None


class Parser(object):
    def __init__(self, fileobj):
        # type: (any) -> None
        self.fileobj = fileobj  

    def read_file(self):
        # type: () -> File
        header = self.parse_header()  # type: Header
        version = header.version      # type: int
        return File(
            header,
            list(self.parse_notes(version)),
            list(self.parse_layers(header.song_layers, version)),
            list(self.parse_instruments(version)),
        )

    def read_numeric(self, fmt):
        # type: (Struct) -> int
        return fmt.unpack(self.fileobj.read(fmt.size))[0]  # type: int

    def read_string(self):
        # type: () -> str
        length = self.read_numeric(INT)  # type: int
        try:
            return self.fileobj.read(length).decode("utf-8")  # type: str
        except UnicodeDecodeError:
            return ''

    def jump(self):
        # type: () -> iter
        value = -1
        while True:
            jump = self.read_numeric(SHORT)  # type: int
            if not jump:
                break
            value += jump
            yield value  # type: None

    def parse_header(self):
        # type: () -> Header
        song_length = self.read_numeric(SHORT)  # type: int
        if song_length == 0:
            version = self.read_numeric(BYTE)  # type: int
        else:
            version = 0

        return Header(
            version=version,
            default_instruments=self.read_numeric(BYTE) if version > 0 else 10,     # type: int
            song_length=self.read_numeric(SHORT) if version >= 3 else song_length,  # type: int
            song_layers=self.read_numeric(SHORT),                                   # type: int
            song_name=self.read_string(),                                           # type: str
            song_author=self.read_string(),                                         # type: str
            original_author=self.read_string(),                                     # type: str
            description=self.read_string(),                                         # type: str
            tempo=self.read_numeric(SHORT) / 100.0,                                 # type: float
            auto_save=self.read_numeric(BYTE) == 1,                                 # type: bool
            auto_save_duration=self.read_numeric(BYTE),                             # type: int
            time_signature=self.read_numeric(BYTE),                                 # type: int
            minutes_spent=self.read_numeric(INT),                                   # type: int
            left_clicks=self.read_numeric(INT),                                     # type: int
            right_clicks=self.read_numeric(INT),                                    # type: int
            blocks_added=self.read_numeric(INT),                                    # type: int
            blocks_removed=self.read_numeric(INT),                                  # type: int
            song_origin=self.read_string(),                                         # type: str
            loop=self.read_numeric(BYTE) == 1 if version >= 4 else False,           # type: bool
            max_loop_count=self.read_numeric(BYTE) if version >= 4 else 0,          # type: int
            loop_start=self.read_numeric(SHORT) if version >= 4 else 0,             # type: int
        )

    def parse_notes(self, version):
        # type: (int) -> iter
        for current_tick in self.jump():
            for current_layer in self.jump():
                instrument = self.read_numeric(BYTE)                            # type: int
                key = self.read_numeric(BYTE)                                   # type: int
                velocity = self.read_numeric(BYTE) if version >= 4 else 100     # type: int
                panning = self.read_numeric(BYTE) - 100 if version >= 4 else 0  # type: int
                pitch = self.read_numeric(SSHORT) if version >= 4 else 0        # type: int
                yield Note(
                    current_tick,
                    current_layer,
                    instrument,
                    key,
                    velocity,
                    panning,
                    pitch,
                )  # type: None

    def parse_layers(self, layers_count, version):
        # type: (int, int) -> iter
        for i in xrange(layers_count): # type: ignore
            name = self.read_string()                                       # type: str
            lock = self.read_numeric(BYTE) == 1 if version >= 4 else False  # type: bool
            volume = self.read_numeric(BYTE)                                # type: int
            panning = self.read_numeric(BYTE) - 100 if version >= 2 else 0  # type: int
            yield Layer(i, name, lock, volume, panning)  # type: None

    def parse_instruments(self, version):
        # type: (int) -> iter
        for i in xrange(self.read_numeric(BYTE)): # type: ignore
            name = self.read_string()                                # type: str
            sound_file = self.read_string()                          # type: str
            pitch = self.read_numeric(BYTE)                          # type: int
            press_key = self.read_numeric(BYTE) == 1                 # type: bool
            yield Instrument(i, name, sound_file, pitch, press_key)  # type: None


class Writer(object):
    def __init__(self, fileobj):
        # type: (any) -> None
        self.fileobj = fileobj  

    def encode_file(self, nbs_file, version):
        # type: (File, int) -> None
        self.write_header(nbs_file, version)       # type: None
        self.write_notes(nbs_file, version)        # type: None
        self.write_layers(nbs_file, version)       # type: None
        self.write_instruments(nbs_file, version)  # type: None

    def encode_numeric(self, fmt, value):
        # type: (Struct, int) -> None
        self.fileobj.write(fmt.pack(value))  # type: None

    def encode_string(self, value):
        # type: (str) -> None
        self.encode_numeric(INT, len(value))  # type: None
        try:
            self.fileobj.write(value.encode(encoding="utf-8"))  # type: None
        except UnicodeEncodeError:
            pass

    def write_header(self, nbs_file, version):
        # type: (File, int) -> None
        header = nbs_file.header  # type: Header

        if version > 0:
            self.encode_numeric(SHORT, 0)                          # type: None
            self.encode_numeric(BYTE, version)                     # type: None
            self.encode_numeric(BYTE, header.default_instruments)  # type: None
        else:
            self.encode_numeric(SHORT, header.song_length)  # type: None
        if version >= 3:
            self.encode_numeric(SHORT, header.song_length)  # type: None
        self.encode_numeric(SHORT, header.song_layers)      # type: None
        self.encode_string(header.song_name)                # type: None
        self.encode_string(header.song_author)              # type: None
        self.encode_string(header.original_author)          # type: None
        self.encode_string(header.description)              # type: None

        self.encode_numeric(SHORT, int(header.tempo * 100))   # type: None
        self.encode_numeric(BYTE, int(header.auto_save))      # type: None
        self.encode_numeric(BYTE, header.auto_save_duration)  # type: None
        self.encode_numeric(BYTE, header.time_signature)      # type: None

        self.encode_numeric(INT, header.minutes_spent)   # type: None
        self.encode_numeric(INT, header.left_clicks)     # type: None
        self.encode_numeric(INT, header.right_clicks)    # type: None
        self.encode_numeric(INT, header.blocks_added)    # type: None
        self.encode_numeric(INT, header.blocks_removed)  # type: None
        self.encode_string(header.song_origin)           # type: None

        if version >= 4:
            self.encode_numeric(BYTE, int(header.loop))       # type: None
            self.encode_numeric(BYTE, header.max_loop_count)  # type: None
            self.encode_numeric(SHORT, header.loop_start)     # type: None

    def write_notes(self, nbs_file, version):
        # type: (File, int) -> None
        current_tick = -1  # type: int

        for tick, chord in nbs_file:  
            self.encode_numeric(SHORT, tick - current_tick)  # type: None
            current_tick = tick  # type: int
            current_layer = -1   # type: int

            for note in chord:  
                self.encode_numeric(SHORT, note.layer - current_layer)  # type: None
                current_layer = note.layer                  # type: int
                self.encode_numeric(BYTE, note.instrument)  # type: None
                self.encode_numeric(BYTE, note.key)         # type: None
                if version >= 4:
                    self.encode_numeric(BYTE, note.velocity)       # type: None
                    self.encode_numeric(BYTE, note.panning + 100)  # type: None
                    self.encode_numeric(SSHORT, note.pitch)        # type: None

            self.encode_numeric(SHORT, 0)  # type: None
        self.encode_numeric(SHORT, 0)  # type: None

    def write_layers(self, nbs_file, version):
        # type: (File, int) -> None
        for layer in nbs_file.layers:  
            self.encode_string(layer.name)  # type: None
            if version >= 4:
                self.encode_numeric(BYTE, int(layer.lock))  # type: None
            self.encode_numeric(BYTE, layer.volume)         # type: None
            if version >= 2:
                self.encode_numeric(BYTE, layer.panning + 100)  # type: None

    def write_instruments(self, nbs_file, version):
        # type: (File, int) -> None
        self.encode_numeric(BYTE, len(nbs_file.instruments))  # type: None
        for instrument in nbs_file.instruments:
            self.encode_string(instrument.name)                   # type: None
            self.encode_string(instrument.file)                   # type: None
            self.encode_numeric(BYTE, instrument.pitch)           # type: None
            self.encode_numeric(BYTE, int(instrument.press_key))  # type: None
