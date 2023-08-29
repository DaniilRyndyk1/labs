package ru.backend.storages;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import ru.backend.models.User;

import java.util.*;

@Slf4j
@Component
public class UserStorage {
    private final Map<Long, User> objects = new HashMap<>();
    private Long id = 1L;

    public User add(User object) {
        object.setId(id);
        objects.put(id, object);
        id++;
        return object;
    }

    public Optional<User> get(Long id) {
        return Optional.ofNullable(objects.get(id));
    }
}
