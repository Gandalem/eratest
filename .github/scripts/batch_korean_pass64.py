from __future__ import annotations

from pathlib import Path
import re

BOM = b"\xef\xbb\xbf"
TOKEN_RE = re.compile(r'%[^%\n]+%|\{[^{}\n]+\}|\\n|\\@')

TALENT = "ERB/TRANSLATION/OMOGATARI/TALENTNAME_NAS.ERB"
SPELL = "ERB/TRANSLATION/OMOGATARI/ITEM/Omogatari_SpellCards.ERB"
TRLIB = "ERB/TRANSLATION/_TR Lib.ERB"
LIST = "ERB/TRANSLATION/LIST.ERB"

TALENT_MAP = {
    "Love": "연모",
    "Intimate Partner": "친밀한 동반자",
    "Paramour": "애인",
    "Affectionate Slut": "애정 깊은 음탕녀",
    "Corrupt Love": "타락한 사랑",
    "Trojan Souled": "트로이 영혼",
    "Engaged": "약혼",
    "Empathic": "공감적",
    "Apathetic": "무관심",
    "Psychopath": "사이코패스",
    "Desensitized": "둔감",
    "IGNORANT -> SEX KNOWLEDGE FAILED! REPORT THIS!": "무지 -> 성 지식 변환 실패! 이 오류를 보고하세요!",
    "Very Tough": "매우 강인함",
    "Tough": "강인함",
    "Wimp": "나약함",
    "Hard To Get Aroused": "흥분하기 어려움",
    "Easy To Get Aroused": "흥분하기 쉬움",
    "Hard To Get Wet": "젖기 어려움",
    "Easy To Get Wet": "젖기 쉬움",
    "Slow Learner": "느린 학습자",
    "Fast Learner": "빠른 학습자",
    "Very Fast Learner": "매우 빠른 학습자",
    "Hyper Fast Learner": "초고속 학습자",
    "Instant Learner": "순간 학습자",
    "Teetotaler": "금주가",
    "Extreme Drug Weakness": "약물 극도 취약",
    "Strong Drug Weakness": "약물 심각 취약",
    "Moderate Drug Weakness": "약물 중간 취약",
    "Light Drug Weakness": "약물 약간 취약",
    "Normal Drug Tolerance": "보통 약물 내성",
    "Light Drug Tolerance": "약물 약한 내성",
    "Moderate Drug Tolerance": "약물 중간 내성",
    "Strong Drug Tolerance": "약물 강한 내성",
    "Heavy Drug Tolerance": "약물 매우 강한 내성",
    "Extreme Drug Tolerance": "약물 극도 내성",
    "Drug Immune": "약물 면역",
    "Can't Pee": "배뇨 불가",
    "Urinary Continence": "요실금 없음",
    "Peeing Habit": "배뇨 습관",
    "Urinary Incontinence": "요실금",
    "Inchling": "소인",
    "Baby-Sized": "아기 크기",
    "Toddler-Sized": "유아 크기",
    "Child-Sized": "어린이 크기",
    "Petite": "작은 체구",
    "Normal Size": "보통 체구",
    "Tall": "장신",
    "Huge": "거구",
    "Giant": "거인",
    "C Insensitive": "C 둔감",
    "C Sensitive": "C 민감",
    "C Hypersensitive": "C 초민감",
    "V Insensitive": "V 둔감",
    "V Sensitive": "V 민감",
    "V Hypersensitive": "V 초민감",
    "A Insensitive": "A 둔감",
    "A Sensitive": "A 민감",
    "A Hypersensitive": "A 초민감",
    "B Insensitive": "B 둔감",
    "B Sensitive": "B 민감",
    "B Hypersensitive": "B 초민감",
    "Flat Chest": "평평한 가슴",
    "Tiny Breasts": "아주 작은 가슴",
    "Small Breasts": "작은 가슴",
    "Average Breasts": "보통 가슴",
    "Big Breasts": "큰 가슴",
    "Huge Breasts": "매우 큰 가슴",
    "Gigantic Breasts": "거대한 가슴",
    "Mystifying Breasts": "불가사의한 가슴",
    "Thick Semen": "농후 정액",
    "Sterilized": "불임",
    "Nondrinker": "비음주자",
    "Occasional Drinker": "가끔 마심",
    "Alcohol Adverse": "알코올 취약",
    "Light Drinker": "술이 약함",
    "Weak Drinker": "술에 매우 약함",
    "Moderate Drinker": "보통 주량",
    "Strong Drinker": "술이 강함",
    "Heavy Drinker": "대주가",
    "Alcohol Addict": "알코올 중독",
    "Drunkard": "술꾼",
    "Heavy Drunkard": "심한 술꾼",
    "Alcohol Immune": "알코올 면역",
    "Slow Recovery": "느린 회복",
    "Fast Recovery": "빠른 회복",
    "Very Fast Recovery": "매우 빠른 회복",
    "Hyper Fast Recovery": "초고속 회복",
    "Sex Friend": "섹스 프렌드",
    "Hooked Fuckbudy": "푹 빠진 섹스 파트너",
    "Animal": "동물",
    "God": "신",
    "Missile": "미사일",
    "Yandere": "얀데레",
    "Friend": "친구",
    "Slave": "노예",
    "Can't Poo": "배변 불가",
    "Bowel Continence": "변실금 없음",
    "Pooping Habit": "배변 습관",
    "Bowel Incontinence": "변실금",
    "Youjutsu: ": "요술: ",
    "Lewd Urethra": "음란한 요도",
    "Dead Calm": "완전한 침착",
    "Serene": "평온",
    "Over-Estimative": "과대평가형",
    "Under-Estimative": "과소평가형",
    "Aggressive": "공격적",
    "Bloodlust": "피의 갈망",
    "Pacifist": "평화주의자",
    "Confident": "자신만만",
    "Opportunist": "기회주의자",
    "War Stubborn": "전투 고집",
    "Danmaku Restrained": "탄막 자제",
    "Prefers Danmaku": "탄막 선호",
    "Likes Danmaku": "탄막을 좋아함",
    "Likes Lethal": "살상전을 좋아함",
    "Prefers Lethal": "살상전 선호",
    "Lethal Restrained": "살상전 자제",
    " Bladder": " 방광",
    " Bowels": " 장",
    "Unbreakable Soul": "불굴의 영혼",
    "Unbreakable Mind": "불굴의 정신",
    "Steel Mind": "강철 정신",
    "Strong Mind": "강인한 정신",
    "Strengthened Mind": "강화된 정신",
    "Stable Mind": "안정된 정신",
    "Dented Mind": "흔들린 정신",
    "Weak Mind": "약한 정신",
    "Unstable Mind": "불안정한 정신",
    "Very Unstable Mind": "매우 불안정한 정신",
    "Extremely Unstable Soul": "극도로 불안정한 영혼",
    "U Insensitive": "U 둔감",
    "U Sensitive": "U 민감",
    "U Hypersensitive": "U 초민감",
    "Padded Guardian": "패드의 수호자",
    "Soggy Legend": "축축한 전설",
    "Squishy Legend": "물컹한 전설",
    "Padded Legend": "패드의 전설",
    "Guardian of Omorashi": "오모라시의 수호자",
    "Leaky Legend": "새는 전설",
    "Messy Legend": "지저분한 전설",
    "Third Eye": "제3의 눈",
    "Loves Urine": "소변을 좋아함",
    "Scat Addict": "스캇 중독",
    "Jelly Freak": "젤리광",
    "Logic Breaker": "논리 파괴자",
    "Ouroboros Orgasm": "우로보로스 오르가즘",
    " (Pull)": " (당기기)",
    " (Push)": " (밀기)",
    "Husband": "남편",
    "Spouse": "배우자",
    "Wife": "아내",
    "Ex-Husband": "전남편",
    "Ex-Spouse": "전 배우자",
    "Ex-Wife": "전 아내",
    "Ex-Lover": "전 연인",
    "Concubine": "첩",
    "Son": "아들",
    "Offspring": "자녀",
    "Daughter": "딸",
    "Brother": "형제",
    "Sibling": "형제자매",
    "Sister": "자매",
    "Half-Brother": "이복형제",
    "Halfsibling": "이복형제자매",
    "Half-Sister": "이복자매",
    "Father": "아버지",
    "Parent": "부모",
    "Mother": "어머니",
    "Grandson": "손자",
    "Grandchild": "손주",
    "Granddaughter": "손녀",
    "Kin": "혈족",
    "Father-in-law": "시아버지/장인",
    "Parent-in-law": "배우자의 부모",
    "Mother-in-law": "시어머니/장모",
    "Son-in-law": "사위",
    "Child-in-law": "자녀의 배우자",
    "Daughter-in-law": "며느리",
    "Clone": "클론",
    "Grandfather": "할아버지",
    "Grandparent": "조부모",
    "Grandmother": "할머니",
    "Dirge of Decay": "부패의 장송곡",
    "Hourai Sanctification": "봉래 성화",
    "Divine Mortality": "신성한 필멸",
    "Ignore U Insensitivity": "U 둔감 무시",
    "Fae Nullifier": "요정 무효화",
    "Abnormal Cum Production": "비정상 정액 생성",
    "Technology Knowledge: ": "기술 지식: ",
    "Sex Knowledge: ": "성 지식: ",
    "Tentacle Seedbed": "촉수 묘상",
    "Necro Freak": "네크로광",
    "Milk Cow": "젖소",
    "Bastard": "사생아",
    "Lewd Feet": "음란한 발",
    "Yielding": "굴복",
    "Stockholm Syndrome": "스톡홀름 증후군",
    "Custom Char.": "사용자 캐릭터",
    "Custom Char. Ver: ": "사용자 캐릭터 버전: ",
    "Born Child": "출생 자녀",
    "Blort Prone": "블로트 경향",
    "Urgency Sense": "급박감 감지",
    "Continence Ignorant": "배설 조절 무지",
    "Toilet Ignorant": "화장실 무지",
    "Volatile Potty Learner": "불안정한 배변 학습자",
    "Messy Stamina": "실수 내구력",
    "Quadrupedal": "사족보행",
    "Unipedal (Ghost Lower)": "외다리형(유령 하체)",
    "Unipedal (Tail Lower)": "외다리형(꼬리 하체)",
    "Kemonomimi": "케모노미미",
    "Oviparous Bipedal": "난생 이족보행",
    "Insectlike Bipedal": "곤충형 이족보행",
    "Bipedal Android": "이족보행 안드로이드",
    "Satori": "사토리",
    "Car (4W, ICE)": "자동차(4륜, 내연기관)",
    "Car (4W, EV)": "자동차(4륜, 전기)",
    "Bike (Manual)": "자전거(수동)",
    "Bike (ICE)": "바이크(내연기관)",
    "Bike (EV)": "바이크(전기)",
    "Helicopter": "헬리콥터",
    "Quadcopter": "쿼드콥터",
    "Muscle Tracer": "머슬 트레이서",
    "Muscle Tracer (Armless)": "머슬 트레이서(팔 없음)",
    "Armored Core": "아머드 코어",
    "NEXT Armored Core": "NEXT 아머드 코어",
    "Non Sentient": "비지성체",
    "Raider": "약탈자",
    "Crafting Lv": "제작 Lv",
    "Technology Knowledge": "기술 지식",
    "Custom Character": "사용자 캐릭터",
    "Custom Character Version": "사용자 캐릭터 버전",
    "Sexual Knowledge": "성 지식",
    "U Sensitivity": "U 감도",
    "Sanity": "정신건강",
    "Youjutsu Knowledge": "요술 지식",
    "Bladder Size": "방광 크기",
    "Bowel Size": "장 크기",
    "Accident Addict": "실수 중독",
    "Abnormal Pee Production": "비정상 소변 생성",
    "Abnormal Poop Production": "비정상 대변 생성",
    "Body Type": "신체 유형",
    "Unmanned Vehicle": "무인 차량",
}

