package ru.backend.models;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.LocalDate;

@Data
@AllArgsConstructor
public class User {
    private Long id;
    private String name;
    private String email;
    private String login;
    private LocalDate birthday;
}
