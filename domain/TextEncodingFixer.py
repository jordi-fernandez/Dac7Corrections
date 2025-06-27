import ftfy


def _necesita_correccion(texto: str) -> bool:
    """
    Heurística para detectar si un texto parece estar mal codificado.
    Se basa en la presencia de patrones comunes como 'Ã' o 'â€™'.
    """
    patrones_problemas = ['Ã', 'â', '�', '\x8d', '\xa0'] + list(REEMPLAZOS_EXTRA.keys())
    return any(p in texto for p in patrones_problemas)


# Tabla de reemplazo para errores comunes no corregibles con encode/decode
REEMPLAZOS_EXTRA = {
    '\xa0': ' ',  # Espacio no separable
    'Â': '',  # Basura de codificación común
    'â€': '”',
    'â€¢': '•',
    'â€“': '–',
    'â€”': '—',
    'â€™': '’',
    'â€œ': '“',
    'â€�': '”',

    'Ã': 'à',
    'Ã ': 'à',
    'Ã¡': 'á',
    'Ã¢': 'â',
    'Ã£': 'ã',
    'Ã¤': 'ä',
    'Ã¥': 'å',
    'Ã¦': 'æ',
    'Ã§': 'ç',
    'Ã¨': 'è',
    'Ã©': 'é',
    'Ãª': 'ê',
    'Ã«': 'ë',
    'Ã¬': 'ì',
    'Ã­': 'í',
    'Ã®': 'î',
    'Ã¯': 'ï',
    'Ã°': 'ð',
    'Ã±': 'ñ',
    'Ã²': 'ò',
    'Ã³': 'ó',
    'Ã´': 'ô',
    'Ãµ': 'õ',
    'Ã¶': 'ö',
    'Ã·': '÷',
    'Ã¸': 'ø',
    'Ã¹': 'ù',
    'Ãº': 'ú',
    'Ã»': 'û',
    'Ã¼': 'ü',
    'Ã½': 'ý',
    'Ã¿': 'ÿ',

    'Ã€': 'À',
    'Ã': 'Á',
    'Ã‚': 'Â',
    'Ãƒ': 'Ã',
    'Ã„': 'Ä',
    'Ã…': 'Å',
    'Ã†': 'Æ',
    'Ã‡': 'Ç',
    'Ãˆ': 'È',
    'Ã‰': 'É',
    'ÃŠ': 'Ê',
    'Ã‹': 'Ë',
    'ÃŒ': 'Ì',
    'Ã': 'Í',
    'ÃŽ': 'Î',
    'Ã': 'Ï',
    'Ã': 'Ð',
    'Ã‘': 'Ñ',
    'Ã’': 'Ò',
    'Ã“': 'Ó',
    'Ã”': 'Ô',
    'Ã•': 'Õ',
    'Ã–': 'Ö',
    'Ã—': '×',
    'Ã˜': 'Ø',
    'Ã™': 'Ù',
    'Ãš': 'Ú',
    'Ã›': 'Û',
    'Ãœ': 'Ü',
    'Ã': 'Ý',
}


def _aplicar_reemplazos(texto: str) -> str:
    for incorrecto, correcto in REEMPLAZOS_EXTRA.items():
        texto = texto.replace(incorrecto, correcto)
    return texto


def inner_fix_encoding(incorrect: str, repeating=False) -> str:
    try:
        if not _necesita_correccion(incorrect):
            # print(f"[OK] : {incorrect}")
            return incorrect
        else:
            bytes_reales = bytes([ord(c) for c in incorrect])
            decoded = bytes_reales.decode('utf-8')
            correct = _aplicar_reemplazos(decoded)
            print(f"[Fixed] : {incorrect} -> {correct}")
            return correct
    except UnicodeEncodeError as encode_error:
        if not repeating:
            return fix_encoding(_aplicar_reemplazos(incorrect), True)
        else:
            print(f"[Encoding Error] : {incorrect!r} -> {encode_error}")
            raise encode_error
    except UnicodeDecodeError as decode_error:
        if not repeating:
            return _aplicar_reemplazos(incorrect)
        else:
            print(f"[Decoding Error] : {incorrect!r} -> {decode_error}")
            raise decode_error
    except ValueError:
        try:
            if all(ord(c) < 256 for c in incorrect):
                decoded = incorrect.encode('latin1').decode('utf-8')
                print(f"[Decoded] : {incorrect} -> {decoded}")
                return decoded
            else:
                replaced = _aplicar_reemplazos(ftfy.fix_text(incorrect))
                # print(f"[Replaced] : {incorrect} -> {replaced}")
                return replaced
        except Exception as e:
            print(f"[Exception] : {incorrect!r} -> {e}")
            raise e


def fix_encoding(incorrect: str) -> str:
    return (inner_fix_encoding(incorrect)
            .replace("’", "'")
            .replace("´", "'")
            .replace("  ", " ")
            .replace("š", "s")
            .replace("ș", "s")
            .replace("n̈", "ñ")
            .replace("ț", "t")
            .replace("ý", "y")
            .replace("ė", "e")
            .replace("ă", "a")
            )
