package ru.backend.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
        value = HttpStatus.NOT_FOUND,
        reason = "Объект не найден"
)
public class NotFoundException extends RuntimeException {

    public NotFoundException(Long id, String name) {
        super(String.format("Не удалось найти {0} id = {1}", name, id));
    }
}
