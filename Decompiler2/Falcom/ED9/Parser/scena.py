from Assembler.function import Function
from Assembler.instruction import Instruction
from ..InstructionTable import ScenaOpTable as ED9ScenaOpTable
from .scena_types import *
import pathlib

if TYPE_CHECKING:
    from Assembler.instruction_table import InstructionTable

__all__ = (
    'ScenaParser',
    'ScenaHeader',
    'ScenaFunctionType',
    'ScenaFunction',
    'ScenaFunctionEntry',
)

class ScenaFormatter(Assembler.Formatter):
    def __init__(self, parser: 'ScenaParser', instructionTable: 'InstructionTable', *args, **kwargs):
        super().__init__(instructionTable, *args, **kwargs)
        self.parser = parser

    def formatLabel(self, name: str) -> List[str]:
        return [
            f'def _{name}(): pass',
            '',
            f"label('{name}')",
        ]

    def formatFuncion(self, func: ScenaFunction) -> List[str]:
        funcName = func.name
        if not funcName:
            if func.type == ScenaFunctionType.BattleSetting:
                funcName = f'{func.type}{func.index:02X}'
            else:
                funcName = f'func_{func.offset:X}'

        f = [
            f'# id: 0x{func.index:04X} offset: 0x{func.offset:X}',
            f'@scena.{func.type}(\'{func.name}\')',
            f'def {funcName}():',
        ]

        if func.type in ScenaDataFunctionTypes:
            body = self.formatDataFunction(func)

        elif func.type == ScenaFunctionType.Code:
            body = self.formatCode(func)

        else:
            raise NotImplementedError(f'unknown func type: {func.type}')

        if not body:
            body = ['pass']

        f.extend([f'{GlobalConfig.DefaultIndent}{l}'.rstrip() for l in body])
        if f[-1] != '':
            f.append('')

        return f

    def formatCode(self, f: ScenaFunction) -> List[str]:
        func: Function = f.obj

        if func is None:
            return

        body = []
        blk = self.formatBlock(func.block, genLabel = False)
        for b in blk:
            body.append(b)

        return body

    def formatDataFunction(self, f: ScenaFunction) -> List[str]:
        if f.obj is None:
            return

        body = f.obj.toPython()
        body[0] = 'return ' + body[0]
        return body

class ScenaParser:
    def __init__(self, fs: fileio.FileStream):
        self.fs                 = fs                # type: fileio.FileStream
        self.name               = ''                # type: str
        self.header             = None              # type: ScenaHeader
        self.functions          = []                # type: List[ScenaFunction]
        self.functionNameMap    = {}                # type: Dict[str, bool]
        self.instructionCb      = None              # type: Callable[[Instruction], None]

    def __str__(self) -> str:
        funcs = '\n'.join([str(f) for f in self.functions])
        return '\n'.join([
            f'magic                 = {self.header.magic}',
            f'functionEntryOffset   = 0x{self.header.functionEntryOffset:08X}',
            f'functionCount         = 0x{self.header.functionCount:08X}',
            f'globalVarOffset       = 0x{self.header.globalVarOffset:08X}',
            '',
            f'{funcs}',
        ])

    def parse(self):
        self.readHeader()
        self.disasmFunctions()

    def readHeader(self):
        fs = self.fs
        fs.Position = 0

        self.header = ScenaHeader(fs = fs)

        hdr = self.header

        funcEntries = [ScenaFunctionEntry(fs = fs) for _ in range(hdr.functionCount)]

        for index, f in enumerate(funcEntries):
            assert f.nameOffset >> 30 == 3
            fs.Position = f.nameOffset & 0x3FFFFFFF
            self.functions.append(ScenaFunction(index = index, offset = f.addr, name = fs.ReadMultiByte(), type = ScenaFunctionType.Code, entry = f))

            f.name = self.functions[-1].name

            # print('\n'.join(f.toPython()))

    def getCodeFuncName(self, funcID: int) -> str:
        return self.functions[funcID].name

    def setInstructionCallback(self, cb: Callable[[Instruction], None]):
        self.instructionCb = cb

    def disasmFunctions(self):
        fs = self.fs
        dis = Assembler.Disassembler(ED9ScenaOpTable)
        ctx = Assembler.DisasmContext(fs, instCallback = self.instructionCb, scriptName = self.name)

        for func in self.functions:
            log.debug(f'disasm func: {func}')

            match func.type:
                case ScenaFunctionType.Code:
                    fs.Position = func.offset
                    try:
                        func.obj = dis.disasmFunction(ctx, name = func.name)
                    except KeyError as e:
                        e.args = (f'0x{e.args[0]:X} ({e.args[0]})',)
                        raise

                case _:
                    if func.type not in ScenaDataFunctionTypes:
                        raise NotImplementedError(f'unknown func type: {func.type}')

    def generatePython(self, filename: str) -> List[str]:
        formatter = ScenaFormatter(self, ED9ScenaOpTable, name = self.name)

        lines = f'''\
import sys
sys.path.append(r'{pathlib.Path(__file__).parent.parent.parent.parent}')

from Falcom.ED9.Parser.scena_writer_helper import *
try:
    import {pathlib.Path(filename).stem.strip()}_hook
except ModuleNotFoundError:
    pass

scena = createScenaWriter('{filename}')

'''.splitlines()

        for func in self.functions:
            lines.extend(formatter.formatFuncion(func))

        main = '''\
def main():
    scena.run(globals())

if __name__ == '__main__':
    Try(main)

'''

        lines.extend(main.splitlines())

        # print('\n'.join(lines))

        return lines

