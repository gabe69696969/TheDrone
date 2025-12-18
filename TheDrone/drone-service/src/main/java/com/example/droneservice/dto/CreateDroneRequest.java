package com.example.droneservice.dto;

import com.example.droneservice.model.enums.DroneModel;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class CreateDroneRequest {
    @NotBlank
    private String serialNumber;
    @NotNull
    private DroneModel model;
    @NotNull
    @Min(1)
    @Max(1000)
    private Integer weightLimit;
    private Integer batteryCapacity;

    public String getSerialNumber() { return serialNumber; }
    public void setSerialNumber(String serialNumber) { this.serialNumber = serialNumber; }
    public DroneModel getModel() { return model; }
    public void setModel(DroneModel model) { this.model = model; }
    public Integer getWeightLimit() { return weightLimit; }
    public void setWeightLimit(Integer weightLimit) { this.weightLimit = weightLimit; }
    public Integer getBatteryCapacity() { return batteryCapacity; }
    public void setBatteryCapacity(Integer batteryCapacity) { this.batteryCapacity = batteryCapacity; }
}

