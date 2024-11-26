import os
import sys
import pygame as pg
import random

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の設定
    bb_img = pg.Surface((20, 20))#爆弾の空のsurfaceを作成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)#爆弾円を作成
    bb_img.set_colorkey((0, 0, 0))#爆弾の黒色を透明化
    bb_rct = bb_img.get_rect()#爆弾Rectを抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)#爆弾の初期位置をランダムに設定
    # bb_rct.x = random.randint(0, WIDTH)
    # bb_rct.y = random.randint(0, HEIGHT)
    vx, vy = 5, 5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # キャラクターの移動
        DELTA = {
            pg.K_UP: (0, -5),
            pg.K_DOWN: (0, +5),
            pg.K_LEFT: (-5, 0),
            pg.K_RIGHT: (5, 0)
        }

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        # キー入力による移動量の計算
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]

        kk_rct.move_ip(sum_mv)

        # 爆弾の移動
        bb_rct.move_ip(vx, vy)

        

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
