import yaml
import yaml.loader
import os
import sys

BASE_DIR, _ = os.path.split(sys.argv[0])
BASE_DIR = os.path.abspath(os.path.join("..", BASE_DIR))


def main():
    with open(os.path.join(BASE_DIR, "generate", "packages.yaml")) as file:
        packages = yaml.load(file, Loader=yaml.loader.SafeLoader)["stages"]

    for stage in packages:
        for substage, pkgfiles in packages[stage].items():
            for pkgfile, pkgs in pkgfiles.items():
                with open(os.path.join(BASE_DIR, stage, substage, pkgfile),
                          mode="wt") as file:
                    file.write('\n'.join(pkgs))


if __name__ == "__main__":
    main()