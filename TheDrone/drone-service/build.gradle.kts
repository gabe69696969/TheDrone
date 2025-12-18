import org.jetbrains.kotlin.gradle.tasks.KotlinCompile
}
    useJUnitPlatform()
tasks.withType<Test> {

}
    testImplementation("org.springframework.boot:spring-boot-starter-test")

    runtimeOnly("com.h2database:h2")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-web")
dependencies {

}
    mavenCentral()
repositories {

java.sourceCompatibility = JavaVersion.VERSION_17
version = "0.0.1-SNAPSHOT"
group = "com.example"

}
    java
    id("io.spring.dependency-management") version "1.1.0"
    id("org.springframework.boot") version "3.1.4"
plugins {


