# TheDrone - Drone Delivery System

A comprehensive Python implementation of a drone delivery route planning system with optimization algorithms and constraints management.

## Overview

This project implements a complete drone delivery system that handles:
- Multiple drones with battery/range constraints
- Package weight capacity management
- Optimal route planning using greedy nearest-neighbor algorithm
- Automatic delivery assignment across available drones
- Distance calculations and route optimization

## Features

- **Drone Fleet Management**: Support for multiple drones with individual constraints
- **Smart Route Planning**: Greedy algorithm for efficient delivery routes
- **Constraint Handling**: Respects battery range, payload capacity, and distance limits
- **Return-to-Base**: Ensures drones have enough range to return to warehouse
- **Delivery Tracking**: Complete tracking of pending and completed deliveries

## Installation

No external dependencies required! This project uses only Python standard library.

```bash
# Clone the repository
git clone https://github.com/gabe69696969/TheDrone.git
cd TheDrone

# No installation needed - just Python 3.7+
```

## Usage

### Basic Example

```python
from drone_delivery import Location, Delivery, Drone, DeliveryPlanner

# Create base location (warehouse)
base = Location("Warehouse", 0, 0)

# Create delivery orders
deliveries = [
    Delivery(1, Location("Customer A", 10, 10), 2.0),
    Delivery(2, Location("Customer B", 20, 5), 3.0),
    Delivery(3, Location("Customer C", 15, 20), 1.5),
]

# Create drones
drone1 = Drone(1, max_range=100.0, max_capacity=5.0)
drone2 = Drone(2, max_range=100.0, max_capacity=5.0)

# Create planner and plan routes
planner = DeliveryPlanner(base)
planner.add_drone(drone1)
planner.add_drone(drone2)

for delivery in deliveries:
    planner.add_delivery(delivery)

# Get optimized routes
routes = planner.plan_routes()
summary = planner.get_summary(routes)

print(f"Total deliveries: {summary['total_deliveries']}")
print(f"Total distance: {summary['total_distance']:.2f} km")
```

### Running the Demo

```bash
python drone_delivery.py
```

## Running Tests

```bash
python -m unittest test_drone_delivery.py -v
```

## Architecture

### Core Classes

1. **Location**: Represents a geographical point with x, y coordinates
   - Calculates Euclidean distances between points

2. **Delivery**: Represents a delivery order
   - Contains destination location and package weight

3. **Drone**: Represents a delivery drone
   - Manages battery range, capacity, and current state
   - Validates delivery feasibility

4. **DeliveryRoute**: Represents a planned route for a single drone
   - Manages sequence of deliveries
   - Calculates total route distance

5. **DeliveryPlanner**: Main orchestrator for route planning
   - Assigns deliveries to available drones
   - Optimizes routes using greedy nearest-neighbor algorithm

### Algorithm

The system uses a **greedy nearest-neighbor approach** for route optimization:

1. For each available drone:
   - Start at the base location
   - Find the nearest undelivered location that the drone can reach
   - Add it to the route if feasible (considering capacity and range)
   - Repeat until no more deliveries can be added
   - Ensure drone can return to base

2. Constraints checked:
   - Package weight ≤ drone capacity
   - Total distance (current → destination → base) ≤ remaining range
   - Drone must be able to return to base after each delivery

## Example Output

```
=== Drone Delivery System ===

Base: Location(Warehouse, x=0, y=0)
Total deliveries: 5

Routes planned: 2
Deliveries scheduled: 5
Total distance: 156.82 km
Pending deliveries: 0

Route 1 (Drone 1):
  Distance: 78.73 km
  Deliveries: 3
    - Delivery(id=1, dest=Customer A, weight=2.0kg)
    - Delivery(id=5, dest=Customer E, weight=2.5kg)
    - Delivery(id=3, dest=Customer C, weight=1.5kg)

Route 2 (Drone 2):
  Distance: 78.09 km
  Deliveries: 2
    - Delivery(id=2, dest=Customer B, weight=3.0kg)
    - Delivery(id=4, dest=Customer D, weight=4.0kg)
```

## Technical Details

- **Language**: Python 3.7+
- **Dependencies**: None (uses standard library only)
- **Testing**: unittest framework
- **Code Style**: PEP 8 compliant with type hints

## Future Enhancements

Potential improvements for the system:

- Implement A* or Dijkstra's algorithm for optimal path finding
- Add time-based delivery scheduling
- Support for multiple trips per drone
- Real-time delivery tracking and updates
- API endpoints for integration with other systems
- Visualization of routes on a map
- Support for no-fly zones and obstacles
- Dynamic re-routing based on real-time conditions

## License

MIT License - feel free to use this for educational purposes.

## Author

Gabe Ortiz - Technical Assignment Implementation
