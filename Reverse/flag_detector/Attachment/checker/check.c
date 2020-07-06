#include "check.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define word_var1_SIZE 256

typedef enum { false,
               true } bool;

typedef enum {
    nop,    // 1
    pop,    // 2
    push,   // 3
    jmp,    // 4
    pushb,  // 5
    addb,   // 6
    cmpb,   // 7
    jmpfb,  // 8
    cmp,    // 9
    popb,
    call,        // a
    ret,         // b
    add,         // c
    sub,         // d
    mul,         // e
    divv,        // f
    mod,         // 10
    xor,         // 11
    read,        // 12
    printc,      // 13
    stoA,        // 14
    lodA,        // 15
    pushflag,    // 16
    popflag,     // 17
    Dpush,       // 18
    printd,      // 19
    stoB,        // 1a
    lodB,        // 1b
    nopnop,      // 1c
    set_var_ret  // 1d
} opcode;

typedef struct {
    int word_var1[word_var1_SIZE];
    int word_var2;
    int word_var3;
    int word_var4;
} frame;

typedef struct {
    int dword_var5[word_var1_SIZE];
} func;

frame dword_var6[word_var1_SIZE];
func dword_var8[word_var1_SIZE];

bool word_var9           = true;
int word_var1[word_var1_SIZE]   = {0};
int dword_var5[word_var1_SIZE] = {0};
int word_var2;
int word_var3;
int word_var3c;
int var;
int dword_var10;
int dword_var11 = 0;

int byte_var1 = 0;
int byte_var2 = 0;

char str_var1[50];
int dword_var2[50] = {2};
char file_name[] = "./asdf";
char flag_name[] = "./hjkl";

int var_ret = 1;
void check_fun4() {
    memset(str_var1, 0, sizeof(str_var1));
    memset(dword_var2, 0, sizeof(dword_var2));
    memset(word_var1, 0, sizeof(word_var1));
    memset(dword_var5, 0, sizeof(dword_var5));
    memset(dword_var6, 0, sizeof(dword_var6));
}
void check_fun10() {
    int i = 0;
    for (i = 1; str_var1[i - 1]; i++) {
        dword_var2[i] = (int)str_var1[i - 1];
    }
    dword_var2[i] = 1;
}

void check_fun11(int *a, int *b) {
    int i = 0;
    do {
        b[i] = a[i];
        i++;
    } while (a[i]);
    b[i] = 0;
}

int check_fun1(char *filename) {
    int file_fun = 1;
    word_var3c          = 0;
    word_var9     = true;
    dword_var11      = 0;
    FILE *file   = fopen(filename, "r");
    int i        = 0;

    do {
        int num      = 0;
        int arr[256] = {0};
        while (fscanf(file, "%d", &num) > 0) {
            if (num == -1) {
                file_fun += 1;
                i = 0;
            } else if (num == -2) {
                file_fun -= 1;
                break;
            } else {
                arr[i] = num;
                i++;
            }
        }
        check_fun11(arr, dword_var8[dword_var11].dword_var5);
        dword_var11 += 1;
    } while (file_fun);
    fclose(file);
    return 1;
}

void check_fun12(int id) {
    dword_var6[id].word_var2    = 0;
    dword_var6[id].word_var3    = 0;
    dword_var6[id].word_var4 = 0;
}

void check_fun2(int id) {
    dword_var10 = id > 0 ? id : dword_var6[word_var3c].word_var4;
    word_var2        = dword_var6[word_var3c].word_var2;
    word_var3        = dword_var6[word_var3c].word_var3;
    check_fun11(dword_var6[word_var3c].word_var1, word_var1);
    check_fun11(dword_var8[dword_var10].dword_var5, dword_var5);
}

void check_fun13() {
    dword_var6[word_var3c].word_var2    = word_var2;
    dword_var6[word_var3c].word_var3    = word_var3;
    dword_var6[word_var3c].word_var4 = dword_var10;
    check_fun11(word_var1, dword_var6[word_var3c].word_var1);
}

void check_fun9(int deal_flag, int var) {
    if (deal_flag) {
        // call function
        int id = var;
        check_fun13();
        word_var3c += 1;
        check_fun2(id);
        word_var2 -= 1;
    } else {
        // return
        check_fun12(word_var3c);
        word_var3c -= 1;
        check_fun2(-1);
        if (word_var3c == -1) {
            word_var9 = false;
        }
    }
}

void check_fun7() {
    FILE *file = fopen(flag_name, "r");
    fscanf(file, "%s", str_var1);
    fclose(file);
    check_fun10();
}

int check_fun5() { return dword_var5[word_var2]; }

void check_fun6(int opcode) {
    switch (opcode) {
        case nop:
            word_var9 = false;
            break;
        case pop:
            word_var3 -= 1;
            break;
        case push:
            word_var1[word_var3++] = dword_var5[++word_var2];
            break;
        case jmp:
            var = dword_var5[++word_var2];
            word_var2 += var;
            break;
        case pushb:
            break;
        case addb:
            break;
        case cmpb:
            break;
        case jmpfb:
            var = dword_var5[++word_var2];
            if (word_var1[--word_var3] != 0) {
                word_var2 += var;
            }
            break;
        case cmp:
            word_var1[word_var3] = word_var1[word_var3 - 1] == dword_var5[++word_var2];
            word_var3 += 1;
            break;
        case call:
            check_fun9(1, dword_var5[++word_var2]);
            break;
        case ret:
            check_fun9(0, 1);
            break;
        case add:
            word_var1[word_var3 - 2] += word_var1[word_var3 - 1];
            word_var3 -= 1;
            break;
        case sub:
            word_var1[word_var3 - 2] -= word_var1[word_var3 - 1];
            word_var3 -= 1;
            break;
        case mul:
            break;
        case divv:
            break;
        case mod:
            break;
        case xor:
            word_var1[word_var3 - 2] ^= word_var1[word_var3 - 1];
            word_var3 -= 1;
            break;
        case read:
            check_fun7();
            break;
        case printc:
            printf("%c", word_var1[word_var3 - 1]);
            break;
        case printd:
            printf("%d", word_var1[word_var3 - 1]);
            break;
        case stoA:
            byte_var1 = word_var1[--word_var3];
            break;
        case lodA:
            word_var1[word_var3++] = byte_var1;
            break;
        case stoB:
            byte_var2 = word_var1[--word_var3];
            break;
        case lodB:
            word_var1[word_var3++] = byte_var2;
            break;
        case pushflag:
            var         = word_var1[word_var3 - 1];
            word_var1[word_var3++] = dword_var2[var];
            break;
        case popflag:
            var                   = word_var1[--word_var3];
            dword_var2[word_var1[--word_var3]] = var;
            break;
        case Dpush:
            var         = word_var1[word_var3 - 1];
            word_var1[word_var3++] = var;
            break;
        case nopnop:
            printf("\n[|] breadk!\n");
            break;
        case set_var_ret:
            var_ret = byte_var1;
            break;
    }
}

void check_fun3() {
    while (word_var9) {
        check_fun6(check_fun5());
        word_var2 += 1;
    }
}

int machine() {
    if (check_fun1(file_name)) {
        check_fun2(0);
        check_fun3();
    }
    check_fun4();
    return var_ret;
}