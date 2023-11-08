import React from 'react';
import $ from 'jquery';
import { Link } from "react-router-dom";

export default class RegisterView extends React.Component {

    state = {
        login: "",
        password: ""
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
            url: 'http://localhost:8080/register',
            type: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                "Content-Length": body.length
            },
            data: body,
            success: function () {
                alert("Вы были успешно зарегистрированы!");
                navigate('/', {state: state})
            },
            error: function (error) {
                alert("Не удалось зарегистрироваться, " + error.responseJSON.error);
            }
        });
    }


    render() {
        return (
            <div class="row">
                <div class="col">
                    <div class="row">
                        <div class="col-3"></div>
                        <div class="col">
                            <p></p>
                            <h2>Регистрация</h2>
                        </div>
                        <div class="col-3"></div>
                    </div>
                    <div class="row">
                        <div class="col-3"></div>
                        <div class="col">
                            <div class="form-group">
                                <label for="loginInput">Логин</label>
                                <input type="text" class="form-control" id="loginInput" aria-describedby="loginHelp" placeholder="Введите логин" onChange={this.updateLogin}/>
                                <small id="loginHelp" class="form-text text-muted">Вы уже зарегистрированы? Вам <Link to="/">сюда</Link></small>
                            </div>
                            <div class="form-group">
                                <label for="passwordInput">Пароль</label>
                                <input type="text" class="form-control" id="passwordInput" placeholder="Пароль" onChange={this.updatePassword}/>
                            </div>
                            <button type="submit" class="btn btn-primary" style={{marginTop: 15 + 'px'}}  onClick={(e) => {this.handleSubmit(this.props.navigate);}}>Отправить</button>
                        </div>
                        <div class="col-3"></div>
                    </div>
                </div>
            </div>
        );
    }
}