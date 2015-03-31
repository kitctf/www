---
layout: post
title: "Advanced Heap Exploitation: 0CTF 2015 'freenote' writeup"
categories: writeups 0CTF2015
tags: exploitation
author: saelo, eboda
---

*freenote* was a pwnable worth 400 points during 0CTF 2015.

We're provided with a [binary](https://github.com/kitctf/writeups/raw/master/0CTF2015/freenote/freenote) as well as the IP address and port of the target server.
Here's an excerpt from running the binary:

    $ ./freenote
    == 0ops Free Note ==
    1. List Note
    2. New Note
    3. Edit Note
    4. Delete Note
    5. Exit
    ====================
    Your choice: 2
    Length of new note: 10
    Enter your note: AAAAAAAAA
    Done.
    == 0ops Free Note ==
    1. List Note
    2. New Note
    3. Edit Note
    4. Delete Note
    5. Exit
    ====================
    Your choice: 3
    Note number: 0
    Length of note: 15
    Enter your note: BBBBBBBBBBBBBB
    Done.
    == 0ops Free Note ==
    1. List Note
    2. New Note
    3. Edit Note
    4. Delete Note
    5. Exit
    ====================
    Your choice: 1
    0. BBBBBBBBBBBBBB

    == 0ops Free Note ==
    1. List Note
    2. New Note
    3. Edit Note
    4. Delete Note
    5. Exit
    ====================
    Your choice: 5
    Bye

##Reversing + Bug Discovery

Reverse engineering the binary is fairly simple. Here are the key points:

- All notes are stored on the heap, chunk sizes are rounded up to the next multiple of 0x80 bytes
- There's a table storing the pointers to the notes as well as their size and a flag indicating whether they are currently in use
- The table can store up to 256 notes and is also allocated on the heap during program initialization
- Upon deleting a note the corresponding chunk is freed and the in\_use flag is cleared in the table

The bug is also fairly simple to discover: The delete\_note function never checks if the note that is to be deleted is actually in use. With this we can delete a note twice, resulting in a controlled double free condition.

The heap of the target process will roughly look like this:

    +----------------------------------------------+----------+----------+--------
    |                    Table                     |  Note 1  |  Note 2  | Unused
    | n | m | note1 entry | note2 entry | ...      |          |          |
    +----------------------------------------------+----------+----------+--------

Where n indicates the number of available slots in the table (256) and m holds the number of used slots (two in the above example).

##Heap Basics

Glibc malloc manages heap chunks using the structure shown below.

{% highlight C %}
struct malloc_chunk {

  INTERNAL_SIZE_T      prev_size;  /* Size of previous chunk (if free).  */
  INTERNAL_SIZE_T      size;       /* Size in bytes, including overhead. */

  struct malloc_chunk* fd;         /* double links -- used only if free. */
  struct malloc_chunk* bk;

  /* Only used for large blocks: pointer to next larger size.  */
  struct malloc_chunk* fd_nextsize; /* double links -- used only if free. */
  struct malloc_chunk* bk_nextsize;
};
{% endhighlight %}

The pointer returned to the client points to 'fd' as the two pointers, fd and bk, are only used when the chunk is free. Then they form a doubly linked list of free chunks. Since chunks sizes are always even numbers, the LSB of the size field is not used. It is thus used to indicate whether the *previous* chunk is in use. This allows for some elegant heap managment, I encourage you to read through the malloc implementation in glibc/malloc/malloc.c if you're interested in this.

For the sake of this post it suffices to know that a malloc() operation returns the first free chunk for the appropriate size and unlinks it from the freelist. An unlink operation basically performs

    chunk->bk->fd = chunk->fd;
    chunk->fd->bk = chunk->bk;

A free() on the other hand performs roughly the following operations:

- Some basic consistency checks of the size field (i.e. size >= min\_size and size <= max\_size)
- Make sure there is a valid chunk following the current chunk and that the current chunk is marked as in use (next\_chunk->size & 0x1 == 1)
- Make sure that the current chunk is not at the top of the corresponding freelist (indicating a double free). Note that malloc does not traverse the whole freelist (performance > security), so if the same chunk is already somewhere else in the freelist, malloc will not notice it and happily free the chunk again
- Check if the next chunk or the previous chunk are also free
- If so, coalescate the current chunk with these, unlinking the other chunks first
- Link the current chunk into the corresponding freelist by setting the FD and BK pointers

