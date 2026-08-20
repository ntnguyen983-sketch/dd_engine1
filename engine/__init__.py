"""Duyên Dịch engine package.

Compatibility package: the runtime entrypoint imports modules from engine.*.
"""
from .pipeline import cast_and_run, run_pipeline

__version__ = "1.0.0"
