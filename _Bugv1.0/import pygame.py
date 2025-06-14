import pygame
import random

# 初始化
pygame.init()
WIDTH, HEIGHT = 400, 450
GRID_SIZE = 10
CELL_SIZE = 40
MINE_COUNT = 15
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("简易扫雷")

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
RED = (255, 0, 0)
COLORS = [None, (0, 0, 255), (0, 128, 0), (255, 0, 0), (0, 0, 128), 
          (128, 0, 0), (0, 128, 128), (0, 0, 0), (128, 128, 128)]

# 字体
font = pygame.font.SysFont('Arial', 20)
big_font = pygame.font.SysFont('Arial', 30)

# 创建游戏板
def create_board():
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # 放置地雷
    mines = 0
    while mines < MINE_COUNT:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if board[y][x] != -1:
            board[y][x] = -1
            mines += 1
            
            # 更新周围单元格的数字
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and board[ny][nx] != -1:
                        board[ny][nx] += 1
    return board

# 绘制游戏板
def draw_board():
    screen.fill(WHITE)
    
    # 绘制状态栏
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 50))
    text = big_font.render(f"剩余地雷: {MINE_COUNT - flagged}", True, BLACK)
    screen.blit(text, (10, 10))
    
    # 绘制网格
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE + 50, CELL_SIZE, CELL_SIZE)
            
            if revealed[y][x]:
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, DARK_GRAY, rect, 1)
                
                if board[y][x] == -1:  # 地雷
                    pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE//3)
                elif board[y][x] > 0:  # 数字
                    text = font.render(str(board[y][x]), True, COLORS[board[y][x]])
                    screen.blit(text, (x*CELL_SIZE + CELL_SIZE//3, y*CELL_SIZE + 50 + CELL_SIZE//4))
            else:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, DARK_GRAY, rect, 1)
                if flags[y][x]:  # 旗帜
                    pygame.draw.polygon(screen, RED, [
                        (x*CELL_SIZE + CELL_SIZE//2, y*CELL_SIZE + 50 + CELL_SIZE//4),
                        (x*CELL_SIZE + CELL_SIZE//4, y*CELL_SIZE + 50 + CELL_SIZE//2),
                        (x*CELL_SIZE + CELL_SIZE//2, y*CELL_SIZE + 50 + 3*CELL_SIZE//4),
                        (x*CELL_SIZE + 3*CELL_SIZE//4, y*CELL_SIZE + 50 + CELL_SIZE//2)
                    ])

# 揭示单元格
def reveal(x, y):
    if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE) or revealed[y][x] or flags[y][x]:
        return
    
    revealed[y][x] = True
    
    if board[y][x] == 0:  # 如果是空白单元格，递归揭示周围
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                reveal(x + dx, y + dy)
    elif board[y][x] == -1:  # 踩到地雷
        global game_over
        game_over = True
        # 显示所有地雷
        for my in range(GRID_SIZE):
            for mx in range(GRID_SIZE):
                if board[my][mx] == -1:
                    revealed[my][mx] = True

# 检查胜利条件
def check_win():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x] != -1 and not revealed[y][x]:
                return False
    return True

# 游戏主循环
def main():
    global board, revealed, flags, flagged, game_over
    
    board = create_board()
    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    flagged = 0
    game_over = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos[0] // CELL_SIZE, (event.pos[1] - 50) // CELL_SIZE
                    
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        if event.button == 1:  # 左键点击
                            reveal(x, y)
                            if board[y][x] == -1:  # 踩到地雷
                                game_over = True
                        elif event.button == 3:  # 右键点击
                            if not revealed[y][x]:
                                flags[y][x] = not flags[y][x]
                                flagged += 1 if flags[y][x] else -1
        
        draw_board()
        
        # 检查胜利
        if not game_over and check_win():
            text = big_font.render("你赢了!", True, BLACK)
            screen.blit(text, (WIDTH//2 - 50, 10))
            game_over = True
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()