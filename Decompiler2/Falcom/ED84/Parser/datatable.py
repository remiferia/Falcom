from Falcom.Common import *
from Falcom.ED83.Parser.datatable import *
from Falcom.ED83.Parser.datatable import createDataTable

class BGMTableData(TableDataEntry):
    ENTRY_NAME = 'bgm'
    DESCRIPTOR  = (
        ('id',      'H'),
        ('file',    'S'),
        ('word3',   'H'),
        ('float4',  'f'),
    )

class VoiceTableData(TableDataEntry):
    ENTRY_NAME = 'voice'
    DESCRIPTOR  = (
        ('id',      'W'),
        ('symbol',  'S'),
        ('file',    'S'),
        ('word4',   'H'),
        ('float5',  'f'),
        ('float6',  'f'),
        ('word7',   'H'),
        ('word8',   'H'),
        ('float9',  'f'),
        ('text',    'S'),
    )

class StatusTableData(TableDataEntry):
    ENTRY_NAME = 'status'
    DESCRIPTOR  = (
        ('algoFile',             'S'),
        ('model',                'S'),
        ('ani',                  'S'),
        ('float1',               'f'),
        ('float2',               'f'),
        ('float3',               'f'),
        ('float4',               'f'),
        ('float5',               'f'),
        ('float6',               'f'),
        ('float7',               'f'),
        ('short8',               'W'),
        ('short9',               'W'),
        ('byte10',               'B'),
        ('level',                'C'),
        ('hpBase',               'I'),
        ('hpFactor',             'f'),
        ('epMax',                'H'),
        ('epInit',               'H'),
        ('cpMax',                'H'),
        ('cpInit',               'H'),
        ('str',                  'I'),
        ('strFactor',            'f'),
        ('def_',                 'I'),
        ('defFactor',            'f'),
        ('ats',                  'I'),
        ('atsFactor',            'f'),
        ('adf',                  'I'),
        ('adfFactor',            'f'),
        ('dex',                  'H'),
        ('dexFactor',            'f'),
        ('agl',                  'H'),
        ('aglFactor',            'f'),
        ('evade',                'H'),
        ('spd',                  'H'),
        ('spdFactor',            'f'),
        ('mov',                  'H'),
        ('movFactor',            'f'),
        ('exp',                  'H'),
        ('expFactor',            'f'),
        ('brk',                  'H'),
        ('brkFactor',            'f'),
        ('efficacyEarth',        'C'),
        ('efficacyWater',        'C'),
        ('efficacyFire',         'C'),
        ('efficacyWind',         'C'),
        ('efficacyTime',         'C'),
        ('efficacySpace',        'C'),
        ('efficacyMirage',       'C'),
        ('efficacyPoison',       'C'),
        ('efficacySeal',         'C'),
        ('efficacyMute',         'C'),
        ('efficacyBlind',        'C'),
        ('efficacySleep',        'C'),
        ('efficacyBurn',         'C'),
        ('efficacyFreeze',       'C'),
        ('efficacyPetrify',      'C'),
        ('efficacyFaint',        'C'),
        ('efficacyConfuse',      'C'),
        ('efficacyCharm',        'C'),
        ('efficacyDeathblow',    'C'),
        ('efficacyNightmare',    'C'),
        ('efficacyATDelay',      'C'),
        ('efficacyVanish',       'C'),
        ('efficacySPDDown',      'C'),
        ('efficacySlash',        'H'),
        ('efficacyThurst',       'H'),
        ('efficacyPierce',       'H'),
        ('efficacyStrike',       'H'),
        ('sepithEarth',          'C'),
        ('sepithWater',          'C'),
        ('sepithFire',           'C'),
        ('sepithWind',           'C'),
        ('sepithTime',           'C'),
        ('sepithSpace',          'C'),
        ('sepithMirage',         'C'),
        ('sepithMass',           'C'),
        ('sepithEarthFactor',    'f'),
        ('sepithWaterFactor',    'f'),
        ('sepithFireFactor',     'f'),
        ('sepithWindFactor',     'f'),
        ('sepithTimeFactor',     'f'),
        ('sepithSpaceFactor',    'f'),
        ('sepithMirageFactor',   'f'),
        ('sepithMassFactor',     'f'),
        ('dropItemId1',          'W'),
        ('dropRate1',            'C'),
        ('dropItemId2',          'W'),
        ('dropRate2',            'C'),
        ('float11',              'f'),
        ('float12',              'f'),
        ('flags',                'S'),
        ('chrId',                'W'),
        ('name',                 'S'),
        ('description',          'S'),
    )

    FLAGS_TABLE = {
        'M':  0x00000001,
        'E':  0x00000002,
        'N':  0x00000004,
        'K':  0x00000008,
        'T':  0x00000010,
        'H':  0x00000020,
        'D':  0x00000040,
        'S':  0x00000080,
        'R':  0x00000200,
        'J':  0x00000400,
        'C':  0x00000800,
        'F':  0x00001000,
        'I':  0x00002000,
        'X':  0x00004000,
        'Z':  0x00008000,
        'V':  0x00010000,
        'W':  0x00020000,
        'O':  0x00040000,
        'G':  0x00080000,
        'U':  0x00100000,
        'A':  0x00200000,
        'Y':  0x00400000,
        'B':  0x00800000,
        'P':  0x01000000,
        'Q':  0x02000000,
        'L':  0x04000000,
    }

