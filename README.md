# InteliLink (only ~ 95% ready, still testing)
#### new release version 2.0 (2024)

InteliLink is a web scraper designed to check publicly accessible websites from a list of domains, extract imprint and contact information, and match this information with an existing CSV database. If the contact information is not in the database, it will be added.

## Table of Contents

- [Project Goal](#project-goal)
- [Data Sources](#data-sources)
- [Features](#features)
- [Workflow](#workflow)
- [Setup](#setup)
- [Usage](#usage)
- [Logging](#logging)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Project Goal

The goal of this project is to create a web scraper named InteliLink that:

1. Checks publicly accessible websites from a list of domains.
2. Extracts imprint and contact information using regex and pattern matching techniques.
3. Matches the extracted data with an existing CSV database.
4. Adds new contact information to the database if not already present.

## Data Sources

- **Domain List**: A text file containing the domains to be checked.
- **Proxy List**: A text file containing proxies in the format `ip:port`.
- **CSV Database**: A CSV file with existing contact data (columns: Name, Address, Phone, Fax, Mobile, Email, Website, Social Network Accounts).

## Features

- **Load Proxies**: Load proxies from a file.
- **Load Domains**: Load domains from a file.
- **Load and Save CSV Database**: Read and update the CSV file.
- **Fetch Website**: Retrieve a website using a randomly selected proxy.
- **Extract Data**: Extract imprint and contact information from the HTML content using regex and pattern matching techniques.
- **Match Data**: Compare new data with existing data in the CSV database.
- **Save New Data**: Insert new data into the CSV database.

## Workflow

1. **Initialization**:
   - Load proxies and domains from their respective files.
   - Load existing contact data from the CSV database.
2. **Website Checking**:
   - For each domain:
     - Select a random proxy.
     - Fetch the website.
     - Extract imprint and contact information using regex and pattern matching techniques.
3. **Data Matching**:
   - Compare the extracted data with existing data in the CSV database.
   - Add new data if it is not already present.
4. **Saving**:
   - Save the updated CSV database.

## Setup

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/InteliLink.git
    cd InteliLink
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the setup script to create the necessary directory structure and files:

    ```bash
    python setup_project.py
    ```

## Usage

1. Place your domain list in `data/domains.txt`.
2. Place your proxy list in `data/proxies.txt`.
3. Ensure your CSV database is available in `data/contacts.csv`.
4. Run the main script:

    ```bash
    python src/main.py
    ```

## Logging

Logging information is stored in `logs/scraping.log`. The log file contains detailed information about the scraping process, including errors and successful operations.

## Testing

To run the tests, use the following command:

```bash
python -m unittest discover -s tests
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request.

## ❤️ Thank you for your support!
If you appreciate my work, please consider supporting me:

- Become a Sponsor: [Link to my sponsorship page](https://github.com/sponsors/volkansah)
- :star: my projects: Starring projects on GitHub helps increase their visibility and can help others find my work. 
- Follow me: Stay updated with my latest projects and releases.

## License Privat, till yet!
 

