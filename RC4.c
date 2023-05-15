#include <stdio.h>
#include <stdlib.h>

/*
Código desenvolvido por Ana Clara Mueller Miranda aplicando o algoritmo de criptografia
RC4 em C.
*/
int S[256];

void swap(int a, int b){
    int aux;
    aux=a;
    a=b;
    b=aux;
}

void inicia_s(char chave[], int tamanho_chave){
    for(int i=0;i<256;i++){
        S[i] = i;
    }
    int j=0;
    for(int i=0;i<256;i++){
        j=(j+S[i]+chave[i%tamanho_chave])%256;
        swap(S[i], S[j]);
    }
}

void gerar_k_xor(int tamanho, char palavra[]){
    char cifrada[tamanho];
    int i,j=0;
    for(int l=0;l<tamanho;l++){ //gerando chave k
        i=(i+1)%256;
        j=(j+S[i])%256;
        swap(S[i],S[j]);
        int k = S[(S[i]+S[j])%256];
        cifrada[l]=k ^ palavra[l]; //fazendo xor de k com primeiro caracter da palavra
        printf("%x:", cifrada[l]);
    }
}

void cifrar(char chave[], char palavra[], int tamanho_chave, int tamanho_palavra){
    inicia_s(chave, tamanho_chave); //inicialização do vetor e permutação inicial de S
    gerar_k_xor(tamanho_palavra, palavra);
}

int main(){
    char P[256]; //palavra
    char K[256]; //chave
    char c,d;
    int TamP=0, TamK=0;

    while(1){//lendo  a palavra
        c = getchar();
        if(c == '\n'){//return pressed!
            break;
        }
        P[TamP] = c;
        TamP++;
    }
    while(1){//lendo a chave
        d = getchar();
        if(d == '\n'){//return pressed!
            break;
        }
        K[TamK] = d;
        TamK++;
    }
    

    for(int i=0;i<15;i++){
        printf("%c", K[i]);
    }
    printf("\n");
    for(int i=0;i<15;i++){
        printf("%c", P[i]);
    }
    //cifrar(K, P, TamK, TamP);
    return 0;
}