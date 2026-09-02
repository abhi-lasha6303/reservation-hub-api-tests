# API Bug Report

## Overview

The automated API test suite identified multiple validation defects in the booking creation endpoint.

**API under test:** Restful Booker
**Endpoint:** `POST /booking`
**Environment:** `https://restful-booker.herokuapp.com`

The defects below were reproduced through automated pytest tests and verified from the actual API responses.

---

# BUG-001 — API accepts zero and negative booking prices

**Severity:** High

**Endpoint:** `POST /booking`

### Description

The API accepts invalid `totalprice` values such as `0`, `-1`, and `-100` and successfully creates a booking.

A booking price should not be zero or negative for a valid booking. The API should validate the value and reject invalid prices with a client-side validation response.

### Reproducible request

```bash
curl -X POST "https://restful-booker.herokuapp.com/booking" ^
  -H "Content-Type: application/json" ^
  -d "{\"firstname\":\"Abhi\",\"lastname\":\"Tester\",\"totalprice\":-100,\"depositpaid\":true,\"bookingdates\":{\"checkin\":\"2026-09-10\",\"checkout\":\"2026-09-15\"},\"additionalneeds\":\"Breakfast\"}"
```

### Test data

```json
{
  "firstname": "Abhi",
  "lastname": "Tester",
  "totalprice": -100,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-09-10",
    "checkout": "2026-09-15"
  },
  "additionalneeds": "Breakfast"
}
```

### Expected result

The API should reject the request with:

```text
HTTP 400 Bad Request
```

or:

```text
HTTP 422 Unprocessable Entity
```

No booking should be created.

### Actual result

The API returned:

```text
HTTP 200 OK
```

and created a booking with:

```json
"totalprice": -100
```

The automated test reported:

```text
Actual status: 200
```

### Impact

Invalid financial data can be stored in the system. This can result in incorrect booking amounts and downstream data-integrity issues.

### Automated test

```text
tests/test_booking_validation.py::test_create_booking_invalid_price
```

The test was executed with values:

```text
0
-1
-100
```

All three invalid values were accepted by the API.

---

# BUG-002 — API accepts malformed booking dates

**Severity:** High

**Endpoint:** `POST /booking`

### Description

The API accepts malformed or invalid booking dates instead of rejecting them.

For invalid date values, the API can return a successful response containing corrupted date values such as:

```text
0NaN-aN-aN
```

The API should validate that `checkin` and `checkout` are valid dates in the expected format.

### Reproducible request

```bash
curl -X POST "https://restful-booker.herokuapp.com/booking" ^
  -H "Content-Type: application/json" ^
  -d "{\"firstname\":\"Abhi\",\"lastname\":\"Tester\",\"totalprice\":150,\"depositpaid\":true,\"bookingdates\":{\"checkin\":\"invalid-date\",\"checkout\":\"2026-09-15\"},\"additionalneeds\":\"Breakfast\"}"
```

### Test data

```json
{
  "firstname": "Abhi",
  "lastname": "Tester",
  "totalprice": 150,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "invalid-date",
    "checkout": "2026-09-15"
  },
  "additionalneeds": "Breakfast"
}
```

### Expected result

The API should reject the malformed date with:

```text
HTTP 400 Bad Request
```

or:

```text
HTTP 422 Unprocessable Entity
```

No booking should be created.

### Actual result

The API returned:

```text
HTTP 200 OK
```

and created a booking containing:

```json
"bookingdates": {
  "checkin": "0NaN-aN-aN",
  "checkout": "2026-09-15"
}
```

### Additional observations

The automated tests also identified other date-validation problems:

| Input                    | Actual behavior                        |
| ------------------------ | -------------------------------------- |
| `10-09-2026`             | Accepted and converted incorrectly     |
| `2026/09/10`             | Accepted                               |
| `invalid-date`           | Accepted and converted to `0NaN-aN-aN` |
| Empty check-in date      | Accepted and converted to `0NaN-aN-aN` |
| Checkout before check-in | Accepted                               |

For example:

```text
checkin: 2026-09-20
checkout: 2026-09-10
```

was accepted with:

