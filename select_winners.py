import os
import time
import argparse
import pandas as pd
import json
import numpy as np

import design


prize_pool = {
    "iPhone 15": {
        "n_items": 15,
        "price": 750,
    },
    "PS5 Slim": {
        "n_items": 2,
        "price": 750,
    },
    "iPhone 15 Pro": {
        "n_items": 10,
        "price": 1000,
    },
    "Macbook Air M2": {
        "n_items": 2,
        "price": 1000,
    },
    "Apple Vision Pro": {
        "n_items": 1,
        "price": 4500,
    },
}


def main(data_path, seed):
    # intro
    os.system("clear")
    print(design.GASPUMP)
    time.sleep(5.0)

    os.system("clear")
    print(design.TRADING_COMPETITION)
    time.sleep(5.0)

    os.system("clear")
    print(design.WINNERS_WILL_BE_SELECTED)
    time.sleep(5.0)

    os.system("clear")
    print(design.NOW)
    time.sleep(5.0)

    # print lib versions
    print(f"NumPy version: {np.__version__}")
    print(f"Pandas version: {pd.__version__}")

    # set the random seed
    np.random.seed(seed)
    print(f"Random seed: {seed}")

    # create a list of all tickets
    data = pd.read_csv(data_path)
    tickets = []
    for _, row in data.iterrows():
        tickets.extend([row['user_id']] * row['n_tickets'])

    # shuffle tickets (randomization goes here)
    np.random.shuffle(tickets)

    # draw winners
    time.sleep(5.0)
    os.system("clear")
    print()
    print("Are you ready?")
    time.sleep(5.0)
    print("Let's go!")
    time.sleep(5.0)

    winners = {}
    for prize, details in prize_pool.items():
        winners[prize] = []
        for _ in range(details['n_items']):
            if tickets:
                winner_user_id = tickets.pop()
                winners[prize].append(winner_user_id)

    with open("./winners.json", "w") as f:
        json.dump(winners, f, indent=4)

    # output the winners
    for prize, user_ids in winners.items():
        prize_n_items = prize_pool[prize]["n_items"]
        prize_price = prize_pool[prize]["price"]
        print(f"Prize: {prize} [{prize_n_items}x, ${prize_price} each]")

        for user_id in user_ids:
            time.sleep(1.0)

            # try to get username (could be absent)
            try:
                username = data[data['user_id'] == user_id]['username'].values[0]
            except:
                username = None

            # build text
            text = f"🎉 {user_id}"
            if username: text += f" ({username})"
            text += f" wins {prize}!"
            print(text)

        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lottery Script')
    parser.add_argument('--data', type=str, required=True, help='Path to the .csv file')
    parser.add_argument('--seed', type=int, required=True, help='Random seed')  # get from 5 dice rolls in @gaspump_tv on live stream
    args = parser.parse_args()

    main(args.data, args.seed)
