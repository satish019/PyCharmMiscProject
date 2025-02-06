from transformers import    pipeline
summarizer = pipeline('summarization', model="facebook/bart-large-cnn")
def summarize_results(results):
    data_str = "\n".join([str(row) for row in results])
    summary = summarizer(data_str, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']
