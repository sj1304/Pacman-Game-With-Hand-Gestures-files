import pygame
import sys

YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)

def show_start_screen(screen, font, release):
    clock = pygame.time.Clock()
    blink = True
    blink_timer = 0

    title_font = pygame.font.SysFont(None, 54)
    subtitle_font = pygame.font.SysFont(None, 30)

    while True:
        screen.fill(BLACK)

        # ----- TITLE -----
        title = title_font.render("GESTURE CONTROLLED PAC-MAN", True, YELLOW)
        screen.blit(
            title,
            (screen.get_width()//2 - title.get_width()//2, 120)
        )

        # ----- SUBTITLE -----
        subtitle = subtitle_font.render(
            "Play using Hand Gestures (No Keyboard)",
            True,
            WHITE
        )
        screen.blit(
            subtitle,
            (screen.get_width()//2 - subtitle.get_width()//2, 180)
        )

        # ----- BLINKING START TEXT -----
        blink_timer += 1
        if blink_timer > 30:
            blink = not blink
            blink_timer = 0

        if blink:
            start_text = font.render("PRESS ENTER TO START", True, WHITE)
            screen.blit(
                start_text,
                (screen.get_width()//2 - start_text.get_width()//2, 280)
            )

        # ----- FOOTER -----
        footer = subtitle_font.render(
            "Press Q to Quit",
            True,
            GRAY
        )
        screen.blit(
            footer,
            (screen.get_width()//2 - footer.get_width()//2, 330)
        )

        pygame.display.flip()
        clock.tick(60)

        # ----- EVENTS -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                release()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    release()
                    sys.exit()


# ---------- GAME OVER SCREEN ----------
def show_game_over(screen, font, score, high_score, save_high_score, reset_game, release):
    WIDTH, HEIGHT = screen.get_size()

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    while True:
        screen.fill((0, 0, 0))

        over = font.render("GAME OVER", True, (255, 0, 0))
        sc = font.render(f"Your Score: {score}", True, (255, 255, 255))
        hs = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        restart = font.render("Press ENTER for New Game", True, (255, 255, 255))
        quit_txt = font.render("Press Q to Quit", True, (255, 255, 255))

        screen.blit(over, (WIDTH//2 - over.get_width()//2, 160))
        screen.blit(sc, (WIDTH//2 - sc.get_width()//2, 210))
        screen.blit(hs, (WIDTH//2 - hs.get_width()//2, 250))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 310))
        screen.blit(quit_txt, (WIDTH//2 - quit_txt.get_width()//2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                release()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    return high_score
                if event.key == pygame.K_q:
                    pygame.quit()
                    release()
                    sys.exit()
