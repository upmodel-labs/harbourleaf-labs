"""A fake grounded assistant for the hallucination and drift labs: answers from a small
corpus of numbered lines, with no model. Deterministic; standard library only.

A corpus is a folder holding index.json plus the text files it lists. Each text file has
one numbered line per row, for example "L3  Tomas to post the summary by 13 November."
(or "S3  ..." for a guide). index.json lists, for each file: key, file, title, revision,
status ("current" or "superseded"), topic, and optionally "invented" (see "hallucinate").

answer(question) returns a GroundedAnswer (a dict that also allows attribute access):
  text           the answer, one sentence per claim
  claims         a list of {"text": ..., "support": "<key>-<line id>" or None}
  retrieved      the line ids the answer was built from, such as ["a-L4"]
  served_version the version string of the (fake) model that answered
  prompt_id      the id of the prompt the answer used
  manifest       the index manifest: file, checksum and revision of every file in the index

How it answers (the same every time): the question's content words are matched to each
line (plural and -ing/-ed endings are ignored; the word "group" is ignored); the
best-matching file is chosen; up to three of its best-matching lines (the best score, or
one less) become the claims, in file order. No match gives
"I could not find that in the notes." with no claims.

Flags switch defects on:
  "hallucinate"  adds one more claim with no support (support is None)
  "stale_note"   answers from the superseded revision of a topic when there is one
  "drift"        the served version string changes (its last digits go up by one) and the
                 answer keeps only its single best line, so some answers lose a fact
"""
import hashlib
import json
import re
from pathlib import Path

FLAGS = ("hallucinate", "stale_note", "drift")
MAX_CLAIMS = 3
NOT_FOUND = "I could not find that in the notes."
DEFAULT_INVENTED = "The supplier also offers a longer guide."
# Used when index.json gives no "invented" line for a file. Keeps the practice notes' index free of any claim text.
INVENTED_BY_TOPIC = {
    "meeting-a": "The group will vote on the next book by post.",
    "meeting-b": "The town hall will print copies of the map.",
    "meeting-c": "The group will invite a guest speaker.",
}

_STOP = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "to", "of", "in", "on", "at", "by",
    "for", "and", "or", "it", "its", "this", "that", "do", "does", "did", "i", "we", "you", "me",
    "my", "our", "what", "which", "who", "whom", "when", "where", "how", "many", "much", "with",
    "as", "from", "about", "any", "there", "so", "if", "can", "will", "should", "not", "group",
}
_LINE = re.compile(r"^([A-Z]+\d+)\s+(.+?)\s*$")
_VERSION = re.compile(r"^(.*?)(\d+)$")


def checksum(text):
    """Short fingerprint of a file's text (first 12 hex characters of sha256)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _stem(word):
    for suffix in ("ing", "ed", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            if suffix == "s" and word.endswith("ss"):
                return word
            return word[: -len(suffix)]
    return word


def _words(text):
    return {_stem(w) for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in _STOP}


def parse_lines(text):
    """Numbered lines to a list of (line id, text). Lines that do not start with an id are skipped."""
    out = []
    for raw in text.splitlines():
        m = _LINE.match(raw.strip())
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def load_corpus(directory):
    """Reads index.json and the files it lists. Returns a list of document dicts."""
    directory = Path(directory)
    index = json.loads((directory / "index.json").read_text(encoding="utf-8"))
    docs = []
    for entry in index:
        text = (directory / entry["file"]).read_text(encoding="utf-8")
        doc = dict(entry)
        doc["text"] = text
        doc["lines"] = parse_lines(text)
        doc.setdefault("topic", entry["key"])
        docs.append(doc)
    return docs


def line_ids(corpus, current_only=False):
    """Every evidence id in the corpus, such as "a-L3". With current_only, superseded files are left out."""
    return {
        "%s-%s" % (d["key"], lid)
        for d in corpus
        if not (current_only and d["status"] == "superseded")
        for lid, _ in d["lines"]
    }


def manifest_of(corpus):
    """The index manifest: file, checksum and revision of every file in the index."""
    return [{"file": d["file"], "checksum": checksum(d["text"]), "revision": d["revision"]} for d in corpus]


def bump_version(version):
    """"reader-model-0412" -> "reader-model-0413": the digits at the end go up by one."""
    m = _VERSION.match(version)
    if not m:
        return version + "-next"
    return m.group(1) + str(int(m.group(2)) + 1).zfill(len(m.group(2)))


class GroundedAnswer(dict):
    """A dict that also allows answer.text, answer.claims and so on."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


