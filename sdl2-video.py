# coding=utf-8
import threading
import sys
from sdl2 import *
import time


class video_ctx:  # Context

    def __init__(self, fid):
        self.f = open(fid, 'rb')
        self.videoing = 1

    def __del__(self):
        self.f.close


def refresh_video(obj):

    c = obj
    ev = SDL_Event()
    while c.videoing:
        ev.type = SDL_USEREVENT + 1
        SDL_PushEvent(ev)
        SDL_Delay(40)

    ev.type = SDL_USEREVENT + 2
    SDL_PushEvent(ev)


def main():
    print ("begin ...")

    ctx = video_ctx('test_yuv420p_480x272.yuv')

    threads = []
    threads.append(
        threading.Thread(target=refresh_video, args=(ctx,)))  # args must be tuple
    for t in threads:
        t.setDaemon(True)  # run at backend
        t.start()

    SDL_Init(SDL_INIT_VIDEO)
    screen = SDL_CreateWindow(b"Hello World",
                              SDL_WINDOWPOS_UNDEFINED,
                              SDL_WINDOWPOS_UNDEFINED,
                              480, 272,
                              SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE)
    sdlRenderer = SDL_CreateRenderer(screen, -1, 0)
    sdlTexture = SDL_CreateTexture(
        sdlRenderer, SDL_PIXELFORMAT_IYUV, SDL_TEXTUREACCESS_STREAMING, 480, 272)

    ev = SDL_Event()
    running = True
    screen_w = 480
    screen_h = 272
    sdlRect = SDL_Rect(0, 0, screen_w, screen_h)
    while running:

        SDL_WaitEvent(ev)
        if ev.type == SDL_USEREVENT + 1:

            buffer = ctx.f.read(int(480 * 272 * 12 / 8))
            if not buffer:
                ctx.videoing = 0
                running = False
            else:
                SDL_UpdateTexture(sdlTexture, None, buffer, 480)
                SDL_RenderClear(sdlRenderer)
                SDL_RenderCopy(sdlRenderer, sdlTexture, None, sdlRect)
                SDL_RenderPresent(sdlRenderer)

        elif ev.type == SDL_QUIT:
            print (ev.type)
            ctx.videoing = 0
            running = False

    t.join()
    print ("exit ... %s" % time.ctime())
    SDL_DestroyWindow(screen)
    SDL_Quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