SPELL_MAP = {
    "「King Crimson」": "「킹 크림슨」",
    "Dream Sign 「Duplex Barrier」": "몽부 「이중 결계」",
    "Moon Sign 「Moonlight Ray」": "월부 「달빛 광선」",
    "Ice Sign 「Icicle Fall」": "빙부 「고드름 낙하」",
    "Fire Sign 「Agni Shine」": "화부 「아그니 샤인」",
    "Flower Sign 「Gorgeous Sweet Flower」": "화부 「화려하고 달콤한 꽃」",
    "Otherworld 「Oumagatoki」": "이계 「오우마가토키」",
    "Generic Bomb": "범용 봄",
    "「Chaos Skip」": "「카오스 스킵」",
    "Dream Land 「Great Duplex Barrier」": "몽경 「대이중 결계」",
    "Night Sign 「Night Bird」": "야부 「나이트 버드」",
    "Hail Sign 「Hailstorm」": "박부 「우박 폭풍」",
    "Conjuring 「Misdirection」": "기술 「미스디렉션」",
    "Water Sign 「Princess Undine」": "수부 「프린세스 운디네」",
    "Flower Sign 「Selaginella 9」": "화부 「셀라기넬라 9」",
    "Impossible Request 「Jewel from the Dragon's Neck -Five-Colored Shots-」": "난제 「용의 목에 걸린 구슬 -오색 탄환-」",
    "Earth 「Impurity Within One's Body」": "대지 「몸속의 부정」",
    "Spirit Sign 「Dream Seal -Spread-」": "영부 「몽상봉인 -산-」",
    "Darkness Sign 「Demarcation」": "암부 「디마케이션」",
    "Freeze Sign 「Perfect Freeze」": "동부 「퍼펙트 프리즈」",
    "Conjuring 「Mesmerizing Misdirection」": "기술 「현혹의 미스디렉션」",
    "Wood Sign 「Sylphy Horn」": "목부 「실피 혼」",
    "Rainbow Sign 「Colorful Rainbow Wind Chime」": "홍부 「채색의 무지개 풍경」",
    "Divine Treasure 「Brilliant Dragon Barrette」": "신보 「찬란한 용의 비녀」",
    "Moon 「Apollo Reflection Mirror」": "달 「아폴로 반사경」",
    "Scattered Spirit 「Dream Seal -Worn-」": "산령 「몽상봉인 -마모-」",
    "Snow Sign 「Diamond Blizzard」": "설부 「다이아몬드 블리자드」",
    "Illusion Existence 「Clock Corpse」": "환존 「클록 콥스」",
    "Earth Sign 「Lazy Trilithon」": "토부 「레이지 트릴리톤」",
    "Illusion Sign 「Imaginary Flower Yumekazura」": "환부 「몽환화 유메카즈라」",
    "Impossible Request 「Buddha's Stone Bowl -Indomitable Will-」": "난제 「부처의 석발 -불굴의 의지-」",
    "Otherworld 「Hell's Non-Ideal Danmaku」": "이계 「지옥의 비이상 탄막」",
    "Dream Sign 「Evil-Sealing Circle」": "몽부 「봉마진」",
    "Metal Sign 「Metal Fatigue」": "금부 「금속 피로」",
    "Colorful Sign 「Vivid Chaotic Dance」": "채부 「선명한 혼돈의 춤」",
    "Divine Treasure 「Buddhist Diamond」": "신보 「불교의 금강석」",
    "Earth 「Rain Falling in Hell」": "대지 「지옥에 내리는 비」",
    "Divine Arts 「Omnidirectional Dragon-Slaying Circle」": "신기 「전방위 용살진」",
    "Fire Sign 「Agni Shine High Level」": "화부 「아그니 샤인 상급」",
    "Impossible Request 「Robe of Fire Rat -Unhurried Mind-」": "난제 「불쥐의 가죽옷 -느긋한 마음-」",
    "Moon 「Lunatic Impact」": "달 「루나틱 임팩트」",
    "Spirit Sign 「Dream Seal -Concentrate-」": "영부 「몽상봉인 -집중-」",
    "Wood Sign 「Sylphy Horn High Level」": "목부 「실피 혼 상급」",
    "Colorful Sign 「Dazzling Color Typhoon」": "채부 「눈부신 색채 태풍」",
    "Divine Treasure 「Salamander Shield」": "신보 「샐러맨더 실드」",
    "「Trinitarian Rhapsody」": "「트리니테리언 랩소디」",
    "Migrating Spirit 「Dream Seal -Marred-」": "천령 「몽상봉인 -훼손-」",
    "Earth Sign 「Lazy Trilithon High Level」": "토부 「레이지 트릴리톤 상급」",
    "Impossible Request 「Swallow's Cowrie Shell -Everlasting Life-」": "난제 「제비의 자패 -영원한 생명-」",
    "「First and Last Nameless Danmaku」": "「처음이자 마지막인 이름 없는 탄막」",
    "Boundary 「Duplex Danmaku Barrier」": "경계 「이중 탄막 결계」",
    "Fire Sign 「Agni Radiance」": "화부 「아그니 레이디언스」",
    "Impossible Request 「Bullet Branch of Hourai -Rainbow Danmaku-」": "난제 「봉래의 탄환 가지 -무지개 탄막-」",
    "Great Barrier 「%nameArray:ARG:na_LastName% Danmaku Barrier」": "대결계 「%nameArray:ARG:na_LastName% 탄막 결계」",
    "It's hardly possible to tell what's going on any more. If you look closely, the barriers turn the background inside-out too.": "이제는 무슨 일이 벌어지는지 알아보기조차 어렵다. 자세히 보면 결계가 배경마저 안팎으로 뒤집고 있다.",
    "Water Sign 「Bury In Lake」": "수부 「호수에 묻어라」",
    "Visually similar to \\"Princess Undine\\", Patchouli shoots thin lasers that close in on the player, as she produces circles of blue aimed bullets around her. When she finishes, she moves to the side while shooting lanes of large bullets around the player, then quickly returns to the middle.": "겉보기에는 \\"프린세스 운디네\\"와 비슷하다. 파츄리는 주변에 파란 조준탄의 원을 만들면서 플레이어를 조여 오는 가느다란 레이저를 쏜다. 마무리할 때는 옆으로 이동하며 플레이어 주변에 큰 탄환의 통로를 만들고, 곧바로 중앙으로 돌아온다.",
    "Divine Treasure 「Jeweled Branch of Hourai -Dreamlike Paradise-」": "신보 「봉래의 옥가지 -꿈같은 낙원-」",
    "It's hard for modern people to understand why a regular old \\"orb\\" (玉) is so coveted. This jewel outranks even gold and silver. Oh, I'm talking about shogi, by the way. Gold general, silver general, jeweled general.": "현대인에게는 평범한 \\"옥\\"(玉)이 왜 그토록 귀하게 여겨졌는지 이해하기 어렵다. 이 옥은 금과 은보다도 높은 격이다. 아, 장기 말 이야기다. 금장, 은장, 옥장 말이다.",
    "Divine Spirit 「Dream Seal -Blink-」": "신령 「몽상봉인 -점멸-」",
    "The world as %CALLNAME:ARG% sees it is quite different from the player's perspective. It feels like the player has been sealed in the %CALLNAME:ARG% Dimension.": "%CALLNAME:ARG%의 눈에 보이는 세계는 플레이어의 시점과 상당히 다르다. 마치 플레이어가 %CALLNAME:ARG% 차원에 봉인된 듯한 느낌이다.",
    "Wood Sign 「Green Storm」": "목부 「그린 스톰」",
    "Very similar to \\"Silphy Horn\\", but both sides of the screen shoot bullets towards the opposite side.": "\\"실피 혼\\"과 매우 비슷하지만, 화면 양쪽에서 반대편을 향해 탄환을 쏜다.",
    "End of Imperishable Night 「Matsuyoi」": "영야의 끝 「마츠요이」",
    "Kaguya's night starts here. The time on the clock advances at a tremendous speed. Ah, I forgot to mention this, but \\"time\\" and \\"the time on a clock\\" are two completely different things.": "카구야의 밤은 여기서 시작된다. 시계의 시간이 엄청난 속도로 흘러간다. 아, 말하는 걸 잊었는데 \\"시간\\"과 \\"시계에 표시되는 시각\\"은 완전히 다른 것이다.",
    "「Innate Dream」": "「선천적인 꿈」",
    "Earth Sign 「Trilithon Shake」": "토부 「트릴리톤 셰이크」",
    "End of Imperishable Night 「Half Past Midnight」": "영야의 끝 「자정 30분」",
    "Metal Sign 「Silver Dragon」": "금부 「실버 드래곤」",
    "End of Imperishable Night 「Half Past 2」": "영야의 끝 「2시 30분」",
    "Wood & Fire Sign 「Forest Blaze」": "목화부 「포레스트 블레이즈」",
    "End of Imperishable Night 「Half Past 4」": "영야의 끝 「4시 30분」",
    "Water & Wood Sign 「Water Elf」": "수목부 「워터 엘프」",
    "End of Imperishable Night 「Rising World」": "영야의 끝 「떠오르는 세계」",
    "Metal & Water Sign 「Mercury Poison」": "금수부 「수은 독」",
    "「Tree-Ocean of Hourai」": "「봉래의 수해」",
    "Earth & Metal Sign 「Emerald Megalith」": "토금부 「에메랄드 거석」",
}

