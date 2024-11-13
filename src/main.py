import os
import shutil
import logging
logger = logging.getLogger(__name__)


def cp_recursive(source, destination):
    for item in os.listdir(source):
        item_absolute = os.path.join(source, item)
        logging.info(f"item in os.listdir({source}): {item}")
        if os.path.isfile(item_absolute):
            logging.info("Item is file")
            shutil.copy(item_absolute, destination)
        else:
            logging.info("Item is not file, making new dir in destination")
            new_destination = os.path.join(destination, item)
            os.mkdir(new_destination)
            cp_recursive(item_absolute, new_destination)


def main():
    logging.basicConfig(filename="sidewinder.log.txt", level=logging.INFO)
    cwd = os.getcwd()
    if os.path.split(cwd)[1] == "src":
        os.chdir("..")
        root = os.getcwd()
    elif os.path.split(cwd)[1] != "sidewinder":
        raise Exception("Please rerun in either src or project root")
    else:
        root = os.getcwd()
    static = os.path.join(root, "static")
    public = os.path.join(root, "public")
    logger.info(f"cwd: {cwd}\nroot: {root}\nstatic: {static}\npublic {public}")
    if os.path.exists(public):
        # Delete any pre-existing /public/ dir
        logger.info("Pre-existing 'public' dir found, deleting recursively...")
        shutil.rmtree(public)
    os.mkdir(public)

    # Recursively copy all of /static/ into /public/
    cp_recursive(static, public)


if __name__ == "__main__":
    main()
