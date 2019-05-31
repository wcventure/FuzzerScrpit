#include<stdio.h>
#include<stdlib.h>
#include<string>
#include<openssl/evp.h>

using std::string;

int main(int argc, char **argv)
{
    unsigned char *data;
    size_t size;

    if(argc == 2) {
        FILE *fp;
        if ((fp = fopen(argv[1], "rb")) == NULL)
            exit(0);
        fseek(fp, 0, SEEK_END);
        int fileLen = ftell(fp);
        size = fileLen;
        data = (unsigned char *) malloc(sizeof(unsigned char)*fileLen);
        fseek(fp, 0, SEEK_SET);
        fread(data, fileLen, sizeof(unsigned char), fp);
        fclose(fp);

        /* Program under test */
        const uint8_t *bufp = data;
        EVP_PKEY_free(d2i_AutoPrivateKey(NULL, &bufp, size));
        return 0;
        /* Program under test */

        free(data);
    }
    else if (argc <2)
        printf("No input file.\n");
    else
        printf("Too many parameter.\n");
    
    return 0;
}