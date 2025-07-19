import re
from typing import List, Dict, Generator
import language_tool_python
from language_tool_python.utils import correct
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import spacy

# === Load models and tools ===
model_id = "prithivida/grammar_error_correcter_v1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
corrector = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
_tool = language_tool_python.LanguageTool('en-US')
nlp = spacy.load("en_core_web_sm")
MAX_TOKENS = tokenizer.model_max_length

# === Token count helper ===
def count_tokens(text: str) -> int:
    return len(tokenizer.tokenize(text))

# === Spacing cleaner ===
def clean_spacing(text: str) -> str:
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    return re.sub(r'\s{2,}', ' ', text).strip()

# === Custom spaCy pattern checker ===
singular_to_plural_dets = {"this": "these", "that": "those"}
singular_aux_to_plural = {"is": "are", "was": "were"}

def detect_determiner_verb_noun_mismatch(text: str) -> List[Dict[str, str]]:
    doc = nlp(text)
    issues = []

    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "ROOT" and token.pos_ == "AUX" and token.text.lower() in singular_aux_to_plural:
                verb = token
                subj = next((child for child in verb.children if child.dep_ == "nsubj" and child.text.lower() in singular_to_plural_dets), None)
                attr = next((child for child in verb.children if child.dep_ == "attr" and child.tag_ == "NNS"), None)

                if subj and attr:
                    suggestions = [
                        f"{singular_to_plural_dets[subj.text.lower()].capitalize()} {singular_aux_to_plural[verb.text.lower()]} {attr.text}",
                        f"{subj.text} {verb.text} {attr.lemma_}"
                    ]
                    issues.append({
                        "message": f"Mismatch: singular subject '{subj.text}' with plural noun '{attr.text}' via verb '{verb.text}'.",
                        "offset": str(subj.idx),
                        "length": str(len(subj) + len(verb) + len(attr) + 2),
                        "replacements": ', '.join(suggestions),
                        "is_pos_issue": 'True'
                    })

    return issues

def detect_missing_articles(text: str) -> List[Dict[str, str]]:
    doc = nlp(text)
    issues = []

    for sent in doc.sents:
        for token in sent:
            if token.pos_ == "NOUN" and token.tag_ == "NN":
                has_determiner = any(child.dep_ == "det" for child in token.children)
                is_named_entity = token.ent_type_ != ""
                is_compound_noun = any(child.dep_ == "compound" and child.pos_ == "NOUN" for child in token.children)

                if not has_determiner and not is_named_entity and not is_compound_noun:
                    if token.text.lower()[0] in "aeiou":
                        issues.append({
                            "message": f"Missing article an/the before noun '{token.text}'",
                            "offset": str(token.idx),
                            "length": str(len(token)),
                            "replacements": "an, the",
                            "is_pos_issue": 'True'
                        })
                    else:
                        issues.append({
                            "message": f"Missing article a/the before noun '{token.text}'",
                            "offset": str(token.idx),
                            "length": str(len(token)),
                            "replacements": "a, the",
                            "is_pos_issue": 'True'
                        })

    return issues

# === Full grammar + polish pipeline ===
def polish_text(text: str) -> Dict[str, object]:
    if count_tokens(text) > MAX_TOKENS:
        raise ValueError(f"Input text exceeds max token limit of {MAX_TOKENS} tokens.")

    # LanguageTool
    matches = _tool.check(text)
    lt_corrected = correct(text, matches) if matches else text
    lt_issues = [{
        'message': m.message,
        'offset': str(m.offset),
        'length': str(m.errorLength),
        'replacements': ', '.join(m.replacements),
        'is_pos_issue': 'False'
    } for m in matches]

    # Custom spaCy mismatch issues
    spacy_issues = detect_determiner_verb_noun_mismatch(text) + detect_missing_articles(text)

    all_issues = lt_issues + spacy_issues

    # Generate polished version
    result = corrector(lt_corrected, max_length=MAX_TOKENS)[0]['generated_text']
    polished = clean_spacing(result)

    return {
        "original": text,
        "polished": polished,
        "issues": all_issues,
        "token_count": count_tokens(text)
    }

# === Sentence splitting ===
def split_into_sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip()) if s.strip()]

# === Streaming polish per sentence ===
def stream_polish_sentences(input_text: str) -> Generator[Dict[str, object], None, None]:
    for idx, sentence in enumerate(split_into_sentences(input_text), 1):
        result = polish_text(sentence)
        yield {
            "sentence_number": idx,
            "original": result['original'],
            "polished": result['polished'],
            "issues": result['issues'],
            "token_count": result['token_count']
        }

# === Full doc correction ===
def polish_full_text(input_text: str) -> Dict[str, object]:
    final_polished_text = ""
    all_issues = []
    all_details = []

    for idx, sentence in enumerate(split_into_sentences(input_text), 1):
        result = polish_text(sentence)
        final_polished_text += result['polished'] + " "
        all_issues.extend(result['issues'])
        all_details.append({
            "sentence_number": idx,
            "original": result['original'],
            "polished": result['polished'],
            "issues": result['issues'],
            "token_count": result['token_count']
        })

    return {
        "polished_text": final_polished_text.strip(),
        "details": all_details,
        "total_tokens": count_tokens(input_text),
        "total_sentences": len(all_details),
        "issues": all_issues
    }

# === CLI Mode ===
if __name__ == "__main__":
    try:
        input_text = input("Enter your text:\n")

        print("\n=== STREAMED POLISHED SENTENCES ===")
        for detail in stream_polish_sentences(input_text):
            print(f"\nSentence {detail['sentence_number']}")
            print(f"Original: {detail['original']}")
            print(f"Polished: {detail['polished']}")
            print(f"Token count: {detail['token_count']}")
            if detail['issues']:
                print("Issues:")
                for i, issue in enumerate(detail['issues'], 1):
                    print(f"  {i}. {issue['message']}")
                    print(f"     Suggestions: {issue['replacements']}")
            else:
                print("  ✅ No issues found.")

    except ValueError as e:
        print(f"❌ Error: {e}")
