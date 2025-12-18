"""
Unit tests for the Drone Delivery System.
"""

import unittest
import math
from drone_delivery import Location, Delivery, Drone, DeliveryRoute, DeliveryPlanner


class TestLocation(unittest.TestCase):
    """Test the Location class."""
    
    def test_location_creation(self):
        """Test creating a location."""
        loc = Location("Test", 10, 20)
        self.assertEqual(loc.name, "Test")
        self.assertEqual(loc.x, 10)
        self.assertEqual(loc.y, 20)
    
    def test_distance_calculation(self):
        """Test distance calculation between locations."""
        loc1 = Location("A", 0, 0)
        loc2 = Location("B", 3, 4)
        # Distance should be 5 (3-4-5 triangle)
        self.assertEqual(loc1.distance_to(loc2), 5.0)
    
    def test_distance_same_location(self):
        """Test distance to same location is 0."""
        loc = Location("A", 5, 5)
        self.assertEqual(loc.distance_to(loc), 0.0)


class TestDelivery(unittest.TestCase):
    """Test the Delivery class."""
    
    def test_delivery_creation(self):
        """Test creating a delivery."""
        loc = Location("Customer", 10, 10)
        delivery = Delivery(1, loc, 2.5)
        self.assertEqual(delivery.id, 1)
        self.assertEqual(delivery.destination, loc)
        self.assertEqual(delivery.weight, 2.5)


class TestDrone(unittest.TestCase):
    """Test the Drone class."""
    
    def test_drone_creation(self):
        """Test creating a drone."""
        drone = Drone(1, max_range=100, max_capacity=5)
        self.assertEqual(drone.drone_id, 1)
        self.assertEqual(drone.max_range, 100)
        self.assertEqual(drone.max_capacity, 5)
        self.assertIsNone(drone.current_location)
    
    def test_drone_reset(self):
        """Test resetting a drone."""
        base = Location("Base", 0, 0)
        drone = Drone(1)
        drone.distance_traveled = 50
        drone.current_load = 3
        drone.reset(base)
        
        self.assertEqual(drone.distance_traveled, 0)
        self.assertEqual(drone.current_load, 0)
        self.assertEqual(drone.current_location, base)
    
    def test_drone_fly_to(self):
        """Test drone flying to a location."""
        loc1 = Location("A", 0, 0)
        loc2 = Location("B", 3, 4)
        
        drone = Drone(1)
        drone.current_location = loc1
        distance = drone.fly_to(loc2)
        
        self.assertEqual(distance, 5.0)
        self.assertEqual(drone.distance_traveled, 5.0)
        self.assertEqual(drone.current_location, loc2)
    
    def test_can_deliver_within_range(self):
        """Test if drone can deliver within range."""
        base = Location("Base", 0, 0)
        dest = Location("Dest", 10, 10)
        delivery = Delivery(1, dest, 2.0)
        
        drone = Drone(1, max_range=100, max_capacity=5)
        drone.current_location = base
        
        self.assertTrue(drone.can_deliver(delivery, base))
    
    def test_can_deliver_exceeds_capacity(self):
        """Test drone cannot deliver if weight exceeds capacity."""
        base = Location("Base", 0, 0)
        dest = Location("Dest", 10, 10)
        delivery = Delivery(1, dest, 10.0)  # Too heavy
        
        drone = Drone(1, max_range=100, max_capacity=5)
        drone.current_location = base
        
        self.assertFalse(drone.can_deliver(delivery, base))
    
    def test_can_deliver_exceeds_range(self):
        """Test drone cannot deliver if distance exceeds range."""
        base = Location("Base", 0, 0)
        dest = Location("Dest", 60, 60)  # Far away
        delivery = Delivery(1, dest, 2.0)
        
        drone = Drone(1, max_range=50, max_capacity=5)  # Limited range
        drone.current_location = base
        
        self.assertFalse(drone.can_deliver(delivery, base))


class TestDeliveryRoute(unittest.TestCase):
    """Test the DeliveryRoute class."""
    
    def test_route_creation(self):
        """Test creating a delivery route."""
        base = Location("Base", 0, 0)
        drone = Drone(1)
        route = DeliveryRoute(drone, base)
        
        self.assertEqual(route.drone, drone)
        self.assertEqual(route.base, base)
        self.assertEqual(len(route.deliveries), 0)
    
    def test_add_delivery_to_route(self):
        """Test adding a delivery to a route."""
        base = Location("Base", 0, 0)
        dest = Location("Dest", 10, 10)
        delivery = Delivery(1, dest, 2.0)
        
        drone = Drone(1, max_range=100, max_capacity=5)
        drone.current_location = base
        route = DeliveryRoute(drone, base)
        
        result = route.add_delivery(delivery)
        self.assertTrue(result)
        self.assertEqual(len(route.deliveries), 1)
    
    def test_calculate_distance_single_delivery(self):
        """Test distance calculation for single delivery."""
        base = Location("Base", 0, 0)
        dest = Location("Dest", 3, 4)  # Distance = 5
        delivery = Delivery(1, dest, 2.0)
        
        drone = Drone(1)
        route = DeliveryRoute(drone, base)
        route.deliveries.append(delivery)
        
        # Distance: base->dest (5) + dest->base (5) = 10
        self.assertEqual(route.calculate_distance(), 10.0)
    
    def test_calculate_distance_multiple_deliveries(self):
        """Test distance calculation for multiple deliveries."""
        base = Location("Base", 0, 0)
        dest1 = Location("Dest1", 3, 4)  # Distance from base = 5
        dest2 = Location("Dest2", 6, 8)  # Distance from dest1 = 5
        
        drone = Drone(1)
        route = DeliveryRoute(drone, base)
        route.deliveries.append(Delivery(1, dest1, 2.0))
        route.deliveries.append(Delivery(2, dest2, 2.0))
        
        # Distance: base->dest1 (5) + dest1->dest2 (5) + dest2->base (10) = 20
        self.assertEqual(route.calculate_distance(), 20.0)


