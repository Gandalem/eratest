from __future__ import annotations

from collections import Counter
from pathlib import Path
import argparse
import re

BOM = b"\xef\xbb\xbf"
TOKEN_RE = re.compile(r"%[^%\n]+%|\{[^{}\n]+\}|\\n|\\@")
CASE_RE = re.compile(r'^\s*CASE\s+"((?:\\.|[^"\\])*)"')
ENG_RE = re.compile(r"[A-Za-z]{2,}")
HANGUL_RE = re.compile(r"[가-힣]")
MAKE_STR_RE = re.compile(r'(CALLF MAKE_STR\(V_NAME,\s*(?:@)?")((?:\\.|[^"\\])*)("\))')
FN_RE = re.compile(r'^@([A-Za-z0-9_]+)(?:\(|$)')
RETURN_RE = re.compile(r'(^\s*RETURNF\s+(?:@)?")((?:\\.|[^"\\])*)(".*$)')

FILES = {
    "bionic": "ERB/TRANSLATION/OMOGATARI/Body Parts/Bionic List.ERB",
    "ideology": "ERB/TRANSLATION/OMOGATARI/Ideology.ERB",
    "list": "ERB/TRANSLATION/LIST.ERB",
    "itemstr": "ERB/TRANSLATION/OMOGATARI/Omogatari_STR.ERB",
    "trlib": "ERB/TRANSLATION/_TR Lib.ERB",
}


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    assert raw.startswith(BOM), f"UTF-8 BOM missing: {path}"
    return raw.decode("utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.write_bytes(BOM + text.encode("utf-8"))


def tokens(text: str) -> Counter[str]:
    return Counter(TOKEN_RE.findall(text))


def case_keys(text: str) -> list[str]:
    return [m.group(1) for m in map(CASE_RE.match, text.splitlines()) if m]


BODY = {
    "Leg": "다리", "Arm": "팔", "Hand": "손", "Foot": "발", "Heart": "심장",
    "Spine": "척추", "Penis": "음경", "Vagina": "질", "Breasts": "유방",
    "Eye": "눈", "Lung": "폐", "Liver": "간", "Kidney": "신장", "Stomach": "위",
    "Breast": "유방", "Tongue": "혀", "Ear": "귀", "Bladder": "방광",
    "Nose": "코", "Colon": "결장",
}

BIONIC_EXACT = {
    "Peg Leg": "나무 의족", "Iron Arm": "철제 팔", "Iron Hand": "철제 손",
    "Wooden Foot": "나무 발", "Peg Dick": "나무 음경", "Cochlear Implant": "인공와우",
    "Denture": "틀니", "Aesthetic Nose": "미용 코", "Wig": "가발",
    "Hydraulic Vagina": "유압식 질", "Hydraulic Breasts": "유압식 유방",
    "Yagokoro Enhancement": "야고코로 강화체", "Toughskin Gland": "강인피부 샘",
    "Armorskin Gland": "갑옷피부 샘", "Stoneskin Gland": "돌피부 샘",
    "Fertility Enhancer": "생식력 강화장치", "Joywire": "조이와이어",
    "Painstopper": "페인스토퍼", "Learning Assistant": "학습 보조장치",
    "Circadian Assistant": "일주기 보조장치", "Circadian half-cycler": "일주기 하프사이클러",
    "Youjutsu Sensitizer": "요술 감응 증폭기", "Esper Reader": "에스퍼 리더",
    "Prude Harmonizer": "금욕 조율기", "Coagulator": "응고 촉진기",
    "Aesthetic shaper": "미용 성형기", "Healing enhancer": "치유 강화장치",
    "Bat Wings": "박쥐 날개", "Crow Wings": "까마귀 날개",
    "Hieda Memory Enhancer": "히에다 기억 강화장치", "Eternal Slumber Implant": "영원한 잠 임플란트",
    "PnL-Link": "PnL-링크", "Internal Encyclopedia": "내장 백과사전",
    "Hidden DGL-103": "은닉형 DGL-103", "Nuclear Arm Cannon": "핵 팔대포",
    "Copier": "복제기", "Crystal Wings": "수정 날개", "Nuclear Reactor Core": "원자로 코어",
    "Trojan Soul": "트로이 목마 영혼", "Miracle Enhancement": "기적 강화체",
    "Lunar Dial": "루나 다이얼", "Continence Chip": "배설 조절 칩",
    "Incontinence Chip": "실금 유발 칩", "Sweet Poisonbody": "스위트 포이즌바디",
    "Ostomy System": "장루 시스템", "Foley Catheter": "폴리 카테터",
    "Lucifer Incarnate": "루시퍼 인카네이트", "Reflex Surrender": "반사적 항복",
    "Pathetic Penis": "빈약한 음경", "Robust Penis": "튼튼한 음경",
    "Luminescent Penis": "발광 음경", "Warty Penis": "사마귀 음경",
    "Big Penis": "큰 음경", "Ultra Big Penis": "초대형 음경", "Vagina": "질",
    "Ghost Vagina": "유령 질", "Colon Bomb": "결장 폭탄", "Litter Vagina": "다산형 질",
    "slave brand": "노예 낙인", "back slave brand": "등쪽 노예 낙인",
    "LILAC-ARM energy rifle": "LILAC-ARM 에너지 소총",
    'Cactus Company \\"LILAC-ARM\\" arm-mounted energy rifle': 'Cactus Company \\"LILAC-ARM\\" 팔 장착형 에너지 소총',
}
UNSAFE_BIONIC = {"Immature Penis", "Immature Vagina"}


def translate_bionic_value(value: str) -> str:
    if value in BIONIC_EXACT:
        return BIONIC_EXACT[value]
    for prefix, kp in (("Prosthetic ", "인공 "), ("Bionic ", "바이오닉 "), ("Gensou-chan ", "Gensou-chan ")):
        if value.startswith(prefix) and value[len(prefix):] in BODY:
            return kp + BODY[value[len(prefix):]]
    for suffix, ko in ((" Bladder", " 방광"), (" Colon", " 결장")):
        if value.endswith(suffix):
            return value[:-len(suffix)] + ko
    out = value
    replacements = [
        ("time stopping assistant", "시간 정지 보조장치"),
        ("arm-mounted energy rifle", "팔 장착형 에너지 소총"),
        ("Youjutsu Enabler", "요술 활성화 장치"),
        ("Sandevistan", "산데비스탄"),
        ("Assist Hand", "어시스트 핸드"),
        ("Warfighter", "워파이터"),
        ("Hypermancy", "하이퍼맨시"),
        ("My World", "마이 월드"),
        ("Basic", "베이직"),
        ("Gold", "골드"),
        (" Enabler", " 활성화 장치"),
    ]
    for src, dst in replacements:
        out = out.replace(src, dst)
    return out


IDEOLOGY_MAP = {
    "Irreligion": "무종교", "whoever's listening": "듣고 있는 누군가", "Shinto": "신토",
    "a Kami": "카미", "Buddhism": "불교", "God": "신", "Taoism": "도교",
    "Chang'e": "창어", "Christianity": "기독교", "Islam": "이슬람교", "Allah": "알라",
    "Mutsuism": "무츠이즘", "Pantsuism": "팬츠이즘", "Omutsu-sama": "오무츠 님",
    "Opantsu-sama": "오판츠 님", "Zoroastrianism": "조로아스터교", "Monotheism": "일신교",
    "Polytheism": "다신교", "Animism": "애니미즘", "the Energy": "에너지",
    "Atheism": "무신론", "Yourself": "자기 자신", "Gensokyian": "겐소키안",
    "Dragon God": "용신", "Ancient Greek": "고대 그리스", "Player's Religion": "플레이어의 종교",
}

LIST_MAP = {
    "Main Stats": "주요 능력치", "Sense": "감각", "Techniques": "기교", "Marks": "각인",
    "Skills": "기술", "Favor": "호감", "Health": "건강", "Endurance": "지구력",
    "Victories&Etc": "승리 및 기타",
    "STR": "근력", "ESP": "초능력", "USens": "요도 감각", "Urethra": "요도",
    "Semen Add.": "정액 추가", "RAPE": "강간", "REGR": "퇴행", "Shooting": "사격",
    "Melee": "근접전", "Plants": "식물", "Animals": "동물", "Foraging": "채집",
    "Crafting": "제작", "Reliance": "신뢰", "S. Frustration": "성적 욕구불만",
    "Dialog％": "대화％", "Consc.": "의식", "Sight": "시야", "Hearing": "청각",
    "Moving": "이동", "Manip.": "조작", "Talking": "발화", "Breathing": "호흡",
    "Blood Fil.": "혈액 여과", "Blood Pump.": "혈액 순환", "Fertility": "생식력",
    "Sanity": "정신건강", "Pee Hold": "소변 참기", "Poo Hold": "대변 참기",
    "Alcohol": "알코올", "Drug": "약물", "Combat": "전투", "Psi Resist": "사이오닉 저항",
    "Aggressive": "공격성",
    "Rank": "등급", "Fame": "명성", "Infamy": "악명", "Relation": "관계", "Power": "세력",
    "Threat": "위협", "Title": "칭호", "Leader": "지도자", "Lieutenant": "부관",
    "Officer": "간부", "Sr. Member": "고참 구성원", "Member": "구성원", "Jr. Member": "신입 구성원",
    "Technical Level": "기술 수준", "Wealth": "재산", "Neolit": "신석기", "Antiq": "고대",
    "EarlMe": "초기 중세", "LateMe": "후기 중세", "Rennis": "르네상스", "Indust": "산업",
    "Machin": "기계화", "Mid": "미드월드", "Spacer": "우주 시대", "Ultra": "울트라",
    "Archo": "아키텍", "HakSh": "하쿠레이 신사", "MyouT": "묘렌사", "Villa": "인간 마을",
    "SDM": "홍마관", "BFoTL": "미혹의 죽림", "FoM": "마법의 숲", "Nethe": "명계",
    "YMFot": "요괴의 산 기슭", "YMSum": "요괴의 산 정상", "FHell": "구지옥",
    "Moon": "달", "Makai": "마계", "Friendly With": "우호 관계", "Hostile With": "적대 관계",
}

ITEM_FULL_REPLACEMENTS = {
    "The Millennium Stone of Mirada that Monopolizes Lust": "욕망을 독점하는 미라다의 천년석",
    "Replacement mattress for a bed": "침대용 교체 매트리스",
    "Electroshock Resuscitation Pads": "전기충격 소생 패드",
    "Pro Domestic Automation Box": "프로 가사 자동화 박스",
    "Pro Combat Automation Box": "프로 전투 자동화 박스",
    "Pro Sex Automation Box": "프로 성행위 자동화 박스",
    "Miracle Healing Autoinjector": "기적 치유 자동주사기",
    "Auto-Refilling Baby Bottle": "자동 충전 젖병",
    "Monocular Character Scouter": "단안 캐릭터 스카우터",
    "Sentient Makai God Doll": "자아를 지닌 마계 신 인형",
    "Multifunctional Play Mat": "다기능 플레이 매트",
    "Disposable Bedwetting Pad": "일회용 야뇨 패드",
    "Blank VHS Video Cassette": "공 VHS 비디오 카세트",
    "Vigor Boosting Drink": "활력 증진 음료",
    "Dream Suppressant Drop": "꿈 억제 방울제",
    "Filtered Oxygen Mask": "여과식 산소 마스크",
    "Domestic Automation Box": "가사 자동화 박스",
    "Combat Automation Box": "전투 자동화 박스",
    "Sex Automation Box": "성행위 자동화 박스",
    "Field Surgery Kit": "야전 수술 키트", "Electric Washing Machine": "전기 세탁기",
    "Edible Egg Vibrator": "식용 에그 바이브레이터", "Molded Onahole": "성형 오나홀",
    "Birth Control Pill": "피임약", "Ovulation Drug": "배란 촉진제",
    "Powder Diuretic": "분말 이뇨제", "Antidiuretic Pills": "항이뇨제",
    "VHS Camcorder": "VHS 캠코더", "35mm Camera Film": "35mm 카메라 필름",
    "Wand Vibrator": "완드 바이브레이터", "Intimate Lubricant": "성인용 윤활제",
    "Anal Electrode": "항문 전극", "Pad Electrodes": "패드 전극", "Nipple Electrodes": "유두 전극",
    "Urethral Electrode": "요도 전극", "Gas Chainsaw": "가스 체인톱", "Aphrodisiac": "최음제",
    "Tissue Paper": "화장지", "Diaper Booster": "기저귀 부스터", "Bedwetting Alarm": "야뇨 경보기",
    "Shock Wand": "전기 충격봉",
}

FISH_MAP = {
    "redfin dace": "황어", "red-spotted masu salmon": "붉은점 산천어", "masu salmon": "사쿠라마스",
    "whitespotted char": "곤들매기", "amur minnow": "버들개", "freshwater minnow": "민물피라미",
    "crucian carp": "붕어", "piranha": "피라냐", "garpike": "가아", "bluegill": "블루길",
    "chum salmon": "연어", "wakasagi": "빙어", "rainbow trout": "무지개송어", "lamprey eel": "칠성장어",
    "northern snakehead": "가물치", "sculpin": "둑중개", "sweetfish": "은어", "catfish": "메기",
    "eel": "뱀장어", "himemasu": "히메마스", "carp": "잉어", "coelacanth": "실러캔스",
    "sturgeon": "철갑상어", "kunimasu": "쿠니마스", "grass carp": "초어", "herabuna": "헤라붕어",
    "sakhalin taimen": "이토", "largemouth bass": "큰입배스", "pirarucu": "피라루쿠",
    "takitaro": "타키타로", "black carp": "블랙카프",
}
FESTIVAL_MAP = {
    "New year's food": "오세치 요리", "Sestubun Sushi": "세쓰분 에호마키", "New Year's Soba": "해넘이 소바",
    "New Year's Day": "설날", "Girls' Day": "히나마쓰리", "Mother's Day": "어머니의 날",
    "White Evening": "화이트 이브", "White Day": "화이트데이", "Reitaisai": "예대제", "Bunny Day": "토끼의 날",
    "Star Festival": "칠석", "Lantern Festival": "등불 축제", "Wind God 「Storm Day」": "풍신 「폭풍의 날」",
    "Mid-Autumn Festival": "중추절", "Harvest Festival": "수확제", "Halloween": "할로윈",
    "Setsubun Festival": "세쓰분", "Valentine's Day": "밸런타인데이", "Christmas Eve": "크리스마스이브",
    "Christmas Day": "크리스마스", "New Year's Eve": "섣달그믐",
}
BAIT_MAP = {"Shiny": "반짝임", "Nectar": "꿀", "Plant": "식물", "Meat": "고기", "Poison": "독", "Magic": "마력", "Manure": "거름"}
MUSHI_SKL_MAP = {
    "[Attack]": "[공격]", "[Butterfly Effect]": "[나비 효과]", "[Haze]": "[아지랑이]", "[Luminescence]": "[발광]",
    "[Ancient Power]": "[태고의 힘]", "[Aquatic Slayer]": "[수생 특효]", "[Curse Strike]": "[저주 공격]",
    "[Purification]": "[정화]", "[Leader]": "[대장]", "[Sleeping Powder]": "[수면 가루]",
    "[Evasive Maneuvers]": "[고속 회피]", "[Poison Attack]": "[독 공격]", "[Paralysis Attack]": "[마비 공격]",
    "[Dominate]": "[지배]", "[Strong Attack]": "[강공격]", "[Sonic Attack]": "[음파 공격]", "[Autumn Bug]": "[가을 벌레]",
    "[Fierce Attack]": "[맹공]", "[Critical Strike]": "[치명타]", "[Mimic]": "[의태]", "[Venom Attack]": "[맹독 공격]",
    "[Noise Attack]": "[소음 공격]", "[Summer Bug]": "[여름 벌레]", "[Preemptive Move]": "[선제 행동]",
    "[Uplift]": "[고양]", "[Stink Attack]": "[악취 공격]", "[Soft Slayer]": "[연체 특효]", "[Shining Shell]": "[빛의 갑각]",
    "[Stand Firm]": "[버티기]", "[Retaliate]": "[역습]", "[Counter]": "[반격]", "[Minuscule]": "[극소]",
    "[Perfect Guard]": "[완벽 방어]", "[Quicksand]": "[유사]", "[Grotesque Strike]": "[그로테스크 공격]",
    "[Flying Slayer]": "[비행 특효]", "[Extermination]": "[구축]", "[Absorption Attack]": "[흡수 공격]",
    "[Mucus Attack]": "[점액 공격]", "[Regeneration]": "[재생]", "[Fatal Strike]": "[필살 공격]",
    "[Laser Attack]": "[레이저 공격]", "[RED AUTO GOLDEN MAXIMUM BURNING!!!]": "[레드 오토 골든 맥시멈 버닝!!!]",
}
MUSHI_TRIBE_MAP = {
    "[Butterfly]": "[나비]", "[Flying]": "[비행]", "[Grasshopper]": "[메뚜기]", "[Dragonfly]": "[잠자리]",
    "[Aquatic]": "[수생]", "[Beetle]": "[딱정벌레]", "[Stag Beetle]": "[사슴벌레]", "[Kabuto]": "[장수풍뎅이]",
    "[Earthdwelling]": "[지중]", "[Larva]": "[유충]", "[Multiped]": "[다족]", "[Softbodied]": "[연체]",
    "[Crustacean]": "[갑각류]", "[Amphibian]": "[양서류]", "[Frog]": "[개구리]", "[Reptile]": "[파충류]",
    "[Machine]": "[기계]", "[Man-Made Insect]": "[인조 곤충]",
}
MUSHI_STATUS_MAP = {
    "<Poison>": "<독>", "<Venom>": "<맹독>", "<Paralysis>": "<마비>", "<Sleep>": "<수면>",
    "<Confusion>": "<혼란>", "<Slow>": "<둔화>", "<Stink>": "<악취>", "<Counter+>": "<역습+>",
    "<Uplift>": "<고양>", "<Terrain+>": "<지형+>", "<Season+>": "<계절+>", "<Leader>": "<대장>",
    "<Haze>": "<아지랑이>", "<Mimic>": "<의태>",
}
WATER_MAP = {"Plain Water": "맹물", "Misty Lake Water": "안개의 호수 물", "Hell's Hot Spring Water": "지옥 온천수", "Miracle Water": "기적의 물"}
FERMENT_MAP = {
    "Grape Juice": "포도즙", "Potato Water": "감자물", "Honey Water": "꿀물", "Raspberry Water": "산딸기물",
    "Sugared Water": "설탕물", "Fortified Grape Juice": "강화 포도즙", "Botrytized Grape Juice": "귀부 포도즙",
    "Reimu's Chewed Rice": "레이무가 씹은 밥", "Sanae's Chewed Rice": "사나에가 씹은 밥",
    "Reimu&Sanae's Chewed Rice": "레이무와 사나에가 씹은 밥", "Sake Mash (Rice)": "사케 술덧(쌀)",
    "Sake Mash (Kijoshu)": "사케 술덧(기조슈)", "Pumpkin Water": "호박물", "Strawberry Juice": "딸기즙",
    "Unaged Fragolino": "숙성 전 프라골리노", "Watermelon Juice": "수박즙", "Akebia Water": "으름물",
    "Herbaceous Water": "허브물", "Malted Barley": "맥아", "Apple Juice": "사과즙", "Ume Water": "매실물",
    "Macerated Almonds": "침출 아몬드", "Kefir Grains": "케피어 그레인", "Hermit Peach Juice": "선도 복숭아즙",
    "Sake Mash (Polished Rice)": "사케 술덧(정미)", "Liquefied Rotors": "액화 로터", "Ginseng Water": "인삼물",
}
ALCOHOL_MAP = {"Blackout": "필름 끊김", " Wasted ": " 만취 ", "Hammered": "곤드레만드레", "  Drunk ": "  취함 ", "  Tipsy ": "  알딸딸 ", "  Warm  ": "  훈훈함  "}

TR_FUNC_MAPS = {
    "FISH_NAME_TR": FISH_MAP,
    "FESTIVAL_MENU_TR": FESTIVAL_MAP,
    "FESTIVAL_TR": FESTIVAL_MAP,
    "BAIT_TR": BAIT_MAP,
    "MUSHI_SKL_TR": MUSHI_SKL_MAP,
    "MUSHI_TRIBE_TR": MUSHI_TRIBE_MAP,
    "MUSHI_STATUS_TR": MUSHI_STATUS_MAP,
    "VAR_WATER_TR": WATER_MAP,
    "VAR_FERMENT_TR": FERMENT_MAP,
    "ALCOHOL_FACE_TR": ALCOHOL_MAP,
}


def apply_bionic(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    field = None
    seen = eligible = changed = 0
    missed: list[str] = []
    for i, line in enumerate(lines):
        cm = CASE_RE.match(line)
        if cm:
            field = cm.group(1) if cm.group(1) in {"名前", "FullName"} else None
            continue
        if field is None or line.lstrip().startswith(";"):
            continue
        m = MAKE_STR_RE.search(line)
        if not m:
            continue
        value = m.group(2)
        if not ENG_RE.search(value) or HANGUL_RE.search(value):
            continue
        seen += 1
        if value in UNSAFE_BIONIC:
            continue
        eligible += 1
        new = translate_bionic_value(value)
        if new == value:
            missed.append(value)
            continue
        lines[i] = line[:m.start(2)] + new + line[m.end(2):]
        changed += 1
    assert seen == 264, f"Bionic visible English-only name/full count changed: {seen}"
    assert eligible == 260, f"Bionic eligible count changed: {eligible}"
    assert not missed, f"Bionic unmapped values: {missed}"
    assert changed == 260, changed
    return "".join(lines), changed


def apply_ideology(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    field = None
    changed = 0
    for i, line in enumerate(lines):
        cm = CASE_RE.match(line)
        if cm:
            field = cm.group(1) if cm.group(1) in {"Name", "Deity"} else None
            continue
        if field is None or line.lstrip().startswith(";"):
            continue
        m = MAKE_STR_RE.search(line)
        if not m:
            continue
        value = m.group(2)
        if value in IDEOLOGY_MAP:
            new = IDEOLOGY_MAP[value]
            lines[i] = line[:m.start(2)] + new + line[m.end(2):]
            changed += 1
    assert changed == 31, f"Ideology changed {changed}, expected 31"
    return "".join(lines), changed


def apply_list(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    changed_entries = 0
    changed_lines = 0
    for i, line in enumerate(lines):
        if not re.match(r'^#DIMS CONST (DISP_NAME|DISP_MEMO|DISP_FACTION)\s*=', line):
            continue
        original = line
        for src, dst in LIST_MAP.items():
            needle = f'"{src}"'
            count = line.count(needle)
            if count:
                line = line.replace(needle, f'"{dst}"')
                changed_entries += count
        if line != original:
            lines[i] = line
            changed_lines += 1
    assert changed_entries == 83, f"LIST entries changed {changed_entries}, expected 83"
    assert changed_lines == 3, f"LIST lines changed {changed_lines}, expected 3"
    return "".join(lines), changed_lines


def apply_itemstr(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    active = None
    seen = changed = 0
    missed: list[str] = []
    pairs = sorted(ITEM_FULL_REPLACEMENTS.items(), key=lambda kv: len(kv[0]), reverse=True)
    for i, line in enumerate(lines):
        fm = FN_RE.match(line)
        if fm:
            active = fm.group(1)
            continue
        if active != "ItemName_Full" or line.lstrip().startswith(";"):
            continue
        m = RETURN_RE.match(line)
        if not m:
            continue
        value = m.group(2)
        if not ENG_RE.search(value) or HANGUL_RE.search(value):
            continue
        seen += 1
        new = value
        for src, dst in pairs:
            new = new.replace(src, dst)
        if new == value:
            missed.append(value)
            continue
        lines[i] = m.group(1) + new + m.group(3)
        changed += 1
    assert seen == 43, f"ItemName_Full English-only count changed: {seen}"
    assert not missed, f"ItemName_Full unmapped: {missed}"
    assert changed == 43, changed
    return "".join(lines), changed


def apply_trlib(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    active = None
    changed = 0
    by_fn = Counter()
    for i, line in enumerate(lines):
        fm = FN_RE.match(line)
        if fm:
            active = fm.group(1)
            continue
        mapping = TR_FUNC_MAPS.get(active)
        if not mapping or line.lstrip().startswith(";"):
            continue
        original = line
        for src, dst in mapping.items():
            needle = f'"{src}"'
            count = line.count(needle)
            if count:
                line = line.replace(needle, f'"{dst}"')
                changed += count
                by_fn[active] += count
        if line != original:
            lines[i] = line
    expected = {
        "FISH_NAME_TR": 31, "FESTIVAL_MENU_TR": 3, "FESTIVAL_TR": 21, "BAIT_TR": 7,
        "MUSHI_SKL_TR": 46, "MUSHI_TRIBE_TR": 18, "MUSHI_STATUS_TR": 14,
        "VAR_WATER_TR": 4, "VAR_FERMENT_TR": 27, "ALCOHOL_FACE_TR": 6,
    }
    assert dict(by_fn) == expected, f"_TR Lib per-function counts differ: {dict(by_fn)}"
    assert changed == 177, changed
    return "".join(lines), changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root)
    paths = {k: root / v for k, v in FILES.items()}
    before = {k: read_text(p) for k, p in paths.items()}
    before_tokens = {k: tokens(t) for k, t in before.items()}
    before_cases = {k: case_keys(t) for k, t in before.items()}

    outputs = {}
    counts = {}
    outputs["bionic"], counts["bionic"] = apply_bionic(before["bionic"])
    outputs["ideology"], counts["ideology"] = apply_ideology(before["ideology"])
    outputs["list"], counts["list"] = apply_list(before["list"])
    outputs["itemstr"], counts["itemstr"] = apply_itemstr(before["itemstr"])
    outputs["trlib"], counts["trlib"] = apply_trlib(before["trlib"])

    for key, text in outputs.items():
        assert tokens(text) == before_tokens[key], f"protected tokens changed in {FILES[key]}"
        assert case_keys(text) == before_cases[key], f"CASE keys changed in {FILES[key]}"
        write_text(paths[key], text)
        assert paths[key].read_bytes().startswith(BOM)

    assert counts == {"bionic": 260, "ideology": 31, "list": 3, "itemstr": 43, "trlib": 177}, counts
    print("PASS63_COUNTS", counts)
    print("PASS63_CHANGED_LINES_EXPECTED", sum(counts.values()))


if __name__ == "__main__":
    main()
