# AI Auto-Fixer for Your Project

## 🎯 Overview

The AI Auto-Fixer is a comprehensive tool that automatically detects and fixes errors in your Python project using AI (Gemini). It includes a user permission system that asks for your approval before making any changes.

## ✨ Features

- **User Permission System**: Always asks for your approval before making changes
- **Comprehensive Error Detection**: Finds both syntax and runtime errors
- **Automatic Backups**: Creates backups before modifying files
- **Multiple Modes**: Scan all files, fix specific files, or run commands
- **Interactive Mode**: Detailed prompts with fix previews
- **Auto-approve Mode**: For automated workflows

## 🚀 Usage Examples

### 1. Scan All Python Files for Errors
```bash
python ai_fix_project.py --scan-all
```
This will scan all Python files in your project and report any syntax errors.

### 2. Fix a Specific File
```bash
python ai_fix_project.py --fix-file broken_example.py
```
This will:
- Check the file for syntax and runtime errors
- Ask for your permission before applying fixes
- Create a backup before making changes
- Apply the AI-generated fix
- Verify the fix works

### 3. Auto-approve Mode (No Prompts)
```bash
python ai_fix_project.py --fix-file broken_example.py --auto-approve
```
This automatically applies fixes without asking for permission.

### 4. Run a Command and Fix Errors
```bash
python ai_fix_project.py --command "python -m pytest"
```
This runs your command and automatically fixes any errors that occur.

### 5. Interactive Mode with Details
```bash
python ai_fix_project.py --fix-file broken_example.py --interactive
```
This shows detailed information about the proposed fix and lets you see the full changes before approving.

## 🔧 Command Line Options

- `--scan-all`: Scan all Python files for errors
- `--fix-file <path>`: Fix a specific Python file
- `--command <cmd>`: Run a command and fix any errors
- `--max-attempts <n>`: Maximum number of fix attempts (default: 5)
- `--timeout <seconds>`: Timeout for running files/commands (default: 180)
- `--interactive`: Interactive mode with user prompts (default: true)
- `--auto-approve`: Auto-approve all fixes without asking
- `--model <name>`: Gemini model to use (default: auto)

## 🔐 Environment Setup

Make sure you have your Gemini API key set:

```bash
# Option 1: Environment variable
export GEMINI_API_KEY="your_api_key_here"

# Option 2: .env file in project root
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## 📁 Backup System

The tool automatically creates backups in `.ai_fix_backups/` directory before making any changes. Each backup is timestamped, so you can easily restore previous versions if needed.

## 🎯 How It Works

1. **Detection**: Scans files for syntax errors or runs them to detect runtime errors
2. **AI Analysis**: Sends the error and code to Gemini AI for analysis
3. **User Permission**: Shows you the proposed fix and asks for approval
4. **Backup**: Creates a backup of the original file
5. **Application**: Applies the AI-generated fix
6. **Verification**: Tests the fix to ensure it works

## 🛡️ Safety Features

- **User Permission**: Never modifies files without your explicit approval
- **Automatic Backups**: Always creates backups before changes
- **Fix Verification**: Tests fixes to ensure they work
- **Empty Fix Protection**: Won't apply empty or invalid fixes
- **Detailed Logging**: Shows exactly what changes are being made

## 📊 Example Output

```
🔧 Fixing file: broken_example.py
🔍 Checking for runtime errors...
❌ Runtime error: Traceback (most recent call last):
  File "broken_example.py", line 8, in <module>
    print(greet("World"))
          ~~~~~^^^^^^^^^
  File "broken_example.py", line 5, in <module>
    return f"Hello, {nam}!"  # 'nam' is undefined

🔧 AI wants to fix: broken_example.py
📋 Error: NameError: name 'nam' is not defined
💡 Proposed fix preview: def greet(name):
    return f"Hello, {name}!"

❓ Apply this fix? (y/n/d for details): y
💾 Created backup: .ai_fix_backups\broken_example.py.backup_20250901_224114
📝 Applied AI-corrected code to broken_example.py
🔍 Verifying fix...
✅ Fix applied successfully!
```

## 🎉 Success!

Your AI Auto-Fixer is now ready to help maintain your Python project! It will automatically detect errors and ask for your permission before fixing them, ensuring you stay in control while getting AI assistance.
