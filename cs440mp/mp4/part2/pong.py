import random
import numpy as np
import pygame, sys
from pygame.locals import *
import argparse

from util import save_obj, load_obj, output_stat
import q_learning

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")
parser = argparse.ArgumentParser(description = 'Pong Game Q-Learning.')
parser.register('type', 'bool', str2bool)
parser.add_argument("-mode", nargs = '?', default = 'play', help = 'Mode (play/train/test/tune)')
parser.add_argument("-gmode", nargs = '?', default = 'two', help = 'Game Mode (single/two)')
parser.add_argument("-gravity", nargs = '?', type = float, default = 0, help = 'Gravity involved (default = 0, normal = 0.001)')
parser.add_argument("-ctrl", nargs = '?', default = 'manual', help = 'Control method (auto/manual)')
parser.add_argument("-load", nargs = '?', default = 'init', help = 'Trained Q table path to load')
parser.add_argument("-save", nargs = '?', default = 'none', help = 'Trained Q table path to save')
parser.add_argument("--save-tune", nargs = '?', default = 'tuning.lst', help = 'Tuning result path to save')
parser.add_argument("--train-show-stat", nargs = '?', type = 'bool', default = 'True', help = 'Show statistics after training (default = True)')
parser.add_argument("--test-show-stat", nargs = '?', type = 'bool', default = 'False', help = 'Show statistics after testing (default = False)')
parser.add_argument("--play-show-stat", nargs = '?', type = 'bool', default = 'False', help = 'Show statistics after playing (default = False)')
parser.add_argument("-alpha", nargs = '?', type = float, default = 1.0, help = 'Learning rate (default = 1.0)')
parser.add_argument("-decay", nargs = '?', type = int, default = 1000, help = 'Decay factor (default = 1000)')
parser.add_argument("-gamma", nargs = '?', type = float, default = 0.3, help = 'Reward discount (default = 0.3)')
parser.add_argument("-xd", nargs = '?', type = int, default = 12, help = 'Number of discrete value for ball x (default = 12)')
parser.add_argument("-yd", nargs = '?', type = int, default = 12, help = 'Number of discrete value for ball y (default = 12)')
parser.add_argument("-pd", nargs = '?', type = int, default = 12, help = 'Number of discrete value for paddle y (default = 12)')
parser.add_argument("-iter", nargs = '?', type = int, default = 15000, help = 'Training iteration (default = 15000)')
parser.add_argument("-testiter", nargs = '?', type = int, default = 1000, help = 'Testing iteration (default = 1000)')
parser.add_argument("-ne", nargs = '?', type = int, default = 10, help = 'Exploration policy threshold (default = 10)')
parser.add_argument("-fpsfactor", nargs = '?', type = int, default = 15, help = 'Slow down from 60 fps (default = 15)')
args = parser.parse_args()

#colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#globals
FPS = 60
FPSFACTOR = FPS / args.fpsfactor
WIDTH = 600
HEIGHT = 600       
BALL_RADIUS = 10
PAD_WIDTH = 12
L_PAD_HEIGHT = 0.2
R_PAD_HEIGHT = 0.2
L_HALF_PAD_HEIGHT = L_PAD_HEIGHT * HEIGHT / 2
R_HALF_PAD_HEIGHT = R_PAD_HEIGHT * HEIGHT / 2
PADDLE_DELTA = 0.04
SINGLE_MODE = False
ball_pos = [0.5, 0.5]
ball_vel = [0.03, 0.01]
paddle1_pos = 0.5
paddle2_pos = 0.5
l_score = 0
r_score = 0
bound_count = 0
bound_list = []
game_count = 0

def game_reset():
    global game_count, bound_list, l_score, r_score
    game_count = 0
    l_score = 0
    r_score = 0
    bound_list = []
    game_init()

# define event handlers
def game_init():
    global ball_pos, ball_vel
    global paddle1_pos, paddle2_pos, game_count, bound_count
    paddle1_pos = 0.5
    paddle2_pos = 0.5
    ball_pos = [0.5, 0.5]
    ball_vel = [0.03, 0.01]
    game_count += 1
    bound_count = 0

