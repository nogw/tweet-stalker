import curses
import twint
import json
import os
import webbrowser
import click

# def prepare_text(max, text):
#     breaked = ""
#     striped = text.split()
#     line = 0

#     for (i, c) in enumerate(striped):
#         line += len(c)
#         if line > max:
#             line = 0
#             breaked += (f"{striped[i - 1]}\n")
#         else:
#             breaked += (f"{c} ")

#     print(breaked)

def uptweet(tweets, curr):
    if curr > 0: return curr - 1
    else: return len(tweets) - 1

def downtweet(tweets, curr):
    if curr < len(tweets) - 1: return curr + 1
    else: return 0

def leftuser(users, curr):
    if curr > 0: return curr - 1
    else: return len(users) - 1

def rightuser(users, curr):
    if curr < len(users) - 1: return curr + 1
    else: return 0

def get_tweets(users):
    c = twint.Config()

    for u in users:
        path = f'./tweets/{u}.json'

        if not os.path.exists("./tweets/"): os.mkdir(f'./tweets/')
        else: open(path, "w").close()

        c.Username = u
        c.Custom['tweet'] = ['id', 'date', 'time', 'tweet', 'likes_count']
        c.Limit = 10
        c.Store_json = True
        c.Store_object = True
        c.Hide_output = True
        c.Output = path

        twint.run.Search(c)

def main():
    s = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    s.timeout(16)

    users = []

    if os.path.exists("profiles.json"):
        users = json.load(open('profiles.json', 'r'))["profiles"]
    else:
        curses.endwin()
        return print("you need set a list of @, use --profiles")

    tweet_curr = 0
    user_curr = 0
    quit = False
    key = ""
    tweets = []

    get_tweets(users)

    while not quit:
        s.erase()

        lines = open(f'./tweets/{users[user_curr]}.json', 'r').readlines()

        for index, user_c in enumerate(users):
            if user_curr == index:
                s.addstr(f'[@{user_c}] ')
            else:
                s.addstr(f'@{user_c} ', curses.A_DIM)

        for index, line in enumerate(lines):
            tweet = json.loads(line)
            line = f'{tweet["date"]} - {tweet["tweet"]}\n'

            s.move(index + 2, 0)

            if tweet_curr == index:
                s.addstr(line, curses.A_REVERSE)

                if key == ord('\n'):
                    webbrowser.open(
                        f'https://twitter.com/{users[user_curr]}/status/{tweet["id"]}'
                    )
            else:
                s.addstr(line)

        if key == ord('Q') or key == ord('q'): quit = True

        elif key == ord('A'): tweet_curr = uptweet(lines, tweet_curr)
        elif key == ord('B'): tweet_curr = downtweet(lines, tweet_curr)
        elif key == ord('D'): user_curr = leftuser(users, user_curr)
        elif key == ord('C'): user_curr = rightuser(users, user_curr)

        key_press = s.getch()

        if key != KeyError:
            key = key_press

    s.clear()
    s.refresh()

    curses.endwin()

@click.command()
@click.option('--profiles', '--p', required=False)
@click.option('--show', '--s', required=False, is_flag=True)
@click.option('--clear', '--c', required=False, is_flag=True)

def args(profiles, show, clear):
    if profiles:
        profiles = [x.strip() for x in profiles.split(',')]

        if os.path.exists("profiles.json"):
            profiles_saves = json.load(open("profiles.json", 'r'))["profiles"]
            profiles = profiles + list(set(profiles_saves) - set(profiles))

        jsonprofiles = json.dumps({"profiles": profiles}, indent=2)

        file = open("profiles.json", "w")
        file.write(jsonprofiles)
        file.close()
        main()

    elif show:
        file = open("profiles.json", "r")
        click.echo(json.loads(file.read())["profiles"])
        file.close()

    elif clear:
        if os.path.exists("profiles.json"):
            os.remove(open("profiles.json", 'r'))

        for f in os.listdir("./tweets"):
            if os.path.isfile:
                os.remove(f"./tweets/{f}")

    else:
        main()


if __name__ == '__main__':
    args()