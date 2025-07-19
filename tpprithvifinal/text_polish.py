import re
from typing import Tuple, List, Dict
import language_tool_python
from language_tool_python.utils import correct
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# === Load grammar model and tools ===
model_id = "prithivida/grammar_error_correcter_v1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
corrector = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
_tool = language_tool_python.LanguageTool('en-US')
MAX_TOKENS = tokenizer.model_max_length

# === Utility functions ===
def count_tokens(text: str) -> int:
    return len(tokenizer.tokenize(text))

def clean_spacing(text: str) -> str:
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    return re.sub(r'\s{2,}', ' ', text).strip()

def polish_text(text: str) -> Dict[str, object]:
    if count_tokens(text) > MAX_TOKENS:
        raise ValueError(f"Input text exceeds max token limit of {MAX_TOKENS} tokens.")

    matches = _tool.check(text)
    lt_corrected = correct(text, matches) if matches else text

    lt_issues = [{
        'message': m.message,
        'offset': str(m.offset),
        'length': str(m.errorLength),
        'replacements': ', '.join(m.replacements),
        'is_pos_issue': 'False'
    } for m in matches]

    result = corrector(lt_corrected, max_length=MAX_TOKENS)[0]['generated_text']
    polished = clean_spacing(result)

    return {
        "original": text,
        "polished": polished,
        "issues": lt_issues,
        "token_count": count_tokens(text)
    }

def split_into_sentences(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

def polish_full_text(input_text: str) -> Dict[str, object]:
    sentences_list = split_into_sentences(input_text)
    final_polished_text = ""
    all_issues = []
    all_details = []

    for idx, sentence in enumerate(sentences_list, 1):
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
        "total_sentences": len(sentences_list),
        "issues": all_issues
    }

# === Optional: Run as script ===
if __name__ == "__main__":
    try:
        input_text = input("Enter your text:\n")
        result = polish_full_text(input_text)

        print("\n=== FINAL POLISHED TEXT ===\n")
        print(result['polished_text'])

        print("\n=== DETAILS PER SENTENCE ===")
        for detail in result['details']:
            print(f"\nSentence {detail['sentence_number']}")
            print(f"Original: {detail['original']}")
            print(f"Polished: {detail['polished']}")
            print(f"Token count: {detail['token_count']}")
            print("Issues:")
            if detail['issues']:
                for i, issue in enumerate(detail['issues'], 1):
                    print(f"  {i}. {issue['message']} | Suggestions: {issue['replacements']}")
            else:
                print("  ✅ No issues found.")

        print(f"\n=== TOTAL TOKENS: {result['total_tokens']} ===")
        print(f"=== TOTAL SENTENCES: {result['total_sentences']} ===")

    except ValueError as e:
        print(f"❌ Error: {e}")
