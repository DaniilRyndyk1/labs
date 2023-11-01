package ru.backend.services;

import lombok.AllArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import ru.backend.models.User;
import ru.backend.storages.UserStorage;

import java.util.HashSet;
import java.util.List;
import java.util.Objects;

@Service
@AllArgsConstructor
public class UserService implements UserDetailsService {

    private final UserStorage storage;

    public List<User> getAll() {
        return storage.getAll();
    }

    public User getByLogin(String login) {
        return storage.getByLogin(login);
    }

    @Override
    public UserDetails loadUserByUsername(String login) throws UsernameNotFoundException {
        var user = getByLogin(login);
        if (Objects.isNull(user)) {
            throw new UsernameNotFoundException(String.format("Пользователь %s не найден", login));
        }
        return new org.springframework.security.core.userdetails.User(user.getLogin(),
                user.getPassword(), true, true, true, true, new HashSet<>());
    }

    public User add(User user) {
        return storage.add(user);
    }
}