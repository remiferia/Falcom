from Falcom.ED83.Parser.scena_writer_helper import *

def funcCallBack(name: str, f: Callable):
    match name:
        case 'AniBtlStart': return AniBtlStart
        case 'AniBtlMove': return AniBtlMove
        case 'AniBtlAttack': return AniBtlAttack
        # case 'AniBtlAria': return AniBtlAria
        # case '_AniBtlAria': return _AniBtlAria
        # case 'AniBtlArts': return AniBtlArts
        # case '_AniBtlArts': return _AniBtlArts
        case _: pass

    pass

def opcodeCallBack(opcode: int, *args):
    match opcode:
        case 0x02:      # Call
            if args[0] == ScriptId.BtlCom and args[1] == 'AniBtlMove':
                AniBtlMove2()
                return True

def runCallBack(g):
    from Falcom.ED83.Parser.scena_writer import _gScena as scena
    for f in [
        AniBtlCraft05,
        AniBtlCraftDamageAnimeX,
        AniBtlCraftDamageX,
        AniBtlCraftDamageXKnockBack,
        AniBtlPlayLanceEffects,
    ]:
        scena.Code(f.__name__)(f)

def _init():
    from Falcom.ED83.Parser.scena_writer import _gScena as scena
    scena.registerFuncCallback(funcCallBack)
    scena.registerOpCodeCallback(opcodeCallBack)
    scena.registerRunCallback(runCallBack)

_init()

def AniBtlMove2():
    PlayChrAnimeClip(0xFFFE, 'BTL_MOVE', 0x01, 0x00, 0x00, 0x00, 0x00, 0.2, -1, -1, -1, 0x00, 0x00)
    OP_33(0x34)
    Call(0x10, 'AniBtlWait')

