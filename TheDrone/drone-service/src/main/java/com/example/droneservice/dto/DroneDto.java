package com.example.droneservice.dto;

import com.example.droneservice.model.enums.DroneModel;
import com.example.droneservice.model.enums.DroneState;

public class DroneDto {
    private Long id;
    private String serialNumber;
    private DroneModel model;
    private Integer weightLimit;
    private Integer batteryCapacity;
    private DroneState state;

    public DroneDto() {}

    public DroneDto(Long id, String serialNumber, DroneModel model, Integer weightLimit, Integer batteryCapacity, DroneState state) {
        this.id = id;
        this.serialNumber = serialNumber;
        this.model = model;
        this.weightLimit = weightLimit;
        this.batteryCapacity = batteryCapacity;
        this.state = state;
    }

    public Long getId() { return id; }
    public String getSerialNumber() { return serialNumber; }
    public DroneModel getModel() { return model; }
    public Integer getWeightLimit() { return weightLimit; }
    public Integer getBatteryCapacity() { return batteryCapacity; }
    public DroneState getState() { return state; }

    public void setId(Long id) { this.id = id; }
    public void setSerialNumber(String serialNumber) { this.serialNumber = serialNumber; }
    public void setModel(DroneModel model) { this.model = model; }
    public void setWeightLimit(Integer weightLimit) { this.weightLimit = weightLimit; }
    public void setBatteryCapacity(Integer batteryCapacity) { this.batteryCapacity = batteryCapacity; }
    public void setState(DroneState state) { this.state = state; }
}

