# Importance Note

Please spend time reading these documents first before going deeper:
- [How to use venv](venv_usage_guide.md)

---

# Structure Explanation

```bash
.
├── app
│   ├── databases
│   ├── models
│   ├── routers
│   ├── services
│   └── utils
└── venv
```

- `app`: The main application folder.
  - `databases`: Contains connections and methods to interact with the database.
  - `models`: Defines the data structure.
  - `routers`: Handles API endpoints.
  - `services`: Implements business logic.
  - `utils`: Stores core utility functions for the project.

---

# Coding Style

- **File Naming**:
  - File names must use underscores (`_`) between words, e.g., `convert_day.py`, `traffic_count.py`.

- **Function Naming**:
  - Use `camelCase` for function names.
  - For local (file-specific) functions, start with a lowercase letter, e.g., `isLeapYear`.
  - For external (shared) functions, start with an uppercase letter, e.g., `IsLeapYear`.

- **Type Annotations**:
  - Always define input and output types to guide future users:
    - **Do not**:
      ```python
      def isLeapYear(year):
      ```
    - **Do**:
      ```python
      def isLeapYear(year: int) -> bool:
      ```

---

# How to Contribute

To ensure efficient collaboration, follow these steps:

1. **Create a Pull Request**:
   - Spend time writing a detailed description of your changes. This helps reviewers understand your work.

2. **Review Process**:
   - Do **not** merge your Pull Request if the reviewer has not approved it.

---

# Best Practices

- Always use a virtual environment for each project to avoid dependency conflicts.
- Regularly update your `requirements.txt` file when installing or upgrading packages.
- Avoid committing the `venv` directory to version control.