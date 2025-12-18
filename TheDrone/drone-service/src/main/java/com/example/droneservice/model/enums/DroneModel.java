package com.example.droneservice.model.enums;

public enum DroneModel {
    LIGHT_WEIGHT(200),
    MIDDLE_WEIGHT(300),
    CRUISER_WEIGHT(400),
    HEAVY_WEIGHT(500);

    private final int capacity;

    DroneModel(int capacity) {
        this.capacity = capacity;
    }

    public int getCapacity() {
        return capacity;
    }
}

