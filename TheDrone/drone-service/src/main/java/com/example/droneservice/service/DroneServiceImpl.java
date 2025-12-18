package com.example.droneservice.service;

import com.example.droneservice.dto.CreateDroneRequest;
import com.example.droneservice.dto.DroneDto;
import com.example.droneservice.dto.LoadRequest;
import com.example.droneservice.dto.MedicationDto;
import com.example.droneservice.model.entity.Drone;
import com.example.droneservice.model.entity.Medication;
import com.example.droneservice.model.enums.DroneState;
import com.example.droneservice.repository.DroneRepository;
import com.example.droneservice.repository.MedicationRepository;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class DroneServiceImpl implements DroneService {
    private final DroneRepository droneRepository;
    private final MedicationRepository medicationRepository;

    public DroneServiceImpl(DroneRepository droneRepository, MedicationRepository medicationRepository) {
        this.droneRepository = droneRepository;
        this.medicationRepository = medicationRepository;
    }

    @Override
    @Transactional
    public DroneDto registerDrone(CreateDroneRequest request) {
        Optional<Drone> existing = droneRepository.findBySerialNumber(request.getSerialNumber());
        if (existing.isPresent()) throw new IllegalArgumentException("Serial number already exists");
        if (request.getWeightLimit() > request.getModel().getCapacity()) throw new IllegalArgumentException("Weight limit exceeds model capacity");
        Drone drone = new Drone(request.getSerialNumber(), request.getModel(), request.getWeightLimit(), request.getBatteryCapacity(), null);
        Drone saved = droneRepository.save(drone);
        return toDto(saved);
    }

    @Override
    public DroneDto getDrone(Long id) {
        Drone d = droneRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Drone not found"));
        return toDto(d);
    }

    @Override
    public List<DroneDto> listDrones() {
        return droneRepository.findAll().stream().map(this::toDto).collect(Collectors.toList());
    }

    @Override
    public List<DroneDto> availableDrones() {
        return droneRepository.findAll().stream()
                .filter(d -> d.getState() == DroneState.IDLE && d.getBatteryCapacity() >= 25)
                .map(this::toDto)
                .collect(Collectors.toList());
    }

    @Override
    @Transactional
    public void loadDrone(Long id, LoadRequest request) {
        Drone drone = droneRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Drone not found"));
        if (drone.getBatteryCapacity() < 25) throw new IllegalStateException("Battery too low to load");
        int currentLoad = drone.getMedications().stream().mapToInt(Medication::getWeight).sum();
        int incoming = 0;
        if (!CollectionUtils.isEmpty(request.getMedications())) {
            incoming = request.getMedications().stream().mapToInt(m -> m.getWeight()).sum();
        }
        if (currentLoad + incoming > drone.getModel().getCapacity()) throw new IllegalStateException("Exceeds capacity");
        drone.setState(DroneState.LOADING);
        droneRepository.save(drone);
        if (!CollectionUtils.isEmpty(request.getMedications())) {
            for (com.example.droneservice.dto.CreateMedicationRequest cm : request.getMedications()) {
                Medication med = new Medication(cm.getName(), cm.getWeight(), cm.getCode(), cm.getImage());
                med.setDrone(drone);
                medicationRepository.save(med);
                drone.getMedications().add(med);
            }
        }
        drone.setState(DroneState.LOADED);
        droneRepository.save(drone);
    }

    @Override
    public List<MedicationDto> getMedications(Long id) {
        List<Medication> meds = medicationRepository.findByDroneId(id);
        return meds.stream().map(m -> new MedicationDto(m.getId(), m.getName(), m.getWeight(), m.getCode(), m.getImage(), m.getDrone() != null ? m.getDrone().getId() : null)).collect(Collectors.toList());
    }

    @Override
    public int getBattery(Long id) {
        Drone d = droneRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Drone not found"));
        return d.getBatteryCapacity();
    }

    @Override
    @Transactional
    public void dispatch(Long id) {
        Drone drone = droneRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Drone not found"));
        if (drone.getState() != DroneState.LOADED) throw new IllegalStateException("Drone not loaded");
        if (drone.getBatteryCapacity() < 25) throw new IllegalStateException("Battery too low to dispatch");
        drone.setState(DroneState.DELIVERING);
        droneRepository.save(drone);
    }

    private DroneDto toDto(Drone d) {
        return new DroneDto(d.getId(), d.getSerialNumber(), d.getModel(), d.getWeightLimit(), d.getBatteryCapacity(), d.getState());
    }
}