```text
HTTP 200 OK
```

### Impact

Invalid or corrupted booking dates can result in incorrect reservation periods, unreliable search/filter behavior, and data-integrity problems.

### Automated test

```text
tests/test_booking_validation.py::test_create_booking_malformed_dates
```

and:

```text
tests/test_booking_validation.py::test_create_booking_checkout_before_checkin
```

---

# BUG-003 — Invalid firstname data causes HTTP 500

**Severity:** High

**Endpoint:** `POST /booking`

### Description

The API returns an internal server error when `firstname` is supplied with an invalid data type.

Instead of returning a client validation error, the API responds with:

```text
HTTP 500 Internal Server Error
```

This indicates that invalid client input is reaching server-side processing without being handled correctly.

### Reproducible request

```bash
curl -X POST "https://restful-booker.herokuapp.com/booking" ^
  -H "Content-Type: application/json" ^
  -d "{\"firstname\":123,\"lastname\":\"Tester\",\"totalprice\":150,\"depositpaid\":true,\"bookingdates\":{\"checkin\":\"2026-09-10\",\"checkout\":\"2026-09-15\"},\"additionalneeds\":\"Breakfast\"}"
```

### Test data

```json
{
  "firstname": 123,
  "lastname": "Tester",
  "totalprice": 150,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2026-09-10",
    "checkout": "2026-09-15"
  },
  "additionalneeds": "Breakfast"
}
```

### Expected result

The API should reject the invalid `firstname` type with:

```text
HTTP 400 Bad Request
```

or:

```text
HTTP 422 Unprocessable Entity
```

The response should provide a meaningful validation error.

### Actual result

The API returned:

```text
HTTP 500 Internal Server Error
```

with:

```text
Internal Server Error
```

### Additional invalid values tested

The automated suite also tested:

```text
firstname = 123
firstname = true
firstname = []
firstname = {}
```

All four cases resulted in:

```text
HTTP 500 Internal Server Error
```

### Impact

Invalid user input should not cause an internal server error. Returning HTTP 500 exposes poor input handling and can make client-side troubleshooting difficult. It may also indicate an unhandled server-side exception.

### Automated test

```text
tests/test_booking_validation.py::test_create_booking_wrong_firstname_type
```

---

# Additional Validation Findings

The test suite identified additional validation issues that are not included as separate primary bugs above.

## Missing required fields

Requests missing `firstname`, `lastname`, or both returned:

```text
HTTP 500 Internal Server Error
```

Expected:

```text
HTTP 400 or 422
```

Automated test:

```text
tests/test_booking_validation.py::test_create_booking_missing_required_field
```

## Empty request body

An empty JSON payload:

```json
{}
```

returned:

```text
HTTP 500 Internal Server Error
```

Expected:

```text
HTTP 400 or 422
```

Automated test:

```text
tests/test_booking_validation.py::test_create_booking_empty_payload
```

## Invalid totalprice types

The API also accepted invalid `totalprice` values such as:

```text
"100"
"one hundred"
null
[]
```

Some values were converted or stored as `null` instead of being rejected.

Automated test:

```text
tests/test_booking_validation.py::test_create_booking_wrong_price_type
```

---

# Test Execution Evidence

The complete automated suite collected:

```text
45 tests
```

Final execution result:

```text
24 passed
21 failed
```

The 21 failures occurred in the validation tests because the API did not reject invalid input as expected.

The successful tests covered:

* Authentication
* Invalid authentication
* PUT authentication protection
* PATCH authentication protection
* DELETE authentication protection
* Booking creation
* Booking retrieval
* PUT update
* PATCH update
* Booking deletion
* Booking response contract
* Booking search/filtering
* Health check

The generated HTML test report is available at:

```text
reports/test-report.html
```

---

# Conclusion

The automated test suite successfully identified multiple API input-validation defects.

The most significant issues are:

1. **Invalid financial values are accepted.**
2. **Malformed and logically invalid dates are accepted.**
3. **Invalid field types result in HTTP 500 instead of a client validation error.**

These findings demonstrate that the API currently lacks robust validation for several invalid booking creation scenarios.
