package com.example.droneservice.service;

import com.example.droneservice.dto.CreateMedicationRequest;
import com.example.droneservice.dto.MedicationDto;

import java.util.List;

public interface MedicationService {
    MedicationDto createMedication(CreateMedicationRequest req);
    MedicationDto getMedication(Long id);
    List<MedicationDto> listAll();
}

