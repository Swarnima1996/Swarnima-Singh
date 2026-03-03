# Petstore API Test Framework

Automated test suite for the **PET** domain of the [Swagger Petstore API v2](https://petstore.swagger.io/v2).

Covers all CRUD operations: **Create**, **Read**, **Update**, and **Delete**.

---

## Tech Stack

| Tool | Purpose | Why chosen |
|------|---------|-----------|
| **Python 3.10+** | Language | Readable, concise, and great for test automation |
| **pytest** | Test runner | Industry standard with a powerful fixture system and plugin ecosystem |
| **requests** | HTTP client | Simple and reliable HTTP library with no unnecessary overhead |
| **Faker** | Test data generation | Generates realistic randomised data so tests do not rely on hardcoded values |
| **pytest-html** | Reporting | Produces self-contained HTML reports that are easy to share |
| **python-dotenv** | Configuration | Keeps environment-specific config out of the source code |

---

## Project Structure

```
petstore-api-tests/
├── config/
│   ├── __init__.py
│   └── settings.py              # Base URL, timeout, API key
├── clients/
│   ├── __init__.py
│   └── pet_client.py            # All HTTP calls to the /pet endpoints
├── models/
│   ├── __init__.py
│   └── pet.py                   # Pet dataclass and PetFactory for test data
├── tests/
│   ├── __init__.py
│   └── pet/
│       ├── __init__.py
│       ├── test_create_pet.py   # POST /pet
│       ├── test_read_pet.py     # GET /pet/{id}, findByStatus, findByTags
│       ├── test_update_pet.py   # PUT /pet, POST /pet/{id}
│       └── test_delete_pet.py   # DELETE /pet/{id}
├── utils/
│   └── assertions.py            # Shared assertion helpers
├── conftest.py                  # Shared fixtures
├── pytest.ini                   # pytest config and markers
├── requirements.txt             # Dependencies
└── reports/
    └── test_report.html         # Generated test report
```

---

## Setup

### Prerequisites
- Python 3.10 or higher
- pip

### 1. Clone the repository
```bash
git clone https://github.com/Swarnima1996/Swarnima-Singh.git
cd Swarnima-Singh/petstore-api-tests
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment configuration (optional)
The default base URL points to the live Swagger Petstore v2. To override, create a `.env` file:
```
BASE_URL=https://petstore.swagger.io/v2
REQUEST_TIMEOUT=10
API_KEY=special-key
```

---

## How to Run Tests

```bash
export PYTHONPATH=$PYTHONPATH:.
```

### Run the full suite
```bash
pytest
```

### Run only smoke tests
```bash
pytest -m smoke
```

### Run by CRUD operation
```bash
pytest -m create
pytest -m read
pytest -m update
pytest -m delete
```

### Run only negative tests
```bash
pytest -m negative
```

### Run a single file
```bash
pytest tests/pet/test_create_pet.py
```

### Run with detailed output
```bash
pytest -v -s
```

### Open the HTML report
```bash
open reports/test_report.html
```

---

## Approach & Design Decisions

### Layered Architecture
The framework is divided into separate layers so each part has one clear responsibility:

- **Config** — all environment values are in one place. Switching the target server means changing one line.
- **Client** — `PetClient` is the only place that makes HTTP calls. Tests never use `requests` directly, so adding headers or auth is a single-file change.
- **Models** — `Pet` is a typed dataclass. `PetFactory` builds randomised test data using Faker so tests never share hardcoded IDs or names.
- **Tests** — test files only contain assertions. No HTTP logic, no data generation.

### Test Isolation via Fixtures
The `created_pet` fixture in `conftest.py` creates a pet before each test and deletes it in teardown, whether the test passes or fails. This means tests never share state through the API, a failed test does not leave data that affects the next one, and tests can run in any order.

### Custom Markers
Tests are tagged with markers (`smoke`, `create`, `read`, `update`, `delete`, `negative`) so you can run targeted subsets. For example, just smoke tests for a quick check or just negative tests to verify error handling.

### Negative Testing
Every CRUD operation includes negative tests for non-existent IDs (expect 404), invalid input types (expect 400), and invalid enum values.

### Randomised Test Data
Faker and random generate unique pet names and IDs on every run so tests do not depend on any pre-existing data in the shared sandbox.

---

## Test Results

**Executed against:** `https://petstore.swagger.io/v2`
**Environment:** macOS, Python 3.10+
**Full report:** `reports/test_report.html`

### API Issues Found During Testing

Some tests fail because the live Petstore API does not fully follow its own OpenAPI specification. These are expected findings — the tests are correctly identifying real gaps:

| #    | Issue | Endpoint | Expected | Actual |
|------|-------|----------|----------|--------|
| F-01 | PUT with a non-existent ID creates a new pet instead of returning 404 | PUT /pet | 404 | 200 |
| F-02 | Non-integer path parameter returns 404 instead of 400 | GET, DELETE /pet/{id} | 400 | 404 |
| F-03 | Invalid status value accepted with 200 OK — spec enum not enforced | POST /pet | 400 | 200 |
| F-04 | Data changes occasionally do not persist due to shared sandbox usage | PUT /pet | Persisted | Not persisted |

---

## Notes

The Petstore at `petstore.swagger.io/v2` is a public shared environment — anyone on the internet can modify data at any time. A small number of tests may produce inconsistent results because of this. For stable results, the tests can be run against a locally hosted instance using Docker.