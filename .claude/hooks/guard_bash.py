#!/usr/bin/env python3
"""PreToolUse guard for the Bash tool (T000 F20).

Closes the gaps of the permissions.deny rules in .claude/settings.json (F08):
  a) destructive commands in any flag order: rm -r + -f, git push --force/-f/
     --force-with-lease/+refspec, git reset --hard, git clean -f
  b) any Bash access to .env, .env.* or secrets/ paths
  c) Bash writes to docs/architecture/ARCHITECTURE.md or
     docs/conventions/CONVENTIONS.md (redirection, tee, sed -i, cp/mv/rm/...)
Reads the hook JSON from stdin. Exit 0 = allow, exit 2 = block (reason on
stderr). Unreadable input fails closed (exit 2). Standard library only.
"""
import json
import os
import re
import shlex
import sys

PROTECTED_DOCS = ("docs/architecture/architecture.md", "docs/conventions/conventions.md")
SEPARATORS = {";", "&&", "||", "|", "&", "|&", "(", ")", "\n"}
REDIRECTS = {">", ">>", ">|", "&>", "&>>", "<>"}
WRAPPERS = {"sudo", "command", "env", "nohup", "time", "xargs", "exec", "builtin"}
DOC_WRITERS = {"tee", "cp", "mv", "rm", "truncate", "dd", "install", "ln"}


def block(reason):
    print("Blocked by .claude/hooks/guard_bash.py: " + reason, file=sys.stderr)
    sys.exit(2)


def tokenize(command):
    lexer = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=";&|()<>")
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:  # unbalanced quotes: fall back to a plain split
        return command.split()


def segments(tokens):
    seg = []
    for tok in tokens:
        if tok in SEPARATORS:
            if seg:
                yield seg
            seg = []
        else:
            seg.append(tok)
    if seg:
        yield seg


def program(seg):
    """Return (name, args) skipping env assignments and wrapper commands."""
    i = 0
    while i < len(seg) and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", seg[i]) or os.path.basename(seg[i]) in WRAPPERS):
        i += 1
    if i >= len(seg):
        return "", []
    name = os.path.basename(seg[i].replace("\\", "/")).lower()
    if name.endswith(".exe"):
        name = name[:-4]
    return name, seg[i + 1:]


def short_flags(args):
    return "".join(a[1:] for a in args if a.startswith("-") and not a.startswith("--"))


def norm(path):
    return path.replace("\\", "/").strip("'\"").lower()


def is_secret(tok):
    for part in (tok, tok.split("=", 1)[-1]):
        p = norm(part)
        base = p.rstrip("/").rsplit("/", 1)[-1]
        if base == ".env" or base.startswith(".env.") or re.search(r"(^|/)secrets/", p):
            return True
    return False


def is_protected_doc(tok):
    p = norm(tok.split("=", 1)[-1])
    return any(p == d or p.endswith("/" + d) for d in PROTECTED_DOCS)


def check(command, depth=0):
    tokens = tokenize(command)
    for tok in tokens:
        if is_secret(tok):
            block("access to .env / .env.* / secrets/ is not allowed (" + tok + ")")
    for seg in segments(tokens):
        name, args = program(seg)
        flags = short_flags(args)
        if name in ("bash", "sh", "zsh", "dash") and "-c" in args and depth < 3:
            idx = args.index("-c")
            if idx + 1 < len(args):
                check(args[idx + 1], depth + 1)
        if name == "rm":
            recursive = any(c in flags for c in "rR") or "--recursive" in args
            force = "f" in flags or "--force" in args
            if recursive and force:
                block("recursive forced delete (rm -r -f) is not allowed")
        if name == "git":
            rest = list(args)
            while rest and rest[0] in ("-C", "-c"):
                rest = rest[2:]
            sub, sub_args = (rest[0], rest[1:]) if rest else ("", [])
            if sub == "push" and (
                any(a in ("--force", "-f") or a.startswith("--force-with-lease") or a.startswith("--force-if-includes") for a in sub_args)
                or "f" in short_flags(sub_args)
                or any(a.startswith("+") for a in sub_args)
            ):
                block("force push is not allowed")
            if sub == "reset" and "--hard" in sub_args:
                block("git reset --hard is not allowed")
            if sub == "clean" and ("f" in short_flags(sub_args) or "--force" in sub_args):
                block("git clean -f is not allowed")
        for i, tok in enumerate(seg):
            if not is_protected_doc(tok):
                continue
            prev = seg[i - 1] if i else ""
            if prev in REDIRECTS or prev.endswith(">"):
                block("writing to a protected doc (ARCHITECTURE.md / CONVENTIONS.md) is not allowed")
            if name in DOC_WRITERS or (name in ("sed", "perl") and ("i" in flags or any(a.startswith("--in-place") for a in args))):
                block("modifying a protected doc (ARCHITECTURE.md / CONVENTIONS.md) is not allowed")


def main():
    try:
        data = json.load(sys.stdin)
        command = data.get("tool_input", {}).get("command", "")
    except Exception:
        block("could not read the hook input (failing closed)")
    if isinstance(command, str) and command:
        try:
            check(command)
        except Exception as exc:  # a bug in this guard must not let the command through
            block("internal error in guard (failing closed): " + repr(exc))
    sys.exit(0)


if __name__ == "__main__":
    main()
