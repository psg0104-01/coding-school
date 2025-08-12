import pygame
import sys

pygame.init()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("pong")

BACKGROUND_COLOR = (255, 255, 255)
BASECOLOR = (100, 100, 100)
LP_COLOR = (0, 0, 255)  # 왼쪽 패들 색상 (파란색)
RP_COLOR = (255, 0, 0)  # 오른쪽 패들 색상 (빨간색)

FPS = 60
fpsClock = pygame.time.Clock()

PADDLEINSET = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
BALL_SIZE = 10

leftPaddleY = 120
rightPaddleY = 120

leftScore = 0
rightScore = 0

fontObj = pygame.font.Font(None, 32)
TEXT_Y = 5

# 패들 속도 고정
paddleSpeed = 5

# 공 속도 기본값, 최대값, 증가량
BASE_SPEED = 1.5
MAX_SPEED = 10
SPEED_INCREMENT = 0.5  # 2번 튕길 때마다 0.5씩 증가

ballXMomentum = BASE_SPEED
ballYMomentum = BASE_SPEED

roundCount = 1

gameOver = False
winner = None

ballX = WINDOW_WIDTH // 2
ballY = WINDOW_HEIGHT // 2

ballMoveState = 0  # 0: 게임 진행, 1: 점수 후 애니메이션

targetX = ballX
targetY = ballY
animSpeed = 8

bounceCount = 0  # 패들에 튕긴 횟수 (속도 증가용)

def reset_ball_animation(loser):
    global ballX, ballY, ballMoveState, targetX, targetY, ballXMomentum, ballYMomentum, bounceCount
    ballX = WINDOW_WIDTH // 2
    ballY = WINDOW_HEIGHT // 2
    ballMoveState = 1
    bounceCount = 0
    ballXMomentum = BASE_SPEED
    ballYMomentum = BASE_SPEED
    if loser == "left":
        targetX = PADDLEINSET + PADDLE_WIDTH + BALL_SIZE + 1
        targetY = leftPaddleY + PADDLE_HEIGHT // 2
    else:
        targetX = WINDOW_WIDTH - PADDLEINSET - PADDLE_WIDTH - BALL_SIZE - 1
        targetY = rightPaddleY + PADDLE_HEIGHT // 2

def move_ball_to_target():
    global ballX, ballY, ballMoveState, ballXMomentum, ballYMomentum
    dx = targetX - ballX
    dy = targetY - ballY
    dist = (dx**2 + dy**2) ** 0.5
    if dist < animSpeed:
        ballX = targetX
        ballY = targetY
        ballMoveState = 0
        # 애니메이션 끝나면 공 속도 느리게 초기화
        if targetX < WINDOW_WIDTH // 2:
            ballXMomentum = BASE_SPEED
        else:
            ballXMomentum = -BASE_SPEED
        ballYMomentum = BASE_SPEED
    else:
        ballX += animSpeed * dx / dist
        ballY += animSpeed * dy / dist

