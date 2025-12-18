"""
Additional examples and use cases for the Drone Delivery System.
"""

from drone_delivery import Location, Delivery, Drone, DeliveryPlanner


def example_basic():
    """Basic example with simple deliveries."""
    print("=== Example 1: Basic Delivery ===\n")
    
    base = Location("Warehouse", 0, 0)
    drone = Drone(1, max_range=50, max_capacity=5)
    
    planner = DeliveryPlanner(base)
    planner.add_drone(drone)
    planner.add_delivery(Delivery(1, Location("Customer A", 10, 10), 3.0))
    
    routes = planner.plan_routes()
    summary = planner.get_summary(routes)
    
    print(f"Deliveries completed: {summary['total_deliveries']}")
    print(f"Distance traveled: {summary['total_distance']:.2f} km\n")


def example_capacity_limit():
    """Example showing capacity constraints."""
    print("=== Example 2: Capacity Constraint ===\n")
    
    base = Location("Warehouse", 0, 0)
    drone = Drone(1, max_range=100, max_capacity=3)  # Small capacity
    
    planner = DeliveryPlanner(base)
    planner.add_drone(drone)
    
    # Try to deliver a heavy package
    planner.add_delivery(Delivery(1, Location("Customer A", 10, 10), 5.0))
    
    routes = planner.plan_routes()
    summary = planner.get_summary(routes)
    
    print(f"Deliveries completed: {summary['total_deliveries']}")
    print(f"Pending deliveries: {summary['pending_deliveries']}")
    print("Note: Heavy package exceeds drone capacity\n")


def example_range_limit():
    """Example showing range constraints."""
    print("=== Example 3: Range Constraint ===\n")
    
    base = Location("Warehouse", 0, 0)
    drone = Drone(1, max_range=30, max_capacity=5)  # Limited range
    
    planner = DeliveryPlanner(base)
    planner.add_drone(drone)
    
    # Try to deliver to a far location
    planner.add_delivery(Delivery(1, Location("Far Customer", 50, 50), 2.0))
    
    routes = planner.plan_routes()
    summary = planner.get_summary(routes)
    
    print(f"Deliveries completed: {summary['total_deliveries']}")
    print(f"Pending deliveries: {summary['pending_deliveries']}")
    print("Note: Location is too far for the drone's range\n")


def example_multi_drone_optimization():
    """Example with multiple drones and many deliveries."""
    print("=== Example 4: Multi-Drone Fleet ===\n")
    
    base = Location("Warehouse", 0, 0)
    
    # Create a fleet of drones with different capabilities
    drones = [
        Drone(1, max_range=80, max_capacity=4),
        Drone(2, max_range=100, max_capacity=6),
        Drone(3, max_range=60, max_capacity=3),
    ]
    
    # Create multiple deliveries spread across the area
    deliveries = [
        Delivery(1, Location("Customer A", 10, 5), 2.0),
        Delivery(2, Location("Customer B", 15, 10), 3.0),
        Delivery(3, Location("Customer C", 5, 15), 1.5),
        Delivery(4, Location("Customer D", 20, 20), 2.5),
        Delivery(5, Location("Customer E", 25, 10), 4.0),
        Delivery(6, Location("Customer F", 12, 18), 1.0),
        Delivery(7, Location("Customer G", 8, 8), 2.0),
    ]
    
    planner = DeliveryPlanner(base)
    for drone in drones:
        planner.add_drone(drone)
    for delivery in deliveries:
        planner.add_delivery(delivery)
    
    routes = planner.plan_routes()
    summary = planner.get_summary(routes)
    
    print(f"Total drones: {len(drones)}")
    print(f"Total deliveries: {len(deliveries)}")
    print(f"Routes created: {summary['total_routes']}")
    print(f"Deliveries completed: {summary['total_deliveries']}")
    print(f"Total distance: {summary['total_distance']:.2f} km")
    print(f"Pending deliveries: {summary['pending_deliveries']}\n")
    
    for i, route in enumerate(routes, 1):
        print(f"Drone {route.drone.drone_id}: {len(route.deliveries)} deliveries, "
              f"{route.total_distance:.2f} km")


def example_efficient_clustering():
    """Example showing how drones handle clustered deliveries."""
    print("=== Example 5: Clustered Deliveries ===\n")
    
    base = Location("Warehouse", 0, 0)
    drone = Drone(1, max_range=100, max_capacity=10)
    
    # Create deliveries in two clusters
    deliveries = [
        # Cluster 1: North-West
        Delivery(1, Location("NW1", 10, 10), 1.0),
        Delivery(2, Location("NW2", 12, 11), 1.0),
        Delivery(3, Location("NW3", 11, 13), 1.0),
        # Cluster 2: South-East
        Delivery(4, Location("SE1", 20, -5), 1.0),
        Delivery(5, Location("SE2", 22, -6), 1.0),
        Delivery(6, Location("SE3", 21, -4), 1.0),
    ]
    
    planner = DeliveryPlanner(base)
    planner.add_drone(drone)
    for delivery in deliveries:
        planner.add_delivery(delivery)
    
    routes = planner.plan_routes()
    summary = planner.get_summary(routes)
    
    print(f"Deliveries: {summary['total_deliveries']}")
    print(f"Total distance: {summary['total_distance']:.2f} km")
    print("\nDelivery sequence (showing nearest-neighbor optimization):")
    
    for route in routes:
        print(f"\nDrone {route.drone.drone_id} route:")
        for i, delivery in enumerate(route.deliveries, 1):
            print(f"  {i}. {delivery.destination.name} "
                  f"at ({delivery.destination.x:.0f}, {delivery.destination.y:.0f})")


if __name__ == "__main__":
    example_basic()
    example_capacity_limit()
    example_range_limit()
    example_multi_drone_optimization()
    example_efficient_clustering()
    
    print("\n=== All Examples Complete ===")
