package com.example.droneservice.dto;

public class MedicationDto {
    private Long id;
    private String name;
    private Integer weight;
    private String code;
    private String image;
    private Long droneId;

    public MedicationDto() {}

    public MedicationDto(Long id, String name, Integer weight, String code, String image, Long droneId) {
        this.id = id;
        this.name = name;
        this.weight = weight;
        this.code = code;
        this.image = image;
        this.droneId = droneId;
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public Integer getWeight() { return weight; }
    public String getCode() { return code; }
    public String getImage() { return image; }
    public Long getDroneId() { return droneId; }

    public void setId(Long id) { this.id = id; }
    public void setName(String name) { this.name = name; }
    public void setWeight(Integer weight) { this.weight = weight; }
    public void setCode(String code) { this.code = code; }
    public void setImage(String image) { this.image = image; }
    public void setDroneId(Long droneId) { this.droneId = droneId; }
}

