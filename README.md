# Job Description to Portfolio Matcher with Cold Email Generator

### This tool is ideal for business development executives, recruiters, or agencies looking to create targeted outreach and enhance hiring efficiency.

This Streamlit application provides a seamless way to match job descriptions from company career pages with suitable developer portfolios, helping business development executives craft targeted outreach. The application automates the following workflow:

## Job Description Scraping:
Users can input a job posting URL, and the app will scrape and extract relevant job details such as role, required skills, and experience using web scraping tools.

## Data Structuring with LLMs:
Leveraging the power of large language models, the application processes the scraped content into a structured JSON format, containing:

Role
Experience
Required skills
Description
Portfolio Database Management:
The application utilizes a CSV file containing developer portfolios, organized by tech stack and links. These are stored in a vector database for fast and efficient querying.

## Profile Matching:
Using a vector similarity engine, the application matches the skills required in the job description to the most relevant developer portfolios from the database.

## Cold Email Generation:
The app automatically generates a customized cold email based on:

The extracted job description.
Matched portfolios from the database. The email showcases how the team can meet the employer's needs while highlighting relevant projects from the portfolio.

## User-Friendly Interface:
The application is interactive, providing users with an intuitive and streamlined experience for uploading CSVs, entering job URLs, and generating actionable results.
