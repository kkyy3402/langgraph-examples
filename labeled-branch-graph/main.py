from workflow import app

if __name__ == "__main__":
    print("🚀 모델 학습 워크플로우를 시작합니다.")

    final_state = app.invoke({})

    print("\n✅ 워크플로우 종료. 최종 상태:")
    print(final_state)
