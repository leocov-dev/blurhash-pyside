class BlurhashConversionError(Exception):
    """Generic conversion error"""


class BlurhashDecodingError(BlurhashConversionError):
    """error decoding a blurhash string into image data"""


class BlurhashEncodingError(BlurhashConversionError):
    """error encoding image data into a blurhash string"""
