from Falcom.Common import *
from Falcom import ED9
from Falcom.ED9.Parser.scena_types import *
from types import FrameType
import uuid, inspect, opcode

class ScenaGlobalVar(ScenaGlobalVar):
    def load(self):
        pass

    def set(self):
        pass

class IntGlobalVar(ScenaGlobalVar):
    def __init__(self, index: int, name: str):
        super().__init__(index, name, ScenaGlobalVar.Type.Integer)

class StrGlobalVar(ScenaGlobalVar):
    def __init__(self, index: int, name: str):
        super().__init__(index, name, ScenaGlobalVar.Type.String)

class _StringPool:
    PLACE_HOLDER = 0xC5555555

    def __init__(self):
        self.pool = {}                                  # type: Dict[str, int]
        self.xref = []                                  # type: List[Tuple[str, int]]

    def addString(self, s: str, offset: int):
        self.pool.setdefault(s, 0)
        self.xref.append((s, offset))

    def getOffset(self, s: str) -> int:
        return self.pool[s] | 0xC0000000

class ScenaFunctionWrapper:
    def __init__(self, func: ScenaFunction):
        self.func = func

    def __int__(self) -> int:
        return self.func.index

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError

class ED9DisasmContext(Assembler.DisasmContext):
    def __init__(self, writer: '_ScenaWriter', fs: fileio.FileStream):
        super().__init__(fs)
        self.writer = writer

