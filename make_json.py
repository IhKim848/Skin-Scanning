import pandas as pd
import json
import os

def create_real_supply_db():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    data_dir = os.path.join(current_dir, 'data')
    file_path = os.path.join(data_dir, '의약품_조달계약_전처리데이터.xlsx')
    json_path = os.path.join(data_dir, 'medical_supply.json')
    
    if not os.path.join(file_path):
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return

    df = pd.read_excel(file_path)

    
    if '계약체결일자' in df.columns:
        df['계약체결일자'] = df['계약체결일자'].astype(str)
    
    
    df = df.fillna("")

    
    supply_db = {}
    
    for category, group in df.groupby('의료물자_분류'):
        supply_db[category] = group.to_dict(orient='records')

    json_path = 'data/medical_supply.json'
    
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(supply_db, f, ensure_ascii=False, indent=4)

    print(f"JSON 변환 완료! (총 {len(df)}건)")
    print(f"저장 위치: {json_path}")

if __name__ == "__main__":
    create_real_supply_db()