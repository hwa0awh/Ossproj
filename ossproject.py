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
