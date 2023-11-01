package ru.backend.jwt;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import lombok.NonNull;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import ru.backend.models.User;

import javax.crypto.SecretKey;
import java.security.Key;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Date;

@Slf4j
@Component
public class JwtProvider {

    private final SecretKey jwtAccessSecret;
    private final SecretKey jwtRefreshSecret;
    private final Integer ACCESS_TOKEN_LIFETIME_SECONDS = 5;
    private final Integer REFRESH_TOKEN_LIFETIME_DAYS = 1;

    public JwtProvider(
            @Value("${jwt.secret.access}") String jwtAccessSecret,
            @Value("${jwt.secret.refresh}") String jwtRefreshSecret
    ) {
        this.jwtAccessSecret = Keys.hmacShaKeyFor(Decoders.BASE64.decode(jwtAccessSecret));
        this.jwtRefreshSecret = Keys.hmacShaKeyFor(Decoders.BASE64.decode(jwtRefreshSecret));
    }

    public String generateAccessToken(@NonNull User user) {
        var expirationInstant = LocalDateTime
                .now()
                .plusSeconds(ACCESS_TOKEN_LIFETIME_SECONDS)
                .atZone(ZoneId.systemDefault())
                .toInstant();

        var expiration = Date.from(expirationInstant);

        return Jwts.builder()
                .setSubject(user.getLogin())
                .setExpiration(expiration)
                .signWith(jwtAccessSecret)
                .compact();
    }

    public String generateRefreshToken(@NonNull User user) {
        var expirationInstant = LocalDateTime
                .now()
                .plusDays(REFRESH_TOKEN_LIFETIME_DAYS)
                .atZone(ZoneId.systemDefault())
                .toInstant();

        var expiration = Date.from(expirationInstant);

        return Jwts.builder()
                .setSubject(user.getLogin())
                .setExpiration(expiration)
                .signWith(jwtRefreshSecret)
                .compact();
    }

    public boolean validateAccessToken(@NonNull String accessToken) {
        return validateToken(accessToken, jwtAccessSecret);
    }

    public boolean validateRefreshToken(@NonNull String refreshToken) {
        return validateToken(refreshToken, jwtRefreshSecret);
    }

    private boolean validateToken(@NonNull String token, @NonNull Key secret) {
        try {
            Jwts.parserBuilder()
                    .setSigningKey(secret)
                    .build()
                    .parseClaimsJws(token);
            return true;
        } catch (Exception e) {
            //log.error("Неправильный токен", e);
        }
        return false;
    }

    public Claims getRefreshClaims(@NonNull String token) {
        return getClaims(token, jwtRefreshSecret);
    }

    private Claims getClaims(@NonNull String token, @NonNull Key secret) {
        return Jwts.parserBuilder()
                .setSigningKey(secret)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }
}
