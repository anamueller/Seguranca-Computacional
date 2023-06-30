#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int DEBUG = 0;
char P10_KEY[10] = "2416390875";
char P8_KEY[8]   = "52637498";
char P[8]        = "15203746";
char IP[8]       = "30246175";
char EP[8]       = "30121230";
char P4[4]       = "1320";
char S0[4][4]    = {"1032","3210","0213","3132"};
char S1[4][4]    = {"1123","2013","3010","2103"};

// ACHO QUE NAO ESTOU DANDO FREE EM TUDO QUE ALOCO
// VERIFICAR ALOCACOES ( ALOCAR TUDO E TUDO E TESTAR)

char* permuta(char* vetor); // OK
char* Ipermuta(char* vetor); // OK
char* leftShift(char* vetor); // OK
void makeKey(char* K, char* k1, char* k2); // OK
char* cifra(char* B, char* K);
char* descifra(char* B, char* K);
char* fK(char* vetor, char* K);
char* SW(char* vetor);

int main(int argc, char *argv[]){
    char *out;

    out = (char*) malloc(sizeof(char)*8);

    if(argc != 4){
        printf("Argumentos invalidos");
    }

    if(argv[1][0] == 'C'){
        out = cifra(argv[2], argv[3]);
    }
    else{
        out = descifra(argv[2], argv[3]);
    }

    printf("%s", out);
    return 0;
}

char* cifra(char* B, char* K){
    char *seq, *k1, *k2;
    seq = (char*) malloc(sizeof(char)*8);
    k1 = (char*) malloc(sizeof(char)*8);
    k2 = (char*) malloc(sizeof(char)*8);

    seq = permuta(B);
    if (DEBUG) printf("%s  permutacao\n", seq);
    makeKey(K,k1,k2);
    seq = fK(seq,k1);
    if (DEBUG) printf("%s  fk k1: %s\n", seq, k1);
    seq = SW(seq);
    if (DEBUG) printf("%s  SW\n", seq);
    seq = fK(seq,k2);
    if (DEBUG) printf("%s  fk k2: %s\n", seq, k2);
    seq = Ipermuta(seq);
    if (DEBUG) printf("%s  permutacao inv\n", seq);

    return seq;
}

char* descifra(char* B, char* K){
    char *seq, *k1, *k2;
    seq = (char*) malloc(sizeof(char)*8);
    k1 = (char*) malloc(sizeof(char)*8);
    k2 = (char*) malloc(sizeof(char)*8);

    seq = permuta(B);
    if (DEBUG) printf("%s  permutacao inv\n", seq);
    makeKey(K,k1,k2);
    seq = fK(seq,k2);
    if (DEBUG) printf("%s  fk k2: %s\n", seq, k2);
    seq = SW(seq);
    if (DEBUG) printf("%s  SW\n", seq);
    seq = fK(seq,k1);
    if (DEBUG) printf("%s  fk k1: %s\n", seq, k1);
    seq = Ipermuta(seq);
    if (DEBUG) printf("%s  permutacao\n", seq);

    return seq;
}

