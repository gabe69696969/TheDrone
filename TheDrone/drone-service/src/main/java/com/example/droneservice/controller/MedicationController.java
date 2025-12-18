package com.example.droneservice.controller;

import com.example.droneservice.dto.CreateMedicationRequest;
import com.example.droneservice.dto.MedicationDto;
import com.example.droneservice.service.MedicationService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/medications")
public class MedicationController {
    private final MedicationService medicationService;

    public MedicationController(MedicationService medicationService) {
        this.medicationService = medicationService;
    }

    @PostMapping
    public ResponseEntity<MedicationDto> create(@Valid @RequestBody CreateMedicationRequest req) {
        return ResponseEntity.status(201).body(medicationService.createMedication(req));
    }

    @GetMapping("/{id}")
    public ResponseEntity<MedicationDto> get(@PathVariable Long id) {
        return ResponseEntity.ok(medicationService.getMedication(id));
    }

    @GetMapping
    public ResponseEntity<List<MedicationDto>> list() {
        return ResponseEntity.ok(medicationService.listAll());
    }
}

