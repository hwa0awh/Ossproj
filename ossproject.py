# 과목 정보를 저장할 클래스
def load_subjects_from_file(filename):
    subject_sections = []  # 클래스 객체 저장용 리스트
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            # 모든 줄을 split 해서 리스트에 저장
            subject_data = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) not in [6, 9]:
                # 과목명, 분반번호, 과목코드, 요일1, 시작1, 끝1 (6개), 요일2, 시작2, 끝2 포함 시 총 9개
                    print(f"[무시됨] 잘못된 형식: {line.strip()}")
                    continue
                subject_data.append(parts)

                subject = parts[0]
                section_id = parts[1]
                code = parts[2]

                # 시간표 정보 저장
                time_slots = []
                # 첫 번째 요일 시간 정보 저장
                time_slots.append((parts[3], float(parts[4]), float(parts[5])))
                # 두 번째 요일 정보가 있다면 추가 저장
                if len(parts) == 9:
                    time_slots.append((parts[6], float(parts[7]), float(parts[8])))

                # 하나의 분반 정보를 객체로 만들어 리스트에 저장
                section = Subjectsection(subject, section_id, code, time_slots)
                subject_sections.append(section)

            # 과목명 기준 정렬
            subject_sections.sort(key=lambda sec: sec.subject)

            # 정렬된 결과 출력
            print("📂 과목명 순 정렬 결과:")
            for section in subject_sections:
                print(section)
                print("-------------")

        return subject_sections # main() 함수나 다른 함수에서도 사용하려면, return으로 넘겨줘야 함
        

    except FileNotFoundError:
        print(f"[오류] 파일 '{filename}'을 찾을 수 없습니다.")
        return []

# 과목 한 개 분반 정보를 나타내는 클래스
class Subjectsection :
    def __init__(self, subject, section_id, code, time_slots) :
        self.subject = subject         # 과목명
        self.section_id = section_id   # 분반번호
        self.code = code               # 과목코드
        self.time_slots = time_slots   # 수업시간
    
    def __str__(self):
        result = f"{self.subject} 분반 {self.section_id} 코드 {self.code}\n"
        for day, start, end in self.time_slots:
            result += f"  - {day} {start} ~ {end}\n"
        return result    

# 과목명을 기준으로 분반 리스트를 묶는 함수
def group_sections_by_subject(sections):
    grouped = {}  # 딕셔너리 구조: { 과목명: [분반1, 분반2, ...] }

    for sec in sections:
        subject = sec.subject

        # 키가 없으면 빈 리스트 만들어서 추가
        if subject not in grouped:
            grouped[subject] = []

        grouped[subject].append(sec)

    return grouped

# 각 과목에서 한 분반만 선택해 조합을 만드는 함수 (백트래킹 사용)
def generate_combinations(grouped):
    subjects = list(grouped.keys())   # 과목명 리스트
    result = []

    def backtrack(index, current):
        # 모든 과목에 대해 분반 선택이 완료되면 저장
        if index == len(subjects):
            result.append(current[:])  # 현재 조합을 깊은 복사해 저장
            return

        subject = subjects[index]
        for section in grouped[subject]:
            current.append(section)
            backtrack(index + 1, current)
            current.pop()                 # 백트래킹

    backtrack(0, [])
    return result

# 시간표 충돌(겹침)이 있는지 확인하는 함수
def has_conflict(combo):
    schedule = []

    for section in combo:
        for day, start, end in section.time_slots:
            # 같은 요일에 이미 수업 있는지 검사
            for d, s, e in schedule:
                if day == d:
                    # 시간이 겹치면 충돌
                    if not (end <= s or start >= e):
                        return True
            schedule.append((day, start, end))
    
    return False

# 유효한 시간표 조합만 골라내는 함수
def filter_valid_combinations(combinations):
    valid = []
    for combo in combinations:
        if not has_conflict(combo):
            valid.append(combo)
    return valid

# 최종 시간표 출력 함수
def print_timetable(combo):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    timetable = {day: {} for day in days}

    for sec in combo:
        name = f"{sec.subject}({sec.section_id})"
        for day, start, end in sec.time_slots:
            if day not in timetable:
                timetable[day] = {}
            timetable[day][(start, end)] = name

    # 시간 슬롯 모으기
    time_slots = set()
    for day in timetable:
        for slot in timetable[day]:
            time_slots.add(slot)
    time_slots = sorted(time_slots)

    print("🕒   시간       Mon           Tue           Wed           Thu           Fri")
    print("---------------------------------------------------------------------------")

    for start, end in time_slots:
        row = f"{start:>5.1f}~{end:<5.1f}  "
        for day in days:
            name = timetable[day].get((start, end), "  -----")  # 빈칸이면 ----- 출력
            row += f"{name:<12}"  # 칸 고정 너비
        print(row)

    # 마지막 줄에 과목명, 콰목코드 출력
    subjects = [sec.subject for sec in combo]
    print("\n 과목명   : ", ", ".join(subjects))
    codes = [sec.code for sec in combo]
    print("\n 과목코드 : ", ", ".join(codes))

# 실행 시작 지점
def main(): 
    filename = "subjects.txt"
    sections = load_subjects_from_file(filename)

    grouped = group_sections_by_subject(sections)
    combinations = generate_combinations(grouped)
    valid_combinations = filter_valid_combinations(combinations)

    print(f"✅ 충돌 없는 조합 수: {len(valid_combinations)}\n")
    print("\n🗓️ 최적 시간표 추천 결과 :")
    for i in range(min(5, len(valid_combinations))):
        print(f"\n[추천 시간표 {i+1}번]")
        print_timetable(valid_combinations[i])

if __name__ == "__main__":
    main()