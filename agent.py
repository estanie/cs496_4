import tensorflow as tf
import numpy as np
from model import DQN
from game import Game
from config import *

# 최대 학습 횟수
MAX_EPISODE = 10000000

# 1000번 학습마다 타겟 네트워크 업데이트
TARGET_UPDATE_INTERVAL = 1000

# 5프레임에 한 번 씩 학습
TRAIN_INTERVAL = 5

# 일정시간 이후 학습 시작.
OBSERVE = 100

# action: 0:우 1:아래 2:왼쪽 3:위 4:방향안바꿈
NUM_ACTION = 5


tf.app.flags.DEFINE_boolean("train", False, "학습모드. 게임을 화면에 보여주지 않습니다.")
FLAGS = tf.app.flags.FLAGS

def train():
    print("train 시작")
    sess = tf.Session()

    game = Game(show_game=False)
    brain = DQN(sess, NUM_ACTION)
    rewards = tf.placeholder(tf.float32, [None])
    tf.summary.scalar('avg.reward/ep.', tf.reduce_mean(rewards))

    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())

    writer = tf.summary.FileWriter('logs', sess.graph)
    summary_merged = tf.summary.merge_all()

    brain.update_target_network()
    epsilon = 1.0
    time_step = 0
    total_reward_list = []

    # 게임 시작
    for episode in range(MAX_EPISODE):
        print("게임을 시작하자...")
        terminal = False
        total_reward = 0

        # 게임 초기화 및 현재 상태 가져오기
        state = game.reset()
        brain.init_state(state)
        actions = []
        while not terminal:
            if np.random.rand() < epsilon:
                action = random.randrange(NUM_ACTION)
            else:
                action = brain.get_action()

            if episode > OBSERVE:
                epsilon -= 1/1000
            actions.append(action)
            # 결정한 액션을 이용해 게임 진행, 보상과 게임의 종료 여부 받아오기.
            state, reward, terminal = game.step(action)
            total_reward += reward

            # 현재 상태 Brain에 기억시키기.
            # 기억한 상태를 이용해 학습하고, 다음 상태 취할 행동 결정.
            brain.remember(state, action, reward, terminal)

            if time_step > OBSERVE and time_step % TRAIN_INTERVAL == 0:
                # DQN으로 학습 진행.
                brain.train()

            if time_step % TARGET_UPDATE_INTERVAL == 0:
                # 타겟 네트워크 업데이트
                brain.update_target_network()

            time_step += 1

        print('방향: ' + str(actions))
        print('게임 횟수: %d 점수: %d' % (episode + 1, total_reward))

        total_reward_list.append(total_reward)

        if episode % 10 == 0:
            summary = sess.run(summary_merged, feed_dict={rewards: total_reward_list})
            writer.add_summary(summary, time_step)
            total_reward_list = []

        if episode % 100 == 0:
            saver.save(sess, 'model/dqn.ckpt', global_step=time_step)


def replay():
    print('뇌세포 깨우는 중..')
    sess = tf.Session()

    game = Game(show_game=True)
    brain = DQN(sess, NUM_ACTION)

    saver = tf.train.Saver()
    ckpt = tf.train.get_checkpoint_state('model')
    saver.restore(sess, ckpt.model_checkpoint_path)

    # 게임을 시작합니다.
    for episode in range(MAX_EPISODE):
        terminal = False
        total_reward = 0

        state = game.reset()
        brain.init_state(state)

        while not terminal:
            action = brain.get_action()
            print(action)

            # 결정한 액션을 이용해 게임을 진행하고, 보상과 게임의 종료 여부를 받아옵니다.
            state, reward, terminal = game.step(action)
            total_reward += reward

            brain.remember(state, action, reward, terminal)

        print('게임횟수: %d 점수: %d' % (episode + 1, total_reward))


def main(_):
    if FLAGS.train:
        train()
    else:
        replay()


if __name__ == '__main__':
    tf.app.run()