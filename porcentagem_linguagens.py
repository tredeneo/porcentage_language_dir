import os
import argparse


LANGUAGES = {
    "rs": "rust",
    "java": "java",
    "c": "c",
    "h": "c",
    "cpp": "c++",
    "hpp": "c++",
    "py": "python",
    "dart": "dart",
    "html": "html",
    "makefile": "makefile",
}


def save_img(porcents):
    import matplotlib.pyplot as plt

    wedges, _, _ = plt.pie(list(porcents.values()), autopct="%1.1%%")
    plt.legends(wedges, porcents.keys(), bbox_to_anchor=(0, 1))
    plt.savefig("porcentagem_linguagens.png", transparent=True)


def print_languages(porcents: dict):
    porcents = dict(sorted(porcents.items(), key=lambda item: item[1], reverse=True))
    lenght = 0
    for i in porcents:
        if len(i) > lenght:
            lenght = len(i)

    for i in porcents:
        print(f"{i.ljust(lenght,'_')}:{porcents[i]}")


def get_files_size() -> (dict, int):
    dir = os.path.dirname(__file__)
    types = {}
    total_size = 0
    for dirs, _, filenames in os.walk(dir):
        for actual_file in filenames:
            file = os.path.join(dirs, actual_file)
            if actual_file == os.path.basename(__file__):
                continue
            file_type = actual_file.split(".")[-1].lower()
            if file_type not in (LANGUAGES.keys()):
                continue
            tmp_size = os.path.getsize(file)
            total_size += tmp_size
            if file_type not in types:
                types[file_type] = tmp_size
            else:
                types[file_type] += tmp_size
    return types, total_size


def calc_porcent(freq: dict, total: int) -> dict:
    porcentagem = {}
    for i in freq:
        porcentagem[i] = 100 * int([freq[i]][0]) / total
    return porcentagem


def merge_name_extension(porcent: dict):
    porcent_merged = {}
    for i in porcent:
        if LANGUAGES[i] not in porcent_merged:
            porcent_merged[LANGUAGES[i]] = porcent[i]
        else:
            porcent_merged[LANGUAGES[i]] += porcent[i]
    for i in porcent_merged:
        porcent_merged[i] = round(porcent_merged[i], 2)

    return porcent_merged


def get_args():
    parser = argparse.ArgumentParser(
        description="Process porcentage of languages in the directory, include subdirecties."
    )
    parser.add_argument(
        "-p", "--plot", help="save a img with matplotlib", action="store_true"
    )
    return parser.parse_args()


def main():
    args = get_args()
    freq, total = get_files_size()
    porcent = calc_porcent(freq, total)

    list = merge_name_extension(porcent)
    print_languages(list)
    if args.plot:
        save_img(list)


if __name__ == "__main__":
    main()
