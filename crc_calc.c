#include <stdlib.h>

u_int16_t ComputeCRC(unsigned char *Message, unsigned char MessLen)
{
    u_int16_t crc=0xFFFF;
    u_int16_t temp;
    u_int16_t quick;
    int i;
    for( i=0; i< MessLen; i++)
    {
        temp = (crc>>8) ^ Message[i];
        crc <<= 8;
        quick = temp ^ (temp >> 4);
        crc ^= quick;
        quick <<=5;
        crc ^= quick;
        quick <<= 7;
        crc ^= quick;
    }
    return crc;
}