def AniBtlCraft05():
    end = genLabel()

    Call(ScriptId.BtlCom, 'AniBtlCraftBegin')

    LoadEffect(0xFFFE, 0x90, 'battle/cr000_02_1.eff')
    LoadEffect(0xFFFE, 0x91, 'battle/cr000_02_5.eff')
    LoadEffect(0xFFFE, 0x92, 'battle/cr033_00_0.eff')
    LoadEffect(0xFFFE, 0x9F, 'battle/cic033_0.eff')

    Call(ScriptId.Current, 'SpringOff')
    SetEndhookFunction('SpringOn', ScriptId.Current)

    ChrTurnDirection(0xFFFE, 0xFFFB, 0.0, -1.0)
    ChrSavePosition(0xFFFE, 0x00000000)
    ChrCreateDummy(0xFFFE, 1)
    ChrHide(DummyCharBaseId, 0x40 | 0x20)
    ChrTurnDirection(DummyCharBaseId, 0xFFFE, 0.0, -1.0)
    # ChrSetPosByTarget(DummyCharBaseId, 0xFFF5, 0.0, 0.0, -2.0, -1.0, 0x00, 0x00)
    ChrSetPosByTarget(DummyCharBaseId, 0xFFFB, 0.0, 0.0, -2.0, -1.0, 0x00, 0x00)

    if 0:
        # BattleChrCtrl(0xB7, 0x00, 0xFFFE, AbnormalStatus.Death, 0x000000FF, 0x000000FF, 0x00)
        BattleChrCtrl(0xB7, 0x00, 0xFFFB, AbnormalCondition.Death | AbnormalCondition.Deathblow | AbnormalCondition.Vanish, 0x000000FF, 0x000000FF, 0x00)
        SetChrPos(0xFFFB, 0.0, -100.0, 0.0, 0.0)
        Jump(end)

        kisin = ChrCreateTempChar(0, 0xFFFF, 'C_ROB004', 'rob500')
        ChrSetPosByTarget(kisin, 0xFFFE, 0.0, 0.0, -2.0, -1.0, 0x00, 0x00)
        ChrTurnDirection(kisin, 0xFFFB, 0.0, -1.0)

        BattleChrCtrl(0x47)
        CameraCtrl(0x00)
        CameraSetPosByTarget(kisin, '', 0.0, 4.5, -0.22, 0)
        CameraRotateByTarget(kisin, '', 0x03, 6.0, 0, 0, 0, 0x01)
        CameraSetDistance(2.1, 0)
        CameraCtrl(0x0B, 0x03, 40.0, 0x0000)
        CameraSetPosByTarget(kisin, '', 0.0, 4.5, -0.1, 1000)
        CameraRotateByTarget(kisin, '', 0x03, 6.0, 20, 0.0, 1000, 0x01)
        CameraSetDistance(7.5, 700)
        CameraCtrl(0x16, 0x03, 7.5, 700)
        Sleep(1000)

        # SetChrAniFunction(kisin, 0x00, 'AniEvk1001', 0.0, 1.0, 0x00000000)
        # PlayChrAnimeClip(kisin, 'evk1001', 0x00, 0x01, 0x00, 0x00, 0x00, -2.0, 166.6666717529297, 168.63375854492188, -1.0, 0x00, 0x00)
        PlayChrAnimeClip(kisin, 'evk1001', 0x00, 0x01, 0x00, 0x00, 0x00, -2.0, 166.6666717529297, 167.63375854492188, -1.0, 0x00, 0x00)

        Sleep(2000)

        Jump(end)

    BattleChrCtrl(0x47)
    CameraCtrl(0x00)
    CameraSetPosByTarget(0xFFFE, '', 0.0, 0.95, -0.22, 0)
    CameraRotateByTarget(0xFFFE, '', 0x03, 6.0, 0, 0, 0, 0x01)
    CameraSetDistance(2.1, 0)
    CameraCtrl(0x0B, 0x03, 40.0, 0x0000)
    CameraSetPosByTarget(0xFFFE, '', 0.0, 0.75, -0.1, 1000)
    CameraRotateByTarget(0xFFFE, '', 0x03, 6.0, -15.0, 0.0, 1000, 0x01)
    CameraSetDistance(3.5, 1000)

    PlayEffect2(0xFFFE, 0x9F, 0xFFFF, 0, '', *(0.5, 0.0, 0.0), *(0.0, 0.0, 0.0), *(0.8, 0.8, 0.8), 0xFF)
    PlaySound(0x8B7D)
    # Sleep(1666)
    Sleep(800)

    PlayVoice(0x1B8C)
    # PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT00_00', 0x01, 0x00, 0x00, 0x00, 0x00, 0.2, -1.0, -1.0, -1.0, 0x00, 0x00)
    PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x00, 0x01, 0x00, 0x00, 0x00, 0.2, 66.6667, 67.2, -1.0, 0x00, 0x00)
    Sleep(500)

    Fade(0x65, 100, 1.0, 0x0000)
    Fade(0xFE, 0)
    ChrHide(0xFFF9, 64)
    ChrHide(0xFFF9, 32)

    # PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT00_00', 0x01, 0x00, 0x00, 0x00, 0x00, 0.2, -1.0, -1.0, -1.0, 0x00, 0x00)
    # PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x00, 0x01, 0x00, 0x00, 0x00, 0.2, 66.6667, 67.2, -1.0, 0x00, 0x00)
    ChrShow(0xFFF9, 64)
    ChrShow(0xFFF9, 32)
    CameraCtrl(0x00)
    CameraSetDistance(3.2, 0)
    Sleep(64)

    def left():
        CameraSetPosByTarget(0xFFFE, '', 1.5, 2.2, -1.5, 0)
        CameraRotateByTarget(0xFFFE, '', 0x03, 22.0, 135.0, 0.0, 0, 0x01)
        PlayEffect2(0xFFFE, 0x92, 0xFFFE, 0x0000000C, '', *(0.0, 0.0, 0.0), 0.0, 0.0, 0.0, *(1.0, 1.0, 1.0), 0xFF)
        SetChrFace(0x03, 0xFFFE, '2', '2[autoM2]', '0', '2', '0')
        Sleep(1000)
        CameraSetPosByTarget(DummyCharBaseId, '', 2.5, 2.2, -2.8, 700)

        CameraCtrl(0x16, 0x03, 3.2, 700)
        CameraSetDistance(3.2, 700)

        PlayEffect2(0xFFFE, 0x91, 0xFFFE, 0x00000003, '', *(0.0, 0.0, 0.0), 0.0, 0.0, 0.0, *(1.0, 1.0, 1.0), 0xFF)
        PlayEffect2(0xFFFE, 0x90, 0xFFFE, 0x00000003, '', *(0.0, 1.0, 0.0), 0.0, 0.0, 0.0, *(1.0, 1.0, 1.0), 0xFF)
        PlaySound(0xFB1)
        PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x00, 0x01, 0x00, 0x00, 0x00, 0.2, 66.6667, 67.2, -1.0, 0x00, 0x00)
        ChrSetPosByTarget(0xFFFE, 0xFFF5, 0.0, 0.0, -2.0, 7.0, 0x00, 0x00)
        ChrSetPosByTarget(DummyCharBaseId, 0xFFF5, 0.0, 0.0, -2.0, -1.0, 0x00, 0x00)
        CameraSetPosByTarget(0xFFFE, '', 2.5, 2.2, -2.8, 700)

    def right():
        CameraSetPosByTarget(0xFFFE, '', -3.5, 2.2, -2.2, 0)
        CameraRotateByTarget(0xFFFE, '', 0x03, 22.0, 235, 0.0, 0, 0x01)
        PlayEffect2(0xFFFE, 0x92, 0xFFFE, 0x0000000C, '', *(0.0, 0.0, 0.0), 0.0, 0.0, 0.0, *(1.0, 1.0, 1.0), 0xFF)
        SetChrFace(0x03, 0xFFFE, '2', '2[autoM2]', '0', '2', '0')
        Sleep(1000)
        CameraSetPosByTarget(DummyCharBaseId, '', -3.5, 1.5, -0.8, 700)

        CameraCtrl(0x16, 0x03, 3.2, 700)
        CameraSetDistance(3.2, 700)

        PlayEffect2(0xFFFE, 0x91, 0xFFFE, 0x00000003, '', *(0.0, 0.0, 0.0), 0.0, 0.0, 0.0, *(1.0, 1.0, 1.0), 0xFF)
        PlayEffect2(0xFFFE, 0x90, 0xFFFE, 0x00000003, '', *(0.0, 1.0, 0.0), 0.0, 0.0, 0.0, *(1.0, 1.0, 1.0), 0xFF)
        PlaySound(0xFB1)
        PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x00, 0x01, 0x00, 0x00, 0x00, 0.2, 66.6667, 67.2, -1.0, 0x00, 0x00)
        ChrSetPosByTarget(0xFFFE, 0xFFF5, 0.0, 0.0, -2.0, 7.0, 0x00, 0x00)
        ChrSetPosByTarget(DummyCharBaseId, 0xFFF5, 0.0, 0.0, -2.0, -1.0, 0x00, 0x00)
        CameraSetPosByTarget(0xFFFE, '', -3.5, 2.2, -2.2, 700)

    RandIf(50, left, right)

    PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x01, 0x01, 0x00, 0x01, 0x00, 0.2, 67.2333, 67.4333, -0.0333333, 0x00, 0x00)
    Sleep(100)

    ChrCreateAfterImage(0xFFFE)
    ChrSetAfterImageOn(0xFFFE, 0.1, 0.1, 0.22, 0.45, 1.0)

    for i in range(5):
        CreateThread(0xFFFE, 1, ScriptId.Current, 'AniBtlPlayLanceEffects')

        match i:
            case 0 | 2 | 4:
                CreateThread(0xFFFE, 2, ScriptId.Current, 'AniBtlCraftDamageX')
                WaitForThreadExit(0xFFFE, 2)

            case 1 | 3:
                CreateThread(0xFFFE, 2, ScriptId.Current, 'AniBtlCraftDamageAnimeX')
                WaitForThreadExit(0xFFFE, 2)

        WaitForThreadExit(0xFFFE, 1)
        Sleep(100)

    PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x00, 0x01, 0x00, 0x00, 0x00, 0.05, 68.9333, -1.0, -1.0, 0x00, 0x00)
    OP_6C(0xFFFE, 0.5)
    Sleep(800)

    PlayEffect2(0xFFFE, 0x90, 0xFFFE, 0x00000003, '', *(0.0, 1.0, 0.0), 0.0, 180, 0.0, *(1.0, 1.0, 1.0), 0xFF)
    PlaySound(0xFB1)
    ChrSetPosByTarget(0xFFFE, 0xFFF4, 0.0, 0.0, 0.0, 3.0, 0x00, 0x00)
    Sleep(300)

    CreateThread(0xFFFE, 0x02, ScriptId.Current, 'AniBtlCraftDamageXKnockBack')
    WaitForThreadExit(0xFFFE, 0x02)
    Sleep(1000)

    label(end)

    ChrSetAfterImageOff()

    PlayChrAnimeClip(0xFFFE, 'BTL_WAIT', 0x01, 0x00, 0x00, 0x00, 0x00, 0.5, -1.0, -1.0, -1.0, 0x00, 0x00)
    Call(ScriptId.BtlCom, 'AniBtlCraftFinish')

    Return()

