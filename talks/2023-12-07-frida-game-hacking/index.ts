import { log } from "./logger.js";

Interceptor.attach(Module.getExportByName(null, "send"), {
    onEnter(args) {
        const buffer = args[1].readUtf8String();
        log(`send("${buffer}")`);
    }
});

let flag = ''

Interceptor.attach(Module.getExportByName(null, "parse_buffer"), {
    onEnter(args) {
        const msg = args[0].readUtf8String()

        if(!msg) return

        const cmds = msg.split('\n')

        const sus = cmds.filter(c => c.startsWith('F')).map(c => c.substring(1)).join('')

        flag += sus

        log(`${sus} ${flag}`)
    }
})


const base = Module.getBaseAddress('craft')
const yPos = base.add(0x273c20).add(4)
const rot = yPos.add(12)

let flying = false


Interceptor.attach(Module.getExportByName(null, 'on_key'), {
    onEnter(args) {
        if (args[1].toUInt32() !== 290 || args[3].toUInt32() !== 1) {
            return
        }

        flying = !flying

        addMessage(`Hack status: ${flying ? 'on': 'off'}`)
    }
})


Interceptor.attach(Module.getExportByName(null, 'handle_movement'), {
    onEnter() {
        this.preY = yPos.readFloat()
    },
    onLeave() {
        if (flying) {
            yPos.writeFloat(this.preY + rot.readFloat() * .2)
        }

    }
})

const addMessagePtr = Module.getExportByName(null, 'add_message')
const addMessageNative = new NativeFunction(addMessagePtr, 'void', ['pointer'])

const addMessage = (msg: string) => {
    // tracks lifetimes on the js side
    const string = Memory.allocUtf8String(msg)
    addMessageNative(string)
}

Stalker.exclude(Process.getModuleByName('libc.so.6'))

Interceptor.attach(Module.getExportByName(null, "parse_buffer"), {
    onEnter(args) {
        this.buffer = args[0]

        const msg = this.buffer.readCString().toString().trim()

        if (!msg.startsWith('X')) return

        Stalker.follow(this.threadId, {
            events: {
                call: false,
                ret: false,
                exec: true,
                block: false,
                compile: false,
            },
            transform: (iterator: StalkerX86Iterator) => {
                let instruction = iterator.next();
                do {
                    console.log(instruction?.address, instruction);
                    iterator.keep();
                } while ((instruction = iterator.next()) !== null);
            },
        });

        this.stalking = true

        log('code check');
    },
    onLeave() {
        if (this.stalking) {
            Stalker.unfollow(this.threadId);
            log('Stopped tracing');
        }
    }
})
