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
    }//rotação de 1 para esquerda

    for(i=0;i<5;i++){
        chave[i]=aux1[i];
        chave[i+5]=aux2[i];
    }//separados e rotacionados

}

void fk1_e_k2(char chave[], char k1[], char k2[]){
    permutacao(chave);
    rotacionar(chave); //para k1

    char aux[10];
    for(i=0;i<10;i++){
        aux[i]=chave[i];
    } //copiando para usar em k2
    rotacionar(aux);
    rotacionar(aux); //k2 rotaciona 2 para esquerda após ls-1

    for(i=0;i<8;i++){
        k1[i]=chave[P8[i]];
    } //aplica p8

    for(i=0;i<8;i++){
        k2[i]=aux[P8[i]];
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
    char op[1]; //escolha da operacao decifrar ou cifrar
    char K[10]; //chave
    char B[8]; //sequência de bits do bloco a ser utilizado na operação na função complexa
    char R[8]; //resultado final
    char K1[8]; //subchave depois de primeira geração de chave
    char K2[8]; //subchave depois de primeira geração de chave


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

    fk1_e_k2(K, K1, K2);

    printf("\nchave k1\n");
    for(i=0;i<8;i++){
        printf("%c ", K1[i]);
    }

    printf("\nchave k2\n");
    for(i=0;i<8;i++){
        printf("%c ", K2[i]);
    }


    return 0;
}