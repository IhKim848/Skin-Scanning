import json
import os

class MedicalDataLinker:
    def __init__(self):
       
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '../data/integrated_db.json')
        
        with open(db_path, 'r', encoding='utf-8') as f:
            self.db = json.load(f)

    def get_info_by_diagnosis(self, ai_prediction_key):
        result = self.db.get(ai_prediction_key)
        
        if result:
            disease_name = ai_prediction_key.replace("_", " ")
            mma_data = result.get("병무청_가이드")
            dapa_data = result.get("방위사업청_조달내역", [])
            return disease_name, mma_data, dapa_data
        else:
            return "알 수 없는 질환", None, None