To mitigate exploitation of the unlink mechanism (which basically results in an arbitrary write when controlling both pointers, see the code above), glibc implements what is called "safe unlinking". Basically the idea is that if FD and BK are valid pointers, then the chunk they point to will point back to the current chunk.

             Chunk 1                     Chunk 2
        +---------------+           +---------------+
        |               |           |               |
        |      fd  ---------------->|      fd  --------->
        |               |           |               |
    <--------  bk       |<---------------  bk       |
        |               |           |               |
        +---------------+           +---------------+

Here second\_chunk->bk-\>fd points back to itself. This is what glibc verifies before performing the actual unlink.

Here's the corresponding code from glibc

{% highlight C %}
#define unlink(P, BK, FD) {
    FD = P->fd;
    BK = P->bk;
    if (__builtin_expect (FD->bk != P || BK->fd != P, 0))
      malloc_printerr (check_action, "corrupted double-linked list", P);
    else {
        // unlink
        FD->bk = BK;
        BK->fd = FD;
        if (!in_smallbin_range (P->size)
            && __builtin_expect (P->fd_nextsize != NULL, 0)) {
            /* not the case */
            /* ... */
          }
      }
}
{% endhighlight %}

While this mechanism is pretty effective, there are still ways to exploit the unlink mechanism as this post will show.

##Heap Exploitation

One way to exploit a double free condition is to turn it into a UAF: at first allocate some object and free it for the first time. Then allocate another object of approximately the same size (and preferably containing some function pointers) on top of it. Free the first object again (thus freeing the second one which is still in use by the application) and allocate a third object on top of it that allows us to control parts of the underlying second object. The trigger e.g. a function call on the second object. However, in our case there was only one type of heap object that could be allocated by the user (a note), thus preventing this scenario.

With this we are left with manipulating chunk metadata to turn our double free into something more powerful, like an arbitrary write. First, however, we need a primitive to control the chunk metadata of a chunk we are going to free. We can do this as follows:

1. Allocate 2 notes, note1 and note2
2. Free both notes
3. Allocate a third note of size len(note1) + len(note2) that will be placed on top of the two notes
4. Fill its content in a way that builds a fake chunk at the position of the former note2
5. Free note2 again

So

    +------------------------------+------------------------------+
    |          Chunk 1             |            Chunk 2           |
    +------------------------------+------------------------------+
    0x60000                        0x60080

becomes

    +-------------------------------------------------------------+
    |          Chunk 3                                            |
    +-------------------------------------------------------------+
    0x60000                        0x60080

And chunk 2 is now fully controlled and can be freed again.

