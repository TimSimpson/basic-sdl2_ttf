#include <SDL_ttf.h>

int main(int argc, char* argv[])
{
    if(TTF_Init()==-1) {
        return 1;
    }
    return 0;
}
