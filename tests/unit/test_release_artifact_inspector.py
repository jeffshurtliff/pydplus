# -*- coding: utf-8 -*-
"""
:Module:            test_release_artifact_inspector
:Synopsis:          Tests the PyDPlus release artifact inspector
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff (via GPT-6)
:Modified Date:     12 Sep 2026
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from types import ModuleType
from unittest.mock import patch


def load_inspector() -> ModuleType:
    """Load the repository skill's artifact inspector as a module."""
    repository_root = Path(__file__).resolve().parents[2]
    script_path = repository_root / '.agents/skills/pydplus-stable-release-prep/scripts/inspect_release_artifacts.py'
    module = ModuleType('pydplus_release_artifact_inspector')
    module.__file__ = str(script_path)
    with patch.object(sys, 'path', [str(script_path.parent), *sys.path]):
        with patch.dict(sys.modules):
            sys.modules.pop('constants', None)
            exec(compile(script_path.read_text(encoding='utf-8'), str(script_path), 'exec'), module.__dict__)
    return module


def test_inspect_wheel_warns_about_nested_package_tests(tmp_path: Path) -> None:
    """Reject test content nested below the import package in strict runs."""
    inspector = load_inspector()
    wheel_path = tmp_path / 'pydplus-2.0.0-py3-none-any.whl'
    with zipfile.ZipFile(wheel_path, mode='w') as archive:
        archive.writestr('pydplus/__init__.py', '')
        archive.writestr('pydplus/tests/test_embedded.py', '')
        archive.writestr('pydplus-2.0.0.dist-info/METADATA', 'Name: pydplus\nVersion: 2.0.0\n')

    errors, warnings = inspector.inspect_wheel(wheel_path, 'pydplus', '2.0.0')

    assert errors == []
    assert warnings == [f'{wheel_path.name}: test content included: pydplus/tests/test_embedded.py']


def test_wheel_metadata_paths_are_not_treated_as_test_content() -> None:
    """Ignore test-like path components within wheel metadata directories."""
    inspector = load_inspector()

    assert inspector.wheel_test_members(['pydplus-2.0.0.dist-info/tests/metadata.json']) == []


def test_inspector_cli_accepts_candidate_and_rejects_invalid_archives(tmp_path: Path) -> None:
    """Validate a complete candidate and reject wrong versions and local files."""
    import io
    import subprocess
    import tarfile

    project = tmp_path / 'project'
    dist = project / 'dist'
    dist.mkdir(parents=True)
    (project / 'pyproject.toml').write_text(
        '[project]\nname = "pydplus"\nversion = "2.0.1"\nreadme = "README.md"\nlicense = {file = "LICENSE"}\n',
        encoding='utf-8',
    )
    metadata = b'Name: pydplus\nVersion: 2.0.1\n'
    sdist = dist / 'pydplus-2.0.1.tar.gz'
    with tarfile.open(sdist, 'w:gz') as archive:
        for name, data in {
            'PKG-INFO': metadata,
            'pyproject.toml': (project / 'pyproject.toml').read_bytes(),
            'README.md': b'Example package',
            'LICENSE': b'Example license',
            'src/pydplus/__init__.py': b'',
        }.items():
            member = tarfile.TarInfo(f'pydplus-2.0.1/{name}')
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
    wheel = dist / 'pydplus-2.0.1-py3-none-any.whl'
    with zipfile.ZipFile(wheel, 'w') as archive:
        archive.writestr('pydplus/__init__.py', '')
        archive.writestr('pydplus-2.0.1.dist-info/METADATA', metadata)
    script = (
        Path(__file__).resolve().parents[2] / '.agents/skills/pydplus-stable-release-prep/scripts/inspect_release_artifacts.py'
    )
    command = [sys.executable, str(script), '--project-root', str(project), '--strict', '--expected-version', '2.0.1']
    valid = subprocess.run(command, capture_output=True, text=True, check=False)
    assert valid.returncode == 0, valid.stderr
    assert valid.stdout.count('SHA256 ') == 2

    mismatch = subprocess.run([*command[:-1], '2.0.2'], capture_output=True, text=True, check=False)
    assert mismatch.returncode == 1
    assert 'does not match' in mismatch.stderr

    with zipfile.ZipFile(wheel, 'a') as archive:
        archive.writestr('local/helper.json', '{}')
    unsafe = subprocess.run(command, capture_output=True, text=True, check=False)
    assert unsafe.returncode == 1
    assert 'suspicious members' in unsafe.stderr

    wheel.write_bytes(b'not a zip archive')
    corrupt = subprocess.run(command, capture_output=True, text=True, check=False)
    assert corrupt.returncode == 1
    assert 'unreadable wheel' in corrupt.stderr
    assert 'Traceback' not in corrupt.stderr
