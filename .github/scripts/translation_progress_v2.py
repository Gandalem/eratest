#!/usr/bin/env python3
"""Heuristic Korean translation progress scanner for ERB/ERH sources.

Compares the original/main tree with the korean tree using the same extraction
rules. The primary metric is the reduction of meaningful English prose
characters, reported overall and by content category. It also reports remaining
English-only, mixed Korean/English, Korean-containing, and Japanese-kana units.

This is intentionally a localization scanner, not an ERB parser. Its output is
best used as a trend/progress metric and a work queue, not as a proof that every
string is translated correctly. Large proper-name corpora are reported as
excluded reference data instead of being allowed to dominate prose progress.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

ROOTS = (Path("ERB/TRANSLATION"), Path("ERB/NEWGAME"), Path("ERB/MOVEMENTS"))
EXTS = {".ERB", ".ERH"}

# These are proper-name/reference corpora, not prose localization. A single
# generated-name file contains more English than the rest of the player-facing
# script combined and used to make the headline percentage almost meaningless.
# Keep the list explicit and surface it in the report rather than silently
# teaching the language detector to ignore arbitrary names everywhere.
EXCLUDED_REFERENCE_DATA = {
    "erb/translation/omogatari/newnamegenerator.erb",
    "erb/translation/omogatari/_name_array.erb",
    "erb/translation/_name_array.erb",
}

# Engine dictionaries and render/asset resolvers contain English grammar or
# resource identifiers, not player-facing prose. Keeping this list explicit
# prevents those keys from being mistaken for a localization backlog.
EXCLUDED_INTERNAL_DATA = {
    "erb/translation/lib/irregular_past_verbs.erb",
    "erb/translation/omogatari/aidl_img.erb",
    "erb/translation/omogatari/design/vnstuff.erb",
    "erb/translation/omogatari/k to tw.erb",
    "erb/translation/lib/tense.erb",
}

# Explicit proper-name registries embedded in otherwise translatable files.
# Omogatari_STR lines 1-1645 are the manufacturer/brand/model-name registry;
# later status text, sound effects, and command labels remain in scope.
EXCLUDED_REFERENCE_SECTIONS = {
    "erb/translation/omogatari/omogatari_str.erb": ((1, 1645),),
    # Weather/body-part enum keys consumed by Add_Item parsers.
    "erb/translation/addition/add_item.erb": ((126, 126), (699, 714)),
    # Grammar keys used to assemble the EPL article.
    "erb/translation/omogatari/lore/newspaperotherbullshit.erb": ((45, 50),),
    # Product/model names in the newspaper recall list are intentional proper nouns.
    "erb/translation/omogatari/lore/newspaperads.erb": ((1452, 1461),),
    # Fictional device boot logs deliberately retain vendors, package IDs,
    # paths, and protocol names to read like diagnostic output.
    "erb/translation/omogatari/daily events/lucid dreams/lucid_ev33 propagandize propaganda.erb": ((2039, 2153),),
    "erb/translation/omogatari/internet/tw-internet.erb": ((109, 147),),
}

# A few variables store enum/comparison keys even though their names contain
# display-oriented words. Restrict these skips to the files where that contract
# is known instead of globally suppressing similarly named UI variables.
PATH_INTERNAL_ASSIGNMENT_RE = {
    "erb/translation/anon/betterui.erb": re.compile(
        r"^\s*(?:SFSR_TYPE|DISP_NAME)\s*(?:'\s*)?=", re.IGNORECASE
    ),
    "erb/translation/omogatari/title.erb": re.compile(
        r".*(?:OMOGATARI/Titles/|TITLE_NAS_STR\()", re.IGNORECASE
    ),
    "erb/translation/omogatari/betterui.erb": re.compile(
        r"^\s*RESULTS(?::\d+)?\s*(?:'\s*)?=\s*texts\s*$", re.IGNORECASE
    ),
    "erb/translation/omogatari/setomostats.erb": re.compile(
        r"^\s*nameArray:[^=]*:na_NameType\s*(?:'\s*)?=", re.IGNORECASE
    ),
    "erb/translation/omogatari/omogatari_set.erb": re.compile(
        r"^\s*(?:htmlNameType|nameArray:[^=]*:na_NameType)\s*(?:'\s*)?=",
        re.IGNORECASE,
    ),
    "erb/translation/omogatari/craftingoverhaul.erb": re.compile(
        r"^\s*(?:RETURNF\s+UniversalRank\(\"Extra\"\)|"
        r"LOCALS\s*(?:'\s*)?=\s*\"(?:Bionic|Weapon)\")",
        re.IGNORECASE,
    ),
    "erb/translation/addition/lunatic survival/lunatic survival.erb": re.compile(
        r"^\s*RESULTS\s*(?:'\s*)?=\s*\"Scarlet\"\s*$", re.IGNORECASE
    ),
    "erb/translation/omogatari/smellstuffs.erb": re.compile(
        r"^\s*nTableName\s*(?:'\s*)?=\s*@?\"Smells\"\s*$", re.IGNORECASE
    ),
    "erb/translation/new_update/●kojo_color.erb": re.compile(
        r"^\s*LOCALS\s*(?:'\s*)?=\s*\"Red\",\s*\"Green\",\s*\"Blue\"\s*$",
        re.IGNORECASE,
    ),
    "erb/translation/omogatari/reputation.erb": re.compile(
        r".*GET_STR\(29,\s*\"Reputation\",\s*Rep,\s*\"Name\"\)", re.IGNORECASE
    ),
}

# DT_ROW_ADD stores alternating schema keys and values. Only these values are
# intended for display; identifiers such as defName, techLevel, prerequisites,
# tab, and icon must not enter the translation queue.
VISIBLE_ITEM_DATA_FIELDS = {"fullname", "generic name", "??", "fulldesc"}

VISIBLE_DATA_FIELDS = {
    "label",
    "description",
    "requirement",
    "bonus",
    "category",
    "title",
    "tooltip",
    "message",
    "text",
}

# These tokens are used only to decide whether a line can plausibly emit or
# return user-visible text. PRINT* lines receive special handling below.
VISIBLE_TOKENS = (
    "RETURNF",
    "LOCALS",
    "RESULTS",
    "MAKE_STR",
    "ASK_",
    "HTML",
    "BUTTON",
    "CHOICES",
    "TITLE",
    "DESC",
    "MESSAGE",
    "NAME",
    "SFSR_",
    # Common helpers whose string arguments are emitted as dialogue/prose.
    "TEXT", "SPEAK", "DIALOGUE", "BREAKENG", "LS_SCARLET_YELLOW", "OUTPUT", "PARTS",
)

QUOTED_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')
PRINT_RE = re.compile(r"^\s*(PRINT[A-Z0-9_]*)\b(.*)$", re.IGNORECASE)
EN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]{2,}")
HANGUL_RE = re.compile(r"[가-힣]")
KANA_RE = re.compile(r"[ぁ-ゟ゠-ヿ]")
FORMAT_PERCENT_RE = re.compile(r"%[^%\r\n]+%")
FORMAT_BRACE_RE = re.compile(r"\{[^{}\r\n]+\}")
FORMAT_DOLLAR_RE = re.compile(r"\$[A-Za-z_][A-Za-z0-9_]*\$")
DOMAIN_RE = re.compile(
    r"(?<![A-Za-z0-9-])(?:[A-Za-z0-9-]+\.)+(?:com|net|org|jp|world)(?![A-Za-z0-9-])",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![A-Za-z])")
EXECUTABLE_RE = re.compile(r"(?<![A-Za-z0-9._-])[A-Za-z0-9._-]+\.(?:exe|dll)(?![A-Za-z])", re.IGNORECASE)
EMOTICON_CODE_RE = re.compile(r":[A-Za-z][A-Za-z0-9_]*:")
TECH_COMMAND_RE = re.compile(r"(?<![A-Za-z])git\s+pull(?![A-Za-z])", re.IGNORECASE)
SLASH_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_])/[A-Za-z][A-Za-z0-9_-]*/(?![A-Za-z0-9_])")
USERNAME_RE = re.compile(r"(?<![A-Za-z0-9_])[a-z][a-z_-]*\d{3,}(?![A-Za-z0-9_])")
FSYN_FRAGMENT_RE = re.compile(r'FSYN\("(?:pee|poo):[a-z]?', re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]+>")
HEX_LITERAL_RE = re.compile(r"\b0x[0-9A-Fa-f]{3,8}\b")
TEXT_ADVENTURE_HELP_PREFIX_RE = re.compile(
    r"^\s*(?:look|talk|move|get|use|items|leave)(?:\s+<[^>]+>)?\s*:\s*",
    re.IGNORECASE,
)
SPLIT_G_VISIBLE_RE = re.compile(r'SPLIT_G\(\s*@?"(.*?)"\)', re.IGNORECASE)
MARKDOWN_LINK_TARGET_RE = re.compile(r"\]\([^\)\r\n]+\)")
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
POSIX_PATH_RE = re.compile(r"(?:/[A-Za-z0-9._-]+){2,}")
RELATIVE_RESOURCE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+"
    r"(?:\.(?:csv|gif|jpeg|jpg|json|png|txt|webp|xml)){1,2}(?![A-Za-z0-9_.-])",
    re.IGNORECASE,
)
ESCAPE_RE = re.compile(r"\\(?:n|r|t|%|N)")
FORMAT_CONTROL_RE = re.compile(r"@[A-Za-z]:[^@\r\n]+@")
INLINE_CONDITIONAL_RE = re.compile(
    r"\\@\s*[^?\r\n]*?\?\s*(.*?)\s*#\s*(.*?)\s*\\@"
)
INTERNAL_CODE_IDENTIFIER_RE = re.compile(r"(?<![A-Za-z0-9_])(?:QBit|QLS)[A-Za-z0-9_]+")
INTERNAL_AT_FUNCTION_RE = re.compile(r"@[A-Za-z_][A-Za-z0-9_]*")
INTERNAL_ERB_SYMBOL_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+|"
    r"CALLNAME|TALENTNAME|TALENT|EQUIP|FLAG|ARG|TARGET|MASTER|RESULTS?|LOCALS?)"
    r"(?![A-Za-z0-9_])"
)
INTERNAL_ERB_CALL_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*(?=\s*\()")
INTERNAL_ERB_UPPER_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")
INTERNAL_ERB_CAMEL_RE = re.compile(
    r"\b(?:[a-z][A-Za-z0-9]*[A-Z]|[A-Z][a-z0-9]+[A-Z])[A-Za-z0-9]*\b"
)
INTERNAL_STRING_ARG_FUNCTIONS = {
    "ALL_BRANDS_NAMES", "ARRAYCOPY", "DT_CELL_GET", "DT_CELL_GETS", "DT_EXIST", "DT_SELECT", "FIRSTTIME",
    "FSYN", "GETCONFIG", "GETNUM", "GET_INT", "GET_STR", "GROUPMATCH", "ISPADDED", "NOBYNAME", "SPLIT_CHECK",
    "LS_DESCRIPTION", "ONCE", "STRCOUNT", "STRFIND", "TEXT_ADVENTURE",
    "TOLOWER", "UNDIESCANSOIL", "UNDIESSOILINGTYPE", "PARSE", "CUSTOM_FETISH_NAME",
    "PANTY_REWORK_IS_SOIL", "TITLE_NAS_STR", "MOAN", "PRINT_MALE", "PRINT_PLUR", "PEEANDPOO",
    "VARSIZE", "VERIFYLEGACYACHIEVEMENTDEF", "ADD_APPLY_FAIRY_TITLE_BONUS",
}
# Only the trait selector and loss-tag arguments of FUCK are internal. Later
# quoted arguments contain the actual narration and body-part labels, so the
# whole function must never be blanket-excluded.
INTERNAL_STRING_ARG_POSITIONS = {"AL_GIVE_TALENT": {1}, "FUCK": {1, 2}, "PRINT_PANTY_MOVEMENT_BOTH_GENERAL": {1, 2}, "OPPAI_DESCRIPTION_ACTION": {2}, "REPLACE": {1}, "CHARACTERSINNED": {1}, "GET_RELIGION_PRECEPT": {1}, "SPLIT_SINGLE": {2}, "PRINTBUTTON": {1}, "BROADDAMAGE": {1}}
INTERNAL_STRING_ARG_COMMANDS = {"ARRAYCOPY", "DT_SORT"}
# These helpers return or assemble engine-facing category keys rather than
# player-visible labels. Skip only their bodies; the same words may be visible
# elsewhere and must remain scannable.
INTERNAL_ONLY_FUNCTIONS = {
    "AIMEDSHOTINFO",
    "NASTITLE",
    "NASTITLEABRIV",
    "NASTITLEFETISH",
    "NASTITLESTR",
    "NASTITLESTR_ONLY",
    "PANTY_TOTAL_TAGS",
    "PEE_PAD_NEEDED",
    "SI_PREFIX",
    "VNGETFONT",
}
NON_VISIBLE_CALL_STYLE_LITERALS = {"anger", "blush", "l", "smile", "stare", "strw", "w"}

# Common abbreviations / domain words that should not make an otherwise Korean
# string look untranslated. Proper nouns are deliberately kept conservative:
# unknown names remain visible in the mixed-string review queue.
ENGLISH_ALLOWLIST = {
    "hp", "mp", "sp", "sta", "ene", "exp", "cm", "tsp", "ui", "ux", "ai",
    "html", "nas", "erb", "erh", "fps", "rpm", "usb", "vr", "rpg", "npc",
    "pc", "cpu", "gpu", "ram", "hdd", "ssd", "ddr", "posix", "api",
    "touhou", "gensokyo", "youkai", "danmaku", "youjutsu", "makai",
    "hz", "khz", "mw", "luninco", "resetme", "ctrl", "timelapse", "eac", "dat", "plv", "char",
    # Armor model identifiers; these are inventory codes, not prose.
    "gsh-am", "gshz-as", "lshz-", "ac-untar", "zhp", "zh-",
    # Fictional software/API identifiers shown inside diagnostic logs.
    "gc4casualld", "casualld", "mabclient", "mabapi", "physlink",
    "mabconnect", "exitcode", "neodev", "bbasaikoutw", "maindev",
    # Caliber suffix and attachment/ammunition model identifiers.
    "mmr", "gzh", "acop",
}

# Known schema/data keys that can appear inside a visible expression but are not
# themselves UI text. Keep this list narrow; false negatives are preferable to
# silently hiding real labels.
INTERNAL_LITERAL_ALLOWLIST = {
    "hediff type", "disease", "drug", "no underwear", "shortname", "weaponammo", "vag", "pen",
    "enabled", "channel", "faction", "scenarios", "prank", "rand", "neg", "day", "set", "dot", "wide",
    "strict%nhole%", "reg%nhole%", "rep", "kiss", "guh",
}

# Very short labels that the normal 3+ letter word detector would miss. They
# are counted only when they effectively make up the whole visible unit.
SHORT_ENGLISH_LABELS = {"n/a", "na", "yes", "no", "on", "off", "ok"}

CATEGORY_ORDER = (
    "ui_menu",
    "help_tooltip",
    "item_description",
    "dialogue_event",
    "lore_internet",
    "debug_tools",
    "other_visible",
)
CATEGORY_LABELS = {
    "ui_menu": "UI/메뉴",
    "help_tooltip": "도움말/툴팁",
    "item_description": "아이템 설명",
    "dialogue_event": "대사/이벤트",
    "lore_internet": "세계관/인터넷/뉴스",
    "debug_tools": "디버그/도구",
    "other_visible": "기타 화면 문자열",
}


@dataclass(frozen=True)
class Unit:
    path: str
    line: int
    category: str
    raw: str
    normalized: str
    english_words: tuple[str, ...]
    english_chars: int
    hangul_chars: int
    kana_chars: int
    state: str


@dataclass
class Metrics:
    units: int = 0
    english_chars: int = 0
    english_only: int = 0
    mixed: int = 0
    korean_only: int = 0
    japanese: int = 0
    foreign_other: int = 0

    def add(self, unit: Unit) -> None:
        self.units += 1
        self.english_chars += unit.english_chars
        if unit.kana_chars > 0:
            self.japanese += 1
        if unit.state == "english_only":
            self.english_only += 1
        elif unit.state == "mixed":
            self.mixed += 1
        elif unit.state == "korean_only":
            self.korean_only += 1
        elif unit.state not in {"japanese"}:
            self.foreign_other += 1


def meaningful_english_words(text: str) -> list[str]:
    words = []
    for match in EN_WORD_RE.finditer(text):
        word = match.group(0)
        folded = word.casefold()
        if folded in ENGLISH_ALLOWLIST:
            continue
        # Short all-caps tokens are overwhelmingly stats, caliber names, or UI
        # abbreviations rather than prose.
        letters = re.sub(r"[^A-Za-z]", "", word)
        if letters.isupper() and len(letters) <= 6:
            continue
        words.append(word)

    if not words and not HANGUL_RE.search(text):
        compact = re.sub(r"[^a-z/]+", "", text.casefold())
        if compact in SHORT_ENGLISH_LABELS:
            words.append(compact)
    return words


def normalize_for_language(text: str) -> str:
    # Protect email-like technical identifiers before @function cleanup can
    # split them into misleading fragments.
    text = EMAIL_RE.sub(" ", text)
    # ERB inline conditionals display only the true/false branches. The
    # condition is executable code (often long QBit*/QUEST_FLAG identifiers),
    # so retaining it badly inflates the localization backlog.
    text = INLINE_CONDITIONAL_RE.sub(r" \1 \2 ", text)
    text = TEXT_ADVENTURE_HELP_PREFIX_RE.sub(" ", text)
    # Remove FSYN fragments before the generic call-name cleanup can strip the
    # function name and leave the quoted pee/poo selector behind.
    text = FSYN_FRAGMENT_RE.sub(" ", text)
    text = INTERNAL_CODE_IDENTIFIER_RE.sub(" ", text)
    text = INTERNAL_AT_FUNCTION_RE.sub(" ", text)
    # A quote inside an ERB %...% expression can split a formatted string in
    # the lightweight extractor.  In those fragments, strip only unmistakable
    # ERB symbols/call names so identifiers such as CALLNAME:Add_CULPRIT are
    # never mistaken for player-visible English prose.
    if "%" in text or r"\@" in text or "{" in text or "}" in text:
        text = INTERNAL_ERB_SYMBOL_RE.sub(" ", text)
        text = INTERNAL_ERB_CALL_RE.sub(" ", text)
        text = INTERNAL_ERB_UPPER_RE.sub(" ", text)
        text = INTERNAL_ERB_CAMEL_RE.sub(" ", text)
        text = re.sub(r"(?<=:)[A-Za-z][A-Za-z0-9_]*", " ", text)
    text = URL_RE.sub(" ", text)
    text = EMAIL_RE.sub(" ", text)
    text = EXECUTABLE_RE.sub(" ", text)
    text = EMOTICON_CODE_RE.sub(" ", text)
    text = TECH_COMMAND_RE.sub(" ", text)
    text = SLASH_TOKEN_RE.sub(" ", text)
    text = USERNAME_RE.sub(" ", text)
    # Match relative asset paths before the more general POSIX path cleanup;
    # otherwise a multi-extension path can be split and leave a false prefix.
    text = RELATIVE_RESOURCE_PATH_RE.sub(" ", text)
    text = POSIX_PATH_RE.sub(" ", text)
    text = re.sub(r"(?i)\b(?:resources/custom/|custom\.csv(?:\.txt)?)", " ", text)
    text = DOMAIN_RE.sub(" ", text)
    text = HTML_TAG_RE.sub(" ", text)
    # Wiki link destinations are route keys, while the text before them is
    # player-visible and must still be translated.
    text = MARKDOWN_LINK_TARGET_RE.sub("]", text)
    text = HEX_LITERAL_RE.sub(" ", text)
    text = FORMAT_PERCENT_RE.sub(" ", text)
    text = FORMAT_BRACE_RE.sub(" ", text)
    text = FORMAT_DOLLAR_RE.sub(" ", text)
    text = ESCAPE_RE.sub(" ", text)
    text = FORMAT_CONTROL_RE.sub(" ", text)
    # Keep the text inside ERB inline conditional expressions; only remove the
    # delimiter itself so both visible branches remain measurable.
    text = text.replace(r"\@", " ")
    text = text.replace("＠", " ")
    return " ".join(text.split())


def is_probable_mixed_proper_name(normalized: str, words: tuple[str, ...]) -> bool:
    """Recognize intentional Latin-script brands/models inside Korean prose."""
    if not words or not HANGUL_RE.search(normalized):
        return False
    connectors = {"and", "of", "the", "de", "van", "von", "kai", "ni"}
    if len(words) == 1:
        word = words[0]
        letters = re.sub(r"[^A-Za-z]", "", word)
        if not (letters.isupper() or INTERNAL_ERB_CAMEL_RE.fullmatch(word)
                or "-" in word or any(char.isdigit() for char in word)):
            return False
    for word in words:
        folded = word.casefold()
        letters = re.sub(r"[^A-Za-z]", "", word)
        parts = [part for part in re.split(r"[-']", word) if part]
        if folded in connectors:
            continue
        if letters.isupper() or INTERNAL_ERB_CAMEL_RE.fullmatch(word):
            continue
        if parts and all(part[:1].isupper() or part.isupper()
                         or (len(part) == 1 and part.islower()) for part in parts):
            continue
        return False
    return True


def classify_state(normalized: str) -> tuple[str, tuple[str, ...], int, int, int]:
    words = tuple(meaningful_english_words(normalized))
    if is_probable_mixed_proper_name(normalized, words):
        words = ()
    en_chars = sum(sum(ch.isalpha() and ch.isascii() for ch in word) for word in words)
    hangul_chars = len(HANGUL_RE.findall(normalized))
    kana_chars = len(KANA_RE.findall(normalized))

    has_en = en_chars > 0
    has_ko = hangul_chars > 0
    has_ja = kana_chars > 0

    if has_ko and has_en:
        state = "mixed"
    elif has_ko:
        state = "korean_only"
    elif has_en:
        state = "english_only"
    elif has_ja:
        state = "japanese"
    else:
        state = "foreign_other"
    return state, words, en_chars, hangul_chars, kana_chars


def is_internal_literal(text: str) -> bool:
    stripped = text.strip()
    probe = re.sub(r"^(?:'\s*)?\+?=\s*", "", stripped)
    probe = re.sub(r"\s*;\s*last segment\s*$", "", probe, flags=re.IGNORECASE)
    folded = stripped.casefold()
    compact_label = re.sub(r"[^a-z/]+", "", folded)
    if compact_label in SHORT_ENGLISH_LABELS:
        return False
    if folded in INTERNAL_LITERAL_ALLOWLIST:
        return True
    if re.fullmatch(r"\[\{?VARSIZE\(", stripped, re.IGNORECASE):
        return True
    if re.fullmatch(r"TestVar\{[^}]+\}", stripped, re.IGNORECASE):
        return True
    if re.fullmatch(r"Movement_\{ARG\}", stripped, re.IGNORECASE):
        return True
    if re.fullmatch(r"[A-Z][A-Z0-9_]*:[A-Za-z_][A-Za-z0-9_]*", probe):
        return True
    if re.match(r"^(?:'\s*)?\+?=", stripped) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", probe):
        return True
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9]*:\d+", probe):
        return True
    if RELATIVE_RESOURCE_PATH_RE.fullmatch(probe):
        return True
    if re.search(r"\b(?:priority\s+desc|defName\s*=|faction\s*=|side\s*=)", probe, re.IGNORECASE):
        return True
    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", probe) and re.search(r"[(){}+\-*/]", probe):
        return True
    if probe.startswith(("+", "-")) and re.search(r"[A-Za-z_][A-Za-z0-9_]*\s*\(", probe):
        return True
    if re.fullmatch(r",\s*(?:EQUIP|TARGET|MASTER|LOCAL|ARG)[^,]*,", stripped, re.IGNORECASE):
        return True
    if re.fullmatch(r",\s*[A-Za-z_][A-Za-z0-9_]*\([^,\r\n]+,", stripped):
        return True
    if re.fullmatch(r"button\s+title=.*HTML_ESCAPE\(", stripped, re.IGNORECASE):
        return True
    if re.fullmatch(r"\+\s*(?:RESULTS?|LOCALS?).*\bvalue", stripped, re.IGNORECASE):
        return True
    if re.fullmatch(r"\),\s*ABL:[^,]+,\s*EXP:[^)]+\)%", stripped, re.IGNORECASE):
        return True
    if not stripped:
        return True
    # Strong identifier signals only. Do not suppress ordinary labels like
    # "Body Parts" or "Skill Acquisition".
    if re.fullmatch(r"[A-Za-z0-9_./:+()\-]{1,64}", probe):
        if "_" in probe or probe.isupper():
            return True
    if INTERNAL_ERB_CAMEL_RE.fullmatch(probe):
        return True
    # Executable expressions sometimes reach this function as fragments split
    # from an interpolated string.  Require both a code-style identifier and an
    # operator so ordinary titles containing punctuation remain measurable.
    code_probe = QUOTED_RE.sub("", probe)
    code_identifiers = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code_probe)
    if (
        not HANGUL_RE.search(code_probe)
        and re.search(r"[(),:+*/?#&|]", code_probe)
        and code_identifiers
        and all("_" in token or token.isupper() or len(token) <= 2
                or INTERNAL_ERB_CAMEL_RE.fullmatch(token) for token in code_identifiers)
    ):
        return True
    # A bare function-call expression contains no localizable literal; its
    # returned text is scanned at the function definition or source data.
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*\(.*\)", probe):
        return True
    return False


def is_excluded_reference_path(path: str) -> bool:
    folded = path.replace("\\", "/").casefold()
    return folded in EXCLUDED_REFERENCE_DATA or folded in EXCLUDED_INTERNAL_DATA


def is_path_internal_line(path: str, line: str) -> bool:
    pattern = PATH_INTERNAL_ASSIGNMENT_RE.get(path.replace("\\", "/").casefold())
    return bool(pattern and pattern.match(line))


def is_excluded_reference_line(path: str, line_no: int) -> bool:
    ranges = EXCLUDED_REFERENCE_SECTIONS.get(path.replace("\\", "/").casefold(), ())
    return any(start <= line_no <= end for start, end in ranges)


def quoted_argument_context(line: str, quote_start: int) -> tuple[str, int]:
    """Return the enclosing function and zero-based argument position.

    A regex that merely looks for the last opening parenthesis fails once an
    earlier argument contains a nested call, as in
    ``DT_CELL_GET("table", LOOKUP(ARG), "schemaKey")``. This tiny scanner
    tracks parentheses, quoted strings, and top-level commas so every string
    argument is classified against its actual enclosing call.
    """
    depth = 0
    in_quote = False
    escaped = False
    opening = -1
    for index in range(quote_start - 1, -1, -1):
        char = line[index]
        if in_quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quote = False
            continue
        if char == '"':
            in_quote = True
        elif char == ")":
            depth += 1
        elif char == "(":
            if depth:
                depth -= 1
            else:
                opening = index
                break
    if opening < 0:
        return "", -1

    identifier = re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*$", line[:opening])
    if not identifier:
        return "", -1

    argument = 0
    depth = 0
    in_quote = False
    escaped = False
    for char in line[opening + 1:quote_start]:
        if in_quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quote = False
            continue
        if char == '"':
            in_quote = True
        elif char == "(":
            depth += 1
        elif char == ")" and depth:
            depth -= 1
        elif char == "," and depth == 0:
            argument += 1
    return identifier.group(1).upper(), argument


def quoted_literal_is_internal(line: str, match: re.Match[str]) -> bool:
    literal = match.group(1).strip()
    command = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\b", line)
    if command and command.group(1).upper() in INTERNAL_STRING_ARG_COMMANDS:
        return True
    if command and command.group(1).upper().startswith("DT_"):
        return True
    # PRINTBUTTON's final argument is the internal value returned on click;
    # preceding quoted text is the visible label and must remain scannable.
    if (
        command
        and command.group(1).upper() == "PRINTBUTTON"
        and QUOTED_RE.search(line, match.end()) is None
    ):
        return True
    # CASE operands and quoted comparison operands are enum/tag keys, not
    # displayed text.
    if re.match(r"\s*CASE(?:ELSE)?\b", line, re.IGNORECASE):
        return True
    # A quoted ASCII word followed by the Korean instruction to type it is a
    # required input token, not untranslated prose.
    if (
        HANGUL_RE.search(line)
        and re.search(r"입력(?:하|해)", line)
        and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", literal)
    ):
        return True
    # Quoted operands in comparisons are enum/tag keys, not displayed text.
    if re.search(r"(?:==|!=|>=|<=|>|<)\s*$", line[:match.start()]):
        return True
    function, argument = quoted_argument_context(line, match.start())
    if function in INTERNAL_STRING_ARG_FUNCTIONS:
        return True
    if argument in INTERNAL_STRING_ARG_POSITIONS.get(function, set()):
        return True
    if re.match(r"\s*CALL\b", line, re.IGNORECASE):
        if literal.casefold() in NON_VISIBLE_CALL_STYLE_LITERALS:
            return True
    return is_internal_literal(literal)


def extract_visible_data_values(quoted: list[str]) -> list[str]:
    values = []
    for index, token in enumerate(quoted[:-1]):
        if token.strip().casefold() not in VISIBLE_DATA_FIELDS:
            continue
        value = quoted[index + 1]
        if not is_internal_literal(value):
            values.append(value)
    return values


def extract_strings(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped or stripped.startswith((";", "#", "@")):
        return []

    # Strip markup before looking for quoted strings. Attribute values and ERB
    # expressions inside tags are renderer instructions; visible text between
    # tags remains in the line and is still scanned.
    line = HTML_TAG_RE.sub("", line)
    stripped = line.strip()

    print_match = PRINT_RE.match(line)
    upper = line.upper()
    # PRINTV emits a numeric variable value; its apostrophe/comma payload is
    # formatting syntax rather than player-visible prose.
    if print_match and print_match.group(1).upper() == "PRINTV":
        return []
    if not print_match and not any(token in upper for token in VISIBLE_TOKENS):
        return []

    assignment_match = re.match(
        r"^\s*(?:LOCALS|RESULTS|OUTPUT|PARTS)(?::\d+)?\s*(?:'\s*)?(?:\+?=)\s*(.+)$",
        line,
        re.IGNORECASE,
    )
    # An unquoted display assignment may still contain a quoted title or a
    # quoted argument inside a visible formatter. In that case the full right-
    # hand side is the display value; returning only the quoted fragment loses
    # the surrounding words (for example: Ryuunosuke's "Kappa" ～ Candid Friend).
    if assignment_match:
        payload = assignment_match.group(1).strip()
        # Indexed RESULTS slots conventionally pass engine values between
        # functions. A bare identifier there is executable state, not a label.
        if (re.match(r"^\s*RESULTS:\d+", line, re.IGNORECASE)
                and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", payload)):
            return []
        pure_format_expression = re.fullmatch(r"%.*%", payload)
        if (
            payload
            and not payload.startswith(('"', '@"'))
            and not pure_format_expression
            and not is_internal_literal(payload)
        ):
            return [payload]

    split_g_payloads = [
        match.group(1)
        for match in SPLIT_G_VISIBLE_RE.finditer(line)
        if not is_internal_literal(match.group(1))
    ]
    if split_g_payloads:
        return split_g_payloads

    quoted_matches = list(QUOTED_RE.finditer(line))
    quoted = [match.group(1) for match in quoted_matches]
    if "DT_ROW_ADD" in upper:
        return extract_visible_data_values(quoted)
    visible_quoted = [
        match.group(1) for match in quoted_matches
        if not quoted_literal_is_internal(line, match)
    ]
    if visible_quoted:
        return visible_quoted
    # If quotes were present but every quoted argument was classified as an
    # internal key, do not fall back to rescanning the whole PRINT payload;
    # that would reintroduce the same key through the unquoted path.
    if quoted_matches:
        return []

    # v1 missed unquoted PRINT/PRINTFORM strings entirely. For a PRINT* line
    # with no quotes, scan the payload after the opcode. Format placeholders are
    # removed later by normalize_for_language().
    if print_match:
        payload = print_match.group(2).strip()
        if payload and not is_internal_literal(payload):
            return [payload]
    return []


def classify_category(path: str, text: str, line: str) -> str:
    p = path.replace("\\", "/").casefold()
    normalized = normalize_for_language(text)
    length = len(normalized)

    if "debug" in p or "/cheat/" in p:
        return "debug_tools"

    lore_markers = (
        "/internet/", "/lore/", "new_update", "updatenewsletter", "newspaper",
        "danmaku world", "/ezb/",
    )
    if any(marker in p for marker in lore_markers):
        return "lore_internet"

    help_markers = (
        "html_mouseover", "nas_tips", "talent_info", "tooltip", "/help/",
        "tutorial", "manual", "guide",
    )
    if any(marker in p for marker in help_markers) or re.search(r"\bDESC\b|[\"]DESCRIPTION[\"]\s*,", line.upper()):
        return "help_tooltip"

    item_path = "/item/" in p or p.endswith("/_tr lib.erb") or p.endswith("/_tr%20lib.erb")
    if item_path and length >= 100:
        return "item_description"

    dialogue_markers = (
        "/chara/", "/com/", "/daily events/", "/movements/", "kojo", "conversation",
        "/addition/", "lucid_", "event",
    )
    if any(marker in p for marker in dialogue_markers):
        return "dialogue_event"

    ui_path_markers = (
        "betterui", "item modding", "menu", "setting", "option", "config", "status",
        "shop", "store", "calendar", "character_profile", "character_dialog_status",
    )
    ui_line_markers = ("BUTTON", "CHOICES", "TITLE", "ASK_", "HTML", "SFSR_", "LOCALS")
    if any(marker in p for marker in ui_path_markers):
        return "ui_menu"
    if any(marker in line.upper() for marker in ui_line_markers) and length <= 180:
        return "ui_menu"
    if item_path and length < 100:
        return "ui_menu"
    if PRINT_RE.match(line) and length <= 100:
        return "ui_menu"

    return "other_visible"


def iter_source_files(root: Path) -> Iterable[Path]:
    for rel_root in ROOTS:
        base = root / rel_root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not (path.is_file() and path.suffix.upper() in EXTS):
                continue
            rel = path.relative_to(root).as_posix()
            if not is_excluded_reference_path(rel):
                yield path


def iter_scannable_lines(lines: list[str]) -> Iterable[tuple[int, str]]:
    """Skip non-visible fields inside item catalogs and multiline HTML tags."""
    item_data_depth = 0
    inside_html_tag = False
    item_data_visible = False
    current_function = ""
    for line_no, line in enumerate(lines, 1):
        if inside_html_tag:
            if ">" not in line:
                continue
            line = line.split(">", 1)[1]
            inside_html_tag = False
        if "<" in line and line.rfind("<") > line.rfind(">"):
            line = line[:line.rfind("<")]
            inside_html_tag = True
        stripped = line.strip()
        if not stripped:
            continue
        function_match = re.match(r"@([A-Za-z_][A-Za-z0-9_]*)", stripped)
        if function_match:
            current_function = function_match.group(1).upper()
        if (
            current_function in INTERNAL_ONLY_FUNCTIONS
            or current_function.endswith(("_COMMAND_FROM_SYNONYM", "_TARGET_FROM_SYNONYM"))
        ):
            continue
        if item_data_depth == 0:
            if re.fullmatch(r"SELECTCASE\s+O_DATA", stripped, re.IGNORECASE):
                item_data_depth = 1
                item_data_visible = False
                continue
            yield line_no, line
            continue

        if re.match(r"SELECTCASE\b", stripped, re.IGNORECASE):
            item_data_depth += 1
            continue
        if re.match(r"ENDSELECT\b", stripped, re.IGNORECASE):
            item_data_depth -= 1
            if item_data_depth == 0:
                item_data_visible = False
            continue
        if item_data_depth == 1:
            case_match = re.match(r'CASE\s+"([^"]+)"', stripped, re.IGNORECASE)
            if case_match:
                item_data_visible = case_match.group(1).strip().casefold() in VISIBLE_ITEM_DATA_FIELDS
                continue
            if re.match(r"CASEELSE\b", stripped, re.IGNORECASE):
                item_data_visible = False
                continue
        if item_data_visible:
            yield line_no, line


def scan_tree(root: Path) -> list[Unit]:
    units: list[Unit] = []
    for path in iter_source_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="ignore").splitlines()
        except OSError as exc:
            print(f"warning: failed to read {path}: {exc}", file=sys.stderr)
            continue
        for line_no, line in iter_scannable_lines(lines):
            if is_excluded_reference_line(rel, line_no):
                continue
            if is_path_internal_line(rel, line):
                continue
            for raw in extract_strings(line):
                normalized = normalize_for_language(raw)
                state, words, en_chars, ko_chars, kana_chars = classify_state(normalized)
                # If none of the language signals are present, it is not useful
                # for translation progress and is discarded.
                if not (en_chars or ko_chars or kana_chars):
                    continue
                category = classify_category(rel, raw, line)
                units.append(
                    Unit(
                        path=rel,
                        line=line_no,
                        category=category,
                        raw=raw,
                        normalized=normalized,
                        english_words=words,
                        english_chars=en_chars,
                        hangul_chars=ko_chars,
                        kana_chars=kana_chars,
                        state=state,
                    )
                )
    return units


def aggregate(units: Iterable[Unit]) -> dict[str, Metrics]:
    metrics = {category: Metrics() for category in CATEGORY_ORDER}
    for unit in units:
        metrics.setdefault(unit.category, Metrics()).add(unit)
    return metrics


def total_metrics(metrics: dict[str, Metrics], categories: Optional[set[str]] = None) -> Metrics:
    result = Metrics()
    for category, value in metrics.items():
        if categories is not None and category not in categories:
            continue
        result.units += value.units
        result.english_chars += value.english_chars
        result.english_only += value.english_only
        result.mixed += value.mixed
        result.korean_only += value.korean_only
        result.japanese += value.japanese
        result.foreign_other += value.foreign_other
    return result


def reduction_pct(source: int, target: int) -> Optional[float]:
    if source <= 0:
        return None
    return (source - target) * 100.0 / source


def fmt_pct(value: Optional[float]) -> str:
    return "N/A" if value is None else f"{value:.1f}%"


def rows_for_report(source: dict[str, Metrics], target: dict[str, Metrics]) -> list[dict[str, object]]:
    rows = []
    for category in CATEGORY_ORDER:
        s = source.get(category, Metrics())
        t = target.get(category, Metrics())
        rows.append(
            {
                "category": category,
                "label": CATEGORY_LABELS[category],
                "source_units": s.units,
                "target_units": t.units,
                "source_english_chars": s.english_chars,
                "target_english_chars": t.english_chars,
                "english_reduction_pct": reduction_pct(s.english_chars, t.english_chars),
                "target_english_only": t.english_only,
                "target_mixed": t.mixed,
                "target_korean_only": t.korean_only,
                "target_japanese": t.japanese,
            }
        )
    return rows


def top_remaining_files(units: Iterable[Unit], limit: int = 30) -> list[dict[str, object]]:
    english_chars = Counter()
    english_only = Counter()
    mixed = Counter()
    categories: dict[str, Counter] = defaultdict(Counter)
    for unit in units:
        if unit.english_chars <= 0:
            continue
        english_chars[unit.path] += unit.english_chars
        categories[unit.path][unit.category] += unit.english_chars
        if unit.state == "english_only":
            english_only[unit.path] += 1
        elif unit.state == "mixed":
            mixed[unit.path] += 1
    result = []
    for path, chars in english_chars.most_common(limit):
        category = categories[path].most_common(1)[0][0] if categories[path] else "other_visible"
        result.append(
            {
                "path": path,
                "category": category,
                "english_chars": chars,
                "english_only": english_only[path],
                "mixed": mixed[path],
            }
        )
    return result


def top_review_units(units: Iterable[Unit], state: str, limit: int = 50) -> list[dict[str, object]]:
    selected = [u for u in units if u.state == state]
    selected.sort(key=lambda u: (u.english_chars, len(u.normalized)), reverse=True)
    return [
        {
            "path": u.path,
            "line": u.line,
            "category": u.category,
            "english_chars": u.english_chars,
            "text": u.raw[:500],
        }
        for u in selected[:limit]
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else ["category"]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def make_markdown(
    source_ref: str,
    target_ref: str,
    source_metrics: dict[str, Metrics],
    target_metrics: dict[str, Metrics],
    rows: list[dict[str, object]],
    top_files: list[dict[str, object]],
) -> str:
    s_total = total_metrics(source_metrics)
    t_total = total_metrics(target_metrics)
    core_categories = {"ui_menu", "help_tooltip"}
    s_core = total_metrics(source_metrics, core_categories)
    t_core = total_metrics(target_metrics, core_categories)

    lines = [
        "# 한글패치 진행률 스캐너 v3",
        "",
        f"- 원본 기준: `{source_ref}`",
        f"- 한글화 대상: `{target_ref}`",
        f"- 생성 시각(UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "- 진행률 정의: 동일 스캔 규칙에서 **플레이어 노출 문장의 의미 있는 영문 단어 문자 수가 원본 대비 얼마나 감소했는지**",
        "- 제외 데이터: 대규모 인명 생성 목록, 영어 활용 사전, 렌더/에셋 키, `Omogatari_STR.ERB`의 제조사/모델 레지스트리(1-1645행), `DT_*` 내부 식별자/스키마 값",
        "- 주의: 휴리스틱 스캐너이므로 번역 품질/문맥 정확성 자체를 보증하지는 않음",
        "",
        "## 핵심 지표",
        "",
        "| 범위 | 영문 감소율 | 원본 영문 문자 | 남은 영문 문자 | 영어 전용 문자열 | 한/영 혼합 문자열 | 한글 문자열 |",
        "|---|---:|---:|---:|---:|---:|---:|",
        f"| 전체 | {fmt_pct(reduction_pct(s_total.english_chars, t_total.english_chars))} | {s_total.english_chars:,} | {t_total.english_chars:,} | {t_total.english_only:,} | {t_total.mixed:,} | {t_total.korean_only:,} |",
        f"| 핵심 UI+도움말 | {fmt_pct(reduction_pct(s_core.english_chars, t_core.english_chars))} | {s_core.english_chars:,} | {t_core.english_chars:,} | {t_core.english_only:,} | {t_core.mixed:,} | {t_core.korean_only:,} |",
        "",
        "## 영역별 진행률",
        "",
        "| 영역 | 영문 감소율 | 원본 영문 문자 | 남은 영문 문자 | 영어 전용 | 혼합 | 한글 | 일본어 후보 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['label']} | {fmt_pct(row['english_reduction_pct'])} | "
            f"{int(row['source_english_chars']):,} | {int(row['target_english_chars']):,} | "
            f"{int(row['target_english_only']):,} | {int(row['target_mixed']):,} | "
            f"{int(row['target_korean_only']):,} | {int(row['target_japanese']):,} |"
        )

    lines.extend([
        "",
        "## 남은 영어가 많은 파일",
        "",
        "| 순위 | 영역 | 파일 | 영문 문자 | 영어 전용 | 혼합 |",
        "|---:|---|---|---:|---:|---:|",
    ])
    for index, item in enumerate(top_files, 1):
        lines.append(
            f"| {index} | {CATEGORY_LABELS.get(str(item['category']), str(item['category']))} | "
            f"`{item['path']}` | {int(item['english_chars']):,} | "
            f"{int(item['english_only']):,} | {int(item['mixed']):,} |"
        )

    lines.extend([
        "",
        "## 해석 기준",
        "",
        "- `영어 전용`: 한글 없이 의미 있는 영문 단어가 남은 화면 문자열",
        "- `혼합`: 한글과 의미 있는 영문 단어가 함께 있는 문자열. 고유명사일 수도 있으므로 검토 큐로 사용",
        "- `한글`: 한글이 있고 의미 있는 영문 단어가 없는 문자열",
        "- `일본어 후보`: 히라가나/가타카나가 남은 문자열",
        "- HP/MP/STA/EXP 같은 짧은 약어와 일부 도메인 고유어는 영문 잔량 계산에서 제외",
        "",
    ])
    return "\n".join(lines)


def run_self_test() -> None:
    samples = [
        ("PRINTFORML [999] 돌아가기", "ERB/TRANSLATION/OMOGATARI/ITEM/Item Modding.ERB", "korean_only", "ui_menu"),
        ("PRINTFORML [999] Return", "ERB/TRANSLATION/OMOGATARI/ITEM/Item Modding.ERB", "english_only", "ui_menu"),
        ("PRINTFORML ＜N/A＞", "ERB/TRANSLATION/OMOGATARI/ITEM/Item Modding.ERB", "english_only", "ui_menu"),
        ('HTML = "m"', "ERB/TRANSLATION/OMOGATARI/BetterUI.ERB", "foreign_other", "ui_menu"),
        ("PRINTFORML %AttachmentDisplayName(0, GetAttachmentType(TD_SubPage), ITEM_PICKED)%을(를) 개발했다!", "ERB/TRANSLATION/OMOGATARI/ITEM/Item Modding.ERB", "korean_only", "ui_menu"),
        ('HTML = @"Blood {(MAX(0,BASE:ARG:Blood)*100)/MAX(1,MAXBASE:ARG:Blood)}\\%"', "ERB/TRANSLATION/OMOGATARI/BetterUI.ERB", "english_only", "ui_menu"),
        ('HTML = @"혈액 {(MAX(0,BASE:ARG:Blood)*100)/MAX(1,MAXBASE:ARG:Blood)}\\%"', "ERB/TRANSLATION/OMOGATARI/BetterUI.ERB", "korean_only", "ui_menu"),
        ('PRINTL 카리스마(Charisma) 100 기부', "ERB/TRANSLATION/OMOGATARI/ITEM/Item Modding.ERB", "mixed", "ui_menu"),
        ('HTML = DT_CELL_GET(LOCAL, "Hediff Type")', "ERB/TRANSLATION/OMOGATARI/BetterUI.ERB", None, None),
        ('; PRINTL This is a comment', "ERB/TRANSLATION/TEST.ERB", None, None),
        ('CALL CHARA_TEXT(15, @"Visible spoken dialogue.", "w")', "ERB/TRANSLATION/TEST.ERB", "english_only", "other_visible"),
        ('PRINTL This is a deliberately long item description that should be categorized as an item description because it is well over one hundred characters and remains visible to the player.', "ERB/TRANSLATION/OMOGATARI/ITEM/Test.ERB", "english_only", "item_description"),
        ('HTML = "This character is brave and receives a bonus when facing danger."', "ERB/TRANSLATION/HTML_TALENTS/HTML_MOUSEOVER.ERB", "english_only", "help_tooltip"),
        ('DT_ROW_ADD @"ResearchProject", "defName", "Fire", "label", @"Flamecraft", "description", @"Learn to control fire.", "techLevel", "Animal", "tab", "General",', "ERB/TRANSLATION/OMOGATARI/ResearchProjects.ERB", "english_only", "help_tooltip"),
    ]
    for line, path, expected_state, expected_category in samples:
        strings = extract_strings(line)
        if expected_state is None:
            assert strings == [], (line, strings)
            continue
        assert strings, line
        normalized = normalize_for_language(strings[0])
        state, *_ = classify_state(normalized)
        category = classify_category(path, strings[0], line)
        assert state == expected_state, (line, state, expected_state)
        assert category == expected_category, (line, category, expected_category)
    inline = normalize_for_language(
        r"[0] QBitInternal는 \@ GETBIT(QUEST_FLAG(Alias,Event),QBitInternal) ? ON # OFF \@"
    )
    assert "QBit" not in inline and "GETBIT" not in inline, inline
    assert inline.endswith("ON OFF"), inline
    assert meaningful_english_words(normalize_for_language("gensou-chan.com에서 주문")) == []
    assert meaningful_english_words(normalize_for_language("sags@suaf.gov.seihou로 이메일")) == []
    assert meaningful_english_words(normalize_for_language("Wishmaster.exe를 실행")) == []
    assert meaningful_english_words(normalize_for_language("resources/custom/custom.csv.txt 파일")) == []
    assert meaningful_english_words(normalize_for_language("기저귀 없음 :cirhappy:")) == []
    assert meaningful_english_words(normalize_for_language("git pull로 업데이트")) == []
    assert meaningful_english_words(normalize_for_language("@OSHIKKO_OMORASHI 호출됨")) == []
    assert meaningful_english_words(normalize_for_language("환영해 $alpha$")) == []
    assert meaningful_english_words("M 민감") == []
    assert meaningful_english_words("M") == []
    assert classify_state("AImthropic 스마트 권총「Summers」配置")[0] == "korean_only"
    assert classify_state("Girls are speaking 한국어")[0] == "mixed"
    assert meaningful_english_words("GSh-AM GShZ-AS LShZ-5 AC-UNTAR ZhP Zh-14") == []
    assert meaningful_english_words("GC4CasualLD MabClient MabAPI PHYSLink") == []
    assert meaningful_english_words(normalize_for_language(
        r'%@"【%GET_TALENTNAME_TR(FINDELEMENT(TALENTNAME, '
    )) == []
    assert meaningful_english_words(normalize_for_language(
        r'한국어 %PALAM_NUM_NAS(DiapeCharges:MASTER:0,,,-3,'
    )) == []
    assert meaningful_english_words(normalize_for_language(
        r'한국어 %COND_STR(,CFLAG:MASTER:현재위치)% PRIVATEROOM:21'
    )) == []
    assert extract_strings('CALL COM616_EIRINSPEAK, LOCALS, "smile"') == []
    assert extract_strings('IF STRLENS(GET_STR(nChara, ARGS, ARG, "FullName")) > 1') == []
    assert extract_strings('HTML = DT_CELL_GET(LOCAL, "Hediff Type")') == []
    assert extract_strings('LOCALS = clear') == ["clear"]
    assert extract_strings("PRINTV 'LV,VALUE,'(,50,')") == []
    mixed_title = 'LOCALS = Akutagawa Ryuunosuke\'s "Kappa" ～ Candid Friend'
    assert extract_strings(mixed_title) == [mixed_title.split("=", 1)[1].strip()]
    assert extract_strings('LOCALS = %VISIBLE_LABEL("internalKey")%') == []
    assert extract_strings('SIF SPLIT_CHECK(ARGS:1, "name")') == []
    assert extract_strings('SIF SPLIT_CHECK(strFlag, "const")') == []
    assert extract_strings('PRINTFORM %PRINT_PANTY_MOVEMENT_BOTH_GENERAL(TARGET, "ing", "long", 1)%') == []
    assert extract_strings('PRINTFORM %PRINT_PANTY_MOVEMENT_BOTH_GENERAL(TARGET, "ing", "short", 1, "visible text")%') == ["visible text"]
    assert extract_strings('PRINTFORM %OPPAI_DESCRIPTION_ACTION(MASTER, TARGET, "fondle")%') == []
    assert extract_strings('PRINTBUTTON "[취소]", "cancel"') == ["[취소]"]
    assert extract_strings('CALL CharacterSinned(CALLNAME:TARGET, "Physical Love", "visible sin description")') == ["visible sin description"]
    assert extract_strings('SIF GET_RELIGION_PRECEPT(RELIGION, "Minimum Age for Sex")') == []
    assert extract_strings('LOCALS = SPLIT_SINGLE(NameArray:ARG:na_Title, 1, "●Ability:")') == []
    assert extract_strings('TEMP_NAME = %TEMP_GET("GET_ID", @"TestVar{LOCAL}")%') == []
    assert extract_strings('LOCALS \'= REPLACE(LOCALS, "button value", @"button title= \'%HTML_ESCAPE("번역: " + RESULTS)%\' value")') == []
    assert is_internal_literal("[{VARSIZE(")
    assert is_internal_literal("), ABL:C_ID:Shooting, EXP:C_ID:Shooting)%")
    assert normalize_for_language("0xFF0000") == ""
    assert meaningful_english_words(normalize_for_language(
        "로그: /home/sdm/.config/game/log/file.log"
    )) == []
    assert is_internal_literal(",EQUIP:103:Weapon,")
    assert is_internal_literal(", PresetAttachment(nWeaponPreset,")
    assert meaningful_english_words("7.62x54mmR PS gzh ACOp") == []
    assert meaningful_english_words(normalize_for_language(
        "look <대상>: 주변의 물건들을 조사한다."
    )) == []
    assert extract_strings('CASE "self",TOLOWER(CALLNAME:MASTER)') == []
    assert extract_strings('@EasyImage(path, nAlign = "left")') == []
    assert extract_strings('DT_COLUMN_ADD nTableName, "chara", "int16"') == []
    assert extract_strings('HTML = @"<img src=\'IconName\' height=\'20px\'>"') == []
    assert is_internal_literal('floorTiles:(currentGridLoc:0-startGridLoc:0)')
    assert meaningful_english_words(normalize_for_language('sav/globalAchievements.xml')) == []
    assert is_path_internal_line('ERB/TRANSLATION/ANON/BetterUI.ERB', 'SFSR_TYPE \'= "Love Route"')
    assert is_path_internal_line(
        "ERB/TRANSLATION/OMOGATARI/CraftingOverhaul.ERB", '''LOCALS '= "Weapon"'''
    )
    assert is_path_internal_line(
        "ERB/TRANSLATION/Addition/Lunatic Survival/Lunatic Survival.ERB",
        '''RESULTS '= "Scarlet"''',
    )
    assert is_path_internal_line(
        "ERB/TRANSLATION/OMOGATARI/SmellStuffs.ERB", '''nTableName '= @"Smells"'''
    )
    assert is_path_internal_line(
        "ERB/TRANSLATION/NEW_UPDATE/●KOJO_COLOR.ERB",
        '''LOCALS '= "Red", "Green", "Blue"''',
    )
    assert is_path_internal_line(
        "ERB/TRANSLATION/OMOGATARI/Reputation.ERB",
        'CALL COLORMESSAGE(@"한국어 【%GET_STR(29, "Reputation", Rep, "Name")%】", C_YELLOW)',
    )
    assert extract_strings('PRINTFORMDL 명령어 목록은 "help"를 입력해라.') == []
    assert extract_strings('CALL LS_SCARLET_YELLOW("yellow paint",0)') == ["yellow paint"]
    assert extract_strings('CALL CHARA_TEXT(21,@"「%SPLIT_G(@"Hello there!:Come on!")%」","w")') == ["Hello there!:Come on!"]
    assert extract_strings('CALL CHARA_TEXT(21,@"%SPLIT_G("First line:First alt")% %SPLIT_G("Second line:Second alt")%","w")') == ["First line:First alt", "Second line:Second alt"]
    assert meaningful_english_words(normalize_for_language(
        "[호기심](Talents/Curiosity), [자제력](Talents/Self-Control)"
    )) == []
    assert extract_strings('LOCALS = InternalCode') == []
    assert extract_strings("RESULTS:1 '= Command") == []
    assert is_internal_literal("FLAG:EStimBox")
    assert is_internal_literal("Movement_{ARG}")
    assert extract_strings('PRINTFORM %ALL_BRANDS_NAMES("lastleak")%') == []
    assert extract_strings('TextLine = %FSYN("diaper")%') == []
    assert extract_strings('RETURNF IsPadded(ARG,"diaper") || IsPadded(ARG,"pull-up")') == []
    assert extract_strings('PRINTFORML %UndiesSoilingType("liquid", nLoop)%') == []
    assert extract_strings('PRINTFORM %PARSE("you pull",1)%') == []
    assert extract_strings('PRINTFORM %MOAN(,,4, "rand")%') == []
    assert extract_strings('PRINTFORM %PRINT_MALE("boy",TARGET)%') == []
    assert extract_strings('PRINTFORM %PRINT_PLUR("Character", nBannedCount)%') == []
    assert extract_strings('PRINTFORM %PeeAndPoo(1,1,"pee","poo")%') == []
    assert meaningful_english_words(normalize_for_language(
        '물:은빛 액체:수분이 넘치는 %FSYN("pee:n'
    )) == []
    assert extract_strings('SIF PANTY_REWORK_IS_SOIL(ARG,"liquid",0)') == []
    assert extract_strings('CALL AL_GIVE_TALENT(MASTER, "meet30", 159, 0, "", "Visible reward text")') == ["Visible reward text"]
    assert extract_strings('OUTPUT = You talk with someone') == ["You talk with someone"]
    assert is_internal_literal('LOCALS+HTML_SPACE(MAX(PADDING-HTML_STRINGLEN(LOCALS)+(PANTY_REWORK_IS_SOIL(C_ID,"liquid",3,TABLE_NAME,P_ID)),0))')
    assert is_internal_literal('= CURRENT_RESEARCH_PROJECT_FACTION(CurrentFactionForResearch)')
    assert is_internal_literal('strText + (strPadding * nPaddingLength)')
    assert is_internal_literal('SUBSTRING(ARGS, LOCAL:1) ;last segment')
    assert is_internal_literal('Output:0')
    assert is_internal_literal(',nPee||nScat)+PeeAndPoo(nPee,nScat,@')
    assert extract_strings('SIF LOCALS != "Underwear"') == []
    internal_function_lines = [
        "@PEE_PAD_NEEDED(ARG)",
        "#FUNCTIONS",
        'RETURNF "Bulky Liner"',
        "@VISIBLE_LABEL()",
        "#FUNCTIONS",
        'RETURNF "Visible Label"',
    ]
    assert list(iter_scannable_lines(internal_function_lines)) == [
        (4, internal_function_lines[3]),
        (5, internal_function_lines[4]),
        (6, internal_function_lines[5]),
    ]
    assert extract_strings('CALL TEXT_ADVENTURE("LS Scarlet Abandoned Mansion")') == []
    assert extract_strings('CALL LS_DESCRIPTION("Scarlet")') == []
    assert extract_strings('ARRAYCOPY "RESULTS", "nEntryTempStr"') == []
    nested_data_line = 'HTML = DT_CELL_GET("LoG_RivalStat", LoG_GetRivalDT(ARG), "charaID", 1)'
    assert extract_strings(nested_data_line) == [], extract_strings(nested_data_line)
    fuck_line = 'CALL FUCK(LOSER, "VAGINAL,BOOBS", "vaginal", 0, ARG, @"Visible NAME narration", "음경")'
    assert extract_strings(fuck_line) == ["Visible NAME narration", "음경"], extract_strings(fuck_line)
    item_data_lines = [
        "SELECTCASE O_DATA",
        'CASE "FullName"',
        'CALLF MAKE_STR(V_NAME, "Visible Product Name")',
        'CASE "Absorbency"',
        'CALLF MAKE_STR(V_NAME, "Heavy Internal Rating")',
        "ENDSELECT",
    ]
    assert list(iter_scannable_lines(item_data_lines)) == [(3, item_data_lines[2])]
    data_line = 'DT_ROW_ADD @"ResearchProject", "defName", "Fire", "label", @"Flamecraft", "description", @"Learn to control fire.", "techLevel", "Animal", "tab", "General",'
    assert extract_strings(data_line) == ["Flamecraft", "Learn to control fire."], extract_strings(data_line)
    assert is_excluded_reference_path("ERB/TRANSLATION/OMOGATARI/NewNameGenerator.ERB")
    assert is_excluded_reference_path("ERB/TRANSLATION/lib/IRREGULAR_PAST_VERBS.ERB")
    assert is_excluded_reference_path("ERB/TRANSLATION/OMOGATARI/AIDL_IMG.ERB")
    assert is_excluded_reference_path("ERB/TRANSLATION/OMOGATARI/K to TW.ERB")
    assert is_excluded_reference_path("ERB/TRANSLATION/lib/TENSE.ERB")
    assert not is_excluded_reference_path("ERB/TRANSLATION/OMOGATARI/ResearchProjects.ERB")
    assert is_excluded_reference_line("ERB/TRANSLATION/OMOGATARI/Omogatari_STR.ERB", 100)
    assert is_excluded_reference_line("ERB/TRANSLATION/Addition/Add_Item.ERB", 705)
    assert is_path_internal_line("ERB/TRANSLATION/OMOGATARI/SetOmoStats.ERB", "nameArray:ARG:na_NameType '= \"Western\"")
    assert is_internal_literal("WoodData")
    assert is_internal_literal("HTML_PURIFY(HTML_GETPRINTEDSTR(),1)")
    assert not is_excluded_reference_line("ERB/TRANSLATION/OMOGATARI/Omogatari_STR.ERB", 2217)
    assert meaningful_english_words(normalize_for_language(
        '당신은 %조사처리(CALLNAME:Add_CULPRIT,'
    )) == []
    assert meaningful_english_words(normalize_for_language(
        r'\@ (Add_CULPRIT == 5 || Add_CULPRIT == 6) ? 한국어'
    )) == []

    print("self-test: ok")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="Original/source checkout root")
    parser.add_argument("--target", type=Path, help="Korean checkout root")
    parser.add_argument("--source-ref", default="main")
    parser.add_argument("--target-ref", default="korean")
    parser.add_argument("--output-dir", type=Path, default=Path("translation-progress-v2"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return 0
    if not args.source or not args.target:
        parser.error("--source and --target are required unless --self-test is used")

    source_units = scan_tree(args.source)
    target_units = scan_tree(args.target)
    source_metrics = aggregate(source_units)
    target_metrics = aggregate(target_units)
    rows = rows_for_report(source_metrics, target_metrics)
    top_files = top_remaining_files(target_units)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    markdown = make_markdown(
        args.source_ref,
        args.target_ref,
        source_metrics,
        target_metrics,
        rows,
        top_files,
    )
    (args.output_dir / "summary.md").write_text(markdown, encoding="utf-8")
    write_csv(args.output_dir / "categories.csv", rows)

    payload = {
        "version": 3,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_ref": args.source_ref,
        "target_ref": args.target_ref,
        "metric": "meaningful_english_character_reduction",
        "excluded_reference_data": sorted(EXCLUDED_REFERENCE_DATA),
        "excluded_internal_data": sorted(EXCLUDED_INTERNAL_DATA),
        "excluded_reference_sections": {
            path: [list(bounds) for bounds in ranges]
            for path, ranges in sorted(EXCLUDED_REFERENCE_SECTIONS.items())
        },
        "categories": rows,
        "source_total": asdict(total_metrics(source_metrics)),
        "target_total": asdict(total_metrics(target_metrics)),
        "top_remaining_files": top_files,
        "top_english_only": top_review_units(target_units, "english_only"),
        "top_mixed": top_review_units(target_units, "mixed"),
    }
    (args.output_dir / "report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(markdown)
    github_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_summary:
        with open(github_summary, "a", encoding="utf-8") as f:
            f.write(markdown)
            f.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
