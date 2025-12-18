package com.example.droneservice.service;

import com.example.droneservice.dto.CreateDroneRequest;
import com.example.droneservice.dto.DroneDto;
import com.example.droneservice.dto.LoadRequest;
import com.example.droneservice.model.entity.Medication;

import java.util.List;

public interface DroneService {
    DroneDto registerDrone(CreateDroneRequest request);
    DroneDto getDrone(Long id);
    List<DroneDto> listDrones();
    List<DroneDto> availableDrones();
    void loadDrone(Long id, LoadRequest request);
    List<com.example.droneservice.dto.MedicationDto> getMedications(Long id);
    int getBattery(Long id);
    void dispatch(Long id);
}

