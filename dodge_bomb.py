import os
import random
import sys
import time
import pygame as pg

# 定数定義
WIDTH, HEIGHT = 1100, 650
DELTA: dict[int, tuple[int, int]] = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

# 現在のディレクトリを変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する。

    Args:
        rct (pg.Rect): 判定対象のRect（こうかとんまたは爆弾）。

    Returns:
        tuple[bool, bool]: 真理値タプル（横方向, 縦方向）。
                           画面内ならTrue、画面外ならFalse。
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def game_over(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示し、5秒後に終了する。

    Args:
        screen (pg.Surface): ゲーム画面のSurface。
    """
    # 半透明の黒い画面を描画
    black_surface = pg.Surface((WIDTH, HEIGHT))
    black_surface.set_alpha(128)
    black_surface.fill((0, 0, 0))
    screen.blit(black_surface, (0, 0))

    # "Game Over"の文字列を描画
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    # 泣いているこうかとん画像を描画
    crying_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)

    # "Game Over"の両端に泣いているこうかとん画像を描画
    left_crying_kk_rct = crying_kk_img.get_rect()
    right_crying_kk_rct = crying_kk_img.get_rect()
    left_crying_kk_rct.center = (text_rect.left - 50, text_rect.centery)
    right_crying_kk_rct.center = (text_rect.right + 50, text_rect.centery)
    screen.blit(crying_kk_img, left_crying_kk_rct)
    screen.blit(crying_kk_img, right_crying_kk_rct)

    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す関数

    Returns:
        tuple[list[pg.Surface], list[int]]: 爆弾Surfaceのリストと加速度リスト
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    移動量の合計値タプルに対応する向きの画像Surfaceを返す関数

    Args:
        sum_mv (tuple[int, int]): 移動量の合計値タプル

    Returns:
        pg.Surface: 向きに対応するこうかとんの画像Surface
    """
    base_img = pg.image.load("fig/3.png")
    base_img2 = pg.transform.flip(base_img, True, False)  # 背景画像を左右反転

    #左
    if sum_mv == (-5, 0):
        return pg.transform.rotozoom(base_img, 0, 0.9)
    #左上
    elif sum_mv == (-5, -5):
        return pg.transform.rotozoom(base_img, -90, 0.9)
    #上
    elif sum_mv == (0, -5):
        return pg.transform.rotozoom(base_img, -90, 0.9)
    #右上
    elif sum_mv == (5, -5):
        return pg.transform.rotozoom(base_img2, 90, 0.9)#ここまではできてる
    
    #右 # 背景画像を左右反転
    elif sum_mv == (5, 0):
        return pg.transform.flip(base_img, True, False) 
    #下
    elif sum_mv == (0, 5):
        return pg.transform.rotozoom(base_img,90, 0.9)
    #静止
    else:
        return pg.transform.rotozoom(base_img, 0, 0.9)
    
def main() -> None:
    """
    ゲームのメインループを実行する。
    """
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = get_kk_img((0, 0))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の初期設定
    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾速度ベクトル

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return  # ゲームオーバー後に終了

        screen.blit(bg_img, [0, 0])

        # こうかとんの移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)

        # こうかとんが画面外なら元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        # こうかとんの画像を移動方向に応じて切り替える
        kk_img = get_kk_img(tuple(sum_mv))
        screen.blit(kk_img, kk_rct)

        # 爆弾の移動と拡大・加速
        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx = -vx
        if not tate:
            vy = -vy

        bb_img = bb_imgs[idx]
        bb_rct = bb_img.get_rect(center=bb_rct.center)
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()