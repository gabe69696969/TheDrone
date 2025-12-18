package com.example.droneservice.service;

import com.example.droneservice.dto.CreateMedicationRequest;
import com.example.droneservice.dto.MedicationDto;
import com.example.droneservice.model.entity.Medication;
import com.example.droneservice.repository.MedicationRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class MedicationServiceImpl implements MedicationService {
    private final MedicationRepository medicationRepository;

    public MedicationServiceImpl(MedicationRepository medicationRepository) {
        this.medicationRepository = medicationRepository;
    }

    @Override
    public MedicationDto createMedication(CreateMedicationRequest req) {
        Medication m = new Medication(req.getName(), req.getWeight(), req.getCode(), req.getImage());
        Medication saved = medicationRepository.save(m);
        return new MedicationDto(saved.getId(), saved.getName(), saved.getWeight(), saved.getCode(), saved.getImage(), saved.getDrone() != null ? saved.getDrone().getId() : null);
    }

    @Override
    public MedicationDto getMedication(Long id) {
        Medication m = medicationRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Medication not found"));
        return new MedicationDto(m.getId(), m.getName(), m.getWeight(), m.getCode(), m.getImage(), m.getDrone() != null ? m.getDrone().getId() : null);
    }

    @Override
    public List<MedicationDto> listAll() {
        return medicationRepository.findAll().stream().map(m -> new MedicationDto(m.getId(), m.getName(), m.getWeight(), m.getCode(), m.getImage(), m.getDrone() != null ? m.getDrone().getId() : null)).collect(Collectors.toList());
    }
}

