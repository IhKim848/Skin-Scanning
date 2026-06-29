import json
import os

def merge_datasets():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    supply_json_path = os.path.join(data_dir, 'medical_supply.json')
    output_json_path = os.path.join(data_dir, 'integrated_db.json')

    if not os.path.exists(supply_json_path):
        print(f"조달 데이터 JSON 파일이 없어 경로 확인이 필요함.: {supply_json_path}")
        return

    with open(supply_json_path, 'r', encoding='utf-8') as f:
        dapa_data = json.load(f)

    skin_medications = dapa_data.get("피부/외용제", [])
    first_aid_supplies = dapa_data.get("구급/응급용품", [])

    integrated_db = {
        "진균_감염": {
            "질환_키워드": ["무좀", "백선", "어루러기", "심부성 사상균 질환"],
            "병무청_가이드": {
                "분류": "피부과 - 백선 및 심부성 사상균 질환",
                "판정기준": "국소성인 경우 1급~2급. 난치성이거나 광범위한 경우 상태에 따라 3급~4급 판정.",
                "필요서류": "최근 6개월 이내의 의무기록지, 피부과 전문의의 병무용 진단서"
            },
            "방위사업청_조달내역": skin_medications
        },
        "세균_감염": {
            "질환_키워드": ["모낭염", "농가진", "종기", "화농성 한선염"],
            "병무청_가이드": {
                "분류": "피부과 - 화농성 한선염 및 기타 세균 감염",
                "판정기준": "경미한 경우 1급~3급. 중증도로 일상생활에 큰 지장을 초래할 정도로 심한 경우 4급(보충역).",
                "필요서류": "입원/외래 치료 기록지, 병무용 진단서"
            },
            "방위사업청_조달내역": skin_medications
        },
        "피부염_습진": {
            "질환_키워드": ["아토피", "접촉성 피부염", "건선"],
            "병무청_가이드": {
                "분류": "피부과 - 아토피성 피부염",
                "판정기준": "경도(체표면적 15% 미만) 3급, 중등도(최근 1년 내 6개월 이상 치료, 최근 3개월 치료 포함) 4급, 고도(체표면적 50% 이상, 2년 내 1년 이상 면역조절제 치료 포함) 5급.",
                "필요서류": "최근 2년간 의무기록사본(투약기록 포함), 병무용 진단서"
            },
            "방위사업청_조달내역": skin_medications
        },
        "외상_출혈": { # 구급용품과 매핑할 수 있는 보너스 카테고리
            "질환_키워드": ["찰과상", "열상", "화상"],
            "병무청_가이드": {
                "분류": "외과 - 피부 및 연부조직 손상",
                "판정기준": "단순 창상의 경우 1급. 기능 장애를 동반하는 광범위한 반흔의 경우 3급~4급.",
                "필요서류": "외과 진단서, 수술 기록지 (해당 시)"
            },
            "방위사업청_조달내역": first_aid_supplies
        }
    }

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(integrated_db, f, ensure_ascii=False, indent=4)

    print(f"병합 완료!")
    print(f"저장 위치: {output_json_path}")

if __name__ == "__main__":
    merge_datasets()