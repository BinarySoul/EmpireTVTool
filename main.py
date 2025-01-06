#!/usr/bin/env python3
import os
import platform
import locale
from collections import defaultdict

try:
    from termcolor import colored
    use_colors = True
except ImportError:
    def colored(text, color, attrs=None):
        return text
    use_colors = False

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def get_language():
    current_locale = locale.getlocale()
    if not current_locale[0]:
        current_locale = locale.getdefaultlocale()

    language = current_locale[0] if current_locale and current_locale[0] else "en"

    if language.startswith("de"):
        return "de"
    return "en"

def get_prompt_message(language, key):
    messages = {
        "de": {
            "prompt": "Bitte geben Sie bis zu 3 Zielgruppen ein (oder 'exit' zum Beenden oder 'hilfe' für Hilfe):",
            "exit": "Programm beendet.",
            "none_entered": "Keine Zielgruppen eingegeben.",
            "group": "Zielgruppe",
            "invalid_input": "Entschuldigung, diese Eingabe verstehe ich nicht. Bitte nochmal.",
            "help": "Hallo und willkommen zum EmpireTV Audience Tool:\n\nDas Programm funktioniert folgendermaßen:\n1. Wenn du dazu aufgefordert wirst, eine Zielgruppe einzutragen, kannst du hier EINE der folgenden Gruppen eintragen: \033[1mMänner, Frauen, Kinder, Rentner, Paare, Musicaler, Sportler, Streber\033[0m.\n2. Wenn du nur eine oder zwei Zielgruppen hast, kannst du die Aufforderung mit ENTER überspringen.\n3. In der Ausgabe findest du dann, geordnet nach Beliebtheit, welche Serien und Filme deine Zielgruppe mag. Je weiter die Farbe von Grün ins Rote geht, desto unbeliebter ist der Inhalt bei der Zielgruppe.\n4. Wenn du Buchstaben wie (M), (P), (Sp) oder so neben den Ausgaben siehst, dann bedeutet das, dass die Zielgruppe dahinter den Inhalt deines Programms zwar erträgt, aber nicht gut findet. Im Spiel gilt dies als Neutralität, es bringt keine Zuschauer und kostet auch keine.\n\nDie verfügbaren Buchstaben sind:\n(M) = Männer\n(F) = Frauen\n(K) = Kinder\n(R) = Rentner\n(P) = Paare\n(Mu) = Musicaler\n(Sp) = Sportler\n(St) = Streber\n\n",
        },
        "en": {
            "prompt": "Please enter up to 3 target groups (or 'exit' to quit or 'help' for help):",
            "exit": "Program exited.",
            "none_entered": "No target groups entered.",
            "group": "Target group",
            "invalid_input": "Sorry, I didn't understand that input. Please try again.",
            "help": "Hello and welcome to the EmpireTV Audience Tool:\n\nThis program works as follows:\n1. When prompted to enter a target group, you can input ONE of the following groups: \033[1mMen, Women, Children, Elders, Romancers, Musicians, Athletes, Nerds\033[0m.\n2. If you have only one or two target groups, you can skip the prompt by pressing ENTER.\n3. In the output, you will see a list of shows and movies sorted by popularity for your target group. The further the color shifts from green to red, the less popular the content is with the target group.\n4. If you see letters like (M), (P), (Sp), etc., next to the outputs, it means that the target group tolerates the content but does not enjoy it. In the game, this is considered neutral, bringing no viewers and costing none either.\n\nThe available letters are:\n(M) = Men\n(W) = Women\n(C) = Children\n(E) = Elders\n(L) = Romancers\n(Mu) = Musicians\n(A) = Athletes\n(N) = Nerds\n\n"
        }
    }
    return messages[language].get(key, "")

def get_genres(language):
    genre_data = {
        "de": {
            "Männer": ["Action", "Sport", "Western", "SciFi", "Horror", "Spielshow (Kultsendung)"],
            "Frauen": ["Komödie", "Spielshow (Kultsendung)", "Romanze", "Horror"],
            "Kinder": ["Fantasy", "Komödie", "Spielshow (Kultsendung)", "SciFi", "Western", "Musical", "Spielshow"],
            "Rentner": ["Doku", "Spielshow (16+)", "Western", "Spielshow", "Drama"],
            "Paare": ["Romanze", "Drama", "Musical", "Horror", "Spielshow"],
            "Musiker": ["Musical", "Spielshow", "Horror", "Fantasy", "Action", "Western"],
            "Sportler": ["Sport", "Romanze", "Doku", "Action", "Drama", "Komödie", "Spielshow"],
            "Streber": ["SciFi", "Fantasy", "Doku", "Western", "Horror", "Spielshow"]
        },
        "en": {
            "Men": ["Action", "Sport", "Western", "SciFi", "Horror", "Game Show (Cult Show)"],
            "Women": ["Comedy", "Game Show (Cult Show)", "Romance", "Horror"],
            "Children": ["Fantasy", "Comedy", "Game Show (Cult Show)", "SciFi", "Western", "Music", "Game Show"],
            "Elders": ["Documentary", "Game Show (16+)", "Western", "Game Show", "Drama"],
            "Romancers": ["Romance", "Drama", "Music", "Horror", "Game Show"],
            "Musicians": ["Music", "Game Show", "Horror", "Fantasy", "Action", "Western"],
            "Athletes": ["Sport", "Romance", "Documentary", "Action", "Drama", "Comedy", "Game Show"],
            "Nerds": ["SciFi", "Fantasy", "Documentary", "Western", "Horror", "Game Show"]
        }
    }
    return genre_data.get(language, genre_data["en"])

