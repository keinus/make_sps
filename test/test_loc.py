"""간단한 LOC 측정 테스트 러너"""
import tempfile
import os
from ..app.parser.code_counter import count_code_lines


def create_test_file(content):
    """테스트용 임시 파일 생성"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
    temp_file.write(content)
    temp_file.close()
    return temp_file.name


def run_test(test_name, content, expected_result):
    """개별 테스트 실행"""
    file_path = create_test_file(content)
    try:
        result = count_code_lines(file_path)
        if result == expected_result:
            print(f"✅ {test_name}: PASSED (expected: {expected_result}, got: {result})")
            return True
        else:
            print(f"❌ {test_name}: FAILED (expected: {expected_result}, got: {result})")
            return False
    finally:
        os.unlink(file_path)


def test_main():
    """메인 테스트 실행 함수"""
    print("LOC 측정 모듈 테스트 시작")
    print("=" * 50)
    
    tests_passed = 0
    tests_failed = 0
    
    # 테스트 케이스들
    test_cases = [
        # (테스트명, 코드 내용, 예상 결과)
        ("기본 코드 라인", """int main() {
    return 0;
}""", 3),
        
        ("빈 파일", "", 0),
        
        ("빈 줄만", "\n\n\n   \n\t\n", 0),
        
        ("한 줄 주석 (C++)", """// This is a comment
int a = 0;
// Another comment
int b = 1; // Inline comment""", 2),
        
        ("한 줄 주석 (Python)", """# This is a comment
x = 10
# Another comment
y = 20  # Inline comment""", 2),
        
        ("여러 줄 주석 (C)", """/*
This is a multi-line comment
spanning multiple lines
*/
int main() {
    /* inline multi-line comment */
    return 0;
}""", 3),
        
        ("여러 줄 주석 (Python)", '''"""
This is a multi-line comment
in Python style
"""
def hello():
    """Another docstring"""
    return "world"''', 2),
        
        ("인라인 여러 줄 주석", """int a = 0; /* comment */ int b = 1;
int c = /* another comment */ 2;
/* comment */ int d = 3;""", 3),
        
        ("혼합 주석", """// Header comment
int main() {
    int a = 0; // Variable a
    /* Multi-line
       comment here */
    int b = 1;
    return 0; /* inline */ // and single line
}
// Footer comment""", 5),
        
        ("주석만 있는 파일", """// Only comments
/* 
   Multi-line comment
*/
# Python comment""", 0),
        
        ("실제 코드 예제", """#include <stdio.h>

/*
 * This is a sample C program
 * Author: Test
 */

int main() {
    // Variable declaration
    int num = 42;
    
    /* Print the number */
    printf("Number: %d\\n", num); // Output
    
    /*
     * Return success
     */
    return 0;
}

// End of file""", 5),
    ]
    
    # 각 테스트 실행
    for test_name, content, expected in test_cases:
        if run_test(test_name, content, expected):
            tests_passed += 1
        else:
            tests_failed += 1
    
    # 파일 없음 테스트
    print("\n파일 없음 테스트:")
    result = count_code_lines("non_existent_file.txt")
    if result == -1:
        print("✅ 파일 없음 테스트: PASSED")
        tests_passed += 1
    else:
        print("❌ 파일 없음 테스트: FAILED")
        tests_failed += 1
    
    # 결과 출력
    print("\n" + "=" * 50)
    print(f"테스트 결과: {tests_passed} 통과, {tests_failed} 실패")
    print(f"총 {tests_passed + tests_failed} 테스트 중 {tests_passed} 통과")
    
    if tests_failed == 0:
        print("🎉 모든 테스트가 통과했습니다!")
        return 0
    else:
        print("⚠️ 일부 테스트가 실패했습니다.")
        return 1


if __name__ == "__main__":
    test_main()