TRLIB_QUOTED_MAP = {
    "Detect Presence": "기척 탐지",
    "Ask Who Needs Help": "도움이 필요한 사람 묻기",
    "Buy Ice Cream": "아이스크림 구매",
    "SDM Services": "홍마관 출장 서비스",
    "Eat at the Stall": "노점에서 식사",
    "Weather Manipulation": "날씨 조작",
    "Dowsing": "다우징",
    "Umbrella Repair": "우산 수리",
    "Buy/Mod Tools": "도구 구매/개조",
    "Buy Medicine": "약 구매",
    "Telegnosis": "천리안",
    "Danmaku": "탄막 승부",
    "Sell Herbal Medicine": "생약 판매",
    "Trade Fish": "물고기 교환",
    "Today's Stacking Theme": "오늘의 돌쌓기 주제",
    "Cleanse Misfortune": "액막이",
    "Trade Dragon Gems": "용주 거래",
    "Kikuri Blessing": "키쿠리의 축복",
    "Contact the Makai God": "마계의 신에게 연락",
    "Insurance Status": "보험 상태",
    "Fortune Telling": "점 보기",
    "Resurrect-O-Nomitron": "리저렉트-O-노미트론",
    "Dispose Body": "시신 처리",
    "[Grasslands]": "[초원]",
    "[Flower Garden]": "[꽃밭]",
    "[Forest]": "[숲]",
    "[Sandy Soil]": "[모래땅]",
    "[Waterfront]": "[물가]",
    "[Rocky]": "[바위 지대]",
    "[Indoors]": "[실내]",
    "[Moon]": "[달]",
    "Broom": "빗자루",
    "Purification Rod": "정화봉",
    "Wooden Sword": "목검",
    "Miracle Mallet": "기적의 망치",
    "Control Rod": "제어봉",
}