def AniBtlPlayLanceEffects():
    effs = [
        ((1.5, 1.5, 0.0),   0xFF),
        ((-1.5, 1.5, 0.0),  0xFF),
        ((1.5, 0, 0.0),     0xFF),
        ((-1.5, 0, 0.0),    0xFF),
        ((0.0, 1.5, 0.0),   0xFF),
        ((0.0, 0.0, 0.0),   0xFF),
    ]

    for eff in effs:
        OP_3B(0x00, (0xFF, 0x8F62, 0x0), 0.8, (0xFF, 0x0, 0x0), 0.0, -1.0, 0x0000, 0xFFFF, 0.0, 0.0, 0.0, 0.0, '', 0x05DC, 0x012C, 0x0000, 0x05DC, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000)
        OP_3B(0x00, (0xFF, 0x8F66, 0x0), 0.5, (0xFF, 0x0, 0x0), 0.0, 0.0, 0x0000, 0xFFFF, 0.0, 0.0, 0.0, 0.0, '', 0x05DC, 0x012C, 0x0000, 0x05DC, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000)
        PlayEffect2(
            TargetSelf,
            0x83,
            TargetSelf,
            0xC,
            '',
            *eff[0],
            0.0, 0.0, 0.0,
            0.5, 0.5, 0.8,
            eff[1],
        )
        Sleep(70)

    Return()

