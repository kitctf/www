<img src="/talks/2023-04-13-advancedGhidra/43f334f3-76d1-4d77-9405-34c21f8ab974.png" height=500>
Taming the dragon

Advanced Ghidra by Simon & Liam

---

## We had a structure for this talk


<small>surely</small>

----

## but then we needed to add some elements in the middle...
<img src="/talks/2023-04-13-advancedGhidra/1edad03a-9f4e-4b5e-bf28-108f1acf6407.png" height=200>


----

## now it is all confusing

----

## see this as a random list of unsorted bits and bytes about Ghidra

---

Ever wondered about:

![](/talks/2023-04-13-advancedGhidra/cb1b2c1f-f12a-4749-8987-6fd4d92cb349.png)

----

you need to place just the right version of a copyrighted pdf here
![](/talks/2023-04-13-advancedGhidra/6b617302-729b-47fa-8741-ac60a1cb4dad.png)
this is pain

----

Just use this script: https://github.com/meenmachine1/ghidra-manuals
![](/talks/2023-04-13-advancedGhidra/71c120bb-8fb1-4d1c-898e-e92ca3b59bb1.png)

---

## Ghidra is a team player

----

## reversing is about combining the tools

----

## Level 1: Decompiler 🤝 Debugger

We want to set a breakpoint on main for a stripped binary

----

1. Check the memory map in Ghidra
<img src="/talks/2023-04-13-advancedGhidra/a1003c1e-745b-49b2-836d-d09b920689de.png" height=500>

----

2. Subtract from address in disassembly


![](/talks/2023-04-13-advancedGhidra/a627b517-8068-44af-a9e1-06417ec62346.png)

----

3. Check where the binary is mapped in debugger
<img src="/talks/2023-04-13-advancedGhidra/167b5e62-32a5-4159-8dfb-a5620aebeee4.png" height=500>

----

4. Set a breakpoint
                                                                                        
![](/talks/2023-04-13-advancedGhidra/09620860-a4f0-4678-9de5-9fe12ea1b640.png)

----

## Level 1.5: Decompiler 🤝 Debugger

pwndbg can help you
                                                                                        
![](/talks/2023-04-13-advancedGhidra/9488d8b4-c0c6-4e7b-a87d-3f46ac0c6ab1.png)

----

## Level 2: Decompiler 🤝 Debugger

pwndbg + r2ghidra is your friend

Install https://github.com/radareorg/r2ghidra and

![](/talks/2023-04-13-advancedGhidra/ae556598-e942-4c87-a248-5cc0ce98771b.png)


----

<img src="/talks/2023-04-13-advancedGhidra/5765c943-ba92-4d5b-8cc5-b49880af5279.png" height=700>

----

## Level 3: Decompiler 🤝 Debugger

pwndbg + decomp2dbg = :heart:

deomp2dbg syncs the Ghidra decompilation with gdb

----

* Install from https://github.com/mahaloz/decomp2dbg
* For the newest Ghidra you have to compile the plugin repo separately and place it into the plugin folder
* @ju256 also works for IDA
* @peopleUsingSaneTooling also works for Binja

---

## pcode is cool

----

## someone wrote an emulator for pcode

----

## now we have an emulator for all Ghirda architectures
### (a lot)

----

## check out https://github.com/Nalen98/GhidraEmu

---

## Ghidra is scriptable

----

## in Java and cursed Python 2

### https://github.com/mandiant/Ghidrathon adds Python 3 support

----

## have a look at the script manager

----

## a few random mentions:

* All RTTI scripts
* yara signatures
* ShowCCallsScript
* XorMemoryScript.java
* CreateStructure.java
    * "Automatically creates a structure definition based on the references seen to the structure."

----

How to write our own plugin?
* Option 1 built-in Texteditor in Ghidra
* Option 2 Eclipse official Plugin
* Option 3 IntellJ: https://reversing.technology/2019/11/18/ghidra-dev-pt1.html

---

Someone **statically** linked $LIBRARY, **stripped** the binary and now Ghidra looks like this:

----

<img class="fragment" data-fragment-index="1" height="550px" src="/talks/2023-04-13-advancedGhidra/61b0047d-f51f-4599-a1f0-dac0d4cd1380.png"/>
<img class="fragment" data-fragment-index="2" height="550px" src="/talks/2023-04-13-advancedGhidra/ff3bb8d9-0c06-4a66-82f8-9ae0d5823e56.png"/>
<img class="fragment" data-fragment-index="3" height="550px" src="/talks/2023-04-13-advancedGhidra/d25d3eaa-8b58-4934-a52a-3ded326068ef.png"/>
<img class="fragment" data-fragment-index="4" height="550px" src="/talks/2023-04-13-advancedGhidra/ca1fadb9-0ffc-46b4-8b94-90188aefe905.png"/>
<p class="fragment" data-fragment-index="5">
So much FUN 😬
</p>


