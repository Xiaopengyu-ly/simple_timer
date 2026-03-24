import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 读取历史最高分
try:
    with open("high_score.txt", "r") as file:
        content = file.read().strip()
        if content:
            high_score = int(content)
        else:
            # 文件为空或只包含空白字符，则设置初始历史最高分为0
            high_score = 0
except FileNotFoundError:
    # 如果文件不存在，则设置初始历史最高分为0
    high_score = 0

#状态机循环
while True:
    # 设置游戏窗口大小
    screen_width = 1600
    screen_height = 900

    # 创建游戏窗口
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 设置游戏标题
    pygame.display.set_caption("简易跑酷游戏")

    # 加载角色和背景图片
    character = pygame.image.load("2023-12-04_08-26-05_134.jpg")
    background = pygame.image.load("2023-08-25_13-55-35_722.jpg")

    # 获取背景图片的实际宽度和高度
    background_image_width, background_image_height = background.get_size()

    # 加载金币图片
    coin_image = pygame.image.load("R.png")

    # 更改金币图片大小
    coin_width = 80
    coin_height = 80
    coin_image = pygame.transform.scale(coin_image, (coin_width, coin_height))

    # # 定义方框矩形
    # obstacle_box = pygame.Rect(20, 20, screen_width // 1-20, screen_height // 1-20)

    # 更改角色图片大小
    new_character_width = 120
    new_character_height = 160
    character = pygame.transform.scale(character, (new_character_width, new_character_height))

    # 设置角色初始位置
    character_x = 50
    character_y = screen_height - character.get_height()

    # Load obstacle texture image
    obstacle_texture = pygame.image.load("CXalien.png")
    # Define obstacle width and height
    obstacle_width = 200
    obstacle_height = 100
    # Resize the obstacle texture if needed
    obstacle_texture = pygame.transform.scale(obstacle_texture, (obstacle_width, obstacle_height))

    # 创建障碍物列表
    obstacles = []
    num_obstacles = 5
    # 障碍物移动速度
    obstacle_speed_value = 4
    for i in range(num_obstacles):
        obstacle_x = random.randint(0, screen_width - obstacle_width)
        obstacle_y = random.randint(0, screen_height - obstacle_height - 100)
        # 随机选择初始方向
        obstacle_speed = random.choice([(4, 0), (-4, 0), (0, 4), (0, -4)])
        obstacles.append({"rect": pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height),
                        "speed": obstacle_speed, "last_update": 0})

    # 新增变量来追踪障碍物移动方向的冷却时间
    obstacle_direction_cooldown = 0  # 计时器初始化为0

    # 创建金币列表
    coins = []
    num_coins = 3
    for i in range(num_coins):
        coin_x = random.randint(0, screen_width - coin_width)
        coin_y = random.randint(0, screen_height - coin_height - 100)
        coins.append({"rect": pygame.Rect(coin_x, coin_y, coin_width, coin_height), "value": 50})

    # 初始化分数
    score = 0

    # 新增变量来追踪角色是否处于屏幕中央
    reached_center = False

    # 新增变量来追踪屏幕中央计分的冷却时间
    center_cooldown = 0  # 计时器初始化为0

    # 新增变量来追踪游戏是否结束
    game_over = False

    # 游戏主循环
    while not game_over:
        # 处理用户输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # 处理按键
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_x -= 9
        if keys[pygame.K_RIGHT]:
            character_x += 9
        if keys[pygame.K_UP]:
            character_y -= 9
        if keys[pygame.K_DOWN]:
            character_y += 9

        # 限制角色在屏幕内移动
        character_x = max(min(character_x, screen_width - character.get_width()), 0)
        character_y = max(min(character_y, screen_height - character.get_height()), 0)

        # 检查角色是否与障碍物碰撞
        character_center_x = character_x + character.get_width() // 2
        character_center_y = character_y + character.get_height() // 2
        buffer1 = character.get_width() // 1.1  # 或者 character.get_height() // 4
        for obstacle in obstacles:
            obstacle_center_x = obstacle["rect"].x + obstacle["rect"].width // 2
            obstacle_center_y = obstacle["rect"].y + obstacle["rect"].height // 2

            if (character_center_x > obstacle_center_x - buffer1 and character_center_x < obstacle_center_x + buffer1) and \
                    (character_center_y > obstacle_center_y - buffer1 and character_center_y < obstacle_center_y + buffer1):
                game_over = True

        # 检查角色是否吃到金币
        character_rect = pygame.Rect(character_x, character_y, character.get_width(), character.get_height())
        for coin in coins:
            if character_rect.colliderect(coin["rect"]):
                score += coin["value"]
                coins.remove(coin)


        # 更新障碍物位置
        current_time = pygame.time.get_ticks()

        # 当冷却时间结束时，改变所有障碍物的移动方向，并重置冷却时间
        if obstacle_direction_cooldown == 0:
            for obstacle in obstacles:
                obstacle["speed"] = random.choice([(obstacle_speed_value, 0), (-obstacle_speed_value, 0), (0, obstacle_speed_value), (0, -obstacle_speed_value)])
            obstacle_direction_cooldown = 1200  # 冷却时间设置为20秒（60帧/秒 * 20秒）
            obstacle_speed_value = obstacle_speed_value + 0.3

        # 更新冷却时间
        if obstacle_direction_cooldown > 0:
            obstacle_direction_cooldown -= 1

        for obstacle in obstacles:
            if current_time - obstacle["last_update"] > 30:  # 降低速度以更好地观察
                # 移动障碍物
                obstacle["rect"].move_ip(obstacle["speed"])

                # 碰撞检测
                if obstacle["rect"].left < 0 or obstacle["rect"].right > screen_width:
                    obstacle["speed"] = (-obstacle["speed"][0], obstacle["speed"][1])
                if obstacle["rect"].top < 0 or obstacle["rect"].bottom > screen_height:
                    obstacle["speed"] = (obstacle["speed"][0], -obstacle["speed"][1])

                obstacle["last_update"] = current_time

        center_rect = pygame.Surface((100, 100))
        center_rect.fill((0, 0, 0))

        # 绘制背景
        screen.blit(background, (0, 0))
        # 绘制背景
        screen.blit(background, (0, 0))

        # # 绘制方框边缘
        # pygame.draw.rect(screen, (255, 0, 0), obstacle_box, 2)  # 红色边框，宽度为2像素

        # 绘制障碍物
        for obstacle in obstacles:
            # Draw the obstacle texture instead of a black rectangle
            screen.blit(obstacle_texture, (obstacle["rect"].x, obstacle["rect"].y))

        # 绘制角色
        screen.blit(character, (character_x, character_y))

        # 检查角色是否到达背景图片中心
        character_center_x = character_x + character.get_width() // 2
        character_center_y = character_y + character.get_height() // 2
        buffer2 = character.get_width() // 8  # 或者 character.get_height() // 4
        background_center_x = screen_width // 2 + 5
        background_center_y = screen_height - 530
        # pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(background_center_x - buffer2, background_center_y - buffer2, buffer2 * 2, buffer2 * 2))
        if (character_center_x > background_center_x - buffer2 and character_center_x < background_center_x + buffer2) and \
                (character_center_y > background_center_y - buffer2 and character_center_y < background_center_y + buffer2):
            # 只有在冷却时间结束且角色之前没有到达过屏幕中央时，才得分
            if center_cooldown == 0 and not reached_center:
                score += 100
                reached_center = True
                center_cooldown = 120  # 冷却时间设置为2秒（60帧/秒 * 2秒）
        # 更新冷却时间
        if center_cooldown > 0:
            center_cooldown -= 1

        # 如果所有金币都被吃掉，且角色到达屏幕中央，生成新的金币，并重置状态
        if len(coins) == 0 and reached_center:
            for i in range(num_coins):
                coin_x = random.randint(0, screen_width - coin_width)
                coin_y = random.randint(0, screen_height - coin_height - 100)
                coins.append({"rect": pygame.Rect(coin_x, coin_y, coin_width, coin_height), "value": 50})
            reached_center = False  # 重置状态

        # 绘制金币
        for coin in coins:
            screen.blit(coin_image, (coin["rect"].x, coin["rect"].y))

        # 绘制分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (screen_width - 180, 20))

        # 更新游戏窗口
        pygame.display.update()

        # 控制帧率
        pygame.time.Clock().tick(60)

    if score > high_score:
        high_score = score
    # 更新历史最高分记录
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

    # 结算界面
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RCTRL:  # 处理大写和小写R
                    game_over = False

        screen.fill((0, 0, 0))  # 清空屏幕

        # 显示最终得分
        score_text_large = font_large.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(score_text_large, (screen_width // 2 - score_text_large.get_width() // 2, screen_height // 4))

        # 显示历史最高分
        high_score_text = font_small.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height * 3 // 8))

        # 显示游戏结束提示
        game_over_text = font_large.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))

        # 显示重新开始提示
        restart_text = font_small.render("Press RCTRL to restart", True, (255, 255, 255))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height * 5 // 8))

        # 显示退出提示
        exit_text = font_small.render("Press ESC to exit", True, (255, 255, 255))
        screen.blit(exit_text, (screen_width // 2 - exit_text.get_width() // 2, screen_height * 3 // 4))

        pygame.display.update()
        pygame.time.Clock().tick(60)