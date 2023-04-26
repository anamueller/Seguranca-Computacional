#include <stdio.h>
#include <stdlib.h>

int P10[10] ={2,4,1,6,3,9,0,8,7,5};
int P8[8] = {5,2,6,3,7,4,9,8};
int i;

void permutacao(char chave[]){
    char aux[10];
    for(i=0;i<10;i++){
        aux[i]=chave[i];
    }

    for(i=0;i<10;i++){
        chave[i]=aux[P10[i]];
    }
}

void rotacionar(char chave[]){
    char aux1[5], aux2[5];
    for(i=0;i<5;i++){
        if(i==0){
            aux1[4]=chave[0];
            aux2[4]=chave[5];
        }
        else{
            aux1[i-1]=chave[i];
            aux2[i-1]=chave[i+5];
        }
    }//rotação para k1

    for(i=0;i<5;i++){
        chave[i]=aux1[i];
        chave[i+5]=aux2[i];
    }//separados e rotacionados

}

void fk1(char chave[], char chave_de_8[]){
    rotacionar(chave);
    for(i=0;i<8;i++){
        chave_de_8[i]=chave[P8[i]];
    } //aplica p8
}

void cifrar(int chave[], int bloco[]){
    //permutação inicial
    //função complexa
    //permutação de troca de duas metades
    //função complexa dnv
    //permutação inicial inversa
}


int main(){
    int L;
    char op[1];
    char K[10]; //chave
    char B[8]; //sequência de bits do bloco a ser utilizado na operação
    char R[8];
    char K1[8]; //subchave depois de primeira geração de chave


    scanf("%d", &L);

    for(int i=0;i<L;i++){
        scanf(" %c", &op[0]); //C ou D, C=cifrar, D=decifrar
        
        for(int j=0;j<10;j++){ //ler a chave
            scanf(" %c", &K[j]);
        }
        
        for(int j=0;j<8;j++){ //ler o bloco
            scanf("%c", &B[j]);
        }

        //fazer a operação
    }

    permutacao(K);
    fk1(K, K1);

    printf("\nchave\n");
    for(i=0;i<8;i++){
        printf("%c ", K1[i]);
    }


    return 0;
}