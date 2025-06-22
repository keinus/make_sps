# 각 파일 타입에 해당하는 확장자 리스트 정의
EXECUTION_EXTENSIONS = {".exe", ".dll", ".so", ".bin",
                        '.msi', '.bat', '.sh', '.app',
                        '.dmg', '.jar', '.com', '.out',
                        '.csh', '.run', '.cmd', '.ps1', '.action',
                        '.elf', '.o', }
CONFIGURATION_EXTENSIONS = {
    '.ini', '.conf', '.config', '.cfg', '.json', '.xml', '.yaml', '.yml',
    '.plist', '.properties', '.env', '.toml', '.cnf', '.prefs', '.settings',
    '.reg', '.inf', '.desktop', '.md'
}

DATABSE_EXTENSIONS = {
    '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.sql', '.dat', '.dbf',
    '.sdf', '.myd', '.myi', '.frm',
    '.gdb', '.fdb',
    '.abs',
    '.kdb', '.kdbx',
    '.csv',
    '.mdf', '.ldf'
}

PROJECT_EXTENSIONS = {
    '.sln', '.csproj', '.vbproj', '.vcxproj', '.fsproj',  # Visual Studio
    '.xcodeproj', '.xcworkspace',  # Xcode
    '.gradle', '.idea',  # Android Studio, IntelliJ
    '.project', '.classpath',  # Eclipse
    '.Rproj',  # RStudio
    '.sublime-project', '.sublime-workspace',  # Sublime Text
    '.vscode',  # Visual Studio Code (폴더 기반이지만, 설정 파일 확장자로 간주)
    '.unity',  # Unity
    '.uproject'  # Unreal Engine
}

SOURCE_EXTENSIONS = {
    '.py', '.java', '.c', '.cpp', '.cs', '.js', '.ts', '.html', '.css', '.php',
    '.rb', '.go', '.rs', '.swift', '.kt', '.kts', '.scala', '.r', '.m', '.pl',
    '.lua', '.scss', '.vue', '.jsx', '.tsx'
}

IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp',
    '.svg', '.ico', '.heic', '.heif', '.jp2', '.jxr', '.wdp', '.avif',
    '.raw', '.cr2', '.nef', '.arw', '.orf', '.sr2',
    '.eps', '.psd', '.ai', '.indd'
}
