# Dijkstra's Algorithm in Assembly

This is an implementation of Dijkstra's shortest path algorithm in x86 assembly language.

## Requirements
- NASM (Netwide Assembler)
- Linux environment or WSL on Windows

## Building and Running
1. Assemble the code:
```bash
nasm -f elf32 dijkstra.asm -o dijkstra.o
```

2. Link the object file:
```bash
ld -m elf_i386 dijkstra.o -o dijkstra
```

3. Run the program:
```bash
./dijkstra
```

## Implementation Details
- Uses adjacency matrix representation for the graph
- Maximum number of vertices: 100
- Infinity represented as 0x7FFFFFFF
- Starting vertex is assumed to be vertex 0

To modify the graph, edit the values in the `graph` array in the data section of `dijkstra.asm`.
