package ru.backend.controllers;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import ru.backend.exceptions.NotFoundException;
import ru.backend.exceptions.ValidationException;
import ru.backend.models.User;
import ru.backend.storages.UserStorage;

import java.time.LocalDate;
import java.util.Map;

@RestController
@Slf4j
@RequestMapping("/users")
@AllArgsConstructor
public class UserController {

    private final UserStorage storage;

    @GetMapping("{id}")
    public User get(@PathVariable Long id) {
        var object = storage.get(id);
        if (object.isEmpty()) {
            throw new NotFoundException(id, object.getClass().getSimpleName());
        }
        return object.get();
    }

    @PostMapping
    public User create(@RequestBody User object) {
        validate(object);
        return storage.add(object);
    }

    public void validate(User user) {
        if (user.getEmail() == null) {
            throw new ValidationException("Email не задан");
        } else if (user.getEmail().isBlank()) {
            throw new ValidationException("Электронная почта не может быть пустой");
        }  else if (!user.getEmail().contains("@")) {
            throw new ValidationException("Электронная почта должна содержать символ @");
        } else if (user.getLogin() == null) {
            throw new ValidationException("Логин не может отсутствовать");
        } else if (user.getLogin().isBlank()) {
            throw new ValidationException("Логин не может быть пустым");
        } else if (user.getLogin().contains(" ")) {
            throw new ValidationException("Логин не может содержать пробелы");
        } else if (user.getBirthday() == null) {
            throw new ValidationException("День рождения не может отсутствовать");
        } else if (user.getBirthday().isAfter(LocalDate.now())) {
            throw new ValidationException("Дата рождения не может быть в будущем");
        }
    }

    @ExceptionHandler
    @ResponseStatus(
            value = HttpStatus.BAD_REQUEST,
            reason = "Данные не корректны"
    )
    public Map<String, String> handleWrongData(final ValidationException e) {
        return Map.of("error", e.getMessage());
    }
}

