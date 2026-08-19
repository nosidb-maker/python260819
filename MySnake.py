import random
import sys
from collections import deque

import pygame


# 게임판은 작은 정사각형 칸들로 구성되고, 뱀의 위치는 (가로 칸, 세로 칸)으로 저장한다.
CELL_SIZE = 24
GRID_WIDTH = 25
GRID_HEIGHT = 20
PLAY_WIDTH = CELL_SIZE * GRID_WIDTH
PLAY_HEIGHT = CELL_SIZE * GRID_HEIGHT
HEADER_HEIGHT = 64
WINDOW_WIDTH = PLAY_WIDTH
WINDOW_HEIGHT = PLAY_HEIGHT + HEADER_HEIGHT

BACKGROUND = (18, 24, 32)
BOARD_COLOR = (27, 36, 47)
GRID_COLOR = (38, 49, 62)
SNAKE_HEAD_COLOR = (82, 212, 137)
SNAKE_BODY_COLOR = (49, 168, 111)
SNAKE_DARK_COLOR = (28, 111, 76)
SNAKE_EYE_COLOR = (246, 250, 232)
SNAKE_PUPIL_COLOR = (18, 24, 32)
AI_HEAD_COLOR = (255, 190, 79)
AI_BODY_COLOR = (211, 133, 48)
AI_DARK_COLOR = (132, 78, 28)
FOOD_COLOR = (247, 106, 93)
TEXT_COLOR = (235, 241, 245)
MUTED_TEXT_COLOR = (154, 169, 181)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# 동시에 화면에 보여 줄 사과의 개수
FOOD_COUNT = 3


def make_font(size: int, bold: bool = False) -> pygame.font.Font:
    """Windows 기본 한글 글꼴을 우선 사용하고, 없으면 pygame 기본 글꼴을 사용한다."""
    candidates = ["malgungothic", "맑은 고딕", "segoeui", "arial"]
    for name in candidates:
        font_path = pygame.font.match_font(name, bold=bold)
        if font_path:
            return pygame.font.Font(font_path, size)
    return pygame.font.Font(None, size)


def new_foods(count: int, *snakes: deque[tuple[int, int]]) -> list[tuple[int, int]]:
    # 뱀의 몸이 차지한 칸을 제외한 빈 칸 목록을 만든다.
    occupied = {part for snake in snakes for part in snake}
    available = [
        (x, y)
        for y in range(GRID_HEIGHT)
        for x in range(GRID_WIDTH)
        if (x, y) not in occupied
    ]
    # 빈 칸 중에서 중복 없이 count개를 무작위로 선택한다.
    return random.sample(available, min(count, len(available)))


