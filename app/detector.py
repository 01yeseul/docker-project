import re

def detect_personal_info(text: str) -> list:
    results = []

    # 1. 이메일
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, text)
    results += [{"type": "이메일", "value": e} for e in emails]

    # 2. 전화번호
    phone_pattern = r"01[0-9]-\d{3,4}-\d{4}|0\d{1,2}-\d{3,4}-\d{4}"
    phones = re.findall(phone_pattern, text)
    results += [{"type": "전화번호", "value": p} for p in phones]

    # 3. 주민등록번호
    rrn_pattern = r"\d{6}-\d{7}"
    rrns = re.findall(rrn_pattern, text)
    results += [{"type": "주민등록번호", "value": r} for r in rrns]

    # 4. 이름 (2~3글자, 블랙리스트 제외)
    name_pattern = r"\b[가-힣]{2,3}\b"
    blacklist = {"이메일", "이름은", "정보", "주소", "성명", "전화번호","문서","한쇼", "서울","이름","이랑", "이고","정기"}

    for name in re.findall(name_pattern, text):
        if name in blacklist or "○" in name:
            continue
        if is_probable_korean_name(name):
            results.append({"type": "이름", "value": name})

    # 5. 도로명 주소 (무등로 123, 상무대로 77)
    for match in re.finditer(r"[가-힣0-9\s]+(로|길|대로)\s?\d+", text):
        results.append({"type": "도로명 주소", "value": match.group()})

    return results


import re

def mask_personal_info(text: str) -> str:
    # 이메일
    text = re.sub(
        r"([a-zA-Z0-9._%+-])[a-zA-Z0-9._%+-]*(@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
        r"\1****\2",
        text
    )
    # 전화번호
    text = re.sub(
        r"(01[0-9]|0\d{1,2})-(\d{3,4})-(\d{4})",
        r"\1-****-\3",
        text
    )
    # 주민등록번호
    text = re.sub(
        r"(\d{6})-(\d{7})",
        r"\1-*******",
        text
    )
    # 도로명 주소
    text = re.sub(r"[가-힣0-9\s]+(로|길|대로)(\s?\d+)", r"****\2", text)

    # **이름 마스킹** (성씨 + 한글 1~2글자, 조사 등도 커버)
   

    common_surnames = '김국박최정강조윤장임한신서문홍이'
    blacklist = {"이메일", "이름", "정보", "주소", "성명", "전화번호", "문서", "이름은", "서울", "광주", "한쇼", "이고", "이랑","정기"}
    name_pattern = (
    r"(?<![가-힣])"
    r"([" + common_surnames + r"][가-힣]{1,2})"
    r"(?=(입니다|이고|은|는|이|가|의|를|을|과|와|도|만|로|으로|에서|부터|까지|에게|한테|조차|밖에|마다|께서|든지|든가|이야|야|가요|인가요|인가|이다|였|다|요|!|\.|,| |\n|$))"
)

    def replace_name(match):
        name = match.group(1)
        if name in blacklist or "○" in name:
            return name
        if name[0] in common_surnames and all('가' <= ch <= '힣' for ch in name):
            if len(name) == 3:
                return name[0] + "○○"
            elif len(name) == 2:
                return name[0] + "○"
        return name

    text = re.sub(name_pattern, replace_name, text)
    return text

def is_probable_korean_name(word: str) -> bool:
    """
    2~3글자 고유 한글 이름 여부 판단
    """
    common_surnames = {'김', '국', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '신', '서', '문', '홍','이'}
    return (
        len(word) in {2, 3}
        and word[0] in common_surnames
        and all('가' <= ch <= '힣' for ch in word)
    )

