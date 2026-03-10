# Database Scripts and Migrations

This directory contains all database-related scripts for the Thunderball application.

## Directory Structure

- **ddl/** - Data Definition Language scripts (CREATE TABLE, INDEX, VIEW)
- **dml/** - Data Manipulation Language scripts (seed data, test data)
- **stored-procedures/** - Stored procedures and database functions
- **migrations/** - Database migration scripts (Liquibase/Flyway if used)

## Usage

### Creating Tables

Place your DDL scripts in the `ddl/` directory:
- `01_create_tables.sql` - Main table definitions
- `02_create_indexes.sql` - Index definitions
- `03_create_views.sql` - View definitions

### Loading Data

Place your seed and test data scripts in the `dml/` directory:
- `seed_data.sql` - Initial data for application
- `test_data.sql` - Test data for development/testing

### Running Migrations

Use the migration scripts in `migrations/` directory or configure Liquibase/Flyway.

## Db2 Connection

Ensure you have proper Db2 connection credentials configured in your environment variables.
