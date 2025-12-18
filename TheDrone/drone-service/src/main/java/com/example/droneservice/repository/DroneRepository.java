package com.example.droneservice.repository;

import com.example.droneservice.model.entity.Drone;
import com.example.droneservice.model.enums.DroneState;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface DroneRepository extends JpaRepository<Drone, Long> {
    Optional<Drone> findBySerialNumber(String serialNumber);
    List<Drone> findByState(DroneState state);
}

