import line
import os, sys, traceback

lines = line.Linepoll(
    authToken ="",
    email="",
    password="",
    device = "DESKTOPWIN",
    lhost = 'gxx.line.naver.jp' ,
)

def restarter():
    os.system('clear')
    _ = sys.executable
    os.execl(_, _,*sys.argv)

def receiverPreviewing(message, users=None):
    if message.toType == 0:
        if message._from != users:
            receiver = message._from
        else:
            receiver = message.to

    if message.toType == 1:
        receiver = message.to
    if message.toType == 2:
        receiver = message.to

    return receiver

def contentPreviewing(message):
    pass

def commander(text, rname, sname):
    cmd = ""
    pesan = text
    if pesan.lower().startswith(rname):
        pesan = pesan.replace(rname, "", 1)
        if " & " in text:
            cmd = pesan.split(" & ")
        else:
            cmd = [pesan]
    if pesan.lower().startswith(sname):
        pesan = pesan.replace(sname, "", 1)
        if " & " in text:
            cmd = pesan.split(" & ")
        else:
            cmd = [pesan]
    return cmd

def lineUnofficial(op):
    try:
        if op.type == 0:
            return

        if op.type == 13 or op.type == 124:
            if op.param3 == Line.profile.mid:
                try:
                    lines.acceptGroupInvitation(op.param1)
                except:pass

        if op.type == 26:
            msg = op.message
            if(msg.toType == 0 or msg.toType == 1 or msg.toType == 2):
                receiver = receiverPreviewing(op.message,users=lines.profile.mid)
                if msg.contentType == 0:
                    if msg.text is None:
                        return
                    else:
                        if(msg.text == "hi"):
                            lines.sendMessage(receiver, "Yes am i...")

        if op.type == 25:
            msg = op.message
            if(msg.toType == 0 or msg.toType == 1 or msg.toType == 2):
                receiver = receiverPreviewing(op.message,users=lines.profile.mid)
                if msg.contentType == 0:
                    if msg.text is None:
                        return
                    else:
                        txt = message.text.lower()
                        txt = " ".join(txt.split())
                        if txt.startswith(rname) or txt.startswith(sname):
                            cmds = commander(txt, rname, sname)
                        else:
                            cmds = []

                        for prefix in cmds:
                            if(prefix == 'reboot'):
                                try: lines.sendMessage(receiver,'rebooting....!')
                                except: pass
                                restarter()
                            elif(prefix == "Hello"):
                                line.sendMessage(receiver," Hai")

    except Exception:
        traceback.format_exc()

def main():
    while True:
        try:
            Ops =lines.singleTrace()
            if Ops is not None:
                for op in Ops:
                    lineUnofficial(op)
                    lines.setRevision(op.revision)
                    if op.type != 0:
                        print("OP->",lines.console.operations[op.type].replace("_","::"))
        except EOFError:
            return

if __name__=='__main__':
    main()