def AniBtlCraftDamageAnimeX():
    AniBtlCraftDamageT(False, 0)

def AniBtlCraftDamageX():
    AniBtlCraftDamageT(True, 0)

def AniBtlCraftDamageXKnockBack():
    AniBtlCraftDamageT(True, 5)

def AniBtlCraftDamageT(damage: bool, knockBack: float):
    def cb():
        status = AbnormalCondition.Deathblow | AbnormalCondition.Burn
        BattleChrCtrl(0xB7, 0x00, 0xFFFB, status, 0x000000FF, 0x000000FF, 0x00)
        # SetChrPos(0xFFFB, 0.0, -100.0, 0.0, 0.0)
        # ChrSetVisibleFlags(0x00, 0xFFFB, 0xFFFFFFFF)

    ForEachTarget(cb)

    def cb():
        if damage:
            BattleChrCtrl(0x00, 0xFFFB, 0xFFFE, 0x64)
        BattleChrCtrl(0x01, 0xFFFB, (0xEE, knockBack, 0x0), (0xEE, 0.5, 0x0), 0x01)

    ForEachTarget(cb)

    Return()

def AniBtlStart():
    OP_3B(0x39, 0xFFFE)
    # CreateThread(0xFFFF, 3, ScriptId.Current, 'AniBtlUndead')
    Return()