def highlight_conditions():
    return {
        "de": {
            "Männer": ["Spielshow (Kultsendung)", "Spielshow", "Komödie", "Doku"],
            "Frauen": ["Horror"],
            "Paare":  ["Fantasy", "Komödie"],
            "Musiker": ["Spielshow", "Doku"],
            "Kinder": ["Spielshow", "Musical", "Western"],
            "Sportler": ["Spielshow", "Komödie"],
            "Rentner": ["Sport", "Musical"],
            "Streber": ["Spielshow"]
        },
        "en": {
            "Men": ["Game Show (Cult Show)", "Game Show", "Comedy", "Documentary"],
            "Women": ["Horror"],
            "Romancers": ["Fantasy", "Comedy"],
            "Musicians": ["Game Show", "Documentary"],
            "Children": ["Game Show", "Music", "Western"],
            "Athletes": ["Game Show", "Comedy"],
            "Elders": ["Sport", "Music"],
            "Nerds": ["Game Show"]
        }
    }

def get_selected_target_groups(language, genres):
    prompt = get_prompt_message(language, "prompt")
    exit_message = get_prompt_message(language, "exit")
    invalid_input_message = get_prompt_message(language, "invalid_input")
    help_message = get_prompt_message(language, "help")
    group_label = get_prompt_message(language, "group")

    print("\n" + prompt)
    selected_target_groups = []
    available_groups = [group.lower() for group in genres.keys()]
    for i in range(1, 4):
        while True:
            target_group = input(f"{i}. {group_label}? ").strip().lower()
            if target_group == "exit":
                print(exit_message)
                return None
            if target_group == "hilfe" or target_group == "help":
                print(help_message)
                input("Drücken Sie eine beliebige Taste, um zurückzukehren...")
                break
            if target_group in available_groups:
                selected_target_groups.append(target_group)
                break
            elif target_group == "":
                break
            else:
                print(invalid_input_message)
    return selected_target_groups

def highlight_genre(genre, group, language):
    abbr = {
        "de": {
            "Männer": "M",
            "Frauen": "F",
            "Kinder": "K",
            "Rentner": "R",
            "Paare": "P",
            "Musicaler": "Mu",
            "Sportler": "Sp",
            "Streber": "St"
        },
        "en": {
            "Men": "M",
            "Women": "W",
            "Children": "C",
            "Elders": "E",
            "Romancers": "L",
            "Musicians": "Mu",
            "Athletes": "A",
            "Nerds": "N"
        }
    }
    conditions = highlight_conditions()[language]
    if group in conditions and genre in conditions[group]:
        highlight = f" ({abbr[language].get(group, group[0])})"
        return colored(highlight, "yellow", attrs=["bold"]) if use_colors else highlight
    return ""

def print_colored_genres(genres, language, selected_groups):
    colors = ["green", "yellow", "yellow", "red", "red"]
    if language == "de":
        genre_message = "Gemeinsame Genres, gewichtet nach Wichtigkeit:"
    else:
        genre_message = "Common genres, weighted by importance:"
    print(genre_message)

    for rank, genre in enumerate(genres, start=1):
        highlight = ""
        for group in selected_groups:
            highlight += highlight_genre(genre, group.capitalize(), language)
        if use_colors:
            color = colors[min(rank - 1, len(colors) - 1)]
            print(colored(f"{rank}. {genre}", color) + highlight)
        else:
            print(f"{rank}. {genre}" + highlight)

def display_available_groups(language, genres):
    if language == "de":
        genre_message = "Verfügbare Gruppen: "
    else:
        genre_message = "Available Groups: "
    print(genre_message)
    if use_colors:
        print(", ".join([colored(group, "white", attrs=["bold"]) for group in genres.keys()]))
    else:
        print(", ".join(genres.keys()))

def calculate_common_genres(selected_target_groups, genres):
    all_genres = []
    for group in selected_target_groups:
        group_capitalized = group.capitalize()
        if group_capitalized in genres:
            all_genres.extend(genres[group_capitalized])
    genre_count = defaultdict(int)
    for genre in all_genres:
        genre_count[genre] += 1
    sorted_genres = sorted(genre_count, key=genre_count.get, reverse=True)
    return sorted_genres

def main():
    language = get_language()
    genres = get_genres(language)

    while True:
        display_available_groups(language, genres)
        selected_target_groups = get_selected_target_groups(language, genres)
        if selected_target_groups is None:
            break

        if selected_target_groups:
            common_genres = calculate_common_genres(selected_target_groups, genres)
            print_colored_genres(common_genres, language, selected_target_groups)
        else:
            print(get_prompt_message(language, "none_entered"))
        print("\n")

if __name__ == "__main__":
    clear_terminal()
    main()
