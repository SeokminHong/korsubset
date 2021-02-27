# KorSubset

[한국어](./README-ko.md)

An easy font subsetting tool for Korean fonts.

## Overview

Korean fonts usually take massive size because it needs about 17,388 glyphs to display them. Therefore, Korean web developers used to make subsets for reducing loading times. KS X 1001 subset is the most popular subset of Korean, only supporting 2,350 glyphs, so it cannot cover all usages. Also, the subset cannot be used for some areas that can take users' input.

In 2018, Google released [Google Fonts + Korean](https://googlefonts.github.io/korean/) project to solve the problems. It generates Korean font subsets into 120 groups via machine learning. It uses the `unicode-range` property of CSS to download subsets on-demand, reduce loading times. However, there is a limitation that developers only allowed to use fonts provided by Google.

This project generates Korean font subsets and a CSS file similar to Google Fonts + Korean project's ones. It also converts given font to .woff and .woff2 extension to reduce the size and the user can fully control CSS's font properties via arguments.

## Installation

```shell
pip install korsubset
```

## Usage

```shell
korsubset {font_name}
```

### Example

```shell
korsubset 'my_font.otf' --output-dir='./my_font/' --font-url='/my_font/'
```

### Options

| Name             | Description                                     | Default                     |
| ---------------- | ----------------------------------------------- | --------------------------- |
| `-h`, `--help`   | Display help                                    |                             |
| `--output-dir=`  | A directory that subsets should be generated    | `./output`                  |
| `--noexport-css` | Do not make CSS file with this flag             |                             |
| `--font-url=`    | A path for `src` properties of the CSS file     | `/`                         |
| `--family=`      | A value for `family` properties of the CSS file | The family of the font file |
| `--style=`       | A value for `style` properties of the CSS file  | The style of the font file  |
| `--weight=`      | A value for `weight` properties of the CSS file | `400`                       |
| `--format=`      | Output formats. `woff`, `woff2` or `woff,woff2` | `woff2`                     |

## Note

This script transforms fonts to generate subsets. Please check the fonts' license before use. Also, this script includes Unicode ranges for general Korean fonts. Ligatures, emojis, and Chinese characters may not be included in output files.
