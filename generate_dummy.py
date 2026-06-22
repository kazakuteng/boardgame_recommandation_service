import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key 설정 (환경 변수 또는 직접 입력)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def generate_dummy_reviews():
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY가 설정되지 않아 로컬에 작성된 dummy_reviews.json을 사용/참고하십시오.")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    
    # 3.5 혹은 flash 모델 선택
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    보드게임 추천 시스템을 위한 유저 리뷰 및 플레이 기록 더미 데이터를 JSON 형식으로 10개 생성해줘.
    
    - 포함해야 할 필드:
      "game_id": (정수, 224517(Brass: Birmingham), 342942(Ark Nova), 161936(Pandemic Legacy), 174430(Gloomhaven) 중 하나)
      "title": (문자열, 게임 이름)
      "user_id": (문자열, 예: "user101")
      "player_count": (정수, 각 게임의 실제 허용 인원 수 범위 내에서 모순이 없도록 작성)
      "play_time_minutes": (정수, 소요 시간, 각 게임의 평균 플레이 시간과 유사하게)
      "rating": (실수, 1.0 ~ 10.0 사이의 만족도)
      "user_preference": (문자열, 유저 성향 예: "Strategy", "Family", "Party", "RPG")
      "review_text": (문자열, 게임에 대한 구체적이고 현실적인 한글 리뷰)
      "is_recommended": (boolean, 추천 여부)
      
    응답은 순수하게 JSON 배열 형식만 출력해줘. 마크다운 백틱(```json ... ```) 없이 출력해줘.
    결측치나 타입 오류가 없어야 하며, 2인 전용 게임에 5명이 플레이했다는 식의 모순이 없어야 해.
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
            
        data = json.loads(content)
        
        with open('dummy_reviews_gen.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("dummy_reviews_gen.json 생성 완료!")
    except Exception as e:
        print(f"데이터 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    generate_dummy_reviews()