class TestDeliveryPlanner(unittest.TestCase):
    """Test the DeliveryPlanner class."""
    
    def test_planner_creation(self):
        """Test creating a delivery planner."""
        base = Location("Base", 0, 0)
        planner = DeliveryPlanner(base)
        
        self.assertEqual(planner.base, base)
        self.assertEqual(len(planner.drones), 0)
        self.assertEqual(len(planner.pending_deliveries), 0)
    
    def test_add_drone(self):
        """Test adding a drone to the planner."""
        base = Location("Base", 0, 0)
        planner = DeliveryPlanner(base)
        drone = Drone(1)
        
        planner.add_drone(drone)
        self.assertEqual(len(planner.drones), 1)
    
    def test_add_delivery(self):
        """Test adding a delivery to the planner."""
        base = Location("Base", 0, 0)
        planner = DeliveryPlanner(base)
        dest = Location("Dest", 10, 10)
        delivery = Delivery(1, dest, 2.0)
        
        planner.add_delivery(delivery)
        self.assertEqual(len(planner.pending_deliveries), 1)
    
    def test_plan_routes_single_drone(self):
        """Test planning routes with a single drone."""
        base = Location("Base", 0, 0)
        planner = DeliveryPlanner(base)
        
        drone = Drone(1, max_range=100, max_capacity=10)
        planner.add_drone(drone)
        
        deliveries = [
            Delivery(1, Location("A", 10, 10), 2.0),
            Delivery(2, Location("B", 20, 5), 3.0),
        ]
        for delivery in deliveries:
            planner.add_delivery(delivery)
        
        routes = planner.plan_routes()
        
        self.assertEqual(len(routes), 1)
        self.assertEqual(len(routes[0].deliveries), 2)
    
    def test_plan_routes_multiple_drones(self):
        """Test planning routes with multiple drones."""
        base = Location("Base", 0, 0)
        planner = DeliveryPlanner(base)
        
        drone1 = Drone(1, max_range=100, max_capacity=5)
        drone2 = Drone(2, max_range=100, max_capacity=5)
        planner.add_drone(drone1)
        planner.add_drone(drone2)
        
        deliveries = [
            Delivery(1, Location("A", 10, 10), 2.0),
            Delivery(2, Location("B", 20, 5), 3.0),
            Delivery(3, Location("C", 15, 20), 1.5),
        ]
        for delivery in deliveries:
            planner.add_delivery(delivery)
        
        routes = planner.plan_routes()
        
        # Should create at least one route
        self.assertGreater(len(routes), 0)
        # Should deliver all or most deliveries
        total_deliveries = sum(len(r.deliveries) for r in routes)
        self.assertGreater(total_deliveries, 0)
    
    def test_plan_routes_capacity_constraint(self):
        """Test that planning respects capacity constraints."""
        base = Location("Base", 0, 0)
        planner = DeliveryPlanner(base)
        
        drone = Drone(1, max_range=200, max_capacity=3)
        planner.add_drone(drone)
        
        # Heavy delivery that exceeds capacity
        delivery = Delivery(1, Location("A", 10, 10), 5.0)
        planner.add_delivery(delivery)
        
        routes = planner.plan_routes()
        
        # Should not be able to deliver
        if routes:
            self.assertEqual(len(routes[0].deliveries), 0)
        # Delivery should remain pending
        self.assertEqual(len(planner.pending_deliveries), 1)
    
    def test_get_summary(self):
        """Test getting a summary of planned routes."""
        base = Location("Base", 0, 0)
        planner = DeliveryPlanner(base)
        
        drone = Drone(1, max_range=100, max_capacity=10)
        planner.add_drone(drone)
        
        deliveries = [
            Delivery(1, Location("A", 10, 10), 2.0),
            Delivery(2, Location("B", 20, 5), 3.0),
        ]
        for delivery in deliveries:
            planner.add_delivery(delivery)
        
        routes = planner.plan_routes()
        summary = planner.get_summary(routes)
        
        self.assertIn('total_routes', summary)
        self.assertIn('total_deliveries', summary)
        self.assertIn('total_distance', summary)
        self.assertIn('pending_deliveries', summary)
        self.assertIn('routes', summary)
    
    def test_cumulative_capacity_tracking(self):
        """Test that cumulative capacity is tracked correctly across multiple deliveries."""
        base = Location("Base", 0, 0)
        planner = DeliveryPlanner(base)
        
        # Drone can carry 5kg total
        drone = Drone(1, max_range=200, max_capacity=5)
        planner.add_drone(drone)
        
        # Add three deliveries: 2kg + 2kg + 2kg = 6kg total
        # Should only be able to take first two (4kg), third should be skipped
        deliveries = [
            Delivery(1, Location("A", 5, 5), 2.0),
            Delivery(2, Location("B", 10, 10), 2.0),
            Delivery(3, Location("C", 15, 15), 2.0),  # This should not fit
        ]
        for delivery in deliveries:
            planner.add_delivery(delivery)
        
        routes = planner.plan_routes()
        
        # Should create one route with only 2 deliveries (capacity: 4kg out of 5kg)
        self.assertEqual(len(routes), 1)
        self.assertEqual(len(routes[0].deliveries), 2)
        # Third delivery should remain pending
        self.assertEqual(len(planner.pending_deliveries), 1)
        self.assertEqual(planner.pending_deliveries[0].id, 3)


if __name__ == '__main__':
    unittest.main()
