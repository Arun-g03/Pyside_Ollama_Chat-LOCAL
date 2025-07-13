#!/usr/bin/env python3
"""Check critical threading issues"""

from pyside_chat.core.utils.threading_audit import ThreadingAuditor

def main():
    auditor = ThreadingAuditor()
    report = auditor.audit_codebase()
    
    print("Critical threading issues:")
    print("=" * 50)
    
    critical_issues = [issue for issue in report['all_issues'] if issue['severity'] == 'error']
    
    if not critical_issues:
        print("✅ No critical threading issues found!")
    else:
        for issue in critical_issues:
            print(f"❌ {issue['file']}:{issue['line']}")
            print(f"   {issue['description']}")
            print(f"   Code: {issue['code']}")
            print()

if __name__ == "__main__":
    main() 