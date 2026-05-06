---
name: di-sdk-project
description: Create, list, and retrieve IBM watsonx Data Integration projects via the Python SDK — project types (wx/cpd), retrieval patterns, and accessing project resources (flows, jobs, engines, environments).
---

# Project Management Skill

This skill covers the essential operations for working with projects in the IBM watsonx.data Integration platform.

---

## How to Create a Project

Creating a project is the first step in building data integration workflows. Projects serve as containers for flows, jobs, connections, and other resources.

### Basic Project Creation

```python
from ibm_watsonx_data_integration.common.auth import IAMAuthenticator
from ibm_watsonx_data_integration import Platform

# Authenticate
auth = IAMAuthenticator(api_key=os.getenv('WATSONX_API_KEY'))
platform = Platform(auth=auth, base_api_url='https://api.ca-tor.dai.cloud.ibm.com')

# Create a new project
project = platform.create_project(
    name='My New Project',
    description='Project for data integration workflows'
)

print(f"Created project: {project.name}")
print(f"Project ID: {project.project_id}")
```

### Project Types

The `type` parameter determines the project type and defaults to `"wx"`:

- **`"wx"`** - watsonx Data Fabric project (default)
- **`"cpd"`** - Classic Cloud Pak for Data project

```python
# Create a watsonx Data Fabric project (default)
wx_project = platform.create_project(
    name='WatsonX Project',
    description='Modern watsonx data fabric project',
    project_type='wx'  # This is the default, can be omitted
)

# Create a Classic Cloud Pak for Data project
cpd_project = platform.create_project(
    name='CPD Project',
    description='Classic Cloud Pak for Data project',
    project_type='cpd'
)
```

### Project Creation with Additional Configuration

```python
# Create project with more details
project = platform.create_project(
    name='Analytics Project',
    description='Project for analytics data pipelines',
    project_type='wx',  # Specify project type
    tags=['analytics', 'production']
)

# Access project properties
print(f"Project Name: {project.name}")
print(f"Project ID: {project.project_id}")
print(f"Project Type: {project.type}")
print(f"Description: {project.description}")
```

### Important Notes

- Project names must be unique within your account
- Use descriptive names that reflect the project's purpose
- The `project_id` is automatically generated and used for API operations
- Store the `project_id` for future reference when accessing the project

---

## How to List and Retrieve Projects

### List All Projects

Use `platform.projects.get_all()` to retrieve all projects you have access to:

```python
# Get all projects
projects = platform.projects.get_all()

# Iterate through projects
for project in projects:
    print(f"Name: {project.name}")
    print(f"ID: {project.project_id}")
    print(f"Description: {project.description}")
    print("---")
```

### Retrieve a Specific Project by Name

Use `platform.projects.get(name='...')` to retrieve a project by its name:

```python
# Get project by name
project = platform.projects.get(name='My Project')

print(f"Found project: {project.name}")
print(f"Project ID: {project.project_id}")
```

### Retrieve a Specific Project by ID

Use `platform.projects.get(project_id='...')` to retrieve a project by its ID:

```python
# Get project by ID (use project_id=, NOT id=)
project = platform.projects.get(project_id='abc-123-def-456')

print(f"Found project: {project.name}")
print(f"Description: {project.description}")
```

### Important Notes

- **Always use `project_id=` parameter**, NOT `id=` when retrieving by ID
- Use `.get_all()` to list projects, NOT `.list()` (which doesn't exist)
- If a project is not found, an exception will be raised
- Project retrieval by name is case-sensitive

---

## Common Project Operations

### Update Project Details

```python
# Get the project
project = platform.projects.get(project_id='abc-123')

# Update project properties
project.name = 'Updated Project Name'
project.description = 'Updated description'

# Save changes
platform.update_project.update(project)
```

### Delete a Project

```python
# Get the project
project = platform.projects.get(project_id='abc-123')

# Delete the project
platform.delete_project.delete(project)
```

### Access Project Resources

Once you have a project, you can access its resources:

```python
# Get project
project = platform.projects.get(project_id='abc-123')

# Access flows
flows = project.flows.get_all()

# Access jobs
jobs = project.jobs.get_all()

# Access engines
engines = project.engines.get_all()

# Access environments
environments = project.environments.get_all()
```

---

## Best Practices

1. **Use Descriptive Names**: Choose clear, descriptive names that indicate the project's purpose
2. **Check Existence**: Before creating a project, check if one with the same name already exists
3. **Handle Exceptions**: Always wrap project operations in try-except blocks to handle errors gracefully

### Example: Safe Project Retrieval

```python
try:
    # Try to get existing project
    project = platform.projects.get(name='My Project')
    print(f"Using existing project: {project.name}")
except Exception:
    # Create new project if it doesn't exist
    project = platform.projects.create(
        name='My Project',
        description='New project for data integration'
    )
    print(f"Created new project: {project.name}")
```

---

## Next Steps

After creating or retrieving a project, you can:

- Create flows using the **`streaming-flows`** or **`batch-flows`** skills
- Set up connections to data sources
- Create and configure engines
- Define environments for flow execution
- Create and run jobs

Refer to the [`platform`] skill for the complete workflow and additional operations.
