from pandas_reader.model import Model, Field


def change_location_to_sido_code(location):
    if location == "서울":
        return "11"
    if location == "부산":
        return "21"
    if location == "대구":
        return "22"
    if location == "인천":
        return "23"
    if location == "광주":
        return "24"
    if location == "대전":
        return "25"
    if location == "울산":
        return "26"
    if location == "세종":
        return "29"
    if location == "경기":
        return "31"
    if location == "강원":
        return "32"
    if location == "충북":
        return "33"
    if location == "충남":
        return "34"
    if location == "전북":
        return "35"
    if location == "전남":
        return "36"
    if location == "경북":
        return "37"
    if location == "경남":
        return "38"
    if location == "제주":
        return "39"


def change_status(status: str):
    if status == "기존" or status == "변경[신설]" or status == "신설":
        return "ACTIVE"
    return "DELETE"


class Major(Model):
    id = Field(index=True, auto_increment=True)
    univ = Field("학교명")
    sido_code = Field("지역", change=change_location_to_sido_code)
    name = Field("학부_과(전공)명")
    department = Field("단과대학명")
    std_lclsf_name = Field("표준분류대계열")
    std_mclsf_name = Field("표준분류중계열")
    std_sclsf_name = Field("표준분류소계열")
    _specification = Field("대학구분", filter=lambda x: x == "대학")
    investigation_year = Field("조사년도", change=lambda x: str(x))
    status = Field("학과상태", change=change_status)
