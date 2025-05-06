
# C++ rev

----

# C++ rev
## how painful is it?

----

# C++ rev
## the how to not die guide

---

## But isn't C++ not just C

----

# no!

----

* Classes
* Cursed Inheritance
* Dynamic Binding
* Template Methods
* Constructors and Destructors

---

I will use Binary Ninja during the talk

----

Ghirda is around less than 4 years

----

Barely enough time to open a basic CTF challenge

----

... I will show how to do the same in Ghidra later

---

## Classes

How do they look in memory?

----

Let's start simple!

----

## Classes

```cpp
#include <stdlib.h>

class CtfTeam {
    public:
        char* name;
        int points;
        char** members;
};

int main(int argc, char** argv) {
    if (argc < 2) {
        return EXIT_FAILURE;
    }
    CtfTeam team;
    team.name = argv[1];
    team.points = 0;
    team.members = new char*[argc - 2];
    for (int i = 2; i < argc; i++)
        team.members[i-2] = argv[i];
    return EXIT_SUCCESS;
}
```

----

# Demo

----

```c
struct CtfTeam {
    char* name;
    int points;
    char** members;
};
```

---

What about methods?

----

```cpp
class CtfTeam {
    public:
        char* name;
        int points;
        char** members;
        void addPoints(int p) {
            points += p;
        }
};
```

----

# Demo

----

Think of it like python
```python
@dataclass
class CtfTeam:
    name: str
    points: int
    members: List[str]

    def add_points(self, points):
        self.points += points


team = CtfTeam(name="ImperfectGreen", points=0, members=["..."])
# equivalent to team.add_points(50)
team.__getattribute__("add_points").__func__(team, 50)
```

----

* Create `struct` with data members
* Find methods where object is passed in as first parameter
* Accesses internals of that object
* Retype explit `this` to class pointer

---

Dynamic Binding (where the fun beginns)

----

```cpp
class CtfTeam {
    public:
        char* name;
        int points;
        char** members;
        virtual void addPoints(int p) {
            points += p;
        }
};
```

----

# Demo

----

```cpp
struct CtfTeamVTable {
    void (*addPoints)(int);
}
struct CtfTeam {
    CtfTeamVTable* vtable;
    char* name;
    int points;
    char** members;
};
```

---

Contructors and Identifying Inheritance

<img style="border-width:0; background: transparent;" src="/imgs/c011d4ea-20ee-4ff8-8372-bf4eb643d365.png" width="200">

----

```cpp
class CtfTeam {
    public:
        char* name;
        int points;
        char** members;
        virtual void addPoints(int p) {
            points += p;
        }
};
class HightSchoolTeam : public CtfTeam {
    private:
        char* schoolName;
    public:
        virtual void addPoints(int p) {
            points += p + 10;
        }
        virtual char* getSchoolName() {
            return schoolName;    
        }
};
```

----

# Demo

----

```cpp
struct CtfTeamData {
    char* name;
    int points;
    char** members;
};
struct CtfTeamVTable {
    void (*addPoints)(int);
};
struct CtfTeam {
    CtfTeamVTable* vtable;
    CtfTeamData data;
};
struct HighSchoolTeamData {
    char* name;
    int points;
    char** members;
    char* schoolName;
};
struct HighSchoolTeamVTable {
    void (*addPoints)(int);
    char* (*getSchoolName)();
};
struct HighSchoolTeam {
    HighSchoolTeamVTable* vtable;
    HighSchoolTeamData data;
};
```

---

all the time I was wondering

----

`char*` rly? How bad of a C++ are you?!

----

Well, yes. But what is this `std::string` after all?

----

```cpp
typedef basic_string<char> string;
```

----

```cpp
template<
    class CharT,
    class Traits = std::char_traits<CharT>,
    class Allocator = std::allocator<CharT>
> class basic_string;
```
But what does that mean?


----

it depends

----

it depends
![](/imgs/22cd2db9-2df0-43e8-9ec6-bff23597aa8e.png)

----

# Cursed Demo
A peek into `libcxx/include/string`

----

And further depends on compile options like `	_LIBCPP_ABI_ALTERNATE_STRING_LAYOUT`

read more: [https://eu90h.github.io/cpp-strings.html](https://eu90h.github.io/cpp-strings.html)

----

But normally you should be fine with
```cpp
struct basic_string {
    char *begin_;
    int size_;
    union {
        int capacity_;  // is >=16 B
        char sso_buffer[16]; // if < 16 B
    };
};
```

---

From the bad to the ugly

**S**tandard **T**emplate **L**ibrary

----

Layout of a cpp vector

```cpp
// In MSVC it is first, last, end
struct vector_<TemplateType> {
    <TemplateType>* start;
    <TemplateType>* end;
    <TemplateType>* last;
};
```

----

<img style="border-width:0; background: transparent" src="/imgs/9bc2cc8e-7b11-4fe8-a5bf-fcef6145bb1c.png">

call graph of a vector<char> push back in O1

---

So far all was fair and well in O0 land

----

Imagine the graph from before, but partially inlined

----

```cpp
size_t size = (vec.end - vec.start) >> 2; // div by 4
```

```cpp
// vector<char[5]>;
// div by 5
size_t size = ((vec.end - vec.start) * 0xCCCCCCCCCCCCCCCD) >> 2;
```

---

Last example: Maps

----

```cpp
struct xy {
    int x;
    int y;
};
struct _Rb_tree_node_base {
    enum _Rb_tree_color _M_color;
    struct _Rb_tree_node* _M_parent;
    struct _Rb_tree_node* _M_left;
    struct _Rb_tree_node* _M_right;
};
struct _Rb_tree_node {
    struct _Rb_tree_node_base _base;
    struct kv_pair {
            int key;
            struct xy* value;
        } pair;
};
struct map {
    void* allocator;
    struct _Rb_tree_node_base _M_header;
    int _M_node_count;
};
```

---

# Painkillers

----

For the IDA user:
(removed IDA meme)

----

* HexRaysPyTools: Quickly creating structures
* Classy: Makes working with vtables and child classes a lot easier.
* Gal Zaban: When Virtual Hell Freezes Over 
    * Virtuailor - IDAPython tool for C++ vtables reconstruction
* Hexrays: Using the IDAClang plugin for IDA Pro
* `ida_medigate` C++ plugin for IDA Pro
* https://github.com/RolfRolles/Miscellaneous/blob/master/STLTypes-ForDistribution.py

----

## Binary Ninja

* Trail of Bits: Devirtualizing C++ with Binary Ninja
* Maybe soon more

----

### Ghirda

* Using Logic Programming to Recover C++ Classes and Methods from Compiled Executables

---

# chal 
    
Look at the ost2 course on C++ revering, specifically the zoo challenge.   

CC-BY-SA Gal Zaban ost2.fyi
