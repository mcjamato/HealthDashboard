# Phase 2 Design Document

## Purpose

Phase 2 implements four compact, extensible data-entry modules while retaining the layered architecture established in Phase 1.

## Scope

- Exercise logging and history
- Health logging and history
- Mental wellness logging and history
- Nutrition logging and history
- Basic summaries and charts
- Administrator soft-deactivation controls
- Client create-and-read permissions

## Architecture

The UI layer contains Streamlit page classes. Dataclasses carry typed records. Repository classes own SQLite access. AnalyticsService provides reusable summary calculations. DatabaseManager controls connections, transactions, and schema creation.

## Database relationships

Each domain table contains a `client_id` foreign key referencing `clients.id`. Records are never physically deleted in the MVP. Administrators set `is_active` to zero, preserving historical integrity.

## Metrics

Exercise: type, duration, intensity, steps, distance, calories, notes.
Health: weight, sleep hours, sleep quality, resting heart rate, blood pressure, water, notes.
Mental Wellness: mood, stress, energy, focus, meditation, journal entry.
Nutrition: meal type, calories, protein, carbohydrates, fat, fiber, water, notes.

## Future phases

Phase 3 adds cross-domain analytics, percent-change cards, and correlation reporting. Phase 4 adds workbook import, PDF/Excel exports, and scheduled-report configuration.
