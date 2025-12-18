package com.example.droneservice.dto;

import java.util.List;

public class LoadRequest {
    private List<CreateMedicationRequest> medications;

    public List<CreateMedicationRequest> getMedications() { return medications; }
    public void setMedications(List<CreateMedicationRequest> medications) { this.medications = medications; }
}