----

## What now?

----

## Function IDs

- **Function identification** based on function **body hash**
- IDA has FLIRT signatures

---

## Creating a Function ID Database - Demo

----

## Creating a Function ID Database - I

- Import `.so` with symbols into Ghidra, decompile it
- "Tools" -> "Function ID" -> "Create new empty FidDb..."
![](/talks/2023-04-13-advancedGhidra/86266390-d21e-441e-973c-71a07dd37736.png)
- Enter a filename "$LIBRARY.fidb"

----

## Creating a Function ID Database - II

- "Tools" -> "Function ID" -> Populate FidDb from programms..."
![](/talks/2023-04-13-advancedGhidra/a1c4d835-602e-43db-9c7f-7c1be64ee6a4.png)

----

## Creating a Function ID Database - III
- Add library name, version and variant are not really relevant for us
- Select a root folder. **ALL files** in that folder will be added to the database

<img height="450px" src="/talks/2023-04-13-advancedGhidra/39c721c4-85e6-494b-836f-ce0ee6de201d.png"/>
<img height="450px" src="/talks/2023-04-13-advancedGhidra/5fbeff43-c6e6-46df-9f99-5e9acbad6468.png"/>

----

## Creating a Function ID Database - IV
🎉 Your database is ready

![](/talks/2023-04-13-advancedGhidra/120832c8-3f7c-4533-8116-43f8a4490450.png)


----

## RESTART GHIDRA (YES, REALLY!)

Without this, Ghidra seems to not apply function IDs!

---

<p>
<span class="fragment" data-fragment-index="1">Before:</span>
<img class="fragment" data-fragment-index="1" src="/talks/2023-04-13-advancedGhidra/5425b09d-8538-49cc-92b0-c2a50f762033.png"/>
<span class="fragment" data-fragment-index="2">After:</span>
<img class="fragment" data-fragment-index="2" src="/talks/2023-04-13-advancedGhidra/12bd21f4-5962-42f5-87c4-2893115d61d1.png"/>
</p>

----

## Troubleshooting & Tips
- Architecture used in database **must** match architecture of binary **exactly**. (RV64GC and RV64G is not the same!)
- Did you try ~~turning it on and off again~~ restarting Ghidra?

---

## Challenge

