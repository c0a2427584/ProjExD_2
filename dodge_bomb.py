import os
import sys
import pygame as pg
import random
import time
from typing import List, Tuple

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def init_bb_imgs() -> Tuple[List[pg.Surface], List[int]]:  #演習２:ゲームオーバー画面
    """

    爆弾が拡大と加速

    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def gameover(screen: pg.Surface) -> None:    #演習１:ゲームオーバー画面
    """

    ゲーム終了画面
    surface
    
    """
    # 1. 黒い矩形を描画する
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(180)  #2 透明度を設定する
    
    # 3. 白文字でGame Overと書かれたフォントSurface
    font = pg.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    
    # 4. こうかとん
    try:
        cry_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.5)
        cry_kk_rect = cry_kk_img.get_rect(center=(WIDTH//1.4, HEIGHT//2.5 + 15))
    except:
        cry_kk_img = None
    
    # 5. 1のSurfaceをscreen Surfaceにblitする
    screen.blit(overlay, (0, 0))
    screen.blit(text, text_rect)
    if cry_kk_img:
        screen.blit(cry_kk_img, cry_kk_rect)
    
    pg.display.update()
    time.sleep(5)  # 6 显示5秒

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))         #ex2
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0)) 

    bb_imgs, bb_accs = init_bb_imgs() #

    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    vx, vy = +5, +5     #

    clock = pg.time.Clock()
    tmr = 0
    
    DELTA = {                 # ex1
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0)
    }

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, delta in DELTA.items(): #
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]

        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # ex3

        stage = min(tmr // 500, 9) 
        avx = vx * bb_accs[stage]  
        avy = vy * bb_accs[stage]  
        bb_img = bb_imgs[stage]

        bb_rct.move_ip(avx, avy) #s

        yoko, tate = check_bound(bb_rct) #
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        if kk_rct.colliderect(bb_rct):     #ex4
            gameover(screen)
            return  

        screen.blit(kk_img, kk_rct)

        screen.blit(bb_img, bb_rct)  # 
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
