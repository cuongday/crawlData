# import csv
# import docx
# import os
#
# # Paths to the uploaded files
# file_paths = [
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0001 - Senior PHP.docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0002 - Senior BA .docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0003 - Senior C++ Dev .docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0004 - Junior Java Dev.docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0006 - Senior C#.docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0007 - Senior .NET.docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0008 - Senior Angular.docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0011 - SAP HANA.docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0012 - Senior Angular .docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0013 - Senior ReactJS.docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0014 - SAP ABAP .docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0015- Senior Fullstack.docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/RQ0023 -Solution Architect (Team Lead).docx",
#     "D:/code/springAiLocal/createDataset/Data/rawData/Senior Mobile iOS .docx"
# ]
#
# # Define the CSV file path
# csv_file_path = "D:\code\springAiLocal\createDataset\Data\Dataset\job_descriptions.csv"
#
#
# # Function to read and extract data from a .docx file
# def extract_text_from_docx(file_path):
#     doc = docx.Document(file_path)
#     text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
#     return text
#
#
# # Function to parse job description text into dictionary
# def parse_job_description(text):
#     # Define sections based on typical JD formatting
#     sections = ["Job Title:", "Location:", "Company:", "About Us:", "Job Description:",
#                 "Key Responsibilities:", "Job Requirements:", "Contact:"]
#     data = {}
#     for i in range(len(sections) - 1):
#         start = text.find(sections[i])
#         end = text.find(sections[i + 1])
#         if start != -1:
#             data[sections[i][:-1]] = text[start + len(sections[i]): end].strip()
#     # Extract last section (Contact)
#     last_section = sections[-1][:-1]
#     if sections[-1] in text:
#         data[last_section] = text[text.find(sections[-1]) + len(sections[-1]):].strip()
#     return data
#
#
# # Collect data from each .docx file and save to CSV
# with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(["Job Title", "Location", "Company", "About Us", "Job Description",
#                      "Key Responsibilities", "Job Requirements", "Contact"])
#
#     for file_path in file_paths:
#         text = extract_text_from_docx(file_path)
#         job_data = parse_job_description(text)
#         writer.writerow([
#             job_data.get("Job Title", ""),
#             job_data.get("Location", ""),
#             job_data.get("Company", ""),
#             job_data.get("About Us", ""),
#             job_data.get("Job Description", ""),
#             job_data.get("Key Responsibilities", ""),
#             job_data.get("Job Requirements", ""),
#             job_data.get("Contact", "")
#         ])
#
# print("Data has been successfully written to", csv_file_path)

import requests
from bs4 import BeautifulSoup

def crawl_fastwork_data(url):
    """
    Crawls a webpage and extracts relevant data from it.

    Args:
        url: The URL of the webpage to crawl.

    Returns:
        A dictionary containing extracted data or None if an error occurs.
        Prints an error message if the extraction fails.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div (adapt to the actual structure of the page)
        # main_content = soup.find('div', class_='entry-content')
        #
        # if main_content:
        #     # Extract text content from the main content
        #     extracted_data = {
        #         "title": soup.find('h1', class_='entry-title').get_text(strip=True),
        #         "content": main_content.get_text(separator='\n', strip=True)
        #     }
        #
        #     return extracted_data
        #
        # else:
        #   print(f"Error: Main content div not found on page {url}")
        #   return None


    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    target_url = "https://fastwork.vn/hris-la-gi/"
    extracted_data = crawl_fastwork_data(target_url)

    if extracted_data:
        print("Extracted Data:")
        for key, value in extracted_data.items():
            print(f"- {key}: {value}")
