[![GitHub](https://img.shields.io/github/license/tomhea/bf2fj)](LICENSE)
[![Website](https://img.shields.io/website?down_color=red&down_message=down&up_message=up&url=https%3A%2F%2Fesolangs.org%2Fwiki%2FFlipJump)](https://esolangs.org/wiki/FlipJump)
[![PyPI - Version](https://img.shields.io/pypi/v/bf2fj)](https://pypi.org/project/bf2fj/)

# bf2fj
A [Brainfuck](https://esolangs.org/wiki/Brainfuck) to [FlipJump](https://github.com/tomhea/flip-jump) Compiler.

## Download:
```
>>> pip install bf2fj
```

## Run the compiler:

```
>>> bf2fj hello_world.bf 
  compile bf->fj:  0.009s
```

You can also run the created flipjump program.
```
>>> bf2fj hello_world.bf -r
  compile bf->fj:  0.008s
  parsing:         0.092s
  macro resolve:   0.141s
  labels resolve:  0.035s
  create binary:   0.143s
  loading memory:  0.017s
Hello World!

Finished by looping after 0.739s (337,484 ops executed; 85.36% flips, 98.88% jumps).
```

### Licenses:
The programs/ folder has a collection of 3rd party brainfuck programs, taken from multiple open-source websites. Each folder under programs/ has a README.md that specifies were the brainfuck files came from, and to whom we owe the credit.