def AniBtlMove():
    LoadEffect(0xFFFE, 0x90, 'battle/cr000_02_1.eff')
    LoadEffect(0xFFFE, 0x94, 'battle/cr000_02_5.eff')

    Call(0x0B, 'SpringOff')
    SetEndhookFunction('SpringOn', 0x0B)

    CameraCtrl(0x00)
    ChrTurnDirection(0xFFFE, 0xFFF5, 0.0, 1)
    OP_33(0x47)

    PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT00_03', 0x01, 0x00, 0x00, 0x00, 0x00, 0.2, 0, 1.0, -1.0, 0x00, 0x00)
    # PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT00_02', 0x00, 0x01, 0x00, 0x00, 0x00, 0.2, 10.4, 10.8, -1.0, 0x00, 0x00)
    Sleep(50)
    # PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT00_01', 0x00, 0x00, 0x00, 0x00, 0x00, 0.2, -1.0, -1.0, -1.0, 0x00, 0x00)
    Sleep(100)

    ChrCreateAfterImage(0xFFFE)
    ChrSetAfterImageOn(0xFFFE, 0.1, 0.1, 0.22, 0.45, 1.0)

    PlayEffect(0xFFFE, (0xFF, 0x94, 0x0), 0xFFFE, 0x00000003, (0xDD, ''), (0xEE, 0.0, 0x0), (0xEE, 0.0, 0x0), (0xEE, 0.0, 0x0), 0.0, 0.0, 0.0, (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), 0xFF)
    PlayEffect(0xFFFE, (0xFF, 0x90, 0x0), 0xFFFE, 0x00000003, (0xDD, ''), (0xEE, 0.0, 0x0), (0xEE, 1.0, 0x0), (0xEE, 0.0, 0x0), 0.0, 0.0, 0.0, (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), 0xFF)
    PlaySound(0xFB1)

    CameraCtrl(0x0A, 0.02, 0.008, 0.0, 0x0064, 0x00FA, 0x0064, 0x0000, 0x0000, 0x00)
    ChrSetPosByTarget(0xFFFE, 0xFFF5, 0.0, 0.0, -1.5, 6.0, 0x00, 0x00)
    CameraCtrl(0x16, 0x02, 5.5, 0x03E8)
    OP_33(0x3A, 0xFFFE)

    ChrSetAfterImageOff()

    # PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT00_02', 0x00, 0x00, 0x00, 0x00, 0x00, 0.5, -1.0, -1.0, -1.0, 0x00, 0x00)
    PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT00_02', 0x00, 0x01, 0x00, 0x00, 0x00, 0.2, 9.75, 11.8, -1.0, 0x00, 0x00)
    ChrSetPosByTarget(0xFFFE, 0xFFF5, 0.0, 0.0, 0.0, 2.0, 0x00, 0x00)
    Sleep(200)
    OP_33(0x47)

    Call(ScriptId.Current, 'AniBtlWait')
    Sleep(500)

    Call(ScriptId.BtlCom, 'ReleaseEffect')

    Return()

def AniBtlAria():
    OP_0C(0x00, 0x01)
    OP_0E(0x00, 0x00, 0x00)
    OP_0C(0x00, 0x01)
    OP_0E(0x00, 0x01, 0x01)
    OP_0C(0x00, 0x01)
    OP_0E(0x00, 0x02, 0x02)
    OP_0C(0x00, 0x01)
    OP_0E(0x00, 0x03, 0x03)

    If(
        (
            (Expr.Eval, "OP_33(0x62, 0xFFFE, 0x0E)"),
            Expr.Return,
        ),
        'loc_12D7',
    )

    OP_33(0x3C, 0xFFFE, 0xFFFB, 0, 0.5)
    EffectCtrl(0x0C, 0xFFFE, (0xFF, 0x7D9, 0x0), 0xFFFE, 0x00000021, (0xDD, ''), (0xEE, 0.0, 0x0), (0x33, 0x3, 0x0), (0xEE, 0.0, 0x0), 0, 0, 0, (0x33, 0x2, 0x0), (0x33, 0x2, 0x0), (0x33, 0x2, 0x0), 0x00)
    PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT01_00', 0x01, 0x00, 0x00, 0x00, 0x00, 0, -1, -1, -1, 0x00, 0x00)
    SetChrFace(0x03, 0xFFFE, '7', '0', '', '#b', '0')

    Jump('loc_13DF')

    def _loc_12D7(): pass

    label('loc_12D7')

    CameraCtrl(0x00)
    OP_33(0x47)
    OP_33(0x48, 0xFFFE)
    OP_33(0x46, 0.25, 6, 15)
    OP_33(0x3C, 0xFFFE, 0xFFFB, 0, 0.5)
    EffectCtrl(0x0C, 0xFFFE, (0xFF, 0x7D9, 0x0), 0xFFFE, 0x00000021, (0xDD, ''), (0xEE, 0.0, 0x0), (0x33, 0x3, 0x0), (0xEE, 0.0, 0x0), 0, 0, 0, (0x33, 0x2, 0x0), (0x33, 0x2, 0x0), (0x33, 0x2, 0x0), 0x00)
    OP_3B(0x00, (0xFF, 0x8B7E, 0x0), 1, (0xFF, 0x0, 0x0), 0, 0, 0x0000, 0xFFFF, 0, 0, 0, 0, '', 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000)
    OP_3B(0x3A, 0xFFFE, (0x33, 0x0, 0x0), (0x33, 0x1, 0x0), (0xFF, 0x0, 0x0), (0xFF, 0x0, 0x0))
    SetChrFace(0x03, 0xFFFE, '7', '1', '', '#b', '0')
    PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT01_00', 0x01, 0x00, 0x00, 0x00, 0x00, 0.4, -1, -1, -1, 0x00, 0x00)
    Sleep(1500)
    SetChrFace(0x03, 0xFFFE, '7', '0', '', '#b', '0')

    def _loc_13DF(): pass

    label('loc_13DF')

    Return()

