import React from 'react';  

class AppView extends React.Component {

    state = {
        text: "111+1223+44*123/342",
        lastText: "", 
        error: ""
    }

    click = (string) => {
        var text = this.state.text;
        var first = string[0];
        var last = text[text.length - 1];

        if ((this.isActivity(last) || last == ".") && (this.isActivity(first) || first == ".")) {
            this.setState({text: text, lastText: "", error: "Нельзя добавлять два действия подряд"});
            return;
        }

        if (last == '/' && first == '0') {
            this.setState({text: text, lastText: "", error: "Делить на 0 нельзя"});
            return;
        }

        this.setState({text: text + string, lastText: "", error: ""});
    }

    clear = () => {
        this.setState({text: "", lastText: "", error: ""});
    }

    removeLast = () => {
        this.setState({text: this.state.text.substring(0, this.state.text.length - 1), lastText: "", error: ""});
    }

    change = () => {
        var text = this.state.text;
        var first = text[0];
        var result = "";

        if (first == '+' || first == '-') {
            result += this.changeOneSymbol(first)
        } else {
            result += '-' + first;
        }

        for (var i = 1; i < text.length; i++) {
            var first = text[i];
            if (first == '+' || first == '-') {
                result += this.changeOneSymbol(first); 
            }
            else {
                result += first;
            }
        }

        this.setState({text: result, lastText: "", error: ""});
    }

    changeOneSymbol = (symbol) => {
        if (symbol == '+') {
            return '-';
        }
        else {
            return '+';
        }
    }

    calculate = () => {
        var text = this.state.text;
        var lastText = this.state.lastText;
        if (lastText != "") {
            var index = -1;
            for (var i = lastText.length - 1; i >= 0; i--) {
                var char = lastText[i];
                if (this.isActivity(char)) {
                    index = i;
                    break; 
                }
            }

            if (index != -1) {
                text += lastText.substring(index, lastText.length);
            }
        }

        try {
            this.setState({
                    text: eval(text), 
                    lastText: text, 
                    error: ""
                });
        } catch {
            this.setState({
                text: text, 
                lastText: "", 
                error: "Недопустимое выражение"
            });
        }
    }

    isActivity = (char) => {
        if (char == '+' || char == '-' || char == '*' || char == "/") {
            return true;
        } 
        else {
            return false;
        }
    }


    render() {
        const { text, lastText, error } = this.state;
        return (
            <div>
                <div className="row">
                    <h3 className="error-text">{error}</h3>
                    {/* <p>{lastText}</p> */}
                </div>
                <div className="row">
                    <div className="col-4 calculator">
                        <div className="row">
                            <div className="col">
                                <input id="output" type="text" value={text} readOnly="readonly"/>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col">
                                <input id="7_button" type="button" value="7" onClick={() => this.click("7")}/>
                            </div>
                            <div className="col">
                                <input id="8_button" type="button" value="8" onClick={() => this.click("8")}/>
                            </div>
                            <div className="col">
                                <input id="9_button" type="button" value="9" onClick={() => this.click("9")}/>
                            </div>
                            <div className="col">
                                <input id="devide_button" type="button" value="/" onClick={() => this.click("/")}/>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col">
                                <input id="4_button" type="button" value="4" onClick={() => this.click("4")}/>
                            </div>
                            <div className="col">
                                <input id="5_button" type="button" value="5" onClick={() => this.click("5")}/>
                            </div>
                            <div className="col">
                                <input id="6_button" type="button" value="6" onClick={() => this.click("6")}/>
                            </div>
                            <div className="col">
                                <input id="multiply_button" type="button" value="*" onClick={() => this.click("*")}/>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col">
                                <input id="1_button" type="button" value="1" onClick={() => this.click("1")}/>
                            </div>
                            <div className="col">
                                <input id="2_button" type="button" value="2" onClick={() => this.click("2")}/>
                            </div>
                            <div className="col">
                                <input id="3_button" type="button" value="3" onClick={() => this.click("3")}/>
                            </div>
                            <div className="col">
                                <input id="plus_button" type="button" value="+" onClick={() => this.click("+")}/>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col">
                                <input id="zero_button" type="button" value="0" onClick={() => this.click("0")}/>
                            </div>
                            <div className="col">
                                <input id="clear_button" type="button" value="C" onClick={() => this.clear()}/>
                            </div>
                            <div className="col">
                                <input id="change_button" type="button" value="+-" onClick={() => this.change()}/>
                            </div>
                            <div className="col">
                                <input id="minus_button" type="button" value="-" onClick={() => this.click("-")}/>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col">
                                <input id="stepen_button" type="button" value="^" onClick={() => this.click("**")}/>
                            </div>
                            <div className="col">
                                <input id="dot_button" type="button" value="." onClick={() => this.click(".")}/>
                            </div>
                            <div className="col">
                                <input id="remove_last_button" type="button" value="<" onClick={() => this.removeLast()}/>
                            </div>
                            <div className="col">
                                <input id="result_button" type="button" value="=" onClick={() => this.calculate()}/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default AppView;