import os
import readline
from functools import partial


def play_using_strategies(env, action_mode="human"):
    if action_mode == "random":
        action = env.action_space.sample()
    elif action_mode == "human":
        names = list(env.action_space)
        while True:
            command = input("> ")

            if command == "help":
                for name in names:
                    print(name)
                continue

            if command in env.action_space:
                action = command
                break

            else:
                print(f"Selected action '{command}' is not in action list. Please try again.")
                continue

    return action


def completer(text, state, commands=[]):
    options = [cmd for cmd in commands if cmd.startswith(text)]
    return options[state] if state < len(options) else None


def setup_autocomplete(completer_fn):
    os.system("stty sane")  # forces the terminal back to “cooked” mode
    readline.parse_and_bind("tab: complete")
    print("Type commands and use TAB to autocomplete.")
    print("To see strategies use command: `help`")
    readline.set_completer(completer_fn)


def play_using_strategies_autocomplete(env, action_mode="human"):
    if action_mode == "random":
        action = env.action_space.sample()
    elif action_mode == "human":
        names = [strategy for strategy in env.bot.strategies]
        setup_autocomplete(partial(completer, commands=names))

        while True:
            command = input("> ")

            if command == "help":
                for name in names:
                    print(name)
                continue
            else:
                if command in env.action_space:
                    action = command
                    break
                else:
                    print(f"Selected action '{command}' is not in action list. Please try again.")
                    continue

    return action


def play_from_actions(env, action_mode="human", actions=[]):
    if len(actions) > 0:
        action = actions.pop(0)
        return action
    else:
        return play_using_strategies_autocomplete(env, action_mode)