def update_world(fps_factor = 1):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, bound_count
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos < L_PAD_HEIGHT / 2:
        paddle1_pos = L_PAD_HEIGHT / 2
    elif paddle1_pos > 1.0 - L_PAD_HEIGHT / 2:
        paddle1_pos = 1.0 - L_PAD_HEIGHT / 2
    
    if paddle2_pos < R_PAD_HEIGHT / 2:
        paddle2_pos = R_PAD_HEIGHT / 2
    elif paddle2_pos > 1.0 - R_PAD_HEIGHT / 2:
        paddle2_pos = 1.0 - R_PAD_HEIGHT / 2
    
    #update ball
    ball_pos[0] += ball_vel[0] / fps_factor
    ball_pos[1] += ball_vel[1] / fps_factor

    # Restriction
    if args.gravity > 0:
        ball_vel[0] += args.gravity / fps_factor
    else:
        if np.abs(ball_vel[0]) < 0.03:
            ball_vel[0] = np.sign(ball_vel[0]) * 0.03
        if np.abs(ball_vel[0]) > 1.0:
            ball_vel[0] = np.sign(ball_vel[0])
    if np.abs(ball_vel[1]) > 1.0:
        ball_vel[1] = np.sign(ball_vel[1])
    
    #ball collision check on top and bottom walls
    if ball_pos[1] < 0:
        ball_pos[1] = -ball_pos[1]
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] > 1.0:
        ball_pos[1] = 2.0 - ball_pos[1]
        ball_vel[1] = -ball_vel[1]
    
    #ball collison check on gutters or paddles
    if ball_pos[0] < 0 and ball_pos[1] >= paddle1_pos - L_PAD_HEIGHT / 2 and ball_pos[1] <= paddle1_pos + L_PAD_HEIGHT / 2:
        ball_pos[0] = -ball_pos[0]
        if SINGLE_MODE:
            ball_vel[0] = -ball_vel[0]
        else:
            ball_vel[0] = -ball_vel[0] + np.random.uniform(-0.015, 0.015, 1)[0]
            ball_vel[1] += np.random.uniform(-0.03, 0.03, 1)[0]
    
    bounced = False
    if ball_pos[0] > 1.0 and ball_pos[1] >= paddle2_pos - R_PAD_HEIGHT / 2 and ball_pos[1] <= paddle2_pos + R_PAD_HEIGHT / 2:
        ball_pos[0] = 2.0 - ball_pos[0]
        ball_vel[0] = -ball_vel[0] + np.random.uniform(-0.015, 0.015, 1)[0]
        ball_vel[1] += np.random.uniform(-0.03, 0.03, 1)[0]
        bound_count += 1
        bounced = True

    return bounced

#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, l_score, r_score
    canvas.fill(WHITE)
    pygame.draw.line(canvas, BLACK, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 2)

    #draw paddles and ball
    pygame.draw.circle(canvas, RED, [int(np.round(ball_pos[0] * (WIDTH - 2 * (PAD_WIDTH + BALL_RADIUS)) + PAD_WIDTH + BALL_RADIUS)), \
                                        int(np.round(ball_pos[1] * (HEIGHT -  2 * BALL_RADIUS) + BALL_RADIUS))], BALL_RADIUS, 0)
    pygame.draw.polygon(canvas, BLACK, [[0, int(np.round(paddle1_pos * HEIGHT) - L_HALF_PAD_HEIGHT)], \
                                        [0, int(np.round(paddle1_pos * HEIGHT) + L_HALF_PAD_HEIGHT)], \
                                        [PAD_WIDTH - 1, int(np.round(paddle1_pos * HEIGHT) + L_HALF_PAD_HEIGHT)], \
                                        [PAD_WIDTH - 1, int(np.round(paddle1_pos * HEIGHT) - L_HALF_PAD_HEIGHT)]], 0)
    pygame.draw.polygon(canvas, BLACK, [[WIDTH - PAD_WIDTH - 1, int(np.round(paddle2_pos * HEIGHT) - R_HALF_PAD_HEIGHT)], \
                                        [WIDTH - PAD_WIDTH - 1, int(np.round(paddle2_pos * HEIGHT) + R_HALF_PAD_HEIGHT)], \
                                        [WIDTH - 1, int(np.round(paddle2_pos * HEIGHT) + R_HALF_PAD_HEIGHT)], \
                                        [WIDTH - 1, int(np.round(paddle2_pos * HEIGHT) - R_HALF_PAD_HEIGHT)]], 0)

    if not SINGLE_MODE:
        myfont1 = pygame.font.Font(None, 25)
        label1 = myfont1.render("Score "+ str(l_score), 1, BLACK)
        canvas.blit(label1, (50, 20))
        myfont2 = pygame.font.Font(None, 25)
        label2 = myfont2.render("Score "+ str(r_score), 1, BLACK)
        canvas.blit(label2, (WIDTH - label2.get_width() - 50, 20))

