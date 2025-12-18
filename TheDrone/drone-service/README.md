# Drone Service

A simple Spring Boot REST API to manage a fleet of drones and medications for delivery.

Prerequisites
- Java 17+
- Gradle (or use an installed Gradle wrapper)

Build & Run

From the `drone-service` folder:

Windows (PowerShell):

    ./gradlew bootRun

or

    gradle bootRun

API
- POST /api/drones - register drone
- GET /api/drones - list drones
- GET /api/drones/available - list drones available for loading
- POST /api/drones/{id}/load - load medications
- GET /api/drones/{id}/medications - get meds loaded on drone
- GET /api/drones/{id}/battery - get battery level
- POST /api/drones/{id}/dispatch - set drone to DELIVERING (if LOADED)

H2 Console
- http://localhost:8081/h2-console
- JDBC URL: jdbc:h2:mem:drone-db

Notes
- In-memory H2 database is used; sample data is preloaded on startup.
- Scheduler simulates state transitions and battery drain.

