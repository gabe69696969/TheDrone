package com.example.droneservice.config;

import com.example.droneservice.model.entity.Drone;
import com.example.droneservice.model.entity.Medication;
import com.example.droneservice.model.enums.DroneModel;
import com.example.droneservice.model.enums.DroneState;
import com.example.droneservice.repository.DroneRepository;
import com.example.droneservice.repository.MedicationRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DataLoader {
    @Bean
    CommandLineRunner init(DroneRepository droneRepository, MedicationRepository medicationRepository) {
        return args -> {
            Drone d1 = new Drone("DR-001", DroneModel.LIGHT_WEIGHT, 200, 100, DroneState.IDLE);
            Drone d2 = new Drone("DR-002", DroneModel.MIDDLE_WEIGHT, 300, 80, DroneState.IDLE);
            Drone d3 = new Drone("DR-003", DroneModel.CRUISER_WEIGHT, 400, 60, DroneState.LOADED);
            Drone d4 = new Drone("DR-004", DroneModel.HEAVY_WEIGHT, 500, 50, DroneState.DELIVERING);
            Drone d5 = new Drone("DR-005", DroneModel.HEAVY_WEIGHT, 500, 15, DroneState.RETURNING);
            Drone d6 = new Drone("DR-006", DroneModel.LIGHT_WEIGHT, 200, 99, DroneState.LOADING);
            Drone d7 = new Drone("DR-007", DroneModel.MIDDLE_WEIGHT, 300, 30, DroneState.IDLE);
            Drone d8 = new Drone("DR-008", DroneModel.CRUISER_WEIGHT, 400, 25, DroneState.IDLE);
            Drone d9 = new Drone("DR-009", DroneModel.MIDDLE_WEIGHT, 300, 10, DroneState.IDLE);
            Drone d10 = new Drone("DR-010", DroneModel.HEAVY_WEIGHT, 500, 100, DroneState.IDLE);

            droneRepository.save(d1);
            droneRepository.save(d2);
            droneRepository.save(d3);
            droneRepository.save(d4);
            droneRepository.save(d5);
            droneRepository.save(d6);
            droneRepository.save(d7);
            droneRepository.save(d8);
            droneRepository.save(d9);
            droneRepository.save(d10);

            Medication m1 = new Medication("MedA", 50, "MEDA_1", null);
            m1.setDrone(d3);
            medicationRepository.save(m1);
            Medication m2 = new Medication("MedB", 100, "MEDB_2", null);
            m2.setDrone(d4);
            medicationRepository.save(m2);
        };
    }
}

