import csv

def get_suggestion(symptom):
    with open('suggestion1.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Symptom'].lower() == symptom.lower():
                return row['Home Care Suggestions']

    return "Symptom not found. Please enter a valid symptom."


user_symptom = input("Enter a symptom: ")
suggestion = get_suggestion(user_symptom)

print(f"\nHome Care Suggestion for '{user_symptom}':\n{suggestion}")
