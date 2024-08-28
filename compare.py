import json
import re
from deepdiff import DeepDiff

# 주석 제거 함수 정의
def remove_comments(json_str):
    json_str = re.sub(r'^\s*//.*$', '', json_str, flags=re.MULTILINE)
    json_str = re.sub(r'(?<!:)//.*$', '', json_str, flags=re.MULTILINE)
    json_str = re.sub(r'\n\s*\n', '\n', json_str)
    return json_str

# 쉼표 정리 함수 정의
def fix_trailing_commas(json_str):
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
    return json_str

# 파일 읽고 주석 및 쉼표 제거
def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        content_no_comments = remove_comments(content)
        content_fixed = fix_trailing_commas(content_no_comments)
        try:
            data = json.loads(content_fixed)
            print(f"JSON 데이터 로드 성공: {filename}")
            return data
        except json.JSONDecodeError as e:
            print(f"JSON 디코딩 오류: {e}")
            return None

# 기존 JSON 파일과 최신 JSON 파일 로드
old_data = load_json_file('old_data.json')
new_data = load_json_file('new_data.json')

if old_data is None or new_data is None:
    print("JSON 파일 로드에 실패했습니다. 파일의 형식을 확인하십시오.")
else:
    # 두 JSON 파일 비교 (키의 추가/제거만 검토)
    diff = DeepDiff(old_data, new_data, ignore_order=True)

    # 정확한 차이점 체크
    added = diff.get('dictionary_item_added', None)
    removed = diff.get('dictionary_item_removed', None)

    if not added and not removed:
        print("두 파일 간에 키의 차이점이 없습니다.")
    else:
        print("비교 결과:")
        if added:
            print("\n추가된 키:")
            for item in added:
                clean_key = item.replace("root['", "").rstrip("']")
                # 추가된 키의 값 가져오기
                key_path = item.replace("root", "").strip("[]").replace("'", "").split("][")
                added_value = new_data
                for key in key_path:
                    added_value = added_value.get(key, {})
                print(f"  - {clean_key} : {added_value}")

        if removed:
            print("\n제거된 키:")
            for item in removed:
                clean_key = item.replace("root['", "").rstrip("']")
                # 제거된 키의 값 가져오기
                key_path = item.replace("root", "").strip("[]").replace("'", "").split("][")
                removed_value = old_data
                for key in key_path:
                    removed_value = removed_value.get(key, {})
                print(f"  - {clean_key} : {removed_value}")
