"""Tests for tools/check-profile.py using disposable fixture profiles and local git repos."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / 'tools' / 'check-profile.py'

VALID_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"></svg>'
README = (
    '<img src="./assets/profile-header.svg" alt="header" width="100%" />\n'
    '| [certconv](https://github.com/nickromney/certconv) | tool |\n'
)


class CheckProfileTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name)
        self.profile = base / 'profile'
        self.repos = base / 'repos'
        (self.profile / 'tools').mkdir(parents=True)
        (self.profile / 'assets').mkdir()
        # Test the script exactly as it exists in this checkout.
        shutil.copy(SCRIPT, self.profile / 'tools' / 'check-profile.py')
        (self.profile / 'README.md').write_text(README)
        (self.profile / 'assets' / 'profile-header.svg').write_text(VALID_SVG)
        self.make_repo('certconv', 'git@github.com:nickromney/certconv.git')

    def make_repo(self, name, remote):
        repo = self.repos / name
        shutil.rmtree(repo, ignore_errors=True)
        repo.mkdir(parents=True)
        subprocess.run(['git', 'init', '-q', str(repo)], check=True)
        if remote is not None:
            subprocess.run(['git', '-C', str(repo), 'remote', 'add', 'origin', remote], check=True)
        return repo

    def run_check(self):
        return subprocess.run(
            [sys.executable, str(self.profile / 'tools' / 'check-profile.py'), '--repos-root', str(self.repos)],
            capture_output=True,
            text=True,
        )

    def test_valid_fixture_passes(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('SVG XML parsed', result.stdout)

    def test_missing_local_image_fails(self):
        (self.profile / 'assets' / 'profile-header.svg').unlink()
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)

    def test_malformed_svg_fails(self):
        (self.profile / 'assets' / 'profile-header.svg').write_text('<svg><g></svg>')
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('SVG is not well-formed XML: assets/profile-header.svg', result.stderr)

    def test_malformed_svg_in_nested_asset_dir_fails(self):
        nested = self.profile / 'assets' / 'extra'
        nested.mkdir()
        (nested / 'broken.svg').write_text('<svg')
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('broken.svg', result.stderr)

    def test_repo_link_without_local_clone_fails(self):
        shutil.rmtree(self.repos / 'certconv')
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Repository link has no local evidence: certconv', result.stderr)

    def test_repo_link_with_different_origin_fails(self):
        self.make_repo('certconv', 'git@github.com:someoneelse/certconv.git')
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Repository link differs from local remote: certconv', result.stderr)

    def test_repo_without_origin_fails_with_message(self):
        shutil.rmtree(self.repos / 'certconv')
        self.make_repo('certconv', None)
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Repository has no origin remote: certconv', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_https_remote_without_git_suffix_passes(self):
        shutil.rmtree(self.repos / 'certconv')
        self.make_repo('certconv', 'https://github.com/nickromney/certconv')
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
