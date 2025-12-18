package com.example.droneservice.model.entity;

import com.example.droneservice.model.enums.DroneModel;
import com.example.droneservice.model.enums.DroneState;
import jakarta.persistence.*;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "drone")
public class Drone {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    @Column(name = "serial_number", length = 100, nullable = false, unique = true)
    private String serialNumber;

    @NotNull
    @Enumerated(EnumType.STRING)
    private DroneModel model;

    @NotNull
    @Min(1)
    @Max(1000)
    @Column(name = "weight_limit")
    private Integer weightLimit;

    @NotNull
    @Min(0)
    @Max(100)
    @Column(name = "battery_capacity")
    private Integer batteryCapacity = 100;

    @NotNull
    @Enumerated(EnumType.STRING)
    private DroneState state = DroneState.IDLE;

    @OneToMany(mappedBy = "drone", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<com.example.droneservice.model.entity.Medication> medications = new ArrayList<>();

    private Instant createdAt = Instant.now();
    private Instant updatedAt = Instant.now();

    // Constructors, getters, setters
    public Drone() {}

    public Drone(String serialNumber, DroneModel model, Integer weightLimit, Integer batteryCapacity, DroneState state) {
        this.serialNumber = serialNumber;
        this.model = model;
        this.weightLimit = weightLimit;
        if (batteryCapacity != null) this.batteryCapacity = batteryCapacity;
        if (state != null) this.state = state;
    }

    @PrePersist
    public void prePersist() {
        createdAt = Instant.now();
        updatedAt = Instant.now();
    }

    @PreUpdate
    public void preUpdate() {
        updatedAt = Instant.now();
    }

    public Long getId() { return id; }
    public String getSerialNumber() { return serialNumber; }
    public void setSerialNumber(String serialNumber) { this.serialNumber = serialNumber; }
    public DroneModel getModel() { return model; }
    public void setModel(DroneModel model) { this.model = model; }
    public Integer getWeightLimit() { return weightLimit; }
    public void setWeightLimit(Integer weightLimit) { this.weightLimit = weightLimit; }
    public Integer getBatteryCapacity() { return batteryCapacity; }
    public void setBatteryCapacity(Integer batteryCapacity) { this.batteryCapacity = batteryCapacity; }
    public DroneState getState() { return state; }
    public void setState(DroneState state) { this.state = state; }
    public List<com.example.droneservice.model.entity.Medication> getMedications() { return medications; }
    public void setMedications(List<com.example.droneservice.model.entity.Medication> medications) { this.medications = medications; }
    public Instant getCreatedAt() { return createdAt; }
    public Instant getUpdatedAt() { return updatedAt; }
}