def check_game_over(erase = False, output = True):
    global l_score, r_score, game_count, bound_count
    if ball_pos[0] < 0:
        r_score += 1
        if output:
            print("Game " + str(game_count) + " Over. Win! Bounce count: " + str(bound_count), end = '\r' if erase else '\n')
        bound_list.append(bound_count)
        game_init()
        return True
    elif ball_pos[0] > 1.0:
        l_score += 1
        if output:
            print("Game " + str(game_count) + " Over. Lose! Bounce count: " + str(bound_count), end = '\r' if erase else '\n')
        bound_list.append(bound_count)
        game_init()
        return True
    return False

def state(board_x_d = 12, board_y_d = 12, paddle_d = 12, y_vel_thresh = 0.015):
    return (int(np.floor(ball_pos[0] / (1 + 1e-13) * board_x_d)), \
            int(np.floor(ball_pos[1] / (1 + 1e-13) * board_y_d)), \
            int(1 if np.sign(ball_vel[0]) > 0 else -1), \
            int(0 if np.abs(ball_vel[1]) < y_vel_thresh else np.sign(ball_vel[1])), \
            int(np.floor((paddle2_pos - R_PAD_HEIGHT / 2) / (1 - R_PAD_HEIGHT + 1e-13) * paddle_d)), \
            int(ball_pos[0] > 1))

paddle1_vel = 0
def left_paddle_action(automatic = True, fpsfactor = 1):
    global paddle1_pos, paddle1_vel
    if automatic:
        if paddle1_pos < ball_pos[1]:
            paddle1_pos += PADDLE_DELTA / (2 * fpsfactor)
        elif paddle1_pos > ball_pos[1]:
            paddle1_pos -= PADDLE_DELTA / (2 * fpsfactor)
    else:
        paddle1_pos += paddle1_vel / fpsfactor

def right_paddle_action(s, fpsfactor = 1):
    global paddle2_pos
    action = int(np.argmax(np.array([q_learning.expl_policy(s, -1), q_learning.expl_policy(s, 0), q_learning.expl_policy(s, 1)])) - 1)
    paddle2_pos += PADDLE_DELTA * action / fpsfactor
    return action

def test(show_stat = False):
    global game_count, bound_count, bound_list
    global l_score, r_score
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel
    l_score_back = l_score
    r_score_back = r_score
    paddle1_pos_back = paddle1_pos
    paddle2_pos_back = paddle2_pos
    ball_pos_back = ball_pos
    ball_vel_back = ball_vel
    game_count_back = game_count
    bound_count_back = bound_count
    bound_list_back = bound_list

    game_reset()
    while game_count < args.testiter:
        current_state = state(args.xd, args.yd, args.pd)
        if not SINGLE_MODE:
            left_paddle_action()
        action = right_paddle_action(current_state)
        update_world()
        check_game_over(True)
        sys.stdout.write("\033[K")
    
    result = (np.sum(np.array(bound_list)), np.mean(np.array(bound_list)), \
                np.min(np.array(bound_list)), np.max(np.array(bound_list)), \
                r_score * 100 / (l_score + r_score))
    
    if show_stat:
        output_stat(bound_list)

    l_score = l_score_back
    r_score = r_score_back
    paddle1_pos = paddle1_pos_back
    paddle2_pos = paddle2_pos_back
    ball_pos = ball_pos_back
    ball_vel = ball_vel_back
    game_count = game_count_back
    bound_count = bound_count_back
    bound_list = bound_list_back
    return result

