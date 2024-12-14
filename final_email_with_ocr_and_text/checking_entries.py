import json

# Simulate reading the JSON data
with open('/data/aiuserinj/sarjil/mail_summarizer/final_email_with_ocr_and_text/all_email_results_aug_18.json') as f:
    data = json.load(f)

# Print out the number of entries
print(f"Number of entries: {len(data)}")

# Print out each entry
for entry in data:
    print(json.dumps(entry, indent=4))
