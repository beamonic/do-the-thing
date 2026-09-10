"""The skill folder must stay installable outside Claude Code.

The Agent Skills spec allows six frontmatter keys. Claude Code accepts many
more, and a skill that uses one of its extensions is a hard error everywhere
else: "Unexpected key(s) in SKILL.md frontmatter". The README promises that any
agent supporting SKILL.md can use this folder, so that promise is tested rather
than trusted. Parsed with a regex on purpose: the package depends on nothing
outside the standard library.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/do-the-thing/SKILL.md'
PORTABLE_KEYS = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
LISTING_CAP = 1536


def frontmatter():
    text = SKILL.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if match is None:
        return None
    fields, key = {}, None
    for line in match.group(1).splitlines():
        if line[:1].strip() and ':' in line:
            key, _, value = line.partition(':')
            fields[key.strip()] = value.strip()
        elif key is not None:
            fields[key] += ' ' + line.strip()
    return fields


class FrontmatterTests(unittest.TestCase):
    def setUp(self):
        self.fields = frontmatter()
        self.assertIsNotNone(self.fields, 'opening --- must be the first line of SKILL.md')

    def test_only_portable_keys(self):
        extra = sorted(set(self.fields) - PORTABLE_KEYS)
        self.assertEqual([], extra, f'not in the Agent Skills spec: {extra}')

    def test_name_matches_the_directory(self):
        self.assertEqual(SKILL.parent.name, self.fields.get('name'))

    def test_description_is_present_and_within_the_listing_cap(self):
        description = self.fields.get('description', '')
        self.assertTrue(description.strip(), 'description is recommended and carries the triggers')
        self.assertLessEqual(len(description), LISTING_CAP)

    def test_description_carries_a_trigger_for_each_branch(self):
        description = self.fields.get('description', '')
        quoted = re.findall(r'"([^"]+)"', description)
        self.assertGreaterEqual(len(quoted), 4, 'one trigger per branch: delegate, spec, resume, verify')
        self.assertEqual(len(quoted), len(set(quoted)), 'a repeated trigger is one branch written twice')

    def test_referenced_files_exist(self):
        body = SKILL.read_text(encoding='utf-8')
        for target in re.findall(r'\]\((?!https?://)([^)#]+)\)', body):
            with self.subTest(target=target):
                self.assertTrue((SKILL.parent / target).exists(), f'broken link: {target}')


if __name__ == '__main__':
    unittest.main()
