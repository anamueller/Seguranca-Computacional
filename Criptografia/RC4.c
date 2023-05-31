#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
Código desenvolvido por Ana Clara Mueller Miranda aplicando o algoritmo de criptografia
RC4 em C.
*/
unsigned char S[256];
unsigned char T[256];

void swap(int pos1, int pos2){
    unsigned char aux;
    aux = S[pos1];
    S[pos1]=S[pos2];
    S[pos2]=aux;
}

void inicia_s(unsigned char chave[], int tamanho_chave){
    for(int i=0;i<256;i++){
        S[i] = i;
    }
}

void inicia_t(unsigned char chave[], int tamanho_chave){
    int j=0;
    for(int i=0;i<256;i++){
        if(j==tamanho_chave){
            j=0;
            T[i]=chave[j];
            j++;
        }
        else{
            T[i]=chave[j];
            j++;
        }
    }
}

void permutacao_s(){
    int j=0;
    for(int i=0;i<256;i++){
        j=(j+S[i]+T[i])%256;
        swap(i, j);
    }
}

void gerar_k_xor(int tamanho, unsigned char palavra[]){
    unsigned char cifrada[tamanho];
    int i=0,j=0;
    for(int l=0;l<tamanho;l++){ //gerando chave k
        i=(i+1)%256;
        j=(j+S[i])%256;
        swap(i,j);
        char k = S[(S[i]+S[j])%256];
        cifrada[l]=k ^ palavra[l]; //fazendo xor de k com primeiro caracter da palavra
        printf("%x:", cifrada[l]);
    }
}

void cifrar(unsigned char chave[], unsigned char palavra[], int tamanho_chave, int tamanho_palavra){
    inicia_s(chave, tamanho_chave); //inicialização do vetor S
    inicia_t(chave, tamanho_chave); //inicialização de vetor T
    permutacao_s(); //permutação de S 
    gerar_k_xor(tamanho_palavra, palavra);
}

int main(){
    unsigned char P[256]; //palavra
    unsigned char K[256]; //chave
    
    scanf("%s", P);
    scanf(" %s", K);
    
    cifrar(K, P, strlen(K), strlen(P));
    return 0;
}