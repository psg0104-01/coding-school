#1.랜덤한 숫자르 입력
#2. 입력한 숫자를 입력
#3. 입력한 숫자가 랜덤 숫자보다 크면 down출력
#4. 입력한 숫자가 랜덤 숫자보다 작으면 up출력
#5. 입력한 숫자가 랜덤 숫자와 같으면 정답 출력후 break
#   5번 시도후에도 정답을 맞추지 못하면 "정답은 {랜덤 숫자}"라고 출력

import random
random_number = random.randint(1, 100)  # 1부터 100 사이의 랜덤 숫자 생성

print("1부터 100 사이의 숫자를 맞춰보세요!")

for i in range(5):  # 5번의 기회
    user_input = int(input(f"{i + 1}번째 시도: "))  # 사용자 입력 받기

    if user_input == random_number:
        print("정답입니다! 축하합니다!")
        break
    elif i < 4:  # 마지막 시도가 아니면 UP/DOWN 출력
        if user_input < random_number:
            print("UP! 더 큰 숫자를 입력하세요.")
        else:
            print("DOWN! 더 작은 숫자를 입력하세요.")
else:
    # 5번 모두 틀렸을 때
    print("실패하셨습니다.")
    print("정답은",random_number,"입니다.")

