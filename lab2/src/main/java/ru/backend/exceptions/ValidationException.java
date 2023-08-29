package ru.backend.exceptions;

public class ValidationException extends RuntimeException {

    public ValidationException(String message) {
        super("При создании пользователя: " + message);
    }
}
