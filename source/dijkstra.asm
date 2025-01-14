; Dijkstra's Algorithm Implementation in x86 Assembly
; Uses a simple adjacency matrix representation for the graph

section .data
    ; Constants
    INF     equ     0x7FFFFFFF      ; Represents infinity
    MAXN    equ     100             ; Maximum number of vertices
    
    ; Graph representation
    n       dd      6               ; Number of vertices
    visited times MAXN db 0         ; Visited array
    dist    times MAXN dd INF       ; Distance array
    graph   times MAXN*MAXN dd 0    ; Adjacency matrix

section .text
global _start

_start:
    ; Initialize dist[0] = 0 (starting vertex)
    mov dword [dist], 0
    
    ; Main Dijkstra loop
    mov ecx, 0                      ; Loop counter
main_loop:
    push ecx
    call find_min_vertex           ; Find vertex with minimum distance
    add esp, 4
    
    cmp eax, -1                    ; If no vertex found, exit
    je exit_program
    
    mov ebx, eax                   ; Current vertex in ebx
    mov byte [visited + ebx], 1    ; Mark vertex as visited
    
    ; Update distances
    xor ecx, ecx                   ; Reset counter
update_loop:
    cmp ecx, [n]                   ; Check if we've processed all vertices
    jge main_loop_continue
    
    ; If vertex is not visited and there is an edge
    cmp byte [visited + ecx], 0
    jne next_vertex
    
    ; Calculate offset in adjacency matrix
    push ecx
    mov eax, ebx                   ; Current vertex
    mov edx, MAXN
    mul edx                        ; eax = ebx * MAXN
    pop ecx
    add eax, ecx                   ; Add offset for neighbor
    
    ; Check if edge exists and update distance if needed
    mov edx, [graph + eax*4]       ; Get edge weight
    cmp edx, 0                     ; If no edge, skip
    je next_vertex
    
    ; Calculate new distance
    add edx, [dist + ebx*4]        ; New distance = dist[curr] + weight
    cmp edx, [dist + ecx*4]        ; Compare with current distance
    jge next_vertex                ; If new distance >= current, skip
    
    mov [dist + ecx*4], edx        ; Update distance
    
next_vertex:
    inc ecx
    jmp update_loop
    
main_loop_continue:
    mov ecx, [n]
    dec ecx
    jnz main_loop
    
exit_program:
    mov eax, 1                     ; sys_exit
    xor ebx, ebx                   ; return 0
    int 0x80

; Function to find vertex with minimum distance
find_min_vertex:
    push ebp
    mov ebp, esp
    
    mov eax, -1                    ; Return value (no vertex found)
    mov edx, INF                   ; Minimum distance found
    xor ecx, ecx                   ; Counter
    
find_min_loop:
    cmp ecx, [n]                   ; Check if we've checked all vertices
    jge find_min_done
    
    ; If vertex is not visited and has smaller distance
    cmp byte [visited + ecx], 0
    jne next_min_vertex
    
    mov ebx, [dist + ecx*4]
    cmp ebx, edx
    jge next_min_vertex
    
    mov edx, ebx                   ; Update minimum distance
    mov eax, ecx                   ; Update return value
    
next_min_vertex:
    inc ecx
    jmp find_min_loop
    
find_min_done:
    mov esp, ebp
    pop ebp
    ret