def reset_game() -> tuple[deque[tuple[int, int]], tuple[int, int], tuple[int, int], deque[tuple[int, int]], tuple[int, int], int, int, bool, bool]:
    # deque의 첫 번째 원소가 머리이고, 나머지 원소가 몸통과 꼬리이다.
    player = deque([(5, GRID_HEIGHT // 2)])
    computer = deque([(GRID_WIDTH - 6, GRID_HEIGHT // 2)])
    return player, RIGHT, RIGHT, computer, LEFT, 0, 0, False, False


def choose_computer_direction(
    computer: deque[tuple[int, int]],
    player: deque[tuple[int, int]],
    direction: tuple[int, int],
    foods: list[tuple[int, int]],
) -> tuple[int, int]:
    # 컴퓨터가 먹이를 향해 갈 수 없을 때 사용할 기본 방향이다.
    if not foods:
        return direction

    head_x, head_y = computer[0]
    # 바로 뒤로 돌아가는 것은 자기 몸과 부딪힐 수 있으므로 제외한다.
    reverse = (-direction[0], -direction[1])
    candidates = [UP, DOWN, LEFT, RIGHT]
    # 후보 순서를 섞으면 컴퓨터의 움직임이 매번 똑같지 않다.
    random.shuffle(candidates)
    if random.random() < 0.55:
        # 55% 확률로 가장 가까운 사과를 향하는 방향을 우선한다.
        candidates.sort(
            key=lambda move: min(
                abs(head_x + move[0] - food[0]) + abs(head_y + move[1] - food[1])
                for food in foods
            )
        )
    # 컴퓨터와 플레이어가 차지한 칸은 안전하지 않은 칸으로 취급한다.
    occupied = set(computer) | set(player)
    for candidate in candidates:
        if candidate == reverse:
            continue
        next_head = (head_x + candidate[0], head_y + candidate[1])
        # 게임판 밖으로 나가는 방향은 선택하지 않는다.
        if not (0 <= next_head[0] < GRID_WIDTH and 0 <= next_head[1] < GRID_HEIGHT):
            continue
        if next_head in occupied:
            continue
        return candidate
    return direction


def draw_text(
    screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    position: tuple[int, int],
    color: tuple[int, int, int] = TEXT_COLOR,
    center: bool = False,
) -> None:
    # 문자열을 이미지로 바꾼 뒤 화면에 붙인다. center가 True면 위치를 중앙으로 해석한다.
    image = font.render(text, True, color)
    rectangle = image.get_rect()
    if center:
        rectangle.center = position
    else:
        rectangle.topleft = position
    screen.blit(image, rectangle)


def draw_snake(
    screen: pygame.Surface,
    snake: deque[tuple[int, int]],
    direction: tuple[int, int],
    head_color: tuple[int, int, int],
    body_color: tuple[int, int, int],
    dark_color: tuple[int, int, int],
) -> None:
    # 게임 좌표를 실제 화면 픽셀 좌표로 변환한다.
    centers = [
        (x * CELL_SIZE + CELL_SIZE // 2, HEADER_HEIGHT + y * CELL_SIZE + CELL_SIZE // 2)
        for x, y in snake
    ]
    # 몸통 마디 사이를 굵은 선으로 연결해 하나의 뱀처럼 보이게 한다.
    if len(centers) > 1:
        pygame.draw.lines(screen, body_color, False, centers, CELL_SIZE - 6)

    # 뒤쪽 마디부터 그려야 머리와 몸통이 자연스럽게 겹쳐 보인다.
    for index, center in reversed(list(enumerate(centers))):
        radius = CELL_SIZE // 2 - 3 if index == 0 else CELL_SIZE // 2 - 4
        color = head_color if index == 0 else body_color
        pygame.draw.circle(screen, color, center, radius)
        if index > 0 and index % 3 == 0:
            pygame.draw.circle(screen, dark_color, center, 2)

    # 첫 번째 마디는 머리이므로 눈과 혀를 추가한다.
    head_x, head_y = centers[0]
    direction_x, direction_y = direction
    side_x, side_y = -direction_y, direction_x
    eye_distance = 5
    eye_forward = 5
    # 진행 방향의 양쪽에 눈을 하나씩 배치한다.
    for side in (-1, 1):
        eye_center = (
            head_x + direction_x * eye_forward + side_x * eye_distance * side,
            head_y + direction_y * eye_forward + side_y * eye_distance * side,
        )
        pygame.draw.circle(screen, SNAKE_EYE_COLOR, eye_center, 4)
        pupil_center = (
            eye_center[0] + direction_x * 2,
            eye_center[1] + direction_y * 2,
        )
        pygame.draw.circle(screen, SNAKE_PUPIL_COLOR, pupil_center, 2)

    # 머리 앞쪽에 갈라진 혀를 그린다.
    tongue_start = (
        head_x + direction_x * (CELL_SIZE // 2 - 2),
        head_y + direction_y * (CELL_SIZE // 2 - 2),
    )
    tongue_end = (
        tongue_start[0] + direction_x * 7,
        tongue_start[1] + direction_y * 7,
    )
    pygame.draw.line(screen, FOOD_COLOR, tongue_start, tongue_end, 2)
    pygame.draw.line(
        screen,
        FOOD_COLOR,
        tongue_end,
        (tongue_end[0] + side_x * 4, tongue_end[1] + side_y * 4),
        2,
    )
    pygame.draw.line(
        screen,
        FOOD_COLOR,
        tongue_end,
        (tongue_end[0] - side_x * 4, tongue_end[1] - side_y * 4),
        2,
    )


def draw_game(
    screen: pygame.Surface,
    player: deque[tuple[int, int]],
    player_direction: tuple[int, int],
    computer: deque[tuple[int, int]],
    computer_direction: tuple[int, int],
    foods: list[tuple[int, int]],
    player_score: int,
    computer_score: int,
    game_over: bool,
    paused: bool,
    winner: str | None,
    title_font: pygame.font.Font,
    body_font: pygame.font.Font,
) -> None:
    # 매 프레임마다 배경부터 다시 그려 이전 화면의 흔적을 지운다.
    screen.fill(BACKGROUND)
    draw_text(screen, title_font, "SNAKE", (18, 14))
    draw_text(screen, body_font, f"YOU {player_score:03d}   CPU {computer_score:03d}", (PLAY_WIDTH - 205, 23), MUTED_TEXT_COLOR)

    # 헤더 아래에 실제 게임판을 그린다.
    board = pygame.Rect(0, HEADER_HEIGHT, PLAY_WIDTH, PLAY_HEIGHT)
    pygame.draw.rect(screen, BOARD_COLOR, board)
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, GRID_COLOR, (x * CELL_SIZE, HEADER_HEIGHT), (x * CELL_SIZE, WINDOW_HEIGHT))
    for y in range(GRID_HEIGHT + 1):
        board_y = HEADER_HEIGHT + y * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR, (0, board_y), (PLAY_WIDTH, board_y))

    # 현재 존재하는 모든 사과를 사과 몸통, 꼭지, 잎으로 그린다.
    for food in foods:
        food_center = (
            food[0] * CELL_SIZE + CELL_SIZE // 2,
            HEADER_HEIGHT + food[1] * CELL_SIZE + CELL_SIZE // 2 + 2,
        )
        pygame.draw.circle(screen, FOOD_COLOR, food_center, CELL_SIZE // 2 - 4)
        pygame.draw.line(
            screen,
            (91, 61, 39),
            (food_center[0], food_center[1] - 9),
            (food_center[0] + 2, food_center[1] - 14),
            3,
        )
        pygame.draw.ellipse(
            screen,
            SNAKE_HEAD_COLOR,
            pygame.Rect(food_center[0] + 1, food_center[1] - 15, 7, 4),
        )

    # 플레이어는 초록색, 컴퓨터는 주황색으로 구분한다.
    draw_snake(screen, player, player_direction, SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, SNAKE_DARK_COLOR)
    draw_snake(screen, computer, computer_direction, AI_HEAD_COLOR, AI_BODY_COLOR, AI_DARK_COLOR)

    # 일시정지나 게임 오버 때는 게임판 위에 반투명 안내판을 올린다.
    if paused or game_over:
        overlay = pygame.Surface((PLAY_WIDTH, PLAY_HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 12, 18, 205))
        screen.blit(overlay, (0, HEADER_HEIGHT))
        if game_over:
            result = f"{winner} WINS" if winner else "DRAW"
            draw_text(screen, title_font, result, (PLAY_WIDTH // 2, WINDOW_HEIGHT // 2 - 28), center=True)
            draw_text(screen, body_font, "Press R to play again", (PLAY_WIDTH // 2, WINDOW_HEIGHT // 2 + 18), MUTED_TEXT_COLOR, center=True)
        else:
            draw_text(screen, title_font, "PAUSED", (PLAY_WIDTH // 2, WINDOW_HEIGHT // 2 - 14), center=True)
            draw_text(screen, body_font, "Press P to continue", (PLAY_WIDTH // 2, WINDOW_HEIGHT // 2 + 28), MUTED_TEXT_COLOR, center=True)


def run() -> None:
    # pygame을 초기화하고 게임 창과 시계를 준비한다.
    pygame.init()
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    title_font = make_font(26, bold=True)
    body_font = make_font(18)

    # 게임에 필요한 모든 상태를 한 번에 준비한다.
    player, player_direction, next_player_direction, computer, computer_direction, player_score, computer_score, game_over, paused = reset_game()
    foods = new_foods(FOOD_COUNT, player, computer)
    winner = None
    move_timer = 0
    move_interval = 125

    # 이 반복문이 게임의 심장이다. 입력 받기 -> 이동/판정 -> 화면 그리기를 반복한다.
    while True:
        elapsed = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type != pygame.KEYDOWN:
                continue
            # 창 닫기, ESC, Q는 게임을 종료한다.
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_p and not game_over:
                paused = not paused
            if event.key == pygame.K_r and game_over:
                player, player_direction, next_player_direction, computer, computer_direction, player_score, computer_score, game_over, paused = reset_game()
                foods = new_foods(FOOD_COUNT, player, computer)
                winner = None
                move_timer = 0

            # 키보드 입력을 방향 벡터로 변환한다.
            key_directions = {
                pygame.K_UP: UP,
                pygame.K_w: UP,
                pygame.K_DOWN: DOWN,
                pygame.K_s: DOWN,
                pygame.K_LEFT: LEFT,
                pygame.K_a: LEFT,
                pygame.K_RIGHT: RIGHT,
                pygame.K_d: RIGHT,
            }
            requested_direction = key_directions.get(event.key)
            if requested_direction and requested_direction != (-player_direction[0], -player_direction[1]):
                next_player_direction = requested_direction

        # 게임이 진행 중일 때만 뱀을 이동시킨다.
        if not paused and not game_over:
            move_timer += elapsed
            if move_timer >= move_interval:
            # 일정 시간이 지나면 두 뱀을 같은 순간에 한 칸씩 이동시킨다.
                move_timer -= move_interval
                player_direction = next_player_direction
                computer_direction = choose_computer_direction(computer, player, computer_direction, foods)
                player_head_x, player_head_y = player[0]
                computer_head_x, computer_head_y = computer[0]
                new_player_head = (
                    player_head_x + player_direction[0],
                    player_head_y + player_direction[1],
                )
                new_computer_head = (
                    computer_head_x + computer_direction[0],
                    computer_head_y + computer_direction[1],
                )
                # 머리가 벽, 자기 몸, 상대 뱀, 상대 머리와 부딪혔는지 확인한다.
                player_hit = (
                    not (0 <= new_player_head[0] < GRID_WIDTH and 0 <= new_player_head[1] < GRID_HEIGHT)
                    or new_player_head in list(player)[:-1]
                    or new_player_head in computer
                    or new_player_head == new_computer_head
                )
                computer_hit = (
                    not (0 <= new_computer_head[0] < GRID_WIDTH and 0 <= new_computer_head[1] < GRID_HEIGHT)
                    or new_computer_head in list(computer)[:-1]
                    or new_computer_head in player
                    or new_computer_head == new_player_head
                )

                # 둘 중 하나라도 충돌하면 즉시 게임을 끝내고 승자를 정한다.
                if player_hit or computer_hit:
                    game_over = True
                    if player_hit and not computer_hit:
                        winner = "CPU"
                    elif computer_hit and not player_hit:
                        winner = "YOU"
                else:
                    # 충돌하지 않았다면 머리를 앞에 추가하고, 사과를 먹지 않은 뱀의 꼬리를 제거한다.
                    player_eats = new_player_head in foods
                    computer_eats = new_computer_head in foods and not player_eats
                    player.appendleft(new_player_head)
                    computer.appendleft(new_computer_head)
                    if player_eats:
                        player_score += 1
                    else:
                        player.pop()
                    if computer_eats:
                        computer_score += 1
                    else:
                        computer.pop()
                    # 사과를 먹은 자리에는 새 사과를 하나 추가해 항상 여러 개가 유지되게 한다.
                    if player_eats or computer_eats:
                        eaten_food = new_player_head if player_eats else new_computer_head
                        foods.remove(eaten_food)
                        foods.extend(new_foods(1, player, computer, *[deque([item]) for item in foods]))
                        move_interval = max(65, 125 - (player_score + computer_score) * 2)

        # 계산이 끝난 현재 상태를 화면에 표시한다.
        draw_game(
            screen,
            player,
            player_direction,
            computer,
            computer_direction,
            foods,
            player_score,
            computer_score,
            game_over,
            paused,
            winner,
            title_font,
            body_font,
        )
        pygame.display.flip()


if __name__ == "__main__":
    run()