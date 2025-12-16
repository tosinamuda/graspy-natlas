import sys
import os

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.domains.study.service import get_full_language_name

def test_mappings():
    test_cases = [
        ("pcm", "Nigerian Pidgin English"),
        ("pidgin", "Nigerian Pidgin English"),
        ("ha", "Hausa"),
        ("ig", "Igbo"),
        ("yo", "Yoruba"),
        ("en", "English"),
        ("fr", "fr"), # Fallback test
        ("PCM", "Nigerian Pidgin English"), # Case insensitivity
    ]

    print("Running Language Mapping Verification:\n")
    print(f"{'Code':<10} | {'Expected':<25} | {'Actual':<25} | {'Result'}")
    print("-" * 75)

    all_passed = True
    for code, expected in test_cases:
        actual = get_full_language_name(code)
        passed = actual == expected
        status = "✅ PASS" if passed else "❌ FAIL"
        if not passed:
            all_passed = False
        print(f"{code:<10} | {expected:<25} | {actual:<25} | {status}")

    print("-" * 75)
    if all_passed:
        print("\nAll mappings verified successfully! 🚀")
    else:
        print("\nSome mappings failed. Please check service.py.")

if __name__ == "__main__":
    test_mappings()