def AniBtlArts():
    OP_0C(0x00, 0x01)
    OP_0E(0x00, 0x00, 0x00)
    OP_0C(0x00, 0x01)
    OP_0E(0x00, 0x01, 0x01)
    CameraCtrl(0x00)
    OP_33(0x47)
    OP_33(0x48, 0xFFFE)
    OP_33(0x46, 0.25, 6, 15)
    OP_33(0x4B, 0x00FA, 0x03)
    OP_33(0x3C, 0xFFFE, 0xFFF5, 0, 0.5)
    PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT01_01', 0x00, 0x00, 0x00, 0x00, 0x00, 0.2, -1, -1, -1, 0x00, 0x00)
    Sleep(400)
    SetChrFace(0x03, 0xFFFE, '6', 'B', '', '#b', '0')
    OP_3B(0x3A, 0xFFFE, (0x33, 0x0, 0x0), (0x33, 0x1, 0x0), (0xFF, 0x0, 0x0), (0xFF, 0x0, 0x0))
    WaitAnimeClip(0xFFFE, 0, 0x00)
    PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT01_01a', 0x01, 0x00, 0x00, 0x00, 0x00, 0.2, -1, -1, -1, 0x00, 0x00)

    If(
        (
            (Expr.GetChrWork, 0xFFFE, 0x8),
            (Expr.PushLong, 0x3F),
            Expr.Equ,
            Expr.Return,
        ),
        'loc_1686',
    )

    EffectCtrl(0x0C, 0xFFFE, (0xFF, 0x7DB, 0x0), 0xFFE1, 0x00000003, (0xDD, 'NODE_CENTER'), (0xEE, 0.0, 0x0), (0xEE, 0.0, 0x0), (0xEE, 0.0, 0x0), 0, 0, 0, (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), 0xFF)

    Jump('loc_16D4')

    def _loc_1686(): pass

    label('loc_1686')

    EffectCtrl(0x0C, 0xFFFE, (0xFF, 0x7DB, 0x0), 0xFFFE, 0x00000003, (0xDD, 'NODE_CENTER'), (0xEE, 0.0, 0x0), (0xEE, 0.0, 0x0), (0xEE, 0.0, 0x0), 0, 0, 0, (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), 0xFF)

    def _loc_16D4(): pass

    label('loc_16D4')

    OP_3B(0x00, (0xFF, 0x8B7F, 0x0), 1, (0xFF, 0x0, 0x0), 0, 0, 0x0000, 0xFFFF, 0, 0, 0, 0, '', 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000)
    Sleep(500)
    CameraCtrl(0x00)
    OP_33(0x47)
    OP_33(0x05, 0x00, '')
    OP_33(0x06, 0x00)
    SetChrFace(0x03, 0xFFFE, '0', '0', '', '#b', '0')
    PlayChrAnimeClip(0xFFFE, 'BTL_CRAFT01_01a', 0x00, 0x00, 0x00, 0x00, 0x00, 0.2, -1, -1, -1, 0x00, 0x00)
    WaitAnimeClip(0xFFFE, 0, 0x00)
    EffectCtrl(0x12, 0xFFFE, 0x07DB)

    Return()

