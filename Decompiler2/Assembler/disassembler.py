from Common             import *
from .instruction       import *
from .instruction_table import *
from .function          import *
from .handlers          import *

__all__ = (
    'Disassembler',
    'DisasmContext',
)

class DisasmContext:
    def __init__(self, fs: fileio.FileStream, *, scriptName: str = '', instCallback: Callable[[Instruction], None] = None):
        self.scriptName     = scriptName
        self.fs             = fs
        self.instCallback   = instCallback

class Disassembler:
    def __init__(self, instructionTable: InstructionTable):
        self.instructionTable   = instructionTable      # type: InstructionTable
        self.disassembledBlocks = {}                    # type: Dict[int, CodeBlock]
        self.disassembledOffset = {}                    # type: Dict[int, Instruction]
        self.allocatedBlocks    = {}                    # type: Dict[int, CodeBlock]
        self.currentBlock       = None                  # type: CodeBlock

    def getInstructionByOffset(self, offset: int) -> Instruction:
        return self.disassembledOffset[offset]

    def createCodeBlock(self, offset: int) -> CodeBlock:
        block = self.allocatedBlocks.get(offset)
        if block is None:
            block = CodeBlock(instructions = [], offset = offset, name = f'loc_{offset:X}')

            if offset != Instruction.InvalidOffset:
                self.allocatedBlocks[offset] = block

        return block

    def addBranch(self, offset: int) -> CodeBlock:
        block = self.createCodeBlock(offset)
        return self.currentBlock.addBranch(block)

    def disasmFunction(self, context: DisasmContext, *, name: str = None) -> Function:
        func = Function()

        func.offset = context.fs.Position
        if name:
            func.name = name

        # log.debug(f'disasm func 0x{func.offset:08X} {func.name}')

        func.block = self.disasmBlock(context)

        if name:
            func.block.name = name

        return func

    def disasmBlock(self, context: DisasmContext) -> CodeBlock:
        fs = context.fs
        offset = fs.Position
        block = self.disassembledBlocks.get(offset)

        if block is not None:
            return block

        # log.debug(f'disasm block: 0x{offset:X}')

        block = self.createCodeBlock(offset)

        self.disassembledBlocks[offset] = block

        previousBlock = self.currentBlock
        self.currentBlock = block

        while True:
            pos = fs.Position
            inst = self.disassembledOffset.get(pos)
            if inst:
                # ref by other instructions
                inst.xrefs.append(XRef(self.createCodeBlock(pos).name, -1))
                break

            try:
                inst = self.disasmInstruction(context)
            except:
                # console.pause(f'KeyError: 0x{e.args[0]:X}'); break
                fs.Position = pos
                opcode = self.instructionTable.readOpCode(fs)
                log.debug(f'disasm inst 0x{opcode:02X}<{opcode}> @ 0x{pos:08X}')

                import subprocess
                subprocess.check_call(f'echo 0x{pos:08X}|clip', shell=True)

                raise

            self.disassembledOffset[pos] = inst
            block.instructions.append(inst)

            if inst.flags.endBlock:
                break

            if inst.flags.startBlock:
                block.insertBranch(self.createCodeBlock(context.fs.Position))
                break

            if context.fs.Position in self.allocatedBlocks:
                break

        # log.debug(f'disasm block end: 0x{offset:X}')

        for index, branch in enumerate(block.branches):
            pos = context.fs.Position

            context.fs.Position = branch.offset
            block.branches[index] = self.disasmBlock(context)

            context.fs.Position = pos

        self.currentBlock = previousBlock

        return block

    def disasmInstruction(self, context: DisasmContext) -> Instruction:
        fs = context.fs
        pos = fs.Position

        try:
            opcode = self.instructionTable.readOpCode(fs)
        except Exception as e:
            log.error('error occurred %s @ position %X' % (e, pos))
            raise

        try:
            desc = self.instructionTable.getDescriptor(opcode)
            # log.debug(f'disasm inst 0x{opcode:02X}<{opcode}><{desc.mnemonic}> @ 0x{pos:08X}')
        except:
            # log.debug(f'disasm inst 0x{opcode:02X}<{opcode}> @ 0x{pos:08X}')
            raise

        handlerContext = InstructionHandlerContext(HandlerAction.Disassemble, desc)

        inst = Instruction(opcode)
        inst.offset     = pos
        inst.descriptor = desc
        inst.flags      = desc.flags

        handlerContext.instructionTable = self.instructionTable
        handlerContext.offset           = pos
        handlerContext.disasmContext    = context
        handlerContext.disassembler     = self
        handlerContext.instruction      = inst

        self.instructionTable.preDisasmInstruction(handlerContext)

        inst = desc.handler(handlerContext) if desc.handler else None

        if inst is None:
            inst = self.defaultInstructionDecoder(handlerContext)

        if inst is None:
            raise Exception('disasmInstruction %02X @ %08X failed' % (opcode, pos))

        inst.size = fs.Position - pos

        self.instructionTable.postDisasmInstruction(handlerContext)

        if context.instCallback:
            context.instCallback(inst)

        # if pos == 0x0000DEC0: ibp()

        return inst

    def defaultInstructionDecoder(self, context: InstructionHandlerContext) -> Instruction:
        desc = context.descriptor
        inst = context.instruction
        inst.operands = [self.instructionTable.readOperand(context, oprdesc) for oprdesc in (desc.operands or [])]

        return inst