There are a couple of ways to turn heap memory corruption into an arbitrary write and thus RCE. Sometimes it is possible to create a fake chunk, for example in the .bss of the binary, then allocate that fake chunk and thus be able to corrupt data structures there (e.g. the GOT). [Example](https://github.com/kitctf/archive/blob/master/Hack.lu-2014/Oreo/exploit.py).
There are a couple of conditions that have to be met for such an attack to be successful though which were not met in our case.

Another way would be to somehow free the chunk holding the table data structure, then allocate a note there and overwrite a second note pointer to point into the GOT.
While it is possible to set the prev\_size of chunk2 above in such a way that it points to the table chunk and then free it, malloc will refuse to coalescate the two chunks as the table chunk is currently in use (there are no valid fd and bk pointers).

So, what else can we do? Remember the check for safe unlinking: "FD-\>bk != P \|\| BK-\>fd != P". Basically we will only be able to unlink a chunk if we can find one (or two) pointer(s), pointing to that chunk. Well, there are pointers to the notes in the table, right? So what if we set FD and BK of a chunk to point back into the table? When unlinking that chunk, malloc will do

    FD->bk = BK;
    BK->fd = FD;

bk points into the table, fd points into the table, resulting in the table entry pointing to itself after a sucessful unlink! With this we are then able to overwrite the following entries in the table (by writing to the manipuated note), giving us an arbitrary read and write primitive.

There's a little catch though, the pointers in the note table are "client" pointers while malloc expects internal pointers. The difference is that client pointers point to the first usable address of a chunk (and thus to the address of the FD member) while malloc pointers point to the beginning of the chunk. The two are 16 bytes apart.
To solve this we can either create two notes, 16 bytes apart (we will need some heap metadata corruption for this as the notes are only allocated in multiples of 0x80) or just do the following:

1. Allocate 3 chunks
2. Free the second and the third and allocate a fourth one on top of the two
3. Overwrite what was previously chunk 3 and change the prev\_size so that it points to the beginning of the controlled data in chunk 1
4. Create a fake chunk in chunk 1, set FD and BK to point back into the note table

At this point we have what looks like a valid free chunk to malloc in chunk 1:

    +--------------------------+--------------------------+--------------------------+
    |        Chunk 1           |          Chunk 2         |          Chunk 3         |
    +--------------------------+--------------------------+--------------------------+
    0x60000                    0x60080                    0x60100


    +--------------------------+-----------------------------------------------------+
    |         Chunk 1          |          Chunk 4                                    |
    +--------------------------+-----------------------------------------------------+
    0x60000                    0x60080                    0x60100


    +--------------------------+-----------------------------------------------------+
    |         Chunk 1          |          Chunk 4                                    |
    |   Fake chunk, FD and BK  |                          prev_size points to the    |
    |   point into the table   |                          fake chunk in Chunk 1      |
    +--------------------------+-----------------------------------------------------+
    0x60000                    0x60080                    0x60100

Now freeing chunk 3 again will cause malloc to coalescate it whith the fake chunk set up in chunk 1. Since coalescing involves unlinking the previous chunk, we get our unlink primitive and the table entry will afterwards point to itself. From there its easy going, point a note into the GOT, read a pointer from there and overwrite e.g. atoi with the address of system. Game over :)\\
The GOT is writable and at a static address, but even if the binary was compiled as PIE we could bypass that as we can leak a libc address (see below) from which the binary will be at a static offset [[ref](http://cybersecurity.upv.es/attacks/offset2lib/offset2lib.html)].

For the above attack to work we will have to know the address of the note table in memory. Using our first primitive, leaking a heap address is fairly simple though:

1. Allocate 4 chunks.
2. Free chunk 3 and chunk 1 (in that order, so that malloc writes the two pointers into chunk 1). 
3. Allocate another chunk of size 1 (or 8). This chunk will be placed where chunk 1 used to be and where its FD and BK pointers still are, with the BK pointer pointing to chunk 3.
4. Print the notes, since this is a %s print, we can leak the FD (or BK if chosen size in step 3 was 8) pointer of chunk 1 which in our case points to chunk 3 (heap memory)!

 This same technique can be used to leak a libc address (the head of the freelist is in the .bss of the libc). Simply follow the same steps, but now it suffices to allocate chunks 1 and 2 and free the first. 



##Putting the final exploit together

At this point we are ready for the final part, putting the exploit together. The exploit contains five steps:

1. Leak the libc address with the technique described above. 
2. Leak a pointer into the heap, again as described already. This address is needed to calculate the position of the note table. You will have to calculate the offset beforehand, it will always be the same.
3. Create a fake chunk containing pointers into the note table. Manipulate the following chunks prev_size in such a way that it points to our fake chunk. Free the second chunk, it will now write the pointers to the note table inside the note table: effectively replacing the pointer to our first chunk with a pointer to the note table itself.
4. With one of the note pointers actually pointing inside the note table now, overwrite the note table: Set the pointer of one of the notes to a function in the GOT. We chose to overwrite printf@GOT. Also set the "valid" flag for this note and its length to 8, you don't want to completely destroy the GOT.
5. Edit the note from step 3. This will overwrite the printf@GOT pointer. We can write a specific address inside the libc which directly spawns /bin/sh when we jump to it (from [[Dragon's notes on CTF](http://j00ru.vexillium.org/?p=2485)]). The exact address can be calculated from the leaked libc address in step 1 and an offset (which can be looked up since the libc version was given).


The exploit in action:

    [+] libc @ 0x7fc0c322c7b8
    [+] heap @ 0x167de50
    [+] Exploiting double free
    [+] Overwriting note table
    [+] Overwriting printf@GOT
    [+] Shell ready:
    id
    uid=1001(freenote) gid=1001(freenote) groups=1001(freenote)
    cat /home/freenote/flag
    0ctf{freenote_use_free_to_get_flag}

The full exploit code can be found [here](https://github.com/kitctf/writeups/blob/master/0CTF/freenote/exploit.py).
