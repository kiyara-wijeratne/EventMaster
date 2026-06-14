# EventMaster

**Student ID:** 5631074

A web-based event management system that enables Administrators, Organisers, and Coordinators to manage events through a role-based interface.

---

## Table of Contents

* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Building the Application](#building-the-application)
* [Accessing the Application](#accessing-the-application)
* [User Accounts](#user-accounts)
* [Running Tests](#running-tests)
* [Stopping the Application](#stopping-the-application)

---

## Overview

This application represents the **Minimum Viable Product (MVP)** of the proposed EventMaster system. This current implementation supports **Workshop** events only and is distributed as a Docker container for ease of deployment. 

---

## Prerequisites

Before running the application, ensure that **Docker Desktop** is installed and running before executing any of the commands below.

---

## Building the Application

### 1. Build the Docker Image

Open a terminal in the project's root directory and run:

```bash
docker build --tag eventmaster .
```

### 2. Start the Application

Run the Docker container:

```bash
docker run -p 8080:8080 eventmaster
```

This command maps port **8080** on the host machine to port **8080** within the container.

---

## Accessing the Application

Once the container has started successfully:

1. Open a web browser.
2. Navigate to:

```text
http://localhost:8080
```

Alternatively, click the URL displayed in the terminal output.

---

## User Accounts

The database is automatically seeded during application startup.

Use the following credentials to access the system:

| Role          | Email                                                             | Password    |
| ------------- | ----------------------------------------------------------------- | ----------- |
| Administrator | [admin@eventmaster.com](mailto:admin@eventmaster.com)             | admin       |
| Organiser     | [organiser@eventmaster.com](mailto:organiser@eventmaster.com)     | organiser   |
| Coordinator   | [coordinator@eventmaster.com](mailto:coordinator@eventmaster.com) | coordinator |

For a detailed explanation of the functionality available to each role, please refer to the Requirements section of the accompanying report.

---

## Running Tests

To execute the automated test suite, run:

```bash
docker run eventmaster pytest
```

---

## Stopping the Application

To stop the running container:

### Terminal

Press:

```bash
Ctrl + C
```

### Docker Desktop

Alternatively, stop the container directly through Docker Desktop.

