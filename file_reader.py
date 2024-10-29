# file reader for TXR3 text files

import os
import struct


# defined structs
def rival_struct(file):
    rival_data = {
        'team_id': file.read_uint16(),
        'rival_id': file.read_uint16(),
        'unk1': file.read_uint16(),
        'nickname_1': file.read(0x12),
        'nickname_2': file.read(0x10),
        'data': file.read(0xac)
    }
    return rival_data


def rival_text_struct(file):
    rival_text = {
        'name': file.read(0x23),
        'job': file.read(0x3d),
        'career': file.read(0x0b),
        'motto': file.read(0x51),
        'p2_line1': file.read(0x51),
        'p2_line2': file.read(0x51),
        'p2_line3': file.read(0x51),
        'p2_line4': file.read(0x51),
        'p2_line5': file.read(0x51),
        'p3_line1': file.read(0x51),
        'p3_line2': file.read(0x51),
        'p3_line3': file.read(0x51),
        'p3_line4': file.read(0x51),
        'p3_line5': file.read(0x51),
    }
    return rival_text


def team_text_struct(file):
    team = {
        'team_name': file.read(0x29),
        'line1': file.read(0x33),
        'line2': file.read(0x33),
        'line3': file.read(0x33),
        'line4': file.read(0x33),
        'line5': file.read(0x33),
        'line6': file.read(0x33),
        'line7': file.read(0x33),
        'line8': file.read(0x33),
        'line9': file.read(0x33),
    }
    return team


def car_text_struct(file):
    car = {
        'brand': file.read(0x14),
        'model': file.read(0x20),
        'chassis': file.read(0x0c),
        'spec': file.read(0x28),
        'drivetrain': file.read_uint32(),
        'weight': file.read_uint32(),
        'displacement': file.read_uint32(),
        'rotor_count': file.read_uint32(),  # for rotary engines
        'engine_type': file.read_uint32(),
        'power': file.read_uint32()
    }
    return car


def scrolling_text(file, size):
    text = None
    if size == 0:
        text = file.read(0x709)
    elif size == 1:
        text = file.read(0x321)
    elif size == 2:
        text = file.read(0x1f5)
    elif size == 3:
        text = file.read(0x12d)
    elif size == 4:
        text = file.read(0x51)
    elif size == 5:
        text = file.read(0x21)

    return text


def bad_text(file):
    bad = {
        'val': file.read_uint16(),
        'name': file.read(0x12)
    }
    return bad


# class for reading binary files, little-endian
class FileReader:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'r+b')
        self.file.seek(0, os.SEEK_END)
        self.file_size = self.file.tell()
        self.file.seek(0, os.SEEK_SET)

    def read(self, size):
        return self.file.read(size)

    def write_n_bytes(self, data, n):
        data = data.ljust(n, b'\x00')
        self.file.write(struct.pack('<' + 'B' * n, *data))

    def read_int8(self):
        return struct.unpack('<b', self.file.read(1))[0]

    def read_uint8(self):
        return struct.unpack('<B', self.file.read(1))[0]

    def read_int16(self):
        return struct.unpack('<h', self.file.read(2))[0]

    def read_uint16(self):
        return struct.unpack('<H', self.file.read(2))[0]

    def read_int32(self):
        return struct.unpack('<i', self.file.read(4))[0]

    def read_uint32(self):
        return struct.unpack('<I', self.file.read(4))[0]

    def read_int64(self):
        return struct.unpack('<q', self.file.read(8))[0]

    def read_uint64(self):
        return struct.unpack('<Q', self.file.read(8))[0]

    def read_float(self):
        return struct.unpack('<f', self.file.read(4))[0]

    def read_double(self):
        return struct.unpack('<d', self.file.read(8))[0]

    def seek(self, offset, whence=os.SEEK_SET):
        self.file.seek(offset, whence)

    def close(self):
        self.file.close()

    def __del__(self):
        self.close()


# class for unpacking and repacking .dat archives
class DatFile:
    def __init__(self, filename):
        self.file = FileReader(filename)
        self.num_entries = self.file.read_uint32()
        self.entries = []
        for i in range(self.num_entries):
            offset = self.file.read_uint32()
            self.entries.append(offset)
        self.entries.append(self.file.file_size)  # add the end of the file as the last offset

    def get_entry(self, index):
        entry = self.entries[index]
        next_entry = self.entries[index + 1]
        size = next_entry - entry
        self.file.seek(entry)
        return self.file.read(size)

    def get_all_entries(self):
        entries = []
        for i in range(self.num_entries):
            entries.append(self.get_entry(i))
        return entries

    def close(self):
        self.file.close()

    def __del__(self):
        self.close()


