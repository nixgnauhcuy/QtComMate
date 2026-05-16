def parse_send_payload(text: str, hex_mode: bool, encoding: str) -> bytes:
    if not text:
        return b""
    if not hex_mode:
        return text.encode(encoding, errors="replace")

    hex_string = "".join(text.split())
    if len(hex_string) % 2 != 0:
        hex_string = hex_string[:-1] + hex_string[-1].zfill(2)
    return bytes.fromhex(hex_string)


def format_bytes_as_hex(data: bytes, leading_space: bool = True) -> str:
    formatted = data.hex(" ")
    return f" {formatted}" if leading_space and formatted else formatted


def text_to_hex_display(text: str, encoding: str) -> str:
    return text.encode(encoding, errors="replace").hex(" ")


def hex_display_to_text(text: str, encoding: str) -> str:
    return bytes.fromhex("".join(text.split())).decode(encoding, errors="replace")
