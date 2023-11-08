import React from 'react';
import $ from 'jquery';

export default class AppView extends React.Component {

    state = {
        token: "6824033913:AAESU0MjjEmWO_3IyobafCwZDXRZw0zwOsw",
    }

    constructor (props) {
        super(props);
        this.UsersList = React.createRef();
        this.Message = React.createRef();
    }

    loadUsers = () => {

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
                                    <h2>Виджет телеграма, интегрированный с ботом</h2>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    
                                </div>
                            </div>
                        </div>
                        <div class="col-3"></div>
                    </div>
                    <div class="row">
                        <div class="col-3"></div>
                        <div class="col" >
                            
                        </div>
                        <div class="col-3"></div>
                    </div>
                </div>
                <script async src="https://telegram.org/js/telegram-widget.js?22" data-telegram-post="koliamainer/9702" data-width="100%"></script>
                <script async src="https://telegram.org/js/telegram-widget.js?22" data-telegram-discussion="Ryndyk_Daniil_UITIiA_Lab4_Bot" data-comments-limit="5"></script>
            </div>
        )
    }
}