# class for reading data from 26899.dat (scrolling text, b.a.d. names, car models, rival structs)
# 26899/0005 - scrolling text
# 26899/0009 - b.a.d. names 1
# 26899/0010 - b.a.d. names 2
# 26899/0011 - car models
# 26899/0012 - tokyo rivals struct
# 26899/0013 - nagoya rivals struct
# 26899/0014 - osaka rivals struct
class Dat26899:
    def __init__(self, filename):
        self.dat = DatFile(filename)
        self.file = self.dat.file

    def get_scrolling_text(self, car_only=False):
        self.file.seek(self.dat.entries[5])
        car_text = []
        for i in range(116):
            text = scrolling_text(self.file, 0)
            car_text.append(text)

        if car_only:
            return car_text

        tune_text = []
        for i in range(87):
            text = scrolling_text(self.file, 2)
            tune_text.append(text)

        setup_text = []
        for i in range(11):
            text = scrolling_text(self.file, 1)
            setup_text.append(text)

        parts_text = []
        for i in range(4):
            text = scrolling_text(self.file, 3)
            parts_text.append(text)

        setup2_text = []
        for i in range(6):
            text = scrolling_text(self.file, 1)
            setup2_text.append(text)

        menu_text = []
        for i in range(181):
            text = scrolling_text(self.file, 3)
            menu_text.append(text)

        menu2_text = []
        for i in range(29):
            text = scrolling_text(self.file, 4)
            menu2_text.append(text)

        button_text = []
        for i in range(33):
            text = scrolling_text(self.file, 5)
            button_text.append(text)

        return tune_text + setup_text + parts_text + setup2_text + menu_text + menu2_text + button_text

    def get_bad_names(self, index):
        if index > 1:
            return None
        self.file.seek(self.dat.entries[9 + index])
        bad_names = []
        for i in range(180):
            bad_name = bad_text(self.file)
            bad_names.append(bad_name)
        return bad_names

    def get_car_models(self):
        self.file.seek(self.dat.entries[11])
        car_models = []
        for i in range(119):
            car_model = car_text_struct(self.file)
            car_models.append(car_model)
        return car_models

    def get_tokyo_rivals(self):
        self.file.seek(self.dat.entries[12])
        tokyo_rivals = []
        for i in range(310):
            tokyo_rival = rival_struct(self.file)
            tokyo_rivals.append(tokyo_rival)
        return tokyo_rivals

    def get_nagoya_rivals(self):
        self.file.seek(self.dat.entries[13])
        nagoya_rivals = []
        for i in range(130):
            nagoya_rival = rival_struct(self.file)
            nagoya_rivals.append(nagoya_rival)
        return nagoya_rivals

    def get_osaka_rivals(self):
        self.file.seek(self.dat.entries[14])
        osaka_rivals = []
        for i in range(160):
            osaka_rival = rival_struct(self.file)
            osaka_rivals.append(osaka_rival)
        return osaka_rivals

    def save_rivals(self, region, rivals: rival_struct):
        if region == 0:
            self.file.seek(self.dat.entries[12])
        elif region == 1:
            self.file.seek(self.dat.entries[14])
        elif region == 2:
            self.file.seek(self.dat.entries[13])

        for rival in rivals:
            self.file.seek(0x2 * 3, os.SEEK_CUR)
            self.file.write_n_bytes(rival['nickname_1'], 0x12)
            self.file.write_n_bytes(rival['nickname_2'], 0x10)
            self.file.seek(0xac, os.SEEK_CUR)

    def save_car_models(self, car_models, car_descriptions):
        self.file.seek(self.dat.entries[11])
        for car in car_models:
            self.file.write_n_bytes(car['brand'], 0x14)
            self.file.write_n_bytes(car['model'], 0x20)
            self.file.write_n_bytes(car['chassis'], 0x0c)
            self.file.write_n_bytes(car['spec'], 0x28)
            self.file.seek(0x4 * 6, os.SEEK_CUR)

        self.file.seek(self.dat.entries[5])
        for car in car_descriptions:
            self.file.write_n_bytes(car, 0x709)

    def save_scroll_text(self, text):
        self.file.seek(self.dat.entries[5])
        self.file.seek(0x709 * 116, os.SEEK_CUR)
        for i in text[:87]:
            self.file.write_n_bytes(i, 0x1f5)
        for i in text[87:98]:
            self.file.write_n_bytes(i, 0x321)
        for i in text[98:102]:
            self.file.write_n_bytes(i, 0x12d)
        for i in text[102:108]:
            self.file.write_n_bytes(i, 0x321)
        for i in text[108:289]:
            self.file.write_n_bytes(i, 0x12d)
        for i in text[289:318]:
            self.file.write_n_bytes(i, 0x51)
        for i in text[318:351]:
            self.file.write_n_bytes(i, 0x21)

    def save_bad_names(self, index, bad_names):
        if index > 1:
            return
        self.file.seek(self.dat.entries[9 + index])
        for bad in bad_names:
            self.file.seek(0x2, os.SEEK_CUR)
            self.file.write_n_bytes(bad['name'], 0x12)
    

