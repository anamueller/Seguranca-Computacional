#include <stdio.h>
#include <stdlib.h>

int P10[10] ={2,4,1,6,3,9,0,8,7,5};
int P8[8] = {5,2,6,3,7,4,9,8};
int P4[4] = {1,3,2,0};
int EP[8] = {3,0,1,2,1,2,3,0};
int IP[8] = {1,5,2,0,3,7,4,6};
int IP_inv[8] = {3,0,2,4,6,1,7,5};
int i;
int S0[4][4]= {{1,0,3,2},
                {3,2,1,0},
                {0,2,1,3},
                {3,1,3,2}};

int S1[4][4]= {{1,1,2,3},
                {2,0,1,3},
                {3,0,1,0},
                {2,1,0,3}};

void copy(char copiado[], char copia[], int tam){
    for(i=0;i<tam;i++){
        copia[i]=copiado[i];
    }
}

void permutacao(char chave[]){
    char aux[10];
    copy(chave, aux, 10);
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
    copy(chave, aux, 10);//copiando para usar em k2
    rotacionar(aux);
    rotacionar(aux); //k2 rotaciona 2 para esquerda após ls-1

    for(i=0;i<8;i++){
        k1[i]=chave[P8[i]];
    } //aplica p8

    for(i=0;i<8;i++){
        k2[i]=aux[P8[i]];
    } //aplica p8
}

void permutacao_fk(char chave[]){
    char aux[8];
    copy(chave,aux,8);

    for(i=0;i<8;i++){
        chave[i]=aux[IP[i]];
    }
}

void expansao(char chave_4[], char chave_8[]){
    for(i=0;i<8;i++){
        chave_8[i]=chave_4[EP[i]];
    }
}

void xor(char seq[], char chave[], int n){
    /*
    |xor| 1 | 0 |
    | 1 | 0 | 1 |
    | 0 | 1 | 0 |
    */
    char aux[n];
    copy(seq, aux, n);
    for(i=0;i<n;i++){
        if(aux[i]==1){
            if(chave[i]=='1'){
                seq[i]='0';
            }
            else if(chave[i]=='0'){
                seq[i]='1';
            }
        }
        else if(aux[i]==0){
            if(chave[i]=='1'){
                seq[i]='1';
            }
            else if(chave[i]=='0'){
                seq[i]='0';
            }
        }
    }
}

void s0_s1(char seq_8[], char seq_4[]){
    char left[4], right[4];
    for(i=0;i<4;i++){
        left[i]=seq_8[i];
        right[i]=seq_8[i+4];
    } //separando para irem para s0 e s1
    int L0, C0, L1, C1;
    //00=0, 01=1, 10=2, 11=3;
    if(left[0]=='0'){
        if(left[3]=='0'){
            L0 = 0;
        }
        else if(left[3]=='1'){
            L0 = 1;
        }
    }
    else if(left[0]=='1'){
        if(left[3]=='0'){
            L0 = 2;
        }
        else if(left[3]=='1'){
            L0 = 3;
        }
    }
    if(right[0]=='0'){
        if(right[3]=='0'){
            L1 = 0;
        }
        else if(right[3]=='1'){
            L1 = 1;
        }
    }
    else if(right[0]=='1'){
        if(right[3]=='0'){
            L1 = 2;
        }
        else if(right[3]=='1'){
            L1 = 3;
        }
    }

    switch (S0[L0][L1])
    {
    case 0:
        left[0]='0';
        left[1]='0';
        break;
    
    case 1:
        left[0]='0';
        left[1]='1';
        break;
    
    case 2:
        left[0]='1';
        left[1]='0';
        break;

    case 3:
        left[0]='1';
        left[1]='1';
        break;

    default:
        break;
    }

    switch (S1[L0][L1])
    {
    case 0:
        right[0]='0';
        right[1]='0';
        break;
    
    case 1:
        right[0]='0';
        right[1]='1';
        break;
    
    case 2:
        right[0]='1';
        right[1]='0';
        break;

    case 3:
        right[0]='1';
        right[1]='1';
        break;

    default:
        break;
    }

    for(i=0;i<2;i++){
        seq_4[i] = left[i];
        seq_4[i+2] = right[i];
    }

}

void funcao_complexa(char seq_8[], char k1[]){
    permutacao_fk(seq_8);//permutacao inicial
    char left4bits[4], right4bits[4]; //salvando para utilizar no final da funcao
    for(i=0;i<4;i++){
        left4bits[i]=seq_8[i];
        right4bits[i]=seq_8[i+4];
    }
    expansao(right4bits, seq_8);//expansao de 4 bits para 8
    xor(seq_8, k1, 8);//xor com a k1
    char seq_4[4], result[4];
    s0_s1(seq_8, seq_4); //s0 e s1 e junta para p4
    for(i=0;i<4;i++){
        result[i]=seq_4[P4[i]];
    } //aplica p4
    xor(seq_4, left4bits, 4);//xor com left4bits
    //sai 4 bits
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
            scanf(" %c", &B[j]);
        }

        //fazer a operação
    }

    fk1_e_k2(K, K1, K2);
    funcao_complexa(B, K1);

    printf("\nchave k1\n");
    for(i=0;i<8;i++){
        printf("%c ", K1[i]);
    }

    printf("\nchave k2\n");
    for(i=0;i<8;i++){
        printf("%c ", K2[i]);
    }

    printf("\nchave B\n");
    for(i=0;i<8;i++){
        printf("%c ", B[i]);
    }


    return 0;
}