def increase_speed():
    global ballXMomentum, ballYMomentum, bounceCount
    bounceCount += 1

    # 2번 튕길 때마다 공 속도 0.5씩 증가
    if bounceCount % 2 == 0:
        # 현재 속도의 방향 유지하면서 속도 증가
        speed = min(abs(ballXMomentum) + SPEED_INCREMENT, MAX_SPEED)
        ballXMomentum = speed if ballXMomentum > 0 else -speed
        ballYMomentum = speed if ballYMomentum > 0 else -speed

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if gameOver and event.key == pygame.K_SPACE:
                leftScore = 0
                rightScore = 0
                roundCount = 1
                ballX = WINDOW_WIDTH // 2
                ballY = WINDOW_HEIGHT // 2
                ballXMomentum = BASE_SPEED
                ballYMomentum = BASE_SPEED
                bounceCount = 0
                gameOver = False
                winner = None
                ballMoveState = 0
                leftPaddleY = 120
                rightPaddleY = 120

    pressed = pygame.key.get_pressed()

    if not gameOver:
        if ballMoveState == 0:
            # 패들 이동 (속도 고정)
            if pressed[pygame.K_UP]:
                rightPaddleY -= paddleSpeed
            if pressed[pygame.K_DOWN]:
                rightPaddleY += paddleSpeed
            if pressed[pygame.K_w]:
                leftPaddleY -= paddleSpeed
            if pressed[pygame.K_s]:
                leftPaddleY += paddleSpeed

            # 패들 화면 밖 이동 제한
            leftPaddleY = max(0, min(WINDOW_HEIGHT - PADDLE_HEIGHT, leftPaddleY))
            rightPaddleY = max(0, min(WINDOW_HEIGHT - PADDLE_HEIGHT, rightPaddleY))

            # 공 벽 충돌 시 방향 반전 (속도 증가 없음)
            if ballY < BALL_SIZE:
                ballYMomentum = abs(ballYMomentum)
            if ballY > WINDOW_HEIGHT - BALL_SIZE:
                ballYMomentum = -abs(ballYMomentum)

            # 왼쪽 패들 충돌 시 방향 반전 + 속도 증가
            if ballX <= PADDLEINSET + PADDLE_WIDTH and ballX > PADDLEINSET:
                if leftPaddleY < ballY < leftPaddleY + PADDLE_HEIGHT:
                    ballXMomentum = abs(ballXMomentum)
                    increase_speed()

            # 오른쪽 패들 충돌 시 방향 반전 + 속도 증가
            if ballX >= WINDOW_WIDTH - PADDLEINSET - PADDLE_WIDTH and ballX < WINDOW_WIDTH - PADDLEINSET:
                if rightPaddleY < ballY < rightPaddleY + PADDLE_HEIGHT:
                    ballXMomentum = -abs(ballXMomentum)
                    increase_speed()

            # 점수 처리 및 애니메이션 시작
            if ballX > WINDOW_WIDTH - BALL_SIZE:
                leftScore += 1
                roundCount += 1
                reset_ball_animation("right")

            if ballX < BALL_SIZE:
                rightScore += 1
                roundCount += 1
                reset_ball_animation("left")

            ballX += ballXMomentum
            ballY += ballYMomentum

            # 20점 도달 시 게임 종료
            if leftScore >= 20:
                gameOver = True
                winner = "left"
            elif rightScore >= 20:
                gameOver = True
                winner = "right"

        else:
            # 점수 후 공 애니메이션 이동
            move_ball_to_target()

    scoreText = f"{leftScore} : {rightScore}"
    leftPaddleRect = pygame.Rect(PADDLEINSET, leftPaddleY, PADDLE_WIDTH, PADDLE_HEIGHT)
    rightPaddleRect = pygame.Rect(WINDOW_WIDTH - PADDLEINSET - PADDLE_WIDTH, rightPaddleY, PADDLE_WIDTH, PADDLE_HEIGHT)

    WINDOW.fill(BACKGROUND_COLOR)

    pygame.draw.line(WINDOW, BASECOLOR, (WINDOW_WIDTH // 2, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT), 2)
    pygame.draw.rect(WINDOW, LP_COLOR, leftPaddleRect)
    pygame.draw.rect(WINDOW, RP_COLOR, rightPaddleRect)
    pygame.draw.circle(WINDOW, BASECOLOR, (int(ballX), int(ballY)), BALL_SIZE)

    textObj = fontObj.render(scoreText, True, BASECOLOR, None)
    TENT_X = (WINDOW_WIDTH - textObj.get_size()[0]) // 2
    WINDOW.blit(textObj, (TENT_X, TEXT_Y))

    bigFont = pygame.font.Font(None, 100)
    roundText = bigFont.render(str(roundCount), True, (200, 200, 200))
    roundX = (WINDOW_WIDTH - roundText.get_width()) // 2
    roundY = (WINDOW_HEIGHT - roundText.get_height()) // 2
    WINDOW.blit(roundText, (roundX, roundY))

    if gameOver:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        WINDOW.blit(overlay, (0, 0))

        winText = bigFont.render("WIN", True, (0, 0, 0))
        winX = (WINDOW_WIDTH - winText.get_width()) // 2
        winY = (WINDOW_HEIGHT // 2 - winText.get_height() // 2)
        WINDOW.blit(winText, (winX, winY))

        winnerColor = LP_COLOR if winner == "left" else RP_COLOR
        winnerText = fontObj.render("BLUE" if winner == "left" else "RED", True, winnerColor)
        winnerX = (WINDOW_WIDTH - winnerText.get_width()) // 2
        winnerY = winY - winnerText.get_height() - 10
        WINDOW.blit(winnerText, (winnerX, winnerY))

    pygame.display.update()
    fpsClock.tick(FPS)