class _ScenaWriter:
    ScenaCodeList = set()

    def __init__(self):
        self.labels             = {}                    # type: Dict[str, int]
        self.xrefs              = []                    # type: List[Assembler.XRef]
        self.functions          = []                    # type: List[ScenaFunction]
        self.currentFunctionId  = None                  # type: int
        self.currentStack       = None                  # type: ScenaStack
        self.instructionTable   = None                  # type: ED9.ED9InstructionTable
        self.scenaName          = ''
        self.fs                 = None                  # type: fileio.FileStream
        self.globals            = None                  # type: dict
        self.opcodeCallbacks    = []                    # type: List[Callable[[int, Tuple]]]
        self.funcCallbacks      = []                    # type: List[Callable[[str, Callable]]]
        self.runCallbacks       = []                    # type: List[Callable[[dict]]]
        self.globalVars         = []                    # type: List[ScenaGlobalVar]
        self.stringPool         = _StringPool()         # type: _StringPool

    def init(self, instructionTable: ED9.ED9InstructionTable, scenaName: str):
        self.instructionTable   = instructionTable
        self.scenaName          = scenaName

    def registerRunCallback(self, cb):
        self.runCallbacks.append(cb)

    def registerFuncCallback(self, cb):
        self.funcCallbacks.append(cb)

    def registerOpCodeCallback(self, cb):
        self.opcodeCallbacks.append(cb)

    def setGlobalVars(self, *vars):
        self.globalVars.extend(sorted(vars, key = lambda v: v.index))

    def functionDecorator(self, type: ScenaFunctionType, byte05, byte06, **kwargs) -> Callable[[], None]:
        def wrapper(f: Callable[[], Any]):
            name = f.__name__

            for cb in self.funcCallbacks:
                f2 = cb(name, f)
                if f2 is not None:
                    f = f2

            func = ScenaFunction(len(self.functions), -1, name)
            func.type = type
            func.obj = f

            if type == ScenaFunctionType.Code:
                entry = ScenaFunctionEntry(offset = 0xEEEEEEEE, byte05 = byte05, byte06 = byte06, nameCrc32 = utils.hashFuncName(name))
                func.entry = entry
                func.sig = inspect.signature(f)
                func.decompiled = kwargs.get('compile', False)
                entry.paramCount = len(func.sig.parameters)

            self.functions.append(func)

            return ScenaFunctionWrapper(func)

        return wrapper

    # decorators

    def Code(self, byte05 = 0, byte06 = 0, **kwargs):
        return self.functionDecorator(ScenaFunctionType.Code, byte05, byte06, **kwargs)

    def run(self, g: dict):
        for cb in self.runCallbacks:
            cb(g)

        try:
            self.run2(g)
        except KeyError as e:
            if isinstance(e.args[0], int):
                e.args = (f'0x{e.args[0]:X} ({e.args[0]})',)
            raise

    def run2(self, g: dict):
        self.globals = g

        hdr = ScenaHeader()
        fs = fileio.FileStream(encoding = defaultEncoding()).OpenFile(self.scenaName, 'wb+')

        self.fs = fs

        hdr.functionCount = len(self.functions)
        hdr.globalVarCount = len(self.globalVars)

        fs.Write(hdr.serialize())

        self.writeFuncInfo(fs)
        self.writeDebugSymbols(fs)

        hdr.globalVarOffset = fs.Position
        self.writeGlobalVars(fs)
        self.compileFunctions(fs)

        with fs.PositionSaver:
            self.flushFuncEntries(fs)

        self.writeStringPool(fs)

        fs.Position = 0
        fs.Write(hdr.serialize())

        with fs.PositionSaver:
            for x in self.xrefs:
                offset = self.labels[x.name]
                fs.Position = x.offset
                fs.WriteULong(offset)

            self.xrefs.clear()

        # fs.Flush()
        # fs.Close()
        # raise NotImplementedError

    def writeFuncInfo(self, fs: fileio.FileStream):
        offsetOfFuncName = fs.Position + 0x1C
        for f in self.functions:
            self.stringPool.addString(f.name, offsetOfFuncName)
            offsetOfFuncName += ScenaFunctionEntry.SIZE

        self.flushFuncEntries(fs)

        for f in self.functions:
            entry = f.entry
            entry.defaultParamsOffset = fs.Position

            if entry.paramCount == 0:
                continue

            entry.defaultParamsCount = 0

            for param in reversed(f.sig.parameters.values()):
                value = param.default
                if value is param.empty:
                    continue

                entry.defaultParamsCount += 1

                # print(f'{f.name} @ 0x{fs.Position:08X} {param.name}')

                match value:
                    case RawInt():
                        fs.Write(value.to_bytes(4, defaultIndent()))

                    case int() | float():
                        fs.Write(ScenaValue(value).serialize())

                    case str():
                        self.writeString(value)

            # if entry.defaultParamsCount == 0:
            #     entry.defaultParamsOffset = 0xFFFFFFFF

        for f in self.functions:
            entry = f.entry
            entry.paramFlagsOffset = fs.Position

            if entry.paramCount == 0:
                continue

            for param in f.sig.parameters.values():
                fs.Write(ScenaParamFlags(param.annotation).serialize())

        with fs.PositionSaver:
            self.flushFuncEntries(fs)

    def flushFuncEntries(self, fs: fileio.FileStream):
        fs.Position = 0x18
        for f in self.functions:
            fs.Write(f.entry.serialize())

    def writeDebugSymbols(self, fs: fileio.FileStream):
        pass
        # fs.Write(bytes([0xFF] * 0x3630c))

    def writeGlobalVars(self, fs: fileio.FileStream):
        for gv in self.globalVars:
            self.writeString(gv.name)
            fs.WriteULong(gv.type)

    def compileFunctions(self, fs: fileio.FileStream):
        for f in self.functions[:1]:
            self.currentFunctionId = f.index
            f.entry.offset = fs.Position
            print(f'{f.name} @ 0x{f.entry.offset:08X}')
            if f.decompiled is False:
                f.obj(*[None] * f.entry.paramCount)
            else:
                ibp()
                self.currentStack = ScenaStack()
                self.ScenaCodeList.add(f.obj.__code__)
                sys.settrace(self.onTraceCall)
                f.obj(*[self.currentStack.Arg() for _ in f.entry.paramCount][::-1])
                sys.settrace(None)
                self.currentStack = None

    def writeStringPool(self, fs: fileio.FileStream):
        pool = self.stringPool
        for s in pool.pool.keys():
            pool.pool[s] = fs.Position
            fs.Write(s.encode(defaultEncoding()) + b'\x00')

        with fs.PositionSaver:
            for s, offset in pool.xref:
                fs.Position = offset
                fs.WriteULong(pool.getOffset(s))

    def addLabel(self, name):
        addr = self.labels.get(name)
        if addr is not None:
            raise Exception(f'label exists: {name} -> 0x{addr:08X}')

        self.labels[name] = self.fs.Position

    def writeString(self, s: str):
        self.addString(s)
        self.fs.WriteULong(_StringPool.PLACE_HOLDER)

    def addString(self, s: str):
        self.stringPool.addString(s, self.fs.Position)

    def handleOpCode(self, opcode: int, *args, **kwargs):
        # log.debug(f'handle opcode 0x{opcode:X} @ 0x{self.fs.Position:X}')

        for cb in self.opcodeCallbacks:
            if cb(opcode, *args) is True:
                return

        fs = self.fs
        tbl = self.instructionTable
        desc = tbl.getDescriptor(opcode)

        inst = Assembler.Instruction(opcode)
        inst.descriptor = desc

        for i, a in enumerate(args):
            opr = Assembler.Operand()
            opr.value = a
            opr.descriptor = desc.operands and desc.operands[i] or None
            inst.operands.append(opr)

        context = Assembler.InstructionHandlerContext(Assembler.HandlerAction.Assemble, desc)
        context.disasmContext = ED9DisasmContext(self, fs)
        context.instruction = inst
        context.xrefs = self.xrefs

        if desc.handler:
            if desc.handler(context):
                return

        else:
            assert len(desc.operands or []) == len(args)

        tbl.writeOpCode(fs, opcode)
        tbl.writeAllOperands(context, inst.operands)

    def onTraceCall(self, frame: FrameType, event: str, arg):
        match event:
            case 'call':
                if frame.f_code in self.ScenaCodeList:
                    frame.f_trace_opcodes = True
                    frame.f_trace_lines = False
                    return Tracer(frame.f_code.co_name, self.currentStack).onTraceOpCode