char* fK(char* vetor, char* K){ // VERIFICAR A SEPARACAO ESTA CERTA 4 + SIGNIFICATIVOS OU N
    char *temp1, *temp2, *temp3, p, p2, *z;
    int i, lin, col, val;

    temp1 = malloc(sizeof(char)*8);
    temp2 = malloc(sizeof(char)*8);
    temp3 = malloc(sizeof(char)*4);

    // Seleciona direita e EP
    for(i=0;i<8;i++){
        p = EP[i];
        temp1[i] = vetor[4+atoi(&p)];
    }
    if(DEBUG) printf("\t%s  EP\n", temp1);
    // XOR
    for(i=0;i<8;i++){
        temp2[i] = temp1[i] == K[i] ? '0' : '1';
    }
    if(DEBUG) printf("\t%s  XOR\n", temp2);

    // S0
    p = temp2[0];
    lin = atoi(&p)*2;
    p2 = temp2[3];
    lin += atoi(&p2);
    memset(&p,'a',2);
    memset(&p2,'a',2);
    p = temp2[1];
    col = atoi(&p)*2;
    p2 = temp2[2];
    col += atoi(&p2);
    if(DEBUG) printf("\tl:%d  c:%d\n", lin, col);
    memset(&p,'a',2);
    p = S0[lin][col];
    val = atoi(&p);
    memset(&p,'a',2);
    memset(&p2,'a',2);

    if(DEBUG) printf("\tS0:%d\n", val);
    if(val / 2 == 1){
        temp1[0] = '1';
    }
    else{
        temp1[0] = '0';
    }
    if(val % 2 == 0){
        temp1[1] = '0';
    }
    else{
        temp1[1] = '1';
    }

    // S1
    p = temp2[4];
    lin = atoi(&p)*2;
    p2 = temp2[7];
    lin += atoi(&p2);
    memset(&p2,'a',2);
    memset(&p,'a',2);
    p = temp2[5];
    col = atoi(&p)*2;
    p2 = temp2[6];
    col += atoi(&p2);
    if(DEBUG) printf("\tl:%d  c:%d\n", lin, col);
    memset(&p,'a',2);
    p = S1[lin][col];
    val = atoi(&p);
    if(DEBUG) printf("\tS1:%d\n", val);
    if(val / 2 == 1){
        temp1[2] = '1';
    }
    else{
        temp1[2] = '0';
    }
    if(val % 2 == 0){
        temp1[3] = '0';
    }
    else{
        temp1[3] = '1';
    }
    if(DEBUG) printf("\t%s  CaixaS 4 primeiros\n", temp1);

    // P4
    for(i=0;i<4;i++){
        p = P4[i];
        temp3[i] = temp1[atoi(&p)];
    }
    if(DEBUG) printf("\t%s  P4\n", temp3);

    // XOR E JA ALTERA OS DA DIREITA
    for(i=0;i<4;i++){
        vetor[i] = temp3[i] == vetor[i] ? '0' : '1';
    }

    return vetor;
}

char* leftShift(char* vetor){
    int size = strlen(vetor);
    char *temp;
    int i;

    temp = (char*) malloc(sizeof(char)*size);

    temp[size-1] = vetor[0];
    for(i=0;i<size-1;i++){
        temp[i] = vetor[i+1];
    }


    return temp;
}

char* permuta(char *vetor){ // CONSIDERANDO P8 apenas
    char *temp, p;
    int i;

    temp = (char*) malloc(sizeof(char)*8);
    for(i=0;i<8;i++){
        p = P[i];
        temp[i] = vetor[atoi(&p)];
    }

    return temp;
}

char* Ipermuta(char* vetor){
    char *temp, p;
    int i;

    temp = (char*) malloc(sizeof(char)*8);
    for(i=0;i<8;i++){
        p = IP[i];
        temp[i] = vetor[atoi(&p)];
    }

    return temp;
}

void makeKey(char *vetor, char *k1, char *k2){
    char *temp, p, *part1, *part2;
    int i;

    part1 = (char*) malloc(sizeof(char)*5);
    part2 = (char*) malloc(sizeof(char)*5);
    temp = (char*) malloc(sizeof(char)*10);
    // P10
    for(i=0;i<10;i++){
        p = P10_KEY[i];
        temp[i] = vetor[atoi(&p)];
    }

    // Separa
    for(i=0;i<10;i++){
        if(i<5){
            part1[i] = temp[i];
        }
        else{
            part2[i-5] = temp[i];
        }
    }

    // LS-1
    part1 = leftShift(part1);
    part2 = leftShift(part2);

    // Junta
    for(i=0;i<10;i++){
        if(i<5){
            temp[i] = part1[i];
        }
        else{
            temp[i] = part2[i-5];
        }
    }

    // P8 = K1
    for(i=0;i<8;i++){
        p = P8_KEY[i];
        k1[i] = temp[atoi(&p)];
    }

    //LS-2
    part1 = leftShift(part1);
    part2 = leftShift(part2);
    part1 = leftShift(part1);
    part2 = leftShift(part2);

    // Junta
    for(i=0;i<10;i++){
        if(i<5){
            temp[i] = part1[i];
        }
        else{
            temp[i] = part2[i-5];
        }
    }

    // P8 = K2
    for(i=0;i<8;i++){
        p = P8_KEY[i];
        k2[i] = temp[atoi(&p)];
    }

    free(part1);
    free(part2);
    free(temp);

}

char* SW(char* vetor){
    char *temp;
    int i;
    temp = malloc(sizeof(char)*8);

    for(i=0;i<8;i++){
        if(i<4){
            temp[i] = vetor[i+4];
        }
        else{
            temp[i] = vetor[i-4];
        }
    }
    return temp;
}