class FakeGroundedAssistant:
    def __init__(self, corpus, flags=(), served_version="reader-model-0412", prompt_id="prompt-r1"):
        unknown = [f for f in flags if f not in FLAGS]
        if unknown:
            raise ValueError("unknown flag %s; the flags are %s" % (unknown[0], ", ".join(FLAGS)))
        self.corpus = corpus
        self.flags = tuple(flags)
        self.prompt_id = prompt_id
        self.base_version = served_version
        self.served_version = bump_version(served_version) if "drift" in self.flags else served_version

    def _eligible(self):
        superseded_topics = {d["topic"] for d in self.corpus if d["status"] == "superseded"}
        stale = "stale_note" in self.flags
        out = []
        for d in self.corpus:
            if d["topic"] in superseded_topics and stale:
                if d["status"] == "superseded":
                    out.append(d)
            elif d["status"] != "superseded":
                out.append(d)
        return out

    def answer(self, question):
        q = _words(question)
        best = None  # (best line score, sum of scores, -position, doc, scored lines)
        for pos, doc in enumerate(self._eligible()):
            scored = [(len(q & _words(text)), n, lid, text) for n, (lid, text) in enumerate(doc["lines"])]
            scored = [s for s in scored if s[0] > 0]
            if not scored:
                continue
            title_bonus = len(q & _words(doc.get("title", "")))
            key = (max(s[0] for s in scored) + title_bonus, sum(s[0] for s in scored), -pos)
            if best is None or key > best[0]:
                best = (key, doc, scored)
        claims = []
        retrieved = []
        if best is not None:
            _, doc, scored = best
            keep = 1 if "drift" in self.flags else MAX_CLAIMS
            floor = max(1, max(s[0] for s in scored) - 1)
            top = sorted([s for s in scored if s[0] >= floor], key=lambda s: (-s[0], s[1]))[:keep]
            for _, _, lid, text in sorted(top, key=lambda s: s[1]):
                evidence = "%s-%s" % (doc["key"], lid)
                retrieved.append(evidence)
                shown = text[len("Decision:"):].strip() if text.startswith("Decision:") else text
                shown = shown[:1].upper() + shown[1:]
                claims.append({"text": shown, "support": evidence})
            if "hallucinate" in self.flags:
                claims.append({"text": doc.get("invented") or INVENTED_BY_TOPIC.get(doc.get("topic"), DEFAULT_INVENTED), "support": None})
        text_out = " ".join(c["text"] for c in claims) if claims else NOT_FOUND
        return GroundedAnswer(
            question=question,
            text=text_out,
            claims=claims,
            retrieved=retrieved,
            served_version=self.served_version,
            prompt_id=self.prompt_id,
            manifest=manifest_of(self.corpus),
        )

    def run_questions(self, questions, run_date=None):
        """Runs a fixed question list and returns a run log.

        questions: a list of {"id", "question", "expected_fact"}. A question passes when its
        expected fact appears in the answer text (ignoring case).
        """
        results = []
        for q in questions:
            ans = self.answer(q["question"])
            results.append({"id": q["id"], "pass": q["expected_fact"].lower() in ans["text"].lower()})
        log = {
            "run_date": run_date,
            "served_version": self.served_version,
            "prompt_id": self.prompt_id,
            "manifest": manifest_of(self.corpus),
            "results": results,
        }
        return log