TRLIB_BARE_MAP = {
    "Join Navelgazing": "같이 생각에 잠기기",
    "Join Play": "같이 놀기",
    "Join Meal": "같이 식사하기",
    "Join Snack": "같이 간식 먹기",
    "Join Cleaning": "청소 돕기",
    "Join Exercising": "같이 운동하기",
    "Join Reading": "같이 독서하기",
    "Join Cooking": "요리 돕기",
    "Join Eating": "같이 먹기",
    "Join Jamming": "같이 합주하기",
    "Join Accompaniment": "반주하기",
    "Join Foraging": "채집 돕기",
    "Join Fishing": "같이 낚시하기",
    "Join Experimenting": "실험 돕기",
    "Join Relaxing": "같이 쉬기",
    "Join Drinking": "같이 술 마시기",
    "Join Shopping": "쇼핑 돕기",
    "Join Activity": "같이 자유행동하기",
    "See Eiki's Lecture": "에이키의 설교 지켜보기",
    "Join In A Prank": "장난에 끼기",
    "Check Pitfall": "함정 살펴보기",
    "Make Snowman": "눈사람 만들기",
    "Relax Under Kotatsu": "코타츠에서 쉬기",
    "Watch frog-freezing": "개구리 얼리기 구경",
    "Join Swimming": "같이 수영하기",
    "Watch Juggling": "저글링 구경",
    "Join Sunbathing": "같이 일광욕하기",
    "navelgazing": "생각에 잠기기",
    "playing": "놀기",
    "eating": "먹기",
    "snacking": "간식 먹기",
    "cleaning": "청소하기",
    "exercising": "운동하기",
    "reading": "독서하기",
    "cooking": "요리하기",
    "jamming": "합주하기",
    "accompanying": "반주하기",
    "foraging": "채집하기",
    "fishing": "낚시하기",
    "experimenting": "실험하기",
    "relaxing": "쉬기",
    "drinking": "술 마시기",
    "shopping": "쇼핑하기",
    "their activity": "상대의 활동",
    "relaxing under the kotatsu": "코타츠에서 쉬기",
    "lost in the lecture": "설교에 빠져 있기",
    "pranking": "장난치기",
    "stuck in the pitfall": "함정에 빠져 있기",
    "making a snowman": "눈사람 만들기",
    "swimming": "수영하기",
    "playing with the children": "아이들과 놀기",
    "sunbathing": "일광욕하기",
}

