---
layout: post
title: "Boston Key Party 2015 'Sullivan Square' writeup"
categories: writeups bkp2015
tags: reversing
author: niklasb
---

*Sullivan Square* was a reversing challenge worth 350 points at the Boston Key Party
CTF 2015.

We're given an
[archive](https://github.com/kitctf/writeups/raw/master/bkp2015/sullivan_square/trieharder.tar.gz.584eb2259dfcabe769faffa96b151020)
with compiled Rubinius bytecode and a serialized Ruby datastructure:

    distribute
    ├── cipher.rbc
    ├── run.sh
    ├── trie.dump
    ├── trie_harder.rbc
    └── trie.rbc

    0 directories, 5 files

The challenge description says that they used Rubinius 2.5.2 to compile the
Ruby files to bytecode. However, we were unable to get hold of a version of `rbx`
(the Rubinius interpreter) that was actually able to load the files as is. We
therefore
[patched the version and signature checks out of the loader](https://github.com/kitctf/writeups/blob/master/bkp2015/sullivan_square/rubinius-loader.patch)
to make it work.
[This](https://github.com/rubinius/rubinius/tree/40040f9956833ac13774d745e961c743eeeefcbb)
is the version of Rubinius that we used.

Now we can actually run the program:

                [*] Greetings to all of the eiltes here [*]
    --- I heard you guys all hate ruby, so I have decided to be nice---
                --- enjoy this great bytecode instead! ---


    So, you can tell me now... what's the flag? foo
    nop

Okay, let's see what we can figure out just by loading the two classes and
entering a nice shell:

{% highlight ruby %}
Rubinius::CodeLoader.require_compiled './cipher'
Rubinius::CodeLoader.require_compiled './trie'
require 'pry'
binding.pry
{% endhighlight %}

When run:

{% highlight ruby %}
From: /home/vagrant/sullivan/hack.2.rb @ line 4 :

    1: Rubinius::CodeLoader.require_compiled './cipher'
    2: Rubinius::CodeLoader.require_compiled './trie'
    3: require 'pry'
 => 4: binding.pry

[1] pry(main)> Cipher
=> Cipher
[3] pry(main)> Cipher.new
ArgumentError: method 'initialize': given 0, expected 1
from (pry):3:in `__script__'
[4] pry(main)> Cipher.new "abc"
NoMethodError: undefined method `each' on an instance of String.
from kernel/delta/kernel.rb:78:in `each (method_missing)'
[5] pry(main)> c = Cipher.new ["x", "y", "z"]
=> #<Cipher:0xbdb8
 @map=
  {:encrypt=>
    {"a"=>"x",
     "b"=>"y",
     "c"=>"z",
     "d"=>nil,
     "e"=>nil,
     ...
   :decrypt=>{"x"=>"a", "y"=>"b", "z"=>"c", nil=>" "}}>
[6] pry(main)> c.encrypt "aaabbbcccddd"
=> "xxxyyyzzz"
{% endhighlight %}

So apparently `Cipher` implements some kind of monoalphabetic
substitution. We still don't know what permutation of characters the program
uses to instantiate the cipher though.

At this point we decided to write a [simple bytecode
disassembler](https://github.com/niklasb/rbx-disas) to figure out the basics of
how the script works. Here is the relevant part of the `trie_harder.rbc`
script:

{% highlight ruby %}
...
0063:  push_self
0064:  push_literal        "So, you can tell me now... what's the flag? "
0066:  string_dup
0067:  allow_private
0068:  send_stack          :print, 1
0071:  pop
0072:  push_self
0073:  send_method         :gets
0075:  send_stack          :chomp, 0
0078:  set_local           0    # flag
0080:  pop
0081:  push_const_fast     :File
0083:  push_literal        "trie.dump"
0085:  string_dup
0086:  send_stack          :read, 1
0089:  set_local           1    # dumped
0091:  pop
0092:  push_const_fast     :Marshal
0094:  push_local          1    # dumped
0096:  send_stack          :load, 1
0099:  set_local           2    # t
0101:  pop
0102:  push_local          2    # t
0104:  push_local          0    # flag
0106:  send_stack          :get, 1
0109:  set_local           3    # res
0111:  pop
0112:  push_local          3    # res
0114:  send_stack          :nil?, 0
0117:  send_stack          :!, 0
0120:  goto_if_false       0131:
0122:  push_self
0123:  push_local          3    # res
0125:  allow_private
0126:  send_stack          :puts, 1
0129:  goto                0139:
0131:  push_self
0132:  push_literal        "nop"
0134:  string_dup
0135:  allow_private
0136:  send_stack          :puts, 1
...
{% endhighlight %}

The VM is a stack machine. We can see that the script calls
`Marshal.load(File.read("trie.dump"))` to deserialize an object from the
`trie.dump` file. Let's try to do the same thing and inspect the result:

{% highlight ruby %}
[1] pry(main)> Marshal.load(File.read("trie.dump"))
=> #<Trie:0xaae8
 @root=
  #<Trie::Node:0xaaf0
   @char="W",
   @end=false,
   @left=
    #<Trie::Node:0xaaf8
     @char="D",
     @end=false,
     @left=
      #<Trie::Node:0xab00
       @char="6",
       @end=false,
       @left=nil,
       @mid=
        #<Trie::Node:0xab18
...
                                    #<Trie::Node:0xac28
                                     @char="C",
                                     @end=true,
                                     @left=nil,
                                     @mid=nil,
                                     @right=nil,
                                     @value="not the flag but a true statement ;)">,
...
                                       #<Trie::Node:0xb2b0
                                        @char="8",
                                        @end=false,
                                        @left=nil,
                                        @mid=
                                         #<Trie::Node:0xb2c0
                                          @char="8",
                                          @end=false,
                                          @left=nil,
                                          @mid=
                                           #<Trie::Node:0xb2d0
                                            @char="i",
                                            @end=true,
                                            @left=nil,
                                            @mid=nil,
                                            @right=nil,
                                            @value=
                                             "good boy this is the flag">,
                                          @right=nil,
                                          @value=
                                           "good boy this is the flag">,
                                        @right=nil,
...
{% endhighlight %}

As expected, the object represents a [trie](http://en.wikipedia.org/wiki/Trie)
with values associated with the leafs. Our best guess is that our input is
used to look up a leaf in the trie and the value of that leaf is printed out.

Let's write some code to read the keys and values of the trie, using
depth-first traversal:

{% highlight ruby %}
Rubinius::CodeLoader.require_compiled './cipher'
Rubinius::CodeLoader.require_compiled './trie'

t = Marshal.load(File.read('trie.dump'))
class Trie
  attr_reader :root
  class Node
    def walk(path="")
      path = path + @char
      if @end
        puts path + ' => ' + @value
      end
      @left.walk(path) if @left
      @mid.walk(path) if @mid
      @right.walk(path) if @right
    end
  end
end
t.root.walk
{% endhighlight %}

Output:

    WD6A01IvFSCF3IWFvIIDC => not the flag but a true statement ;)
    WD8wM9VHFciF9CHCFaabyF01cVFyHMvqFC688X => wow not this either
    WDwTFcqFHMqAF2FW8MX => 1 c4n r34d th15 ju57 l1k3 x86 0r 3n6L15h!
    WDwM6WpVpvcA => this isnt the flag
    WyXcXAp9FWMXMW8FAp9WFW9DA => nope lots of fake flags
    WyXcXAFAp9F0Wc8FDHcveFypMWF288i => good boy this is the flag
    WyXcXAFAp9F0g1MTXFciFA80 => stop being such a n00b and get the flag
    WyXcXAFAp9F0gvpzF0Wc8XFvpiFD8cvGFKFvppD => lole n1c3 try
    WyM0qFSVFyAF18Wp => neither is this

This looks promising. It seems like the trie uses a `Cipher` to encrypt the
keys before lookup/insertion. There's at least two ways to extract the
permutation used for the cipher:

1. Create a new trie and insert the value `abcd...xyzABC...XYZ012..89`, check
  out the resulting trie
2. Use the disassembly to extract the constructor argument for `Cipher`

We went with option 2:

{% highlight ruby %}
...
0045:  push_literal        :push
0047:  push_literal        #<Rubinius::CompiledCode push file=stuff/trie.rb>
    0000:  push_const_fast     :Cipher
    0002:  dup_top
    0003:  check_serial        :new, 47
    0006:  goto_if_false       0211:
    0008:  allow_private
    0009:  send_stack          :allocate, 0
    0012:  dup_top
    0013:  push_literal        "K"
    0015:  string_dup
    0016:  push_literal        "D"
    0018:  string_dup
    0019:  push_literal        "w"
    0021:  string_dup
    0022:  push_literal        "X"
    0024:  string_dup
    0025:  push_literal        "H"
    ...
{% endhighlight %}

We can easily extract the permutation from here and [decode the
keys](https://github.com/kitctf/writeups/blob/master/bkp2015/sullivan_square/hack.rb):

{% highlight ruby %}
Rubinius::CodeLoader.require_compiled './cipher'
Rubinius::CodeLoader.require_compiled './trie'

$c = Cipher.new("KDwXH3e1SBgayvI6uWC09bzTAqU4OoENrnmdkxPtRsJLfhZjY57lpc28MVGi QF".chars.to_a)
t = Marshal.load(File.read('trie.dump'))
class Trie
  attr_reader :root
  class Node
    def walk(path="")
      path = path + @char
      if @end
        puts $c.decrypt(path) + ' => ' + @value
      end
      @left.walk(path) if @left
      @mid.walk(path) if @mid
      @right.walk(path) if @right
    end
  end
end
t.root.walk
{% endhighlight %}

Output:

    rbpython is for noobs => not the flag but a true statement ;)
    rb3c4u5e 17 uses llvm th15 me4nz sp33d => wow not this either
    rbcx 1z e4zy 2 r34d => 1 c4n r34d th15 ju57 l1k3 x86 0r 3n6L15h!
    rbc4pr050n1y => this isnt the flag
    rmd1dy0u r4d4r3 y0ur ruby => nope lots of fake flags
    rmd1dy y0u tr13 be1ng m04r 2337 => good boy this is the flag
    rmd1dy y0u tkh4xd 17 y3t => stop being such a n00b and get the flag
    rmd1dy y0u tkn0w tr13d n07 b31n6 a n00b => lole n1c3 try
    rm4tz i5 my h3r0 => neither is this

Something is a little off here, probably we haven't quite understood how the
trie works exactly. After a bit of trial and error, we figured out the correct
flag:

    d1d y0u tr13 be1ng m04r 2337
