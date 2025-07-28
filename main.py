import random
user = input("가위 바위 보 중 하나를 선택하세요: ")
computer = random.choice(["가위", "바위", "보"])

# []는 리스트, 서로 다른 값을 저장할 수 있는 자료형
if user == computer:
    print("컴퓨터도", computer,"를 냈습니다. 비겼습니다!")
elif (user == "가위" and computer == "보") or \
     (user == "바위" and computer == "가위") or \
     (user == "보" and computer == "바위"):
    print("컴퓨터는", computer, "를 냈습니다. 당신이 이겼습니다!")
else:
    print("컴퓨터는", computer, "를 냈습니다. 당신이 졌습니다!")
    