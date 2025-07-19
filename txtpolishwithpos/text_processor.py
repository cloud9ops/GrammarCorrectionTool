import re
import spacy
import lemminflect  # registers ._.inflect
import language_tool_python
from language_tool_python.utils import correct
from typing import Tuple, List, Dict

# Initialize tools
nlp = spacy.load("en_core_web_trf")  # You can change model here if needed
_tool = language_tool_python.LanguageTool('en-US')

# Temporal context hints
PAST_HINTS = {"yesterday", "last", "ago", "earlier", "previously", "once"}
PRESENT_HINTS = {"today", "now", "currently", "at present"}
FUTURE_HINTS = {"tomorrow", "next", "later", "soon"}

def clean_spacing(text: str) -> str:
    """
    Cleans up unnecessary spaces around punctuation.
    """
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    return re.sub(r'\s{2,}', ' ', text).strip()

def detect_temporal_context(text: str) -> str:
    """
    Infers temporal context (past, present, future) from keywords.
    """
    lowered = text.lower()
    if any(word in lowered for word in PAST_HINTS):
        return "past"
    elif any(word in lowered for word in FUTURE_HINTS):
        return "future"
    elif any(word in lowered for word in PRESENT_HINTS):
        return "present"
    return "unknown"

def analyze_pos_agreement(text: str) -> Tuple[List[Dict[str, str]], str]:
    """
    Applies rule-based POS agreement and tense corrections.
    """
    doc = nlp(text)
    corrected_tokens = [token.text for token in doc]
    issues = []
    context = detect_temporal_context(text)

    for i, token in enumerate(doc):
        next_token = doc[i + 1] if i + 1 < len(doc) else None

        # Rule 1: Singular subject with base/plural verb → needs 3rd person singular
        if token.dep_ == "nsubj" and token.tag_ in {"NN", "NNP"}:
            if next_token and next_token.tag_ in {"VBP", "VB"}:
                inflected = next_token._.inflect("VBZ")
                if inflected and inflected != next_token.text:
                    corrected_tokens[next_token.i] = inflected
                    issues.append({
                        'message': f"'{token.text} {next_token.text}' → '{token.text} {inflected}'",
                        'offset': str(token.idx),
                        'length': str(len(f"{token.text} {next_token.text}")),
                        'replacements': inflected,
                        'is_pos_issue': 'True'
                    })

        # Rule 2: Modal + past tense → use base verb
        if token.tag_ == "MD" and next_token and next_token.tag_ == "VBD":
            inflected = next_token._.inflect("VB")
            if inflected and inflected != next_token.text:
                corrected_tokens[next_token.i] = inflected
                issues.append({
                    'message': f"Modal '{token.text}' with past tense '{next_token.text}' → '{inflected}'",
                    'offset': str(next_token.idx),
                    'length': str(len(next_token.text)),
                    'replacements': inflected,
                    'is_pos_issue': 'True'
                })

        # Rule 3: Pronoun + incorrect "be" verb
        if token.dep_ == "nsubj" and token.tag_ == "PRP":
            if next_token and next_token.lemma_ == "be":
                subj, verb = token.text.lower(), next_token.text.lower()
                correct_form = (
                    "is" if subj in {"he", "she", "it"} else
                    "am" if subj == "i" else
                    "are" if subj in {"we", "you", "they"} else
                    None
                )
                if correct_form and correct_form != verb:
                    corrected_tokens[next_token.i] = correct_form
                    issues.append({
                        'message': f"'{token.text} {next_token.text}' → '{token.text} {correct_form}'",
                        'offset': str(token.idx),
                        'length': str(len(f"{token.text} {next_token.text}")),
                        'replacements': correct_form,
                        'is_pos_issue': 'True'
                    })

        # Rule 4: Verb tense mismatch based on inferred context
        if token.pos_ == "VERB" and token.tag_ not in {"MD"}:
            desired_tag = None
            if context == "past" and token.tag_ in {"VB", "VBP", "VBZ"}:
                desired_tag = "VBD"
            elif context == "present" and token.tag_ == "VBD":
                desired_tag = "VBZ"

            if desired_tag:
                inflected = token._.inflect(desired_tag)
                if inflected and inflected != token.text:
                    corrected_tokens[token.i] = inflected
                    issues.append({
                        'message': f"Tense mismatch: '{token.text}' should be '{inflected}'",
                        'offset': str(token.idx),
                        'length': str(len(token.text)),
                        'replacements': inflected,
                        'is_pos_issue': 'True'
                    })

    corrected_text = " ".join(corrected_tokens)
    return issues, corrected_text

def polish_text(text: str) -> Tuple[str, str, List[Dict[str, str]]]:
    """
    Applies grammar corrections (LanguageTool) and POS/tenses fixes (SpaCy + lemminflect).
    Returns original text, final polished version, and all correction metadata.
    """
    # Step 1: Grammar fixes via LanguageTool
    matches = _tool.check(text)
    lt_corrected = correct(text, matches) if matches else text

    lt_issues = [{
        'message': m.message,
        'offset': str(m.offset),
        'length': str(m.errorLength),
        'replacements': ', '.join(m.replacements),
        'is_pos_issue': 'False'
    } for m in matches]

    # Step 2: POS & tense fixes
    pos_issues, pos_corrected = analyze_pos_agreement(lt_corrected)

    # Step 3: Cleanup
    polished_text = clean_spacing(pos_corrected)

    return text, polished_text, lt_issues + pos_issues