def AniBtlAttack():
    LoadEffect(0xFFFE, 0x90, 'battle/cr000_02_1.eff')
    LoadEffect(0xFFFE, 0x91, 'battle/cr000_02_5.eff')

    CameraCtrl(0x00)
    BattleChrCtrl(0x47)
    BattleChrCtrl(0x48, 0xFFFE)
    BattleChrCtrl(0x48, 0xFFFB)
    BattleChrCtrl(0x46, 0.25, 6.0, 15.0)

    # Call(ScriptId.BtlCom, 'AniBtlMove')

    ChrTurnDirection(0xFFFE, 0xFFFB, 0.0, -1.0)
    ChrCreateAfterImage(0xFFFE)
    PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x00, 0x01, 0x00, 0x00, 0x00, 0.2, 66.6667, 67.2, -1.0, 0x00, 0x00)
    WaitAnimeClip(0xFFFE, 0.0, 0x00)

    PlayEffect(0xFFFE, (0xFF, 0x91, 0x0), 0xFFFE, 0x00000003, (0xDD, ''), (0xEE, 0.0, 0x0), (0xEE, 0.0, 0x0), (0xEE, 0.0, 0x0), 0.0, 0.0, 0.0, (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), 0xFF)
    PlayEffect(0xFFFE, (0xFF, 0x90, 0x0), 0xFFFE, 0x00000003, (0xDD, ''), (0xEE, 0.0, 0x0), (0xEE, 1.0, 0x0), (0xEE, 0.0, 0x0), 0.0, 0.0, 0.0, (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), 0xFF)
    PlaySound(0xFB1)
    ChrSetPosByTarget(0xFFFE, 0xFFFB, 0.0, 0.0, -4.0, 7.0, 0x00, 0x00)

    PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x01, 0x01, 0x00, 0x01, 0x00, 0.2, 67.2333, 67.4333, -0.0333333, 0x00, 0x00)

    If(
        (
            (Expr.Eval, "BattleChrCtrl(0x62, 0xFFFE, 0x0A)"),
            (Expr.PushLong, 0x2),
            Expr.Neq,
            Expr.Return,
        ),
        'loc_7F57',
    )

    If(
        (
            (Expr.Eval, "IsBattleModelEqualTo(0xFFFE, 'C_CHR033_C00')"),
            Expr.Return,
        ),
        'loc_7F3B',
    )

    OP_3B(0x3A, 0xFFFE, (0xFF, 0x1B8A, 0x0), (0xFF, 0x1B8B, 0x0), (0xFF, 0x0, 0x0), (0xFF, 0x0, 0x0))

    Jump('loc_7F57')

    def _loc_7F3B(): pass

    label('loc_7F3B')

    OP_3B(0x3A, 0xFFFE, (0xFF, 0x1B5E, 0x0), (0xFF, 0x1B5F, 0x0), (0xFF, 0x0, 0x0), (0xFF, 0x0, 0x0))

    def _loc_7F57(): pass

    label('loc_7F57')

    OP_6C(0xFFFE, 1.0)
    ChrSetAfterImageOn(0xFFFE, 0.1, 0.1, 0.22, 0.45, 1.0)
    SetChrFace(0x03, 0xFFFE, '2', '2', '', '#b', '0')
    PlayEffect(0xFFFE, (0xFF, 0x82, 0x0), 0xFFFE, 0x0000000C, (0xDD, ''), (0xEE, 0.0, 0x0), (0xEE, 0.5, 0x0), (0xEE, 0.0, 0x0), 0.0, 0.0, 0.0, (0xEE, 0.75, 0x0), (0xEE, 0.75, 0x0), (0xEE, 0.75, 0x0), 0xFF)
    OP_3B(0x00, (0xFF, 0x8FAE, 0x0), 0.7, (0xFF, 0x0, 0x0), 0.0, -2.0, 0x0000, 0xFFFF, 0.0, 0.0, 0.0, 0.0, '', 0x04B0, 0x012C, 0x0000, 0x04B0, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000)
    CreateThread(0xFFFE, 0x02, ScriptId.Current, 'AniBtlAttackDamage01')
    CameraCtrl(0x0A, 0.3, 0.25, 0.1, 0x001E, 0x03E8, 0x0190, 0x0000, 0x0000, 0x00)
    OP_5E(0x00, 0x0002, 0.15, 0x001E, 0x03E8, 0x02BC, 0.3, 0xFFFF, -9000.0, -9000.0, -9000.0)
    Sleep(166)
    Sleep(166)
    WaitForThreadExit(0xFFFE, 0x02)
    CreateThread(0xFFFE, 0x02, ScriptId.Current, 'AniBtlAttackDamage01')
    Sleep(166)
    Sleep(166)
    WaitForThreadExit(0xFFFE, 0x02)
    CreateThread(0xFFFE, 0x02, ScriptId.Current, 'AniBtlAttackDamage01')
    Sleep(333)
    ChrSetAfterImageOff()
    Sleep(166)
    ChrSetAfterImageOn(0xFFFE, 0.1, 0.1, 0.22, 0.45, 1.0)
    PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x00, 0x01, 0x00, 0x00, 0x00, 0.4, 68.3, 68.5, -1.0, 0x00, 0x00)
    OP_6C(0xFFFE, 0.5)
    WaitAnimeClip(0xFFFE, 0.0, 0x00)
    PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x00, 0x01, 0x00, 0x00, 0x00, 0.4, 68.5333, 68.6, -1.0, 0x00, 0x00)
    OP_6C(0xFFFE, 0.4)
    WaitAnimeClip(0xFFFE, 0.0, 0x00)
    PlayChrAnimeClip(0xFFFE, 'BTL_ATTACK', 0x00, 0x01, 0x00, 0x00, 0x00, 0.05, 68.6333, -1.0, -1.0, 0x00, 0x00)
    BattleChrCtrl(0x47)
    BattleChrCtrl(0x48, 0xFFFB)
    BattleChrCtrl(0x46, 0.5, 6.0, 15.0)
    PlayEffect(0xFFFE, (0xFF, 0x83, 0x0), 0xFFFE, 0x0000000C, (0xDD, ''), (0xEE, 0.0, 0x0), (0xEE, 0.0, 0x0), (0xEE, 0.0, 0x0), 0.0, 0.0, 0.0, (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), (0xEE, 1.0, 0x0), 0xFF)
    CameraCtrl(0x0A, 0.64, 0.3, 0.2, 0x001E, 0x0258, 0x0258, 0x0000, 0x0000, 0x00)
    OP_5E(0x00, 0x0002, 0.25, 0x001E, 0x02BC, 0x02BC, 0.45, 0xFFFF, -9000.0, -9000.0, -9000.0)
    OP_3B(0x00, (0xFF, 0x8F62, 0x0), 0.8, (0xFF, 0x0, 0x0), 0.0, -1.0, 0x0000, 0xFFFF, 0.0, 0.0, 0.0, 0.0, '', 0x05DC, 0x012C, 0x0000, 0x05DC, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000)
    OP_3B(0x00, (0xFF, 0x8F66, 0x0), 0.5, (0xFF, 0x0, 0x0), 0.0, 0.0, 0x0000, 0xFFFF, 0.0, 0.0, 0.0, 0.0, '', 0x05DC, 0x012C, 0x0000, 0x05DC, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000)
    CreateThread(0xFFFE, 0x02, ScriptId.Current, 'AniBtlAttackDamage01')
    SetChrFace(0x03, 0xFFFE, '2', '0', '', '#b', '0')
    Sleep(133)
    OP_6C(0xFFFE, 0.2)
    ChrSetAfterImageOff()
    Sleep(266)
    OP_6C(0xFFFE, 1.0)
    WaitAnimeClip(0xFFFE, 0.0, 0x00)
    WaitForThreadExit(0xFFFE, 0x02)

    Call(ScriptId.BtlCom, 'ReleaseEffect')
    Return()