# class for reading data from 26900.dat (team profiles, rival profiles)
# 26900/0000 - team profiles
# 26900/0001 - tokyo rivals profiles
# 26900/0002 - osaka rivals profiles
# 26900/0003 - nagoya rivals profiles
class Dat26900:
    def __init__(self, filename):
        self.dat = DatFile(filename)
        self.file = self.dat.file

    def get_team_profiles(self):
        self.file.seek(self.dat.entries[0])
        teams = []
        for i in range(76):
            team = team_text_struct(self.file)
            teams.append(team)
        return teams

    def get_tokyo_rivals(self):
        self.file.seek(self.dat.entries[1])
        tokyo_rivals = []
        for i in range(310):
            tokyo_rival = rival_text_struct(self.file)
            tokyo_rivals.append(tokyo_rival)
        return tokyo_rivals

    def get_osaka_rivals(self):
        self.file.seek(self.dat.entries[2])
        osaka_rivals = []
        for i in range(160):
            osaka_rival = rival_text_struct(self.file)
            osaka_rivals.append(osaka_rival)
        return osaka_rivals

    def get_nagoya_rivals(self):
        self.file.seek(self.dat.entries[3])
        nagoya_rivals = []
        for i in range(130):
            nagoya_rival = rival_text_struct(self.file)
            nagoya_rivals.append(nagoya_rival)
        return nagoya_rivals

    def save_rivals(self, region, rivals: rival_text_struct):
        self.file.seek(self.dat.entries[region + 1])
        for rival in rivals:
            self.file.write_n_bytes(rival['name'], 0x23)
            self.file.write_n_bytes(rival['job'], 0x3d)
            self.file.write_n_bytes(rival['career'], 0x0b)
            self.file.write_n_bytes(rival['motto'], 0x51)
            self.file.write_n_bytes(rival['p2_line1'], 0x51)
            self.file.write_n_bytes(rival['p2_line2'], 0x51)
            self.file.write_n_bytes(rival['p2_line3'], 0x51)
            self.file.write_n_bytes(rival['p2_line4'], 0x51)
            self.file.write_n_bytes(rival['p2_line5'], 0x51)
            self.file.write_n_bytes(rival['p3_line1'], 0x51)
            self.file.write_n_bytes(rival['p3_line2'], 0x51)
            self.file.write_n_bytes(rival['p3_line3'], 0x51)
            self.file.write_n_bytes(rival['p3_line4'], 0x51)
            self.file.write_n_bytes(rival['p3_line5'], 0x51)

    def save_teams(self, teams: team_text_struct):
        self.file.seek(self.dat.entries[0])
        for team in teams:
            self.file.write_n_bytes(team['team_name'], 0x29)
            self.file.write_n_bytes(team['line1'], 0x33)
            self.file.write_n_bytes(team['line2'], 0x33)
            self.file.write_n_bytes(team['line3'], 0x33)
            self.file.write_n_bytes(team['line4'], 0x33)
            self.file.write_n_bytes(team['line5'], 0x33)
            self.file.write_n_bytes(team['line6'], 0x33)
            self.file.write_n_bytes(team['line7'], 0x33)
            self.file.write_n_bytes(team['line8'], 0x33)
            self.file.write_n_bytes(team['line9'], 0x33)

