#include<stdio.h>
#include<stdlib.h>
#include <string>
#include "pcre2posix.h"

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
        if (size < 1) 
            return 0;
        regex_t preg;
        string str(reinterpret_cast<const char*>(data), size);
        string pat(str);
        int flags = data[size/2] - 'a';  // Make it 0 when the byte is 'a'.
        if (0 == regcomp(&preg, pat.c_str(), flags)) {
            regmatch_t pmatch[5];
            regexec(&preg, str.c_str(), 5, pmatch, 0);
            regfree(&preg);
        }
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