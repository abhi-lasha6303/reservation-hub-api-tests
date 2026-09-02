# Reservation Hub API Test Automation

## Overview

This project contains an automated API test suite for the Restful Booker API.

The framework is built using **Python, pytest, and requests** and is designed to validate functional behavior, authentication, CRUD operations, response contracts, search/filtering, and negative/boundary scenarios.

**Base URL:** `https://restful-booker.herokuapp.com`

---

## Test Strategy

The test suite follows a layered API automation approach.

### 1. Configuration Layer

The configuration layer stores:

* Base URL
* API credentials
* Request timeout

Environment-specific values are loaded from the `.env` file.

### 2. HTTP Client Layer

`clients/http_client.py` provides reusable HTTP request handling.

It:

* Sends GET, POST, PUT, PATCH, and DELETE requests.
* Applies the configured base URL and timeout.
* Captures request and response information for the HTML report.

### 3. API Client Layer

`clients/booking_api.py` provides reusable methods for:

* Authentication
* Creating bookings
* Getting bookings
* Updating bookings using PUT
* Updating bookings using PATCH
* Deleting bookings
* Listing/filtering bookings
* Health check

### 4. Pytest Fixtures

`conftest.py` provides shared fixtures for:

* API client
* Authentication token
* Booking payload
* Dynamically created booking data

Tests avoid depending on pre-existing booking IDs for the main CRUD workflow.

### 5. Test Layer

Tests are organized by feature and use pytest markers.

Assertions validate both:

* HTTP status codes
* Response body/content

---

## Test Coverage

### Authentication

The suite covers:

* Successful authentication
* Invalid credentials
* PUT without authentication
* PUT with invalid authentication
* PATCH without authentication
* PATCH with invalid authentication
* DELETE without authentication
* DELETE with invalid authentication

### Booking CRUD

The suite covers:

* Create booking
* Retrieve created booking
* Full update using PUT
* Partial update using PATCH
* Delete booking
* Verify deleted booking returns 404

### Response Contract

The suite validates:

* Create booking response structure
* Get booking response structure
* Required response fields
* Response field types

### Booking Search

The suite covers:

* List all bookings
* Filter by first name
* Filter by last name
* Filter by check-in date
* Filter by check-out date

### Negative and Boundary Testing

The suite validates:

* Missing required fields
* Empty payload
* Zero price
* Negative price
* Invalid price types
* Invalid date formats
* Invalid dates
* Checkout before check-in
* Invalid `firstname` types
* Non-existent booking IDs
* Zero booking ID
* Negative booking ID

### Health Check

The suite validates the `/ping` endpoint.

---

## Test Results

The latest complete execution collected:

```text
45 tests
24 passed
21 failed
```

The 21 failures are concentrated in negative and boundary validation tests.

These failures are intentional because the tests assert the expected API behavior. The API currently accepts or incorrectly processes several invalid inputs.

The identified defects are documented in:

```text
BUGS.md
```

The main defects identified include:

* Zero and negative booking prices being accepted
* Malformed and invalid dates being accepted
* Invalid `firstname` types causing HTTP 500
* Missing required fields causing HTTP 500
* Empty booking payload causing HTTP 500

The passing tests demonstrate successful behavior for the tested authentication, CRUD, search, contract, and health-check scenarios.

---

## Project Structure

```text
reservation-hub-api-tests/
│
├── clients/
│   ├── http_client.py
│   └── booking_api.py
│
├── config/
│   └── settings.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_booking_auth.py
│   ├── test_booking_contract.py
│   ├── test_booking_crud.py
│   ├── test_booking_list.py
│   ├── test_booking_validation.py
│   └── test_health.py
│
├── reports/
│   └── test-report.html
│
├── .env
├── .gitignore
├── BUGS.md
├── conftest.py
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## Pytest Markers

The tests are grouped using pytest markers:

```text
health
auth
create
read
update
delete
contract
search
critical
high
medium
defect
```

### Run authentication tests

```powershell
pytest -v -m auth
```

### Run CRUD tests

```powershell
pytest -v -m "create or read or update or delete"
```

### Run contract tests

```powershell
pytest -v -m contract
```

### Run the complete suite

```powershell
pytest -v
```

---

## How to Run

### 1. Activate the virtual environment

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file containing the required configuration.

Example:

```text
BASE_URL=https://restful-booker.herokuapp.com
USERNAME=KalavakuriAbhilasha
PASSWORD=password123
```

Credentials should not be committed to source control in a real project.

### 4. Run the complete test suite

```powershell
pytest -v
```

---

## Test Report

The project uses `pytest-html` to generate a self-contained HTML report.

The report is generated at:

```text
reports/test-report.html
```

The report contains:

* Overall test results
* Passed tests
* Failed tests
* Test duration
* Failure details
* Request information
* Response status
* Response body

The report is regenerated when the test suite is executed again.

---

## Environment and Test Data Considerations

The Restful Booker API is a shared sandbox environment.

The main CRUD tests create their own booking data and use the booking created during the test instead of depending on fixed booking IDs.

The shared environment can still introduce external factors such as:

* Concurrent users
* Data changes by other test runs
* Sandbox resets
* Temporary API instability
* Network failures
* API-side defects

Therefore, environmental failures should be distinguished from reproducible application defects.

---

## Included Scope

The following areas are included:

* Booking API functionality
* Authentication
* Authorization checks for write operations
* CRUD operations
* Search and filtering
* Input validation
* Boundary testing
* Response contract validation
* Health endpoint
* HTML test reporting

---

## Excluded Scope

The following are outside the current assignment scope:

* UI testing
* Database-level validation
* Large-scale load testing
* Stress testing
* Security penetration testing
* Production deployment testing
* Full performance benchmarking

---

## Limitations

The API is a public/shared sandbox rather than a controlled production environment.

Because of this:

* Test data can be affected by other users.
* The environment may reset.
* API behavior may change.
* Network availability can affect test execution.
* Some invalid requests currently return unexpected server errors.

The negative tests intentionally assert expected behavior and are not weakened simply to achieve a 100% pass rate.

---

## Defect Handling

When an API behavior does not meet the expected contract, the corresponding automated test fails.

Confirmed defects are documented separately in:

```text
BUGS.md
```

Each documented defect contains:

* Defect ID
* Title
* Severity
* Description
* Reproducible request
* Expected result
* Actual result
* Impact
* Automated test reference

---

## Conclusion

This project provides a reusable API automation framework with clear separation between configuration, HTTP communication, API operations, fixtures, and test cases.

The suite contains **45 automated tests** covering positive, negative, boundary, authentication, CRUD, search, health, and response-contract scenarios.

The latest execution produced:

```text
24 passed
21 failed
```

The failures provide reproducible evidence of API validation defects and are documented in `BUGS.md`.
