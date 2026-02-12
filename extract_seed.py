import sys
import re

with open("seed_data.py", "r") as f:
    content = f.read()

# Extract questions_list = [...], utilizing DOTALL to capture multiline content
match = re.search(r"questions_list = \[(.*?)(\s{4}\]\s*print)", content, re.DOTALL)
# The regex needs to be careful about nested brackets? No, simple list of dicts.
# But `seed_data.py` ends the list with `    ]` then `print`.
# I'll rely on indentation.
# Or just use the line numbers I know.

lines = content.splitlines()
start_line = 92 # 0-indexed, line 93 is index 92.
end_line = 523 # line 523 is index 522.

extracted_lines = lines[start_line:end_line]
# Remove indentation (4 spaces)
cleaned_lines = []
for line in extracted_lines:
    if line.startswith("    "):
        cleaned_lines.append(line[4:])
    else:
        cleaned_lines.append(line)

with open("exams/seed_data_list.py", "w") as out:
    out.write("\n".join(cleaned_lines))
    # It might be missing `questions_list = [` at start or `]` at end depending on slicing.
    # line 93 (index 92) is `    questions_list = [`
    # line 523 (index 522) is `    ]`
    # So `cleaned_lines` will have `questions_list = [` at index 0.
    # And `]` at last index.
    # Perfect.

print("Success")