class MagicTableData(TableDataEntry):
    ENTRY_NAME = 'magic'
    DESCRIPTOR  = (
        ('id',              'W'),
        ('chrId',           'W'),
        ('targetType',      'S'),
        ('type',            'B'),
        ('damageType',      'B'),
        ('attribute',       'B'),
        ('byte1',           'B'),
        ('rangeType',       'B'),
        ('range',           'f'),
        ('area',            'C'),
        ('float2',          'f'),
        ('float3',          'f'),
        ('float4',          'f'),

        ('effect1',         'W'),
        ('effect1Param1',   'I'),
        ('effect1Param2',   'I'),
        ('effect1Param3',   'I'),

        ('effect2',         'W'),
        ('effect2Param1',   'I'),
        ('effect2Param2',   'I'),
        ('effect2Param3',   'I'),

        ('effect3',         'W'),
        ('effect3Param1',   'I'),
        ('effect3Param2',   'I'),
        ('effect3Param3',   'I'),

        ('effect4',         'W'),
        ('effect4Param1',   'I'),
        ('effect4Param2',   'I'),
        ('effect4Param3',   'I'),

        ('effect5',         'W'),
        ('effect5Param1',   'I'),
        ('effect5Param2',   'I'),
        ('effect5Param3',   'I'),

        ('ariaAT',          'C'),
        ('at',              'C'),
        ('epcp',            'H'),
        ('unbalanceRate',   'C'),
        ('breakRate',       'H'),
        ('level',           'C'),
        ('byte5',           'B'),
        ('word6',           'W'),
        ('ani',             'S'),
        ('name',            'S'),
        ('description',     'S'),
    )

class BattleCalcTableData(TableDataEntry):
    ENTRY_NAME = 'btcalc'
    DESCRIPTOR  = (
        ('id',              'L'),
        ('value',           'L'),
    )

class AttachTableData(TableDataEntry):
    DESCRIPTOR  = (
        ('chrId',       'W'),
        ('type',        'I'),
        ('itemId',      'L'),
        ('scenaFlags',  'L'),
        ('dword0E',     'L'),
        ('dword12',     'L'),
        ('dword16',     'L'),
        ('str',         'S'),
        ('asset',       'S'),
        ('node',        'S'),
    )

class AttachTransformData(TableDataEntry):
    DESCRIPTOR  = (
        ('chrId',       'W'),
        ('asset',       'S'),
        ('str2',        'S'),
        ('str3',        'S'),
        ('str4',        'S'),
    )

class EventTableData(TableDataEntry):
    DESCRIPTOR  = (
        ('eventId',         'W'),
        ('eventEntry',      'S'),
        ('word01',          'W'),
        ('word02',          'W'),
        ('scena',           'S'),
        ('word03',          'W'),
        ('nextEventId',     'W'),
        ('word03',          'W'),
        ('str04',           'S'),
        ('word04',          'W'),
        ('word05',          'W'),
        ('word06',          'W'),
        ('word07',          'W'),
        ('word08',          'W'),
        ('word09',          'W'),
        ('word0A',          'W'),
        ('word0B',          'W'),
    )

DataTable.DataTableDataTypes.update({
    'AttachTableData'       : AttachTableData,
    'AttachTransformData'   : AttachTransformData,
    'EventTableData'        : EventTableData,
    'bgm'                   : BGMTableData,
    'voice'                 : VoiceTableData,
    'status'                : StatusTableData,
    'magic'                 : MagicTableData,
    'btcalc'                : BattleCalcTableData,
})

DataTable.PythonHeader = [
    'from Falcom.ED84.Parser.datatable import *',
    '',
    'entries = [',
]