LIST_MAP = {
    "STA and ENE": "스태미나와 기력",
    "Technique": "기교",
    "Clothes and ability": "의복과 능력",
    "Exp and Gems": "경험과 보석",
    "Personal Information": "개인 정보",
    "Preferences": "선호",
    "Body Information": "신체 정보",
    "Falling Conditions": "함락 상태",
    "Scouter": "스카우터",
    "Religion": "종교",
    "Faction": "세력",
    "Settings": "설정",
    "Skill Acquisition": "스킬 습득",
    "Shooting": "사격",
    "Melee": "근접전",
    "Logging": "벌목",
    "Homo♀": "동성애♀",
    "Medical": "의료",
    "Fishing": "낚시",
    "Homo♂": "동성애♂",
    "Old HATE": "이전 증오",
    "Youjutsu": "요술",
    "Foraging": "채집",
    "Crafting": "제작",
    "USens": "U감각",
    "Farming": "농사",
    "Urethra": "요도",
    "Animals": "동물",
    "Foot": "발",
    "Semen": "정액",
    "Creampie": "질내사정",
    "A Creampie": "애널 사정",
    "U Creampie": "요도 사정",
    "Homo": "동성애",
    "Lesbian": "레즈비언",
    "Urine": "소변",
    "Peeing": "배뇨",
    "Scat": "대변",
    "Pooing": "배변",
    "Diaper": "기저귀",
    "Masturbation": "자위",
    "Alcohol": "알코올",
    "Drug": "약물",
    "Hypnosis": "최면",
    "Extra protein.\\n": "추가 단백질.\\n",
    "Alternative source of protein.\\n": "대체 단백질 공급원.\\n",
    "This is not even protein.\\n": "이건 단백질조차 아니다.\\n",
    "Progress towards next stage:\\n": "다음 단계까지 진행도:\\n",
    "Progress towards next stage: \\n": "다음 단계까지 진행도: \\n",
    "Progress towards next stage (addiction):\\n": "다음 단계까지 진행도(중독):\\n",
    "Progress towards next stage (withdrawal):\\n": "다음 단계까지 진행도(금단):\\n",
    "Progress towards next stage (strong mind):\\n": "다음 단계까지 진행도(강인한 정신):\\n",
    "Progress towards next stage (broken mind):\\n": "다음 단계까지 진행도(무너진 정신):\\n",
    "Progress towards next stage (continence):\\n": "다음 단계까지 진행도(배설 조절):\\n",
    "Progress towards next stage (incontinence):\\n": "다음 단계까지 진행도(실금):\\n",
    "Progress towards next stage (instability):\\n": "다음 단계까지 진행도(불안정):\\n",
    "Special:\\n": "특수 조건:\\n",
    "Gems:\\n": "보석:\\n",
    "Experience:\\n": "경험:\\n",
    "    Or\\n": "    또는\\n",
    "Makes it easier to negotiate for raw on dangerous days,\\n": "위험한 날에 피임 없이 하자고 설득하기 쉬워진다.\\n",
    "Makes all things piss related more appealing or something.\\n": "소변과 관련된 일 전반을 더 매력적으로 느끼게 한다.\\n",
    "Pee isn't enabled. Ignore this.": "소변 기능이 비활성화되어 있다. 이 항목은 무시해도 된다.",
    "Makes them feel better when they pee themselves.\\n": "실수로 소변을 지렸을 때 기분이 나아진다.\\n",
    "Makes all things scat related more appealing or something.\\n": "대변과 관련된 일 전반을 더 매력적으로 느끼게 한다.\\n",
    "Scat isn't enabled. Ignore this.": "대변 기능이 비활성화되어 있다. 이 항목은 무시해도 된다.",
    "Makes them feel better when they poo themselves.\\n": "실수로 대변을 지렸을 때 기분이 나아진다.\\n",
    "Sexual attraction towards diapers and having accidents inside them.\\n": "기저귀와 그 안에서 실수하는 행위에 성적으로 끌린다.\\n",
    "Diapers aren't enabled. Ignore this.": "기저귀 기능이 비활성화되어 있다. 이 항목은 무시해도 된다.",
    "Makes it easier to get them to masturbate.\\n": "자위를 하도록 권하기 쉬워진다.\\n",
    "A built-up tolerance to alcohol. The more severe this tolerance is, the more alcohol that must be drunk to get the same buzz.\\n": "알코올에 대한 내성이 쌓인다. 내성이 강할수록 같은 취기를 느끼기 위해 더 많은 술을 마셔야 한다.\\n",
    "A built-up tolerance to drugs. The more severe this tolerance is, the more drug it takes to get the same high.\\n": "약물에 대한 내성이 쌓인다. 내성이 강할수록 같은 효과를 느끼기 위해 더 많은 약물이 필요하다.\\n",
    "Makes hypnosis more effective against them.\\n": "이 캐릭터에게 최면이 더 잘 통하게 한다.\\n",
    "Increases with sexual pain, not implemented that much.": "성적 고통으로 증가한다. 아직 구현 범위는 크지 않다.",
    "Required for yearning and love. Good to have overall.\\n": "연모와 사랑에 필요하며 전반적으로 높을수록 좋다.\\n",
    "Helps with requests like \\"teach me\\" and access to certain zones.\\n": "\\"가르쳐 줘\\" 같은 부탁과 일부 구역 출입에 도움이 된다.\\n",
    "Reveals detailed information about Fishing and Hunting, and unlocks special drugs at the shop.\\n": "낚시와 사냥의 상세 정보를 보여 주고 상점의 특수 약물을 해금한다.\\n",
    "Helps with Mixing, Hunting, haggling and quiz game at the casino.\\n": "혼합, 사냥, 흥정과 카지노 퀴즈 게임에 도움이 된다.\\n",
    "Need to have sufficient level to understand Dragon God statue's signs, and see hints when using the Sake Bug.\\n": "용신상 표식을 이해하고 사케 벌레 사용 시 힌트를 보려면 충분한 수준이 필요하다.\\n",
    "Your character must be smarter than the owner's diary to decipher it.\\n": "주인의 일기를 해독하려면 캐릭터의 지식 수준이 충분히 높아야 한다.\\n",
    "Smart characters will look down on you if you're too dumb when speaking with them.\\n": "지적인 캐릭터는 대화 상대가 너무 무지하면 낮춰 볼 수 있다.\\n",
    "Education": "교양",
    "Penis and clitoris sensitivity.\\n": "음경과 음핵의 감도.\\n",
    "Increases caress and such.\\n": "애무 등의 효과를 높인다.\\n",
    "Increased with Handjob Exp * (10 + Technique/2 + Dexterous Fingers*2 + Fast Learner) /10.\\n": "수음 경험 × (10 + 기교/2 + 능숙한 손가락×2 + 빠른 학습자) / 10으로 증가한다.\\n",
    "Makes pain fun.\\n": "고통을 쾌감으로 느끼게 한다.\\n",
    "Increases with multiple simultaneous and devastating climaxes while conscious.": "의식이 있는 상태에서 강렬한 절정을 여러 번 동시에 겪으면 증가한다.",
    "Helps getting more favorable responses from interactions.\\n": "상호작용에서 더 호의적인 반응을 얻는 데 도움이 된다.\\n",
    "Needs when you want to urge girls do things you want from them.\\n": "상대에게 원하는 행동을 권유할 때 필요하다.\\n",
    "Reduces bad param gain in general. Contributes to Favor gain.\\n": "전반적인 부정적 파라미터 증가를 줄이고 호감도 상승에 기여한다.\\n",
    "Useful in all manners of social interactions, and checked for persuasion attempts.\\n": "모든 종류의 사회적 상호작용에 유용하며 설득 시 판정에 사용된다.\\n",
    "Raises the upper limit of discussion topics, preventing awkward moods when talking too much.\\n": "대화 주제의 상한을 높여 너무 오래 이야기할 때 어색해지는 것을 막는다.\\n",
    "Improves haggling skills when opening a street stall.\\n": "노점을 열었을 때 흥정 능력을 높인다.\\n",
    "Vaginal sensitivity.\\n": "질 감도.\\n",
    "Hole quality.\\n": "질 상태.\\n",
    "Increased with V Sex Exp, V Exp, and V Stretch Exp, Technique and Fast learner.\\n": "V 성교 경험, V 경험, V 확장 경험, 기교와 빠른 학습자로 증가한다.\\n",
    "Makes inflicting pain fun.\\n": "상대에게 고통을 주는 것을 즐기게 한다.\\n",
    "Increases with high Submission and Loyalty.": "복종과 충성심이 높을수록 증가한다.",
    "Sexual attraction.\\n": "성적 욕구.\\n",
    "Helps with general spell-card ruled Danmaku ability.\\n": "스펠카드 규칙의 탄막 전투 능력 전반에 도움을 준다.\\n",
    "Does NOT affect lethal combat unless the character uses danmaku as their weapon of choice.\\n": "캐릭터가 탄막을 주 무기로 사용하지 않는 한 살상 전투에는 영향을 주지 않는다.\\n",
    "Anal sensitivity.\\n": "애널 감도.\\n",
    "Anal hole quality.\\n": "애널 상태.\\n",
    "Increased with A Sex Exp, A Exp, and A Stretch Exp, Technique and Fast learner.\\n": "A 성교 경험, A 경험, A 확장 경험, 기교와 빠른 학습자로 증가한다.\\n",
    "Really gay.\\n": "동성에게 매우 강하게 끌린다.\\n",
    "Decrease with good dates, sacrificing 10 panties, giving box of cakes (only at Lv1).": "좋은 데이트, 팬티 10개 희생, 케이크 상자 선물(Lv1에서만)로 감소한다.",
    "Overall technique.\\n": "전반적인 기교.\\n",
    "Affects a character's accuracy with ranged weapons.\\n": "캐릭터의 원거리 무기 명중률에 영향을 준다.\\n",
    "Note that shooting accuracy for the character is calculated per tile, meaning that while a trivial increase (like 1% or so) in shooting accuracy may not matter up close, it can make a huge difference in long distances.\\n": "사격 명중률은 타일마다 계산된다. 따라서 1% 정도의 작은 상승은 근거리에서는 별 차이가 없어도 장거리에서는 큰 차이를 만들 수 있다.\\n",
    "Helps with beating people up and hunting.\\n": "근접 전투와 사냥에 도움이 된다.\\n",
    "Indicates close quarters power level and can prevent push down attempts from other characters.\\n": "근접전 전투력을 나타내며 다른 캐릭터의 밀쳐 넘어뜨리기 시도를 막는 데 영향을 준다.\\n",
    "Checked for intimidation attempts.\\n": "위협 시 판정에 사용된다.\\n",
    "Clean faster, better.\\n": "더 빠르고 깨끗하게 청소한다.\\n",
    "Breast sensitivity.\\n": "가슴 감도.\\n",
    "Better Paizuri and such.\\n": "파이즈리 등의 효과가 좋아진다.\\n",
    "Increased with Paizuri Exp, B Exp, Lactation Exp, Technique, Breast Size, and Fast learner.\\n": "파이즈리 경험, B 경험, 수유 경험, 기교, 가슴 크기와 빠른 학습자로 증가한다.\\n",
    "Servicing of all sorts. General desire to, and pleasure derived from pleasing someone, mostly sexually.\\n": "여러 종류의 봉사 능력. 주로 성적인 방식으로 상대를 기쁘게 하려는 욕구와 그로부터 얻는 쾌감을 나타낸다.\\n",
    "Cook better food.\\n": "더 좋은 음식을 만든다.\\n",
    "Mouth sensitivity.\\n": "입 감도.\\n",
    "Better Fellatio and such.\\n": "펠라치오 등의 효과가 좋아진다.\\n",
    "Increased with Oral Sex Exp, Technique, Skilled Tongue, Fast learner.\\n": "구강 성교 경험, 기교, 능숙한 혀와 빠른 학습자로 증가한다.\\n",
    "Exposure, shameplay stuff, exhibitionism.\\n": "노출, 수치 플레이, 노출증과 관련된다.\\n",
    "Play better music.\\n": "더 좋은 음악을 연주한다.\\n",
    "Increased with Musical Performance, Singing, or Dancing, whichever is the highest.\\n": "악기 연주, 노래, 춤 가운데 가장 높은 경험에 따라 증가한다.\\n",
    "Urethra sensitivity.\\n": "요도 감도.\\n",
    "Increases Thrusting and such.\\n": "허리 움직임 등의 효과를 높인다.\\n",
    "Increased with V Sex Exp, A Sex Exp, Insertion Exp, Technique, Fast learner.\\n": "V 성교 경험, A 성교 경험, 삽입 경험, 기교와 빠른 학습자로 증가한다.\\n",
    "Increases with kisses, B commands, and accidents (Submission, Shame, and Dirty gems).": "키스, B 계열 행동, 실수(복종·수치·불결 보석)로 증가한다.",
    "Fell trees and plant better or something.\\n": "나무를 더 잘 베고 식물을 더 잘 다룬다.\\n",
    "How good you stop orgasms from going through.\\n": "절정을 얼마나 잘 참는지를 나타낸다.\\n",
    "Better Urethral Penetration.\\n": "요도 삽입 능력을 높인다.\\n",
    "Higher level allows bigger things to be inserted but gives a permamant reduction in urinary continence.\\n": "레벨이 높을수록 더 큰 물체를 삽입할 수 있지만 배뇨 조절 능력이 영구적으로 감소한다.\\n",
    "Increased with U Sex Exp, U Exp, and U Stretch Exp, Technique and Fast learner.\\n": "U 성교 경험, U 경험, U 확장 경험, 기교와 빠른 학습자로 증가한다.\\n",
    "How good you stop pee from leaking.\\n": "소변이 새는 것을 얼마나 잘 참는지 나타낸다.\\n",
    "Increases with more severe and hostile actions during sex or rape.\\n": "성행위나 강제적인 성행위 중 더 거칠고 적대적인 행동으로 증가한다.\\n",
    "Makes it harder for Hate and Trauma Marks to accumulate.\\n": "증오와 트라우마 각인이 쌓이기 어렵게 한다.\\n",
    "Source: Submission↑ Loyalty↑ Fear↑ Hostility↓ Deviation↓ Depression↓": "요인: 복종↑ 충성↑ 공포↑ 적대↓ 일탈↓ 우울↓",
    "Increases with more severe and hostile actions. Unlike force marks, which are good, trauma is bad.\\n": "더 심하고 적대적인 행동으로 증가한다. 강제 각인과 달리 트라우마는 부정적인 상태다.\\n",
    "Trauma leads to mental instability and if taken to the extreme, could result in your Touhou becoming a vegetable.\\n": "트라우마는 정신 불안정을 일으키며 극단적으로 심해지면 캐릭터가 정상적인 활동을 하지 못하게 될 수 있다.\\n",
    "Fish better or something.\\n": "낚시를 더 잘한다.\\n",
    "How good you stop shit from destroying you.\\n": "배변을 얼마나 잘 참는지 나타낸다.\\n",
    "Find better things when foraging or something.\\n": "채집할 때 더 좋은 물건을 찾는다.\\n",
    "Increases the amount of plots you have for gardening.\\n": "농사에 사용할 수 있는 밭의 수를 늘린다.\\n",
    "The crafting skill affects the creation of many of the items under the smith, tailor and craft work types. It does so in two ways; crafting quality and minimum crafting levels.\\n": "제작 기술은 대장간, 재봉, 제작 작업으로 만드는 다양한 아이템에 영향을 준다. 제작 품질과 최소 제작 레벨 두 가지에 관여한다.\\n",
    "A character's Crafting skill is a driving factor in the Quality of produced Clothing, Armor, Weapons, and Drugs.\\n": "캐릭터의 제작 기술은 생산한 의복, 방어구, 무기, 약물의 품질을 결정하는 주요 요소다.\\n",
    "Become more dexterious with feet in sexual techniques.\\n": "성적 기교에서 발을 더 능숙하게 사용한다.\\n",
}

