package com.example.droneservice.controller;

import com.example.droneservice.dto.CreateDroneRequest;
import com.example.droneservice.dto.DroneDto;
import com.example.droneservice.dto.LoadRequest;
import com.example.droneservice.service.DroneService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/drones")
public class DroneController {
    private final DroneService droneService;

    public DroneController(DroneService droneService) {
        this.droneService = droneService;
    }

    @PostMapping
    public ResponseEntity<DroneDto> register(@Valid @RequestBody CreateDroneRequest req) {
        DroneDto dto = droneService.registerDrone(req);
        return ResponseEntity.status(201).body(dto);
    }

    @GetMapping("/{id}")
    public ResponseEntity<DroneDto> get(@PathVariable Long id) {
        return ResponseEntity.ok(droneService.getDrone(id));
    }

    @GetMapping
    public ResponseEntity<List<DroneDto>> list() {
        return ResponseEntity.ok(droneService.listDrones());
    }

    @GetMapping("/available")
    public ResponseEntity<List<DroneDto>> available() {
        return ResponseEntity.ok(droneService.availableDrones());
    }

    @PostMapping("/{id}/load")
    public ResponseEntity<Void> load(@PathVariable Long id, @RequestBody LoadRequest req) {
        droneService.loadDrone(id, req);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/{id}/medications")
    public ResponseEntity<?> meds(@PathVariable Long id) {
        return ResponseEntity.ok(droneService.getMedications(id));
    }

    @GetMapping("/{id}/battery")
    public ResponseEntity<?> battery(@PathVariable Long id) {
        return ResponseEntity.ok(java.util.Map.of("batteryCapacity", droneService.getBattery(id)));
    }

    @PostMapping("/{id}/dispatch")
    public ResponseEntity<Void> dispatch(@PathVariable Long id) {
        droneService.dispatch(id);
        return ResponseEntity.ok().build();
    }
}

