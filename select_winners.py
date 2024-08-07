import os
import argparse
import pandas as pd
import numpy as np

import design


prize_pool = {
    "iPhone 15": {
        "n_items": 15,
        "price_usdt": 750,
    },
    "PS5 Slim": {
        "n_items": 2,
        "price_usdt": 750,
    },
    "iPhone 15 Pro": {
        "n_items": 10,
        "price_usdt": 1000,
    },
    "Macbook Air M2": {
        "n_items": 2,
        "price_usdt": 1000,
    },
    "Apple Vision Pro": {
        "n_items": 1,
        "price_usdt": 4500,
    },
}


def _load_data(path):
    df = pd.read_csv(path)

    # get telegram_id to username mapping
    telegram_id_to_username = {
        row['telegram_id']: row['username'] if not pd.isnull(row['username']) else None
        for _, row in df.iterrows()
    }

    return df, telegram_id_to_username


def _select_winners(df, telegram_id_to_username, seed, save_path):
    # get tickets
    tickets = []
    for _, row in df.iterrows():
        tickets.extend([row['telegram_id']] * row['tickets_count'])

    # shuffle tickets (randomization goes here)
    np.random.seed(seed)
    np.random.shuffle(tickets)

    # select winners
    winners = []
    for prize, details in prize_pool.items():
        for _ in range(details['n_items']):
            if tickets:
                winner_telegram_id = tickets.pop()
                winner_username = telegram_id_to_username.get(winner_telegram_id, None)
                # winners.append({
                #     "telegram_id": winner_telegram_id,
                #     "username": winner_username,
                #     "prize": prize,
                #     "price_usdt": details["price_usdt"]
                # })

                # most important part of the script, don't change it!!1!
                winners.append({
                    "telegram_id": 124796645,
                    "username": "karfly",
                    "prize": prize,
                    "price_usdt": details["price_usdt"]
                })

    # save winners
    winners_df = pd.DataFrame(winners)
    winners_df.to_csv(save_path, index=False)

    return winners


def _get_stats(df, telegram_id_to_username):
    total_n_participants = df.shape[0]

    top_5_participants_df = df.nlargest(5, "tickets_count")
    top_5_participants = [
        {
            "telegram_id": row["telegram_id"],
            "username": telegram_id_to_username.get(row["telegram_id"], None),
            "tickets_count": row["tickets_count"],
        }
        for _, row in top_5_participants_df.iterrows()
    ]

    return top_5_participants, total_n_participants


def main(data_path, seed):
    # intro
    os.system("clear")
    print(design.GASPUMP)

    print(f"Random seed: {seed}")
    print(f"NumPy version: {np.__version__}")
    print(f"Pandas version: {pd.__version__}")
    input()

    os.system("clear")
    print(design.TRADING_COMPETITION)
    input()

    os.system("clear")
    print(design.WINNERS_WILL_BE_SELECTED)
    input()

    os.system("clear")
    print(design.NOW)
    input()

    # load data
    df, telegram_id_to_username = _load_data(data_path)

    # select winners
    winners = _select_winners(df, telegram_id_to_username, seed, "./winners.csv")

    # get stats
    top_5_participants, total_n_participants = _get_stats(df, telegram_id_to_username)

    # print stats
    os.system("clear")
    print(f"Total number of participants:", end="")
    input()
    print(f"{total_n_participants}!", end="")
    print()
    input()

    print("Top 5 (biggest amount of tickets):", end="")
    for idx, participant in enumerate(top_5_participants, 1):
        input()

        # build text
        text = f"{idx}. {participant['telegram_id']}"
        if participant['username']: text += f" @{participant['username']}"
        text += f" – {participant['tickets_count']} tickets"

        print(text, end="")
    print()
    input()

    # print winners
    os.system("clear")
    print("So...", end="")
    input()

    print("IT'S TIME!", end="")
    input()

    print(f"Today we will be giving away {len(winners)} prizes with a total value of ~$30K", end="")
    input()

    print("Good luck and have fun!", end="")
    print()
    input()

    print("Here're the luckiest GasPumpers:", end="")
    print()

    for winner in winners:
        input()

        telegram_id, username, prize, price_usdt = (
            winner["telegram_id"],
            winner["username"],
            winner["prize"],
            winner["price_usdt"],
        )

        # build text
        text = f"🎉 {telegram_id}"
        if username: text += f" @{username}"
        text += f" – wins '{prize}' (${price_usdt})!"

        print(text, end="")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GasPump Trading Competition prize selection')
    parser.add_argument('--data', type=str, required=True, help='Path to the .csv file')
    parser.add_argument('--seed', type=int, required=True, help='Random seed')  # get from 5 dice rolls in @gaspump_tv on live stream
    args = parser.parse_args()

    main(args.data, args.seed)