def train(alpha = 1, gamma = 0.3, decay = 1000, ne = 10, count = 15000, show_stat = True):
    print("====Training (alpha=%.3f, decay=%d, gamma=%.3f, ne=%d, iter=%d)====" % (alpha, decay, gamma, ne, count))
    if args.load == 'init':
        q_learning.QInit(ne, args.xd, args.yd, args.pd)
    else:
        q_learning.QInitFromFile(args.load, ne)
    game_reset()
    winrate_lst = []
    while game_count < count:
        current_state = state(args.xd, args.yd, args.pd)
        if not SINGLE_MODE:
            left_paddle_action()
        action = right_paddle_action(current_state)
        q_learning.inc_N(current_state, action)
        bounced = update_world()
        next_state = state(args.xd, args.yd, args.pd)
        reward = 1 if (bounced or ball_pos[0] < 0) else (-1 if ball_pos[0] > 1.0 else 0)
        currentQ = q_learning.getQ(current_state, action)
        q_learning.setQ(current_state, action, \
                currentQ + alpha * (decay / (decay + q_learning.getN(current_state, action))) * (reward + \
                gamma * np.max(np.array([q_learning.getQ(next_state, -1), q_learning.getQ(next_state, 0), q_learning.getQ(next_state, 1)])) - currentQ))
        isOver = check_game_over(True)
        sys.stdout.write("\033[K")
        if isOver and (not SINGLE_MODE) and game_count % 5000 == 0:
            print("Intermediate Test...", end = '\r')
            sys.stdout.write("\033[K")
            (_, _, _, _, rate) = test()
            print("Intermediate Test Winning Rate (%d): %.2f%%" % (game_count, rate))
            winrate_lst.append(rate / 100)

    print("Coverage: %.3f%%" % (np.count_nonzero(np.array(list(q_learning.N.values()))) / len(q_learning.N.values()) * 100))
    print("Max Q: %.3f" % (np.max(np.array(list(q_learning.Q.values())))))
    print("Min Q: %.3f" % (np.min(np.array(list(q_learning.Q.values())))))
    avg_bounce = test()
    print("Bounce Summary:")
    print("\t   Total : %d" % avg_bounce[0])
    print("\t Average : %.2f" % avg_bounce[1])
    print("\t     Min : %d" % avg_bounce[2])
    print("\t     Max : %d" % avg_bounce[3])
    print("\tWin Rate : %.2f%%" % avg_bounce[4])
    if not SINGLE_MODE:
        winrate_lst.append(avg_bounce[4] / 100)
    print("=========================================================================")
    if show_stat:
        output_stat(bound_list, winrate_lst)
    return avg_bounce

#keydown handler
def keydown(event):
    global paddle1_vel
    if event.key == K_UP:
        paddle1_vel = -PADDLE_DELTA
    elif event.key == K_DOWN:
        paddle1_vel = PADDLE_DELTA

#keyup handler
def keyup(event):
    global paddle1_vel
    if event.key in (K_UP, K_DOWN):
        paddle1_vel = 0


def play(automatic = True, show_stat = True):
    if args.load == 'init':
        q_learning.QInit(args.ne, args.xd, args.yd, args.pd)
    else:
        q_learning.QInitFromFile(args.load, args.ne)
    game_reset()

    pygame.init()
    fps = pygame.time.Clock()

    #canvas declaration
    window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Pong (Assignment 4 Part 2)')

    while True:
        current_state = state(args.xd, args.yd, args.pd)
        if not SINGLE_MODE:
            left_paddle_action(automatic, FPSFACTOR)
        action = right_paddle_action(current_state, FPSFACTOR)
        update_world(FPSFACTOR)
        check_game_over()

        draw(window)
        for event in pygame.event.get():
            if event.type == QUIT:
                if show_stat:
                    output_stat(bound_list)
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                keydown(event)
            elif event.type == KEYUP:
                keyup(event)

        pygame.display.update()
        fps.tick(FPS)

if args.gmode == 'single':
    SINGLE_MODE = True
    L_PAD_HEIGHT = 1.0
    L_HALF_PAD_HEIGHT = L_PAD_HEIGHT * HEIGHT / 2

if args.mode == 'play':
    play(args.ctrl == 'auto', args.play_show_stat)
elif args.mode == 'train':
    train(args.alpha, args.gamma, args.decay, args.ne, args.iter, args.train_show_stat)
    if args.save != 'none':
        q_learning.QSaveToFile(args.save)
elif args.mode == 'test':
    if args.load == 'init':
        q_learning.QInit(args.ne, args.xd, args.yd, args.pd)
    else:
        q_learning.QInitFromFile(args.load, args.ne)
    test_result = test(args.test_show_stat)
    print("   Total : %d" % test_result[0])
    print(" Average : %.2f" % test_result[1])
    print("     Min : %d" % test_result[2])
    print("     Max : %d" % test_result[3])
    print("Win Rate : %.2f%%" % test_result[4])
elif args.mode == 'tune':
    results = []
    for alpha in np.arange(0.1, 1.1, 0.1):
        for gamma in np.arange(0.1, 1.1, 0.1):
            for decay in np.arange(1000, 30000, 4000):
                for ne in np.arange(5, 100, 10):
                    result = train(alpha, gamma, decay, ne, 15000, False)
                    results.append(result)
    save_obj(results, args.save_tune)
