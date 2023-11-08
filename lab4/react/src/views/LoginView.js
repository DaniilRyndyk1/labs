import React from "react";
import $ from 'jquery';
import { useNavigate, useLocation, Link } from "react-router-dom";

class LoginView extends React.Component {

    state = {
        login: "",
        password: "",
        accessToken: "",
        refrechToken: ""
    }

    updateLogin = (event) => {
        this.setState({login : event.target.value})
    }

    updatePassword = (event) => {
        this.setState({password : event.target.value})
    }

    handleSubmit = (navigate) => {
        var state = this.state;
        var body = JSON.stringify(state);

        $.ajax({
            url: 'http://localhost:8080/login',
            type: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "Content-Length": body.length
            },
            data: body,
            success: function (data) {
                alert("Вы были успешно авторизованы!");

                state["refrechToken"] = data.refreshToken;
                state["accessToken"] = data.accessToken;

                navigate('/users', {state: state})
            },
            error: function (error) {
                alert("Не удалось авторизоваться, status code " + error.status + ", причина " + error.responseJSON.error);
            }
        });
    }


    render() {
        var state = this.state;

        if (this.props.location.state != null) {
            state = this.props.location.state;
            this.setState(state);
        }

        return (
            <div class="row">
                <div class="col">
                    <div class="row">
                        <div class="col-3"></div>
                        <div class="col">
                            <p></p>
                            <h2>Авторизация</h2>
                        </div>
                        <div class="col-3"></div>
                    </div>
                    <div class="row">
                        <div class="col-3"></div>
                        <div class="col">
                            <div class="form-group">
                                <label for="loginInput">Логин</label>
                                <input type="text" class="form-control" id="loginInput" aria-describedby="loginHelp" placeholder="Введите логин" onChange={this.updateLogin} value={state.login}/>
                                <small id="loginHelp" class="form-text text-muted">Вы не зарегистрированы? Вам <Link to="register">сюда</Link></small>
                            </div>
                            <div class="form-group">
                                <label for="passwordInput">Пароль</label>
                                <input type="text" class="form-control" id="passwordInput" placeholder="Пароль" onChange={this.updatePassword} value={state.password}/>
                            </div>
                            <button type="submit" class="btn btn-primary" style={{marginTop: 15 + 'px'}}  onClick={() => {this.handleSubmit(this.props.navigate)}}>Отправить</button>
                        </div>
                        <div class="col-3"></div>
                    </div>
                </div>
            </div>
        );
    }
}

export default function WithNavigate(props) {
    return <LoginView {...props} navigate={useNavigate()} location={useLocation()} />
}