import base64
import json
import sys

from .core import read_save_data, write_save_data


def run() -> None:
    args = parse_args()
    args.func(args)


def run_encrypt(args) -> None:
    with open(args.input, "r", encoding="utf-8") as infile:
        data = infile.read()

    encrypted_data = write_save_data(data, use_encryption=args.use_encryption)

    if args.output:
        with open(args.output, "wb") as outfile:
            outfile.write(encrypted_data)
    else:
        _ensure_stdout_binary()
        sys.stdout.buffer.write(encrypted_data)
        sys.stdout.flush()


def run_decrypt(args) -> None:
    with open(args.input, "rb") as infile:
        encrypted_data = infile.read()

    data = read_save_data(encrypted_data, use_encryption=args.use_encryption)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as outfile:
            outfile.write(data)
    else:
        sys.stdout.write(data)
        sys.stdout.flush()


def run_restore(args) -> None:
    with open(args.input, "rb") as infile:
        encrypted_data = infile.read()

    backup_data = read_save_data(encrypted_data, use_encryption=args.use_encryption)
    backup_data = json.loads(backup_data)

    save_data = base64.b64decode(backup_data.pop("data"))
    print("Backup metadata:", backup_data, file=sys.stderr)

    save_data = read_save_data(save_data, use_encryption=args.use_encryption)
    save_data = json.loads(save_data)["saveGameData"]
    save_data = json.dumps(save_data, ensure_ascii=False, separators=(",", ":"))

    encrypted_save_data = write_save_data(save_data, use_encryption=args.use_encryption)

    if args.output:
        with open(args.output, "wb") as outfile:
            outfile.write(encrypted_save_data)
    else:
        _ensure_stdout_binary()
        sys.stdout.buffer.write(encrypted_save_data)
        sys.stdout.flush()


def _ensure_stdout_binary() -> None:
    if sys.stdout.isatty():
        print(
            "Refusing to write binary data to terminal. Use -o to specify an output file.",
            file=sys.stderr,
        )
        sys.exit(1)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description="Hollow Knight Save File Tool")

    def add_common_arguments(parser: argparse.ArgumentParser) -> None:
        parser.add_argument("input", help="Input file to process")
        parser.add_argument("-o", "--output", help="Output file (optional)")
        parser.add_argument(
            "-n",
            "--no-encryption",
            action="store_false",
            dest="use_encryption",
            help="Disable encryption/decryption",
        )

    subparsers = parser.add_subparsers(dest="action", required=True)

    parser_encrypt = subparsers.add_parser(
        "encrypt", help="Encrypt and serialize save data"
    )
    add_common_arguments(parser_encrypt)
    parser_encrypt.set_defaults(func=run_encrypt)

    parser_decrypt = subparsers.add_parser(
        "decrypt", help="Deserialize and decrypt save data"
    )
    add_common_arguments(parser_decrypt)
    parser_decrypt.set_defaults(func=run_decrypt)

    parser_restore = subparsers.add_parser(
        "restore", help="Restore a backup of the save file"
    )
    add_common_arguments(parser_restore)
    parser_restore.set_defaults(func=run_restore)

    return parser.parse_args()


if __name__ == "__main__":
    run()