class Tracer:
    class OPCode:
        STORE_FAST  = opcode.opmap['STORE_FAST']
        DELETE_FAST = opcode.opmap['DELETE_FAST']

    class Context:
        def __init__(self, frame: FrameType):
            self.frame = frame
            self.lasti = frame.f_lasti
            self.code = frame.f_code

    class Assignment:
        def __init__(self, dest: StackValue, src: StackValue):
            self.dest = dest
            self.src = src

    def __init__(self, func: str, stack: ScenaStack):
        self.func           = func
        self.stack          = stack
        self.locals         = {}                    # type: dict[str, StackValue]
        self.prevContext    = None                  # type: Tracer.Context
        self.assign         = None                  # type: Tracer.Assignment

    def preTrace(self, frame: FrameType, event: str, arg):
        op = frame.f_code.co_code[frame.f_lasti]
        locals: dict[str, StackValue] = frame.f_locals

        match op:
            case Tracer.OPCode.STORE_FAST:
                # set exists var

                print(f'{opcode.opname[op]} {varname}')
                print(locals)
                print('----------------')

                index = frame.f_code.co_code[frame.f_lasti + 1]
                varname = frame.f_code.co_varnames[index]

                self.assign = Tracer.Assignment(None, None)

                if varname not in locals:
                    return

                self.assign.dest = locals[varname]

            case Tracer.OPCode.DELETE_FAST:
                # del var

                print(f'{opcode.opname[op]} {varname}')
                print(locals)
                print('----------------')

                index = frame.f_code.co_code[frame.f_lasti + 1]
                varname = frame.f_code.co_varnames[index]
                var = locals[varname]

                assert var.stackIndex == self.stack.stackTop

                self.stack.pop()

    def postTrace(self, ctx: Context):
        frame = ctx.frame
        op = ctx.code.co_code[ctx.lasti]
        match op:
            case Tracer.OPCode.STORE_FAST:
                # set new var

                print(f'{opcode.opname[op]} {varname}')
                print(frame.f_locals)
                print('----------------')

                locals = frame.f_locals
                index = ctx.code.co_code[ctx.lasti + 1]
                varname = frame.f_code.co_varnames[index]
                var = locals[varname]

                self.assign.src = var
                self.handleAssignment(self.assign, varname, locals)
                self.assign = None

    def onTraceOpCode(self, frame: FrameType, event: str, arg):
        # print(f'onTraceOpCode: {self.func} {event}')

        if self.prevContext:
            self.postTrace(self.prevContext)
            self.prevContext = None

        if event == 'opcode':
            self.preTrace(frame, event, arg)
            self.prevContext = Tracer.Context(frame)

    def handleAssignment(self, assign: Assignment, varname: str, locals: dict[str, StackValue]):
        from .scena_writer_helper import handleAssignment
        return handleAssignment(self.stack, assign, varname, locals)

_gScena: _ScenaWriter = _ScenaWriter()

def createScenaWriter(scriptName: str) -> _ScenaWriter:
    _gScena.init(instructionTable = ED9.ScenaOpTable, scenaName = scriptName)
    return _gScena

def getScena() -> _ScenaWriter:
    return _gScena

def Compile():
    def wrapper(f):
        _ScenaWriter.ScenaCodeList.add(f.__code__)
        return f

    return wrapper

def label(name: str):
    _gScena.addLabel(name)

def genLabel() -> str:
    return str(uuid.uuid4())

def emit(*b: int):
    for v in b:
        _gScena.fs.WriteByte(v)

def ScenaFlag(offset: int, flag: int, *args) -> int:
    return ((offset & 0xFFFF) << 3) | (flag & 7)

def ArgReg(index: int, b: int = 0) -> Tuple[int, int, int]:
    return (0x11, index, b)

def ArgInt(index: int, b: int = 0) -> Tuple[int, int, int]:
    return (0x33, index, b)

def ArgStr(index: int, b: int = 0) -> Tuple[int, int, int]:
    return (0x44, index, b)

def ParamStr(s: str) -> Tuple[int, str]:
    return (0xDD, s)

def ParamFloat(v: float, b: int = 0) -> Tuple[int, float, int]:
    return (0xEE, v, b)

def ParamInt(v: int, b: int = 0) -> Tuple[int, int, int]:
    return (0xFF, v, b)
