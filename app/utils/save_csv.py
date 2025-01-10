import csv

def save_to_csv(results, output_path="output.csv"):
    with open(output_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "file_name", "name", "phone", "email", "location", "skills", "experience", "contact_url"
        ])
        writer.writeheader()
        for result in results:
            writer.writerow({
                "file_name": result.get("file_name", "N/A"),
                "name": result.get("name", "N/A"),
                "phone": result.get("phone", "N/A"),
                "email": result.get("email", "N/A"),
                "location": result.get("location", "N/A"),
                "skills": ", ".join(result.get("skills", [])),  # Convert list to string
                "experience": result.get("experience", "N/A"),
                "contact_url": result.get("contact_url", {}).get("email", "N/A")  # Lấy email từ contact_url
            })
