import importlib.util
from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


count = module('count', ROOT / 'skills/shanghai-essay-revise/scripts/count_text.py')
save = module('save', ROOT / 'skills/shanghai-essay-revise/scripts/save_review.py')
audit = module('audit', ROOT / 'scripts/audit_public.py')


class ToolsTest(unittest.TestCase):
    def test_count_punctuation_and_unicode(self):
        self.assertEqual(count.counts('甲，乙。 A1\n𠀀')['han_count'], 3)
        self.assertEqual(count.counts('甲，乙。 A1\n𠀀')['nonspace_count'], 7)

    def test_length_boundaries(self):
        for n, good in [(849, False), (850, True), (950, True), (951, False)]:
            self.assertEqual(count.counts('甲' * n)['within_default_target'], good)

    def test_no_overwrite_or_path_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            now = datetime(2026, 1, 1, tzinfo=timezone.utc)
            a = save.save_review(directory, '../../bad:title', 'first', now)
            b = save.save_review(directory, '../../bad:title', 'second', now)
            self.assertNotEqual(a, b)
            self.assertEqual(a.parent, Path(directory).resolve())
            self.assertTrue(a.read_text(encoding='utf-8').endswith('first'))
            self.assertTrue(b.read_text(encoding='utf-8').endswith('second'))

    def test_missing_vault_not_created(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'missing'
            with self.assertRaises(FileNotFoundError):
                save.save_review(target, 'title', 'text')
            self.assertFalse(target.exists())

    def test_private_file_rejected_even_if_forced(self):
        self.assertTrue(audit.violations('private/essay.md', b'private content', {'SKILL.md'}))
        self.assertFalse(audit.violations('SKILL.md', '公共规则'.encode(), {'SKILL.md'}))


if __name__ == '__main__':
    unittest.main()