SIMPLE_QUOTED_RHS_RE = re.compile(r'^(?P<prefix>\s*(?:RETURNF|LOCALS(?::\d+)?\s*(?:\'=|\+=))\s*@?)"(?P<value>(?:\\.|[^"\\])*)"(?P<suffix>\s*)$')
MAKE_RE = re.compile(r'(?P<prefix>CALLF\s+MAKE_STR\(V_NAME,\s*@?)"(?P<value>(?:\\.|[^"\\])*)"')
QUOTE_RE = re.compile(r'"((?:\\.|[^"\\])*)"')


def read_text(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    bom = raw.startswith(BOM)
    return (raw.decode("utf-8-sig") if bom else raw.decode("utf-8"), bom)


def write_text(path: Path, text: str, bom: bool) -> None:
    data = text.encode("utf-8")
    path.write_bytes((BOM if bom else b"") + data)


def token_signature(value: str) -> list[str]:
    return TOKEN_RE.findall(value)


def checked_translation(src: str, dst: str) -> str:
    if token_signature(src) != token_signature(dst):
        raise AssertionError((src, dst, token_signature(src), token_signature(dst)))
    return dst


def apply_simple_rhs(root: Path, rel: str, mapping: dict[str, str]) -> int:
    path = root / rel
    text, bom = read_text(path)
    out = []
    count = 0
    for line in text.splitlines(keepends=True):
        nl = "\n" if line.endswith("\n") else ""
        body = line[:-1] if nl else line
        m = SIMPLE_QUOTED_RHS_RE.match(body)
        if m and m.group("value") in mapping:
            src = m.group("value")
            dst = checked_translation(src, mapping[src])
            body = f'{m.group("prefix")}"{dst}"{m.group("suffix")}'
            count += 1
        out.append(body + nl)
    new = "".join(out)
    if count:
        write_text(path, new, bom)
    return count


def apply_spell(root: Path) -> int:
    path = root / SPELL
    text, bom = read_text(path)
    out = []
    count = 0
    field = ""
    case_re = re.compile(r'^\s*CASE\s+"((?:\\.|[^"\\])*)"')
    for line in text.splitlines(keepends=True):
        cm = case_re.match(line)
        if cm:
            field = cm.group(1)
            out.append(line)
            continue
        if field not in {"名前", "Name", "FullName", "ShortName", "描写", "Description", "Inspect"} or line.lstrip().startswith(";"):
            out.append(line)
            continue
        m = MAKE_RE.search(line)
        if m and m.group("value") in SPELL_MAP:
            src = m.group("value")
            dst = checked_translation(src, SPELL_MAP[src])
            line = line[:m.start("value")] + dst + line[m.end("value"):]
            count += 1
        out.append(line)
    new = "".join(out)
    if count:
        write_text(path, new, bom)
    return count


def apply_trlib(root: Path) -> int:
    path = root / TRLIB
    text, bom = read_text(path)
    lines = text.splitlines(keepends=True)
    out = []
    count = 0
    fn = ""
    fn_re = re.compile(r'^@([A-Za-z0-9_]+)(?:\(|$)')
    allowed_quoted = {"UNIQUE_COM_TR", "NAME_FIELD_TYPE_TR", "SUIKA_WEAPON_TR"}
    allowed_bare = {"JOIN_IN_TR", "JOIN_IN_SINGLE_TR"}
    bare_re = re.compile(r'^(?P<prefix>\s*LOCALS\s*=\s*)(?P<value>[^;\r\n]+?)(?P<suffix>\s*)$')
    for line in lines:
        fm = fn_re.match(line)
        if fm:
            fn = fm.group(1)
        if line.lstrip().startswith(";"):
            out.append(line)
            continue
        if fn in allowed_quoted:
            def repl(m: re.Match[str]) -> str:
                nonlocal count
                src = m.group(1)
                if src not in TRLIB_QUOTED_MAP:
                    return m.group(0)
                dst = checked_translation(src, TRLIB_QUOTED_MAP[src])
                count += 1
                return f'"{dst}"'
            # Inputs are CASE keys: never touch them. Only return/output lines.
            if re.match(r'^\s*(?:RETURNF|LOCALS\s*(?:\'=|\+=))', line):
                line = QUOTE_RE.sub(repl, line)
        if fn in allowed_bare:
            nl = "\n" if line.endswith("\n") else ""
            body = line[:-1] if nl else line
            bm = bare_re.match(body)
            if bm:
                src = bm.group("value").strip()
                if src in TRLIB_BARE_MAP:
                    body = bm.group("prefix") + TRLIB_BARE_MAP[src] + bm.group("suffix")
                    line = body + nl
                    count += 1
        out.append(line)
    new = "".join(out)
    if count:
        write_text(path, new, bom)
    return count


def replace_list_literal(value: str) -> tuple[str, bool]:
    # Preserve intentional alignment padding in display arrays.
    left = len(value) - len(value.lstrip(" "))
    right = len(value) - len(value.rstrip(" "))
    core_end = len(value) - right if right else len(value)
    core = value[left:core_end]
    if core not in LIST_MAP:
        return value, False
    dst = checked_translation(core, LIST_MAP[core])
    return " " * left + dst + " " * right, True


def apply_list(root: Path) -> int:
    path = root / LIST
    text, bom = read_text(path)
    out = []
    count = 0
    simple_locals_re = re.compile(r'^(?P<prefix>\s*LOCALS(?::\d+)?\s*(?:\'=|\+=)\s*)"(?P<value>(?:\\.|[^"\\])*)"(?P<suffix>\s*)$')
    for line in text.splitlines(keepends=True):
        nl = "\n" if line.endswith("\n") else ""
        body = line[:-1] if nl else line
        stripped = body.lstrip()
        if stripped.startswith(";"):
            out.append(line)
            continue
        # Known display-name arrays only; do not touch internal schema arrays.
        if stripped.startswith("#DIMS CONST DISP_NAME =") or stripped.startswith("#DIMS CONST ABL_NAME ="):
            def arr_repl(m: re.Match[str]) -> str:
                nonlocal count
                new_value, changed = replace_list_literal(m.group(1))
                if changed:
                    count += 1
                    return f'"{new_value}"'
                return m.group(0)
            body = QUOTE_RE.sub(arr_repl, body)
        else:
            lm = simple_locals_re.match(body)
            if lm:
                src = lm.group("value")
                if src in LIST_MAP:
                    dst = checked_translation(src, LIST_MAP[src])
                    body = f'{lm.group("prefix")}"{dst}"{lm.group("suffix")}'
                    count += 1
            # Two standalone menu-button lines use a simple quoted visible title.
            if "Skill Acquisition" in body and re.match(r'^\s*PRINT', body):
                old = '"Skill Acquisition"'
                if old in body:
                    body = body.replace(old, '"스킬 습득"')
                    count += 1
        out.append(body + nl)
    new = "".join(out)
    if count:
        write_text(path, new, bom)
    return count


def main() -> None:
    root = Path(".")
    counts = {
        "talent": apply_simple_rhs(root, TALENT, TALENT_MAP),
        "spell": apply_spell(root),
        "trlib": apply_trlib(root),
        "list": apply_list(root),
    }
    total = sum(counts.values())
    print("PASS64_COUNTS", counts)
    print("PASS64_VISIBLE_REPLACEMENTS", total)
    if total < 600:
        raise SystemExit(f"pass64 batch unexpectedly small: {total}")


if __name__ == "__main__":
    main()
