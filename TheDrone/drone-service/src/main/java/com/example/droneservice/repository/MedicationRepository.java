package com.example.droneservice.repository;

import com.example.droneservice.model.entity.Medication;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface MedicationRepository extends JpaRepository<Medication, Long> {
    List<Medication> findByDroneId(Long droneId);
}

