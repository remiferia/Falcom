from Falcom.Common  import *
from Assembler      import *
from Falcom         import ED84

def map_operand_type(t: OperandType) -> str:
    return {
        OperandType.SInt8               : 'int',
        OperandType.SInt16              : 'int',
        OperandType.SInt32              : 'int',
        OperandType.SInt64              : 'int',
        OperandType.UInt8               : 'int',
        OperandType.UInt16              : 'int',
        OperandType.UInt32              : 'int',
        OperandType.UInt64              : 'int',
        OperandType.Float32             : 'float',
        OperandType.Float64             : 'float',
        OperandType.MBCS                : 'str',
        ED84.ED84OperandType.Text       : 'str | tuple',
        ED84.ED84OperandType.Offset     : 'str',
        ED84.ED84OperandType.ScenaFlags : 'int',
        ED84.ED84OperandType.Expression : 'tuple | list',
        ED84.ED84OperandType.ThreadValue: 'tuple | list',
    }[t]

def main():
    import pathlib
    filename = pathlib.Path(__file__)
    filename = filename.parent / ('scena_writer_gen.py')

    lines = [
        'from Falcom.ED84.Parser.scena_writer import _gScena as scena',
        '',
    ]

    for desc in sorted(ED84.ScenaOpTable, key = lambda desc: desc.opcode):
        desc: Assembler.InstructionDescriptor

        func = None

        if desc.handler:
            ctx = InstructionHandlerContext(HandlerAction.CodeGen, desc)
            try:
                func = desc.handler(ctx)
            except NotImplementedError:
                func = [
                    f'def {desc.mnemonic}():',
                    '    raise NotImplementedError',
                    '',
                ]

        if func is None:
            parameters = desc.parameters
            params = []
            args = []
            types = []

            if desc.operands:
                if not parameters:
                    parameters = []
                else:
                    parameters = list(parameters)

                parameters.extend([f'arg{i + 1}' for i in range(len(parameters), len(desc.operands))])

                for i, opr in enumerate(desc.operands):
                    typeHint = map_operand_type(opr.format.type)
                    name = parameters[i]
                    params.append(f'{name}: {typeHint}')
                    args.append(name)
                    types.append(typeHint)

            checkTypes = []

            if types:
                for i, t in enumerate(types):
                    checkTypes.append(f'    assert isinstance({args[i]}, {t})')

            args.insert(0, f'0x{desc.opcode:02X}')

            func = [
                f'def {desc.mnemonic}({", ".join(params)}):',
                f'    # 0x{desc.opcode:02X}',
                *checkTypes,
                f'    scena.handleOpCode({", ".join(args)})',
                '',
            ]

        lines.extend(func)

        if not desc.mnemonic.startswith('OP_'):
            func[0] = func[0].replace(desc.mnemonic, f'OP_{desc.opcode:02X}')
            lines.extend(func)

    open(filename, 'wb').write('\n'.join(lines).encode('UTF8'))

    # console.pause('done')

if __name__ == '__main__':
    Try(main)
