package com.example.droneservice.scheduler;

import com.example.droneservice.model.entity.Drone;
import com.example.droneservice.model.enums.DroneState;
import com.example.droneservice.repository.DroneRepository;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class DroneStateSimulator {
    private static final Logger log = LoggerFactory.getLogger(DroneStateSimulator.class);

    private final DroneRepository droneRepository;

    public DroneStateSimulator(DroneRepository droneRepository) {
        this.droneRepository = droneRepository;
    }

    @Scheduled(fixedDelayString = "${drone.simulator.interval:60000}")
    @Transactional
    public void tick() {
        List<Drone> drones = droneRepository.findAll();
        for (Drone d : drones) {
            switch (d.getState()) {
                case DELIVERING -> {
                    int newBattery = Math.max(0, d.getBatteryCapacity() - 5);
                    d.setBatteryCapacity(newBattery);
                    if (newBattery <= 20) {
                        d.setState(DroneState.RETURNING);
                    } else {
                        // simulate delivery completion quickly for demo
                        d.setState(DroneState.DELIVERED);
                    }
                }
                case RETURNING -> {
                    int newBattery = Math.max(0, d.getBatteryCapacity() - 3);
                    d.setBatteryCapacity(newBattery);
                    if (newBattery == 0) d.setState(DroneState.IDLE);
                }
                case LOADING -> {
                    int newBattery = Math.max(0, d.getBatteryCapacity() - 1);
                    d.setBatteryCapacity(newBattery);
                }
                default -> {
                    // idle/loaded/delivered - small drain
                    if (d.getBatteryCapacity() > 0) d.setBatteryCapacity(Math.max(0, d.getBatteryCapacity() - 0));
                }
            }
            droneRepository.save(d);
        }
        log.debug("Drone state simulator tick processed {} drones", drones.size());
    }
}

