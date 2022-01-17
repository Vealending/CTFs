#include <sodium.h>

__int64 __fastcall bin2hex_length(__int64 a1);

int main(int argc, char* argv[])
{
    sodium_init();

    //char* user_time_string = argv[1];
    char* user_time_string = "username=user:timestamp=1642383996";
    char* bin;
    char* expected_response;
    __int64 user_time_string_length = strlen(user_time_string);
    __int64 bin_length = user_time_string_length + 16;
    __int64 response_size = bin2hex_length(bin_length);
    __int64 hex_response_size;
    __int64 keyfile_size = 32;
    char* keyfile_pointer = sodium_malloc(keyfile_size);

    FILE* keyfile = fopen("./keyfile", "rb");
    fread(keyfile_pointer, 32, 1, keyfile);
    fclose(keyfile);
    char nonce[crypto_secretbox_NONCEBYTES];
    bin = sodium_malloc(bin_length);
    expected_response = calloc(1, response_size);
    memset(nonce, 0, 24);

    crypto_secretbox_easy(bin, user_time_string, user_time_string_length, nonce, keyfile_pointer);

    hex_response_size = bin2hex_length(bin_length);
    sodium_bin2hex(expected_response, hex_response_size, bin, bin_length);

    printf(expected_response);

    return 1;
}

__int64 __fastcall bin2hex_length(__int64 a1)
{
    return 2 * a1 + 1;
}
