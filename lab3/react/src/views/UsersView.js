import React from 'react';
import $ from 'jquery';
import { useNavigate, useLocation, Link } from 'react-router-dom';

class UsersView extends React.Component {

    state = {
        login: "",
        password: "",
        accessToken: "",
        refrechToken: ""
    }

    constructor (props) {
        super(props);
        this.UsersList = React.createRef();
        this.Message = React.createRef();
    }

    drawError = (list, errorText) => {
        var tr = document.createElement("tr");
        var errorTd = document.createElement("td");
        errorTd.innerText = errorText;
        errorTd.setAttribute("colspan", "3");
        tr.appendChild(errorTd);
        list.current.appendChild(tr);
    }

    loadUsers = () => {
        let list = this.UsersList;
        let message = this.Message.current;
        message.innerText = "";
        let state = this.props.location.state;
        let drawError = this.drawError;
        let loadUsers = this.loadUsers;
        list.current.innerText = "";
        $.ajax({
            url: 'https://test-tb6i.onrender.com/users?token=' + state.accessToken,
            type: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            success: function (data) {
                for (var i = 0; i < data.length; i++) {
                    var user = data[i];
                    var tr = document.createElement("tr");

                    var numTd = document.createElement("td");
                    numTd.innerText = i;
                    tr.appendChild(numTd);

                    var loginTd = document.createElement("td");
                    loginTd.innerText = user.login;
                    tr.appendChild(loginTd);

                    var passwordTd = document.createElement("td");
                    passwordTd.innerText = user.password;
                    tr.appendChild(passwordTd);

                    list.current.appendChild(tr);  
                }
            },
            error: function (error) {
                if (error.status === 403) {
                    $.ajax({
                        url: 'https://test-tb6i.onrender.com/refresh?token=' + state.refrechToken,
                        type: "POST",
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        success: function (new_data) {
                            state["refrechToken"] = new_data.refreshToken;
                            state["accessToken"] = new_data.accessToken;

                            loadUsers();
                            message.innerText = "Успешно проведена повторная авторизация";
                        },
                        error: function (error) {
                            var errorText = "Получена неизвестная ошибка, статус " + error.status;
                            if (error.status === 403) {
                                errorText = "Для получения списка пользователей необходимо авторизоваться!";
                            } 
                            drawError(list, errorText);
                        }
                    });
                } else {
                    drawError(list, "Получена неизвестная ошибка, статус " + error.status);
                }
            }
        });
    }

    componentDidMount() { 
        this.loadUsers();
    }

    render() {
        return (
            <div class="row">
                <div class="col">
                    <div class="row">
                        <div class="col-3"></div>
                        <div class="col">
                            <div class="row">
                                <div class="col">
                                    <h2>Список существующих пользователей</h2>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <button onClick={this.loadUsers}>Обновить список</button>
                                    <p ref={this.Message}></p>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <Link to="/">Вернуться на страницу авторизации</Link>
                                </div>
                            </div>
                        </div>
                        <div class="col-3"></div>
                    </div>
                    <div class="row">
                        <div class="col-3"></div>
                        <div class="col" >
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th scope="col">№</th>
                                        <th scope="col">Логин</th>
                                        <th scope="col">Пароль</th>
                                    </tr>
                                </thead>
                                <tbody ref={this.UsersList}>
                                    
                                </tbody>
                            </table>
                        </div>
                        <div class="col-3"></div>
                    </div>
                </div>
            </div>
        )
    }
}

export default function WithLocation(props) {
    return <UsersView {...props} navigate={useNavigate()} location={useLocation()} />
}