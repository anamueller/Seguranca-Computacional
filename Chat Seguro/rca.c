#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Função para trocar os valores de dois bytes
void swap(unsigned char *a, unsigned char *b) {
    unsigned char temp = *a;
    *a = *b;
    *b = temp;
}

// Função para inicializar o estado do vetor S do RC4
void RC4_init(unsigned char *key, int key_length, unsigned char *S) {
    int i, j = 0;
    for (i = 0; i < 256; i++) {
        S[i] = i;
    }
    for (i = 0; i < 256; i++) {
        j = (j + S[i] + key[i % key_length]) % 256;
        swap(&S[i], &S[j]);
    }
}

// Função para cifrar ou decifrar uma string usando o RC4
void RC4_crypt(unsigned char *input, unsigned char *output, int input_length, unsigned char *S) {
    int i = 0, j = 0, k;
    for (k = 0; k < input_length; k++) {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        swap(&S[i], &S[j]);
        output[k] = input[k] ^ S[(S[i] + S[j]) % 256];
    }
}

void hex_to_bytes(char* hex_string, unsigned char* bytes) {
    int length = strlen(hex_string);
    for (int i = 0; i < length / 2; i++) {
        sscanf(hex_string + 2 * i, "%2hhx", &bytes[i]);
    }
}

int main(int argc, char *argv[]) {
    unsigned char *key;
    unsigned char *input;

    input = argv[2];
    key = argv[3];
    char type = argv[1][0];

    if (type == 'C'){
        int key_length = strlen(key);
        int input_length = strlen(input);

        unsigned char S[256];
        RC4_init(key, key_length, S);

        unsigned char *ciphertext = (unsigned char *)malloc(input_length * sizeof(unsigned char));
        RC4_crypt(input, ciphertext, input_length, S);

        for (int i = 0; i < input_length; i++) {
            printf("%02X", ciphertext[i]);
        }
    }
    else if (type == 'O'){
        unsigned char output[256], in[256];

        int input_length = strlen(input) / 2;
        hex_to_bytes(input, in);

        unsigned char S[256];
        RC4_init(key, strlen((char*)key), S);
        RC4_crypt(in, output, input_length, S);

        for (int i = 0; i < input_length; i++) {
            printf("%c", output[i]);
        }
    }

    return 0;
}