Task:
- Build a function ID database for `aes.a` (from https://github.com/kokke/tiny-AES-c)
- Apply it to `challenge_stripped`.
- Find the flag for `challenge_stripped` **without** running it.

(Files are [here](https://github.com/kitctf/www/blob/master/talks/2023-04-13-advancedGhidra/challenges.tar.gz))

---

## Custom Architectures or Yeah Another VM Challenge

----

We can just tell Ghidra about new architectures 🎉

----

Only Eclipse is officially supported.

----

(There is an unofficial [IntelliJ plugin](https://github.com/garyttierney/intellij-ghidra).)

---

## Adding an Architecture - Demo

----

## Micro-programmed Minimal Machine (MIMA)
Used at KIT to teach microprocessors.
Spec: https://github.com/Garmelon/mima-tools#specification

----

- "File" -> "New" -> "Other. ..." or (Strg+N) to open the new project wizard.
![](/talks/2023-04-13-advancedGhidra/f2457e54-86a3-45f8-916b-913d84786828.png)

----
![](/talks/2023-04-13-advancedGhidra/ac9a109b-34a4-494e-ba0c-b098c8e49c4b.png)

----

![](/talks/2023-04-13-advancedGhidra/e5752cae-db73-4eaf-9ef0-d60311277f71.png)

----

```
$ tree mima/data
mima/data
├── buildLanguage.xml
├── languages
│   ├── skel.cspec
│   ├── skel.ldefs
│   ├── skel.opinion
│   ├── skel.pspec
│   ├── skel.sinc
│   └── skel.slaspec
├── README.txt
└── sleighArgs.txt

1 directory, 9 files
```

**Delete all skel.\* files**

----

## `.ldefs` - Language Definition
```xml
<?xml version="1.0" encoding="UTF-8"?>
<language_definitions>
    <language processor="mima"
              endian="big"
              size="24"
              variant="default"
              version="1.0"
              slafile="mima.sla"
              processorspec="mima.pspec"
              id="mima:24:default">
        <description>mima</description>
        <compiler name="default" spec="mima.cspec" id="default"/>
    </language>
</language_definitions>
<!-- See Relax specification: Ghidra/Framework/SoftwareModeling/data/languages/language_definitions.rxg -->
```

----

## `.pspec` - Processor Specification
Can be left completely empty like this:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<processor_spec>
</processor_spec>
<!-- See Relax specification: Ghidra/Framework/SoftwareModeling/data/languages/processor_spec.rxg -->
```

----

Can define program counter register
```xml
<?xml version="1.0" encoding="UTF-8"?>
<processor_spec>
  <programcounter register="iar"/>
</processor_spec>
<!-- See Relax specification: Ghidra/Framework/SoftwareModeling/data/languages/processor_spec.rxg -->
```


----

Or default symbols/entry points
```xml
<?xml version="1.0" encoding="UTF-8"?>
<processor_spec>
  <programcounter register="iar"/>
  <default_symbols>
    <symbol name="start" address="ram:0x133dd11" type="code" entry="true"/>
  </default_symbols>
</processor_spec>
<!-- See Relax specification: Ghidra/Framework/SoftwareModeling/data/languages/processor_spec.rxg -->
```

----

## `.cspec` - Compiler Specification
> Encode information about a target binary which is specific to the compiler that generated that binary.

----

Minimal content
```xml
<?xml version="1.0" encoding="UTF-8"?>
<compiler_spec>
  <default_proto>
    <prototype name="unknown" extrapop="unknown" stackshift="0">
      <input>
      </input>
      <output>
      </output>
    </prototype>
  </default_proto>
</compiler_spec>
<!-- See Relax specification: Ghidra/Framework/SoftwareModeling/data/languages/compiler_spec.rxg -->
```

----

Tell Ghidra that "ram" is globally accessible and where to find the stackpointer
```xml
<?xml version="1.0" encoding="UTF-8"?>
<compiler_spec>
  <global>
    <range space="ram"/>
  </global>
  <stackpointer register="sp" space="ram"/>
  <default_proto>
    <prototype name="unknown" extrapop="unknown" stackshift="0">
      <input>
      </input>
      <output>
      </output>
    </prototype>
  </default_proto>
</compiler_spec>
<!-- See Relax specification: Ghidra/Framework/SoftwareModeling/data/languages/compiler_spec.rxg -->
```

----

## `.sla`
Describes the instruction set.
Unreadable xml file.

----

**Generated based on `.slaspec`**

----

## `.slaspec`
Docs: `<GhidraInstallDirectory>/docs/languages/html/sleigh.html` (yeah apparently, no online version exists)

----

Bit endian, 3-byte alignment
```sql
define endian=big;
define alignment=3;
```

----

Define address spaces:
- ram: 3 byte addresses and 3 byte words
- register: 3 byte words
```sql
define space ram      type=ram_space wordsize=3 size=3 default;
define space register type=register_space size=3 ;
```

----

Define registers: 3 byte words, `iar`, `acc`, and `sp` register
```sql
define register offset=0x00 size=3 [ iar acc sp ];
```

----

Define tokens: layout of an instruction

```sql
#Small opcode:
#+----+ +-----------------------+
#| SO | |         Value/Address |
#+----+ +-----------------------+
#23  20 19                      0
define token small_inst(24)
	s_op  = (20,23)
	s_imm = ( 0,19)
;
```

----

`:FOO is TOKEN_1 & ... & TOKEN_N {}`
`FOO` is the name of the instruction that will be shown in the disassembler
A series of bits is a `FOO` instruction if it satisfies the bit pattern of `TOKEN_1` ... `TOKEN_N`

----

```python
:LDC is s_op=0x00 & s_imm {
}
```

----

Changing `:LDC` to `:LDC s_imm` means that in the disassembler `LDC immediate` will be shown
```python
:LDC s_imm is s_op=0x00 & s_imm {
}
```

----

For a disassembler I could have used Python, what's the point of this?

----

## Adding Semantics

```python
:LDC s_imm is s_op=0x00 & s_imm {
	acc = s_imm;
}
```

----

```python
:LDV s_imm is s_op=0x01 & s_imm {
	local target:3 = zext(s_imm:3);
	acc = *target;
}
```

----

With full semantics, Ghidras decompiler magically works!

---

Before
<img height="550px" src="/talks/2023-04-13-advancedGhidra/fca7c1ef-0571-4982-82b7-625405c6ee09.png"/>

----

After
<img height="550px" src="/talks/2023-04-13-advancedGhidra/341d4dee-82ea-4ab4-afaf-10435f03e728.png"/>

----

### Resources

- https://trenchant.io/expanding-the-dragon-adding-an-isa-to-ghidra/
- https://guedou.github.io/talks/2019_BeeRump/slides.pdf
- https://swarm.ptsecurity.com/creating-a-ghidra-processor-module-in-sleigh-using-v8-bytecode-as-an-example/
- https://spinsel.dev/2020/06/17/ghidra-brainfuck-processor-1.html

(Finished Ghidra processor can be found [here](https://github.com/kitctf/www/blob/master/talks/2023-04-13-advancedGhidra/challenges.tar.gz))

---

Questions? Comments?

![](/talks/2023-04-13-advancedGhidra/a9930763-ff34-46e6-8991-fdde9394ae2f.png)

---
