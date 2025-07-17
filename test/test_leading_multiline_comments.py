
from ..app.parser.get_file_description import leading_multiline_comments

def test_leading_multiline_comments():
    """leading_multiline_comments 함수를 테스트합니다."""
    import tempfile
    import os
    
    test_cases = [
        # Python 스타일 - 한 줄
        {
            'name': 'Python single line docstring (triple double quotes)',
            'content': '"""This is a single line docstring"""\ndef foo(): pass',
            'expected': 'This is a single line docstring'
        },
        {
            'name': 'Python single line docstring (triple single quotes)',
            'content': "'''This is a single line docstring'''\ndef foo(): pass",
            'expected': 'This is a single line docstring'
        },
        # Python 스타일 - 여러 줄
        {
            'name': 'Python multiline docstring',
            'content': '''"""
This is a multiline
docstring with
multiple lines
"""
def foo(): pass''',
            'expected': 'This is a multiline\ndocstring with\nmultiple lines'
        },
        # C 스타일 - 한 줄
        {
            'name': 'C style single line',
            'content': '/* This is a single line comment */ int main() {}',
            'expected': 'This is a single line comment'
        },
        # C 스타일 - 여러 줄
        {
            'name': 'C style multiline',
            'content': '''/*
 * This is a multiline
 * C style comment
 * with asterisks
 */
int main() {}''',
            'expected': 'This is a multiline\nC style comment\nwith asterisks'
        },
        # C 스타일 - 별표 없는 형식
        {
            'name': 'C style multiline without asterisks',
            'content': '''/*
This is a multiline
C style comment
without asterisks
*/
int main() {}''',
            'expected': 'This is a multiline\nC style comment\nwithout asterisks'
        },
        # 단일 줄 주석 - Python
        {
            'name': 'Python single line comments',
            'content': '''# This is the first line
# This is the second line
# This is the third line

def foo(): pass''',
            'expected': 'This is the first line\nThis is the second line\nThis is the third line'
        },
        # 단일 줄 주석 - C++
        {
            'name': 'C++ single line comments',
            'content': '''// This is a C++ comment
// Second line of comment
int main() {}''',
            'expected': 'This is a C++ comment\nSecond line of comment'
        },
        # 단일 줄 주석 - SQL
        {
            'name': 'SQL single line comments',
            'content': '''-- This is a SQL comment
-- Another SQL comment line
SELECT * FROM table;''',
            'expected': 'This is a SQL comment\nAnother SQL comment line'
        },
        # 비어있는 파일
        {
            'name': 'Empty file',
            'content': '',
            'expected': ''
        },
        # 주석이 없는 파일
        {
            'name': 'No comment',
            'content': 'def foo(): pass',
            'expected': ''
        },
        # 빈 주석
        {
            'name': 'Empty Python comment',
            'content': '"""\n"""\ndef foo(): pass',
            'expected': ''
        },
        # 단일 줄 주석 - 빈 내용
        {
            'name': 'Empty single line comments',
            'content': '''#
#
def foo(): pass''',
            'expected': ''
        },
        # 들여쓰기가 있는 주석
        {
            'name': 'Indented comment',
            'content': '    /* Indented comment */ code();',
            'expected': 'Indented comment'
        },
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_case['content'])
            temp_path = f.name
        
        try:
            result = leading_multiline_comments(temp_path)
            passed = result == test_case['expected']
            status = "✓" if passed else "✗"
            
            print(f"{status} {test_case['name']}")
            if not passed:
                print(f"  Expected: {repr(test_case['expected'])}")
                print(f"  Got:      {repr(result)}")
                print(f"  Content:  {repr(test_case['content'][:50])}...")
                all_passed = False
                
        finally:
            os.unlink(temp_path)
    
    # 파일이 없는 경우 테스트
    result = leading_multiline_comments('non_existent_file.py')
    if result == "":
        print("✓ Non-existent file")
    else:
        print("✗ Non-existent file")
        print(f"  Expected: ''")
        print(f"  Got:      {repr(result)}")
        all_passed = False
    
    if all_passed:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    return all_passed


if __name__ == "__main__":
    test_leading_multiline_comments()