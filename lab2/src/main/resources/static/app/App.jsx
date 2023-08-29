import React from "react";
import ReactDom from "react-dom";

class App extends React.Component {

    render() {
    return <div class="row">
               <div class="col-4 calculator">
                   <div class="row">
                       <div class="col">
                           <input id="output" type="text"/>
                       </div>
                   </div>
                   <div class="row">
                       <div class="col">
                           <input id="7_button" type="button" value="7"/>
                       </div>
                       <div class="col">
                           <input id="8_button" type="button" value="8"/>
                       </div>
                       <div class="col">
                           <input id="9_button" type="button" value="9"/>
                       </div>
                       <div class="col">
                           <input id="devide_button" type="button" value="/"/>
                       </div>
                   </div>
                   <div class="row">
                       <div class="col">
                           <input id="4_button" type="button" value="4"/>
                       </div>
                       <div class="col">
                           <input id="5_button" type="button" value="5"/>
                       </div>
                       <div class="col">
                           <input id="6_button" type="button" value="6"/>
                       </div>
                       <div class="col">
                           <input id="multiply_button" type="button" value="*"/>
                       </div>
                   </div>
                   <div class="row">
                       <div class="col">
                           <input id="1_button" type="button" value="1"/>
                       </div>
                       <div class="col">
                           <input id="2_button" type="button" value="2"/>
                       </div>
                       <div class="col">
                           <input id="3_button" type="button" value="3"/>
                       </div>
                       <div class="col">
                           <input id="plus_button" type="button" value="+"/>
                       </div>
                   </div>
                   <div class="row">
                       <div class="col">
                           <input id="zero_button" type="button" value="0"/>
                       </div>
                       <div class="col">
                           <input id="clear_button" type="button" value="C"/>
                       </div>
                       <div class="col">
                           <input id="change_button" type="button" value="+-"/>
                       </div>
                       <div class="col">
                           <input id="minus_button" type="button" value="-"/>
                       </div>
                   </div>
               </div>
           </div>
        }
}
ReactDom.render(<App />, document.getElementById('app'));