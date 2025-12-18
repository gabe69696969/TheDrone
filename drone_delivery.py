"""
Drone Delivery System
A comprehensive system for managing drone deliveries with route optimization.
"""

import math
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Location:
    """Represents a geographical location with x, y coordinates."""
    name: str
    x: float
    y: float
    
    def distance_to(self, other: 'Location') -> float:
        """Calculate Euclidean distance to another location."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def __repr__(self) -> str:
        return f"Location({self.name}, x={self.x}, y={self.y})"


@dataclass
class Delivery:
    """Represents a delivery order."""
    id: int
    destination: Location
    weight: float  # in kg
    
    def __repr__(self) -> str:
        return f"Delivery(id={self.id}, dest={self.destination.name}, weight={self.weight}kg)"


class Drone:
    """Represents a delivery drone with battery and capacity constraints."""
    
    def __init__(self, 
                 drone_id: int,
                 max_range: float = 100.0,  # maximum flight distance in km
                 max_capacity: float = 5.0,  # maximum payload in kg
                 speed: float = 50.0):  # speed in km/h
        self.drone_id = drone_id
        self.max_range = max_range
        self.max_capacity = max_capacity
        self.speed = speed
        self.current_location: Optional[Location] = None
        self.current_load: float = 0.0
        self.distance_traveled: float = 0.0
    
    def can_deliver(self, delivery: Delivery, base: Location) -> bool:
        """Check if drone can complete delivery and return to base."""
        if delivery.weight > self.max_capacity:
            return False
        
        if not self.current_location:
            return False
        
        # Calculate total distance: current -> destination -> base
        to_destination = self.current_location.distance_to(delivery.destination)
        to_base = delivery.destination.distance_to(base)
        total_distance = to_destination + to_base
        
        # Check if within range considering distance already traveled
        remaining_range = self.max_range - self.distance_traveled
        return total_distance <= remaining_range
    
    def fly_to(self, location: Location) -> float:
        """Fly to a location and return the distance traveled."""
        if not self.current_location:
            self.current_location = location
            return 0.0
        
        distance = self.current_location.distance_to(location)
        self.distance_traveled += distance
        self.current_location = location
        return distance
    
    def reset(self, base: Location):
        """Reset drone to base location for a new mission."""
        self.current_location = base
        self.current_load = 0.0
        self.distance_traveled = 0.0
    
    def __repr__(self) -> str:
        return (f"Drone(id={self.drone_id}, range={self.max_range}km, "
                f"capacity={self.max_capacity}kg, traveled={self.distance_traveled:.2f}km)")


class DeliveryRoute:
    """Represents a planned delivery route."""
    
    def __init__(self, drone: Drone, base: Location):
        self.drone = drone
        self.base = base
        self.deliveries: List[Delivery] = []
        self.total_distance: float = 0.0
    
    def add_delivery(self, delivery: Delivery) -> bool:
        """Add a delivery to the route if feasible."""
        # Check if adding this delivery is feasible
        if not self.drone.can_deliver(delivery, self.base):
            return False
        
        self.deliveries.append(delivery)
        return True
    
    def calculate_distance(self) -> float:
        """Calculate total distance for this route."""
        if not self.deliveries:
            return 0.0
        
        total = 0.0
        current = self.base
        
        for delivery in self.deliveries:
            total += current.distance_to(delivery.destination)
            current = delivery.destination
        
        # Return to base
        total += current.distance_to(self.base)
        return total
    
    def __repr__(self) -> str:
        return (f"DeliveryRoute(drone={self.drone.drone_id}, "
                f"deliveries={len(self.deliveries)}, distance={self.calculate_distance():.2f}km)")


class DeliveryPlanner:
    """Plans and optimizes drone delivery routes."""
    
    def __init__(self, base: Location):
        self.base = base
        self.drones: List[Drone] = []
        self.pending_deliveries: List[Delivery] = []
    
    def add_drone(self, drone: Drone):
        """Add a drone to the fleet."""
        self.drones.append(drone)
    
    def add_delivery(self, delivery: Delivery):
        """Add a delivery order to the queue."""
        self.pending_deliveries.append(delivery)
    
    def plan_routes(self) -> List[DeliveryRoute]:
        """
        Plan delivery routes using a greedy nearest-neighbor approach.
        Returns a list of routes, one per drone.
        """
        routes: List[DeliveryRoute] = []
        remaining_deliveries = self.pending_deliveries.copy()
        
        for drone in self.drones:
            if not remaining_deliveries:
                break
            
            # Reset drone to base
            drone.reset(self.base)
            route = DeliveryRoute(drone, self.base)
            
            # Greedy approach: keep adding nearest feasible deliveries
            while remaining_deliveries:
                best_delivery = None
                best_distance = float('inf')
                
                for delivery in remaining_deliveries:
                    if drone.can_deliver(delivery, self.base):
                        distance = drone.current_location.distance_to(delivery.destination)
                        if distance < best_distance:
                            best_distance = distance
                            best_delivery = delivery
                
                if best_delivery is None:
                    break
                
                # Add delivery to route
                route.add_delivery(best_delivery)
                drone.fly_to(best_delivery.destination)
                remaining_deliveries.remove(best_delivery)
            
            if route.deliveries:
                route.total_distance = route.calculate_distance()
                routes.append(route)
                # Reset drone after planning
                drone.reset(self.base)
        
        # Update pending deliveries to only include undelivered items
        self.pending_deliveries = remaining_deliveries
        
        return routes
    
    def get_summary(self, routes: List[DeliveryRoute]) -> dict:
        """Generate a summary of the planned routes."""
        total_deliveries = sum(len(route.deliveries) for route in routes)
        total_distance = sum(route.total_distance for route in routes)
        
        return {
            'total_routes': len(routes),
            'total_deliveries': total_deliveries,
            'total_distance': total_distance,
            'pending_deliveries': len(self.pending_deliveries),
            'routes': routes
        }


def main():
    """Example usage of the drone delivery system."""
    # Create base location
    base = Location("Warehouse", 0, 0)
    
    # Create delivery locations
    deliveries = [
        Delivery(1, Location("Customer A", 10, 10), 2.0),
        Delivery(2, Location("Customer B", 20, 5), 3.0),
        Delivery(3, Location("Customer C", 15, 20), 1.5),
        Delivery(4, Location("Customer D", 30, 25), 4.0),
        Delivery(5, Location("Customer E", 5, 15), 2.5),
    ]
    
    # Create drones
    drone1 = Drone(1, max_range=100.0, max_capacity=5.0)
    drone2 = Drone(2, max_range=100.0, max_capacity=5.0)
    
    # Create planner and add drones and deliveries
    planner = DeliveryPlanner(base)
    planner.add_drone(drone1)
    planner.add_drone(drone2)
    
    for delivery in deliveries:
        planner.add_delivery(delivery)
    
    # Plan routes
    print("=== Drone Delivery System ===\n")
    print(f"Base: {base}")
    print(f"Total deliveries: {len(deliveries)}\n")
    
    routes = planner.plan_routes()
    summary = planner.get_summary(routes)
    
    print(f"Routes planned: {summary['total_routes']}")
    print(f"Deliveries scheduled: {summary['total_deliveries']}")
    print(f"Total distance: {summary['total_distance']:.2f} km")
    print(f"Pending deliveries: {summary['pending_deliveries']}\n")
    
    for i, route in enumerate(routes, 1):
        print(f"Route {i} (Drone {route.drone.drone_id}):")
        print(f"  Distance: {route.total_distance:.2f} km")
        print(f"  Deliveries: {len(route.deliveries)}")
        for delivery in route.deliveries:
            print(f"    - {delivery}")
        print()


if __name__ == "__main__":
    main()
