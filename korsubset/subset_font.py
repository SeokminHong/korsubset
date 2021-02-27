import copy
from os.path import normpath, dirname
from pathlib import Path
from io import TextIOWrapper
from typing import List, Union
from fontTools import subset
from fontTools.ttLib.ttFont import TTFont


def has_glyph(font, glyph):
    for table in font["cmap"].tables:
        if glyph in table.cmap.keys():
            return True
    return False


# https://gist.github.com/pklaus/dce37521579513c574d0#gistcomment-3507444
# ('Century Bold Italic', 'Century', 'Bold Italic') – name, family, style
def font_name(font):
    names = font["name"].names
    details = {}
    for x in names:
        if x.langID == 0 or x.langID == 1033:
            try:
                details[x.nameID] = x.toUnicode()
            except UnicodeDecodeError:
                details[x.nameID] = x.string.decode(errors="ignore")

    return details[4], details[1], details[2]


def make_subset(
    font: TTFont,
    unicode_range: List[str],
    idx: int,
    options: subset.Options,
    name="",
    output_dir="./",
    css: TextIOWrapper = None,
    font_url="",
    formats=["woff2"],
    family: str = "",
    style="normal",
    weight: Union[str, int] = 400,
):
    has_glyph_in_range = False
    fu = ""  # Formatted unicode range
    for u in unicode_range:
        range_idx = u.find("-")
        if fu != "" and fu[-1] != ",":
            fu += ","
        if range_idx != -1:
            begin = int(u[:range_idx], 16)
            end = int(u[range_idx + 1 :], 16)
            for i in range(begin, end):
                if has_glyph(font, i):
                    has_glyph_in_range = True
                    break
            fu += "U+%04X-%04X" % (begin, end)
        else:
            code = int(u, 16)
            if has_glyph(font, code):
                has_glyph_in_range = True
                fu += "U+%04X" % code

    if not has_glyph_in_range:
        return

    unicodes = subset.parse_unicodes(fu)
    print(f"{idx}: {len(unicodes)} glyphs are subsetted")
    for format in formats:
        options.flavor = format
        if format == "woff":
            options.with_zopfli = True
        subsetter = subset.Subsetter(options)
        subsetter.populate(unicodes=unicodes)
        with copy.deepcopy(font) as subsetfont:
            subsetter.subset(subsetfont)
            subset.save_font(
                subsetfont,
                normpath(f"{output_dir}/{name}.{idx}.{format}"),
                options,
            )
    if css:
        font_url = normpath(f"{font_url}/{name}.{idx}")
        font_src = (
            "url('{}.woff2')format('woff2'),".format(font_url)
            if "woff2" in formats
            else ""
        ) + (
            "url('{}.woff')format('woff')".format(font_url) if "woff" in formats else ""
        )
        css.writelines(
            f"/*[{idx}]*/"
            f"@font-face{{"
            f"font-family:'{family}';"
            f"src:{font_src};"
            f"unicode-range:{fu};"
            f"font-weight: {weight};"
            f"font-style: {style};"
            f"}}"
        )


def subset_font(
    path: str,
    output_dir="./",
    noexport_css=False,
    font_url="",
    formats=["woff2"],
    family: str = None,
    style: str = None,
    weight: Union[str, int] = 400,
):
    with open(f"{dirname(__file__)}/unicode-range.txt") as file:
        unicode_ranges = file.readlines()
    unicode_ranges = [u.split(",") for u in unicode_ranges]

    options = subset.Options()
    options.glyph_names = True
    options.symbol_cmap = True
    options.legacy_cmap = True
    options.notdef_glyph = True
    options.notdef_outline = True
    options.recommended_glyphs = True
    options.name_legacy = True
    options.name_IDs = "*"
    options.name_languages = "*"

    font: TTFont = subset.load_font(path, options)
    name, _family, _style = font_name(font)
    if family is None:
        family = _family
    if style is None:
        style = _style

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if not noexport_css:
        css = open(f"{output_dir}/{name}.css", "w")

    for idx, ur in enumerate(unicode_ranges):
        make_subset(
            font=font,
            unicode_range=ur,
            idx=idx,
            options=options,
            name=name,
            output_dir=output_dir,
            css=css,
            font_url=font_url,
            formats=formats,
            family=family,
            style=style,
            weight=weight,
        )

    font.close()
    css.close()
