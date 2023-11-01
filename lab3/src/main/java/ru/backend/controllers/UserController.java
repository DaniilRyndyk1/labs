package ru.backend.controllers;

import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;
import ru.backend.models.User;
import ru.backend.services.AuthService;
import ru.backend.services.UserService;

import javax.security.auth.message.AuthException;
import java.util.List;

@RestController("api")
@Slf4j
@RequestMapping
@AllArgsConstructor
@CrossOrigin(origins = "*")
public class UserController{

    private final AuthService authService;
    private final UserService userService;

    @GetMapping("users")
    public List<User> getAll(@RequestParam String token) throws AuthException {
        if (authService.checkAccessToken(token)) {
            return userService.getAll();
        }
        throw new AuthException("Неверный токен");
